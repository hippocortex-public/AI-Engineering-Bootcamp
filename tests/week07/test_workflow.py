import json
import tempfile
import threading
import unittest
from http.server import HTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from examples.week07.workflow import Engine, Conflict, InvalidEvent, TemporaryFailure, event, fake_drafter
from examples.week07.server import handler_for


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.now = 1000.0
        self.engine = Engine(clock=lambda: self.now)

    def tearDown(self):
        self.engine.close()

    def draft(self):
        self.engine.ingest(event())
        return self.engine.process('evt-001')

    def test_ingest_duplicate(self):
        self.assertTrue(self.engine.ingest(event())[1])
        self.assertFalse(self.engine.ingest(event())[1])
        self.assertEqual(self.engine.metrics(), {'received': 1})

    def test_collision(self):
        self.engine.ingest(event())
        with self.assertRaises(Conflict):
            self.engine.ingest(event(text='Autre contenu'))

    def test_invalid_contract(self):
        for bad in [[], {}, {**event(), 'schema_version': True}, {**event(), 'text': ''}, {**event(), 'extra': 1}, {**event(), 'event_id': '../x'}]:
            with self.assertRaises(InvalidEvent):
                self.engine.ingest(bad)
        self.assertEqual(self.engine.metrics(), {})

    def test_no_publish_before_approval(self):
        job = self.draft()
        self.assertEqual(job['status'], 'awaiting_review')
        self.assertEqual(self.engine.db.execute('SELECT COUNT(*) FROM publications').fetchone()[0], 0)

    def test_approval_idempotent(self):
        job = self.draft()
        for _ in range(2):
            self.engine.decide('evt-001', 'approve', 'reviewer-demo', job['proposal_hash'])
        self.assertEqual(self.engine.db.execute('SELECT COUNT(*) FROM publications').fetchone()[0], 1)
        with self.assertRaises(Conflict):
            self.engine.decide('evt-001', 'reject', 'reviewer-demo', job['proposal_hash'])

    def test_reject(self):
        job = self.draft()
        result = self.engine.decide('evt-001', 'reject', 'reviewer-demo', job['proposal_hash'])
        self.assertEqual(result['status'], 'rejected')
        self.assertEqual(self.engine.db.execute('SELECT COUNT(*) FROM publications').fetchone()[0], 0)

    def test_hash_and_identity(self):
        job = self.draft()
        with self.assertRaises(Conflict):
            self.engine.decide('evt-001', 'approve', 'reviewer-demo', 'wrong')
        with self.assertRaises(InvalidEvent):
            self.engine.decide('evt-001', 'approve', 'untrusted', job['proposal_hash'])

    def test_expired(self):
        job = self.draft()
        self.now += 3600
        with self.assertRaises(Conflict):
            self.engine.decide('evt-001', 'approve', 'reviewer-demo', job['proposal_hash'])
        self.engine.tick()
        self.assertEqual(self.engine.get('evt-001')['status'], 'expired')

    def test_retry_backoff_and_dead_letter(self):
        def down(_):
            raise TemporaryFailure('down')
        self.engine.drafter = down
        self.engine.ingest(event())
        self.assertEqual(self.engine.process('evt-001')['attempts'], 1)
        self.assertEqual(self.engine.process('evt-001')['attempts'], 1)
        self.now += 2
        self.engine.tick()
        self.now += 4
        self.engine.tick()
        self.assertEqual(self.engine.get('evt-001')['status'], 'dead_letter')
        self.engine.drafter = fake_drafter
        self.engine.replay('evt-001')
        self.engine.tick()
        self.assertEqual(self.engine.get('evt-001')['status'], 'awaiting_review')

    def test_bad_model_output_no_retry(self):
        self.engine.drafter = lambda _: {'draft': 'malformed'}
        self.engine.ingest(event())
        self.assertEqual(self.engine.process('evt-001')['status'], 'dead_letter')

    def test_publication_transaction_rollback(self):
        job = self.draft()
        self.engine.db.execute("CREATE TRIGGER reject_insert BEFORE INSERT ON publications BEGIN SELECT RAISE(ABORT, 'simulated failure'); END")
        import sqlite3
        with self.assertRaises(sqlite3.IntegrityError):
            self.engine.decide('evt-001', 'approve', 'reviewer-demo', job['proposal_hash'])
        self.assertEqual(self.engine.get('evt-001')['status'], 'awaiting_review')
        self.assertEqual(self.engine.db.execute('SELECT COUNT(*) FROM publications').fetchone()[0], 0)

    def test_processing_does_not_redraft_pending_review(self):
        calls = []
        def counted(payload):
            calls.append(payload['event_id'])
            return fake_drafter(payload)
        self.engine.drafter = counted
        self.draft()
        self.engine.process('evt-001')
        self.engine.ingest(event())
        self.engine.tick()
        self.assertEqual(calls, ['evt-001'])

    def test_restart_durability(self):
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / 'state.db')
            first = Engine(path)
            first.ingest(event())
            first.close()
            second = Engine(path)
            self.assertEqual(second.get('evt-001')['status'], 'received')
            second.process('evt-001')
            second.close()


class HTTPTests(unittest.TestCase):
    def setUp(self):
        # Engine créé dans le thread qui utilisera SQLite.
        self.ready = threading.Event()
        def run():
            self.engine = Engine()
            self.server = HTTPServer(('127.0.0.1', 0), handler_for(self.engine,'s'*24,'r'*24))
            self.ready.set()
            self.server.serve_forever(poll_interval=0.02)
            self.server.server_close()
            self.engine.close()
        self.thread = threading.Thread(target=run)
        self.thread.start()
        self.ready.wait(5)
        self.base = f'http://127.0.0.1:{self.server.server_port}'

    def tearDown(self):
        self.server.shutdown()
        self.thread.join(5)

    def call(self, path, body=None, token='s'*24):
        req = Request(self.base+path, data=json.dumps(body).encode() if body is not None else None,
                      headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
        try:
            with urlopen(req,timeout=5) as response:
                return response.status, json.load(response)
        except HTTPError as response:
            return response.code, json.load(response)

    def test_http_end_to_end_and_roles(self):
        self.assertEqual(self.call('/events', event())[0], 202)
        self.assertEqual(self.call('/events', event())[0], 200)
        self.assertEqual(self.call('/tick', {})[0], 200)
        job = self.call('/jobs/evt-001')[1]
        decision = {'decision':'approve','proposal_hash':job['proposal_hash']}
        self.assertEqual(self.call('/jobs/evt-001/decision',decision)[0],401)
        self.assertEqual(self.call('/jobs/evt-001/decision',decision,token='r'*24)[1]['status'],'published')
        self.assertEqual(self.call('/events',event('evt-2'),token='r'*24)[0],401)

    def test_http_validation(self):
        self.assertEqual(self.call('/events', {})[0],400)
        self.assertEqual(self.call('/missing')[0],404)
        self.assertEqual(self.call('/events',event(),token='bad')[0],401)


if __name__ == '__main__':
    unittest.main()
