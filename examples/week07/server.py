"""API stdlib locale, séquentielle. Aucune publication externe."""
from __future__ import annotations
import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from .workflow import Engine, Conflict, InvalidEvent


def handler_for(engine: Engine, service_token: str, review_token: str):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # Aucun token ni texte client dans les logs d'accès.

        def respond(self, code, body):
            data = json.dumps(body, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            self.dispatch()

        def do_POST(self):
            self.dispatch()

        def dispatch(self):
            parts = urlparse(self.path).path.strip('/').split('/')
            if self.command == 'GET' and parts == ['health']:
                return self.respond(200, {'status': 'ok'})
            review = len(parts) == 3 and parts[0] == 'jobs' and parts[2] in {'decision','replay'}
            expected = review_token if review else service_token
            provided = self.headers.get('Authorization', '')
            if not hmac.compare_digest(provided, 'Bearer ' + expected):
                return self.respond(401, {'error': 'unauthorized'})
            try:
                body = None
                if self.command == 'POST':
                    length = int(self.headers.get('Content-Length', '0'))
                    if not 0 < length <= 16000:
                        return self.respond(413, {'error': 'invalid_size'})
                    body = json.loads(self.rfile.read(length))
                    if not isinstance(body, dict):
                        raise InvalidEvent('Objet JSON requis')
                if self.command == 'POST' and parts == ['events']:
                    job, created = engine.ingest(body)
                    return self.respond(202 if created else 200, {'event_id': job['event_id'], 'status': job['status'], 'created': created})
                if self.command == 'POST' and parts == ['tick']:
                    return self.respond(200, {'jobs': engine.tick()})
                if self.command == 'GET' and parts == ['metrics']:
                    return self.respond(200, engine.metrics())
                if len(parts) == 2 and parts[0] == 'jobs' and self.command == 'GET':
                    return self.respond(200, engine.get(parts[1]))
                if review and self.command == 'POST':
                    if parts[2] == 'replay':
                        return self.respond(200, engine.replay(parts[1]))
                    if set(body) != {'decision','proposal_hash'}:
                        raise InvalidEvent('Contrat de décision invalide')
                    return self.respond(200, engine.decide(parts[1], body['decision'], 'reviewer-demo', body['proposal_hash']))
                self.respond(404, {'error': 'not_found'})
            except KeyError:
                self.respond(404, {'error': 'not_found'})
            except Conflict as exc:
                self.respond(409, {'error': str(exc)})
            except (InvalidEvent, ValueError, TypeError) as exc:
                self.respond(400, {'error': str(exc)})
    return Handler


def main():
    service = os.environ.get('SERVICE_TOKEN', '')
    review = os.environ.get('REVIEW_TOKEN', '')
    if len(service) < 24 or len(review) < 24 or service == review:
        raise SystemExit('Deux tokens différents de 24 caractères minimum sont requis')
    engine = Engine(os.environ.get('WORKFLOW_DB', 'workflow.sqlite'))
    server = HTTPServer((os.environ.get('WORKFLOW_HOST', '127.0.0.1'), 8080), handler_for(engine, service, review))
    server.timeout = 10
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        engine.close()


if __name__ == '__main__':
    main()
