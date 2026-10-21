from __future__ import annotations
import json
import sys
from .workflow import Engine, event, TemporaryFailure, fake_drafter, Conflict


def scenario(day: int) -> dict:
    now = [1000.0]
    calls = [0]
    def unstable(payload):
        calls[0] += 1
        if calls[0] == 1:
            raise TemporaryFailure('Simulation réseau')
        return fake_drafter(payload)
    engine = Engine(clock=lambda: now[0], drafter=unstable if day == 4 else fake_drafter)
    try:
        first, created = engine.ingest(event())
        if day == 1:
            return {'accepted': created, 'status': first['status']}
        if day == 3:
            duplicate, created_again = engine.ingest(event())
            assert not created_again
            return {'duplicate_created': created_again, 'jobs': engine.metrics()}
        job = engine.process('evt-001')
        if day == 4:
            assert job['status'] == 'retry'
            now[0] += 2
            engine.tick()
            return {'calls': calls[0], 'status': engine.get('evt-001')['status']}
        if day in {2, 5}:
            return {'status': job['status'], 'proposal': job['proposal']}
        published = engine.decide('evt-001', 'approve', 'reviewer-demo', job['proposal_hash'])
        engine.decide('evt-001', 'approve', 'reviewer-demo', job['proposal_hash'])
        if day == 6:
            return {'status': published['status'], 'publication_count': engine.db.execute('SELECT COUNT(*) FROM publications').fetchone()[0]}
        engine.ingest(event('evt-reject'))
        denied = engine.process('evt-reject')
        engine.decide('evt-reject','reject','reviewer-demo',denied['proposal_hash'])
        engine.ingest(event('evt-expire'))
        expired = engine.process('evt-expire')
        now[0] += 3600
        engine.tick()
        try:
            engine.decide('evt-expire','approve','reviewer-demo',expired['proposal_hash'])
        except Conflict:
            pass
        else:
            raise AssertionError('Expiration non appliquée')
        return {'statuses': engine.metrics(), 'publication_count': engine.db.execute('SELECT COUNT(*) FROM publications').fetchone()[0]}
    finally:
        engine.close()


if __name__ == '__main__':
    day = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    if day not in range(1,8):
        raise SystemExit('Jour attendu : 1 à 7')
    print(json.dumps(scenario(day), ensure_ascii=False, indent=2))
