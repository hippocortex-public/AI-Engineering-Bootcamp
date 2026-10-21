"""Moteur pédagogique mono-processus : état durable et effets simulés."""
from __future__ import annotations
import hashlib
import json
import re
import sqlite3
import time
from typing import Callable


class InvalidEvent(ValueError):
    pass


class Conflict(ValueError):
    pass


class TemporaryFailure(RuntimeError):
    pass


def validate_event(event: dict) -> dict:
    if not isinstance(event, dict):
        raise InvalidEvent('Un objet JSON est requis')
    required = {'event_id', 'schema_version', 'type', 'ticket_id', 'text'}
    if set(event) != required:
        raise InvalidEvent('Champs obligatoires manquants ou champs inconnus')
    if type(event['schema_version']) is not int or event['schema_version'] != 1:
        raise InvalidEvent('Version de schéma non supportée')
    if event['type'] != 'support.requested':
        raise InvalidEvent('Type non supporté')
    for key, limit in [('event_id', 100), ('ticket_id', 100), ('text', 4000)]:
        if not isinstance(event[key], str) or not event[key].strip() or len(event[key]) > limit:
            raise InvalidEvent(f'Champ invalide : {key}')
    for key in ('event_id', 'ticket_id'):
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', event[key]):
            raise InvalidEvent(f'Identifiant invalide : {key}')
    return dict(event)


def fake_drafter(event: dict) -> dict:
    """Double déterministe, pas un modèle IA, pas une mesure de confiance."""
    text = event['text'].lower()
    category = 'billing' if 'facture' in text else 'general'
    return {'category': category,
            'draft': f"Demande {event['ticket_id']} reçue. Un conseiller va vous répondre."}


def validate_proposal(proposal: dict) -> dict:
    if not isinstance(proposal, dict) or set(proposal) != {'category', 'draft'}:
        raise InvalidEvent('Contrat du générateur invalide')
    if not isinstance(proposal['category'], str) or proposal['category'] not in {'billing', 'general'}:
        raise InvalidEvent('Catégorie interdite')
    if not isinstance(proposal['draft'], str) or not 1 <= len(proposal['draft']) <= 2000:
        raise InvalidEvent('Brouillon invalide')
    return proposal


class Engine:
    def __init__(self, path: str = ':memory:', clock: Callable = time.time,
                 drafter: Callable = fake_drafter, max_attempts: int = 3,
                 approval_ttl: int = 3600):
        if max_attempts < 1 or approval_ttl <= 0:
            raise ValueError('Configuration invalide')
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.clock, self.drafter = clock, drafter
        self.max_attempts, self.approval_ttl = max_attempts, approval_ttl
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS jobs (
          event_id TEXT PRIMARY KEY, payload TEXT NOT NULL, status TEXT NOT NULL,
          attempts INTEGER NOT NULL DEFAULT 0, ready_at REAL NOT NULL DEFAULT 0,
          proposal TEXT, proposal_hash TEXT, expires_at REAL,
          reviewer TEXT, decision TEXT, error TEXT);
        CREATE TABLE IF NOT EXISTS publications (
          event_id TEXT PRIMARY KEY REFERENCES jobs(event_id), content TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS audit (
          id INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT NOT NULL,
          action TEXT NOT NULL, at REAL NOT NULL);
        ''')

    def close(self):
        self.db.close()

    def _audit(self, event_id: str, action: str):
        self.db.execute('INSERT INTO audit(event_id,action,at) VALUES (?,?,?)',
                        (event_id, action, self.clock()))

    def get(self, event_id: str) -> dict:
        row = self.db.execute('SELECT * FROM jobs WHERE event_id=?', (event_id,)).fetchone()
        if row is None:
            raise KeyError(event_id)
        result = dict(row)
        for key in ('payload', 'proposal'):
            if result[key] is not None:
                result[key] = json.loads(result[key])
        return result

    def ingest(self, event: dict) -> tuple[dict, bool]:
        payload = json.dumps(validate_event(event), sort_keys=True, ensure_ascii=False)
        eid = event['event_id']
        with self.db:
            old = self.db.execute('SELECT payload FROM jobs WHERE event_id=?', (eid,)).fetchone()
            if old:
                if old['payload'] != payload:
                    raise Conflict('Identifiant réutilisé pour un contenu différent')
                return self.get(eid), False
            self.db.execute('INSERT INTO jobs(event_id,payload,status) VALUES (?,?,?)',
                            (eid, payload, 'received'))
            self._audit(eid, 'accepted')
        return self.get(eid), True

    def process(self, eid: str) -> dict:
        job = self.get(eid)
        if job['status'] not in {'received', 'retry'} or job['ready_at'] > self.clock():
            return job
        attempts = job['attempts'] + 1
        # Appel du générateur avant la transaction finale : un crash peut refaire
        # cet appel. Le double n'a aucun effet externe; un LLM peut coûter deux fois.
        try:
            proposal = validate_proposal(self.drafter(job['payload']))
        except (TemporaryFailure, InvalidEvent) as exc:
            permanent = isinstance(exc, InvalidEvent)
            status = 'dead_letter' if permanent or attempts >= self.max_attempts else 'retry'
            with self.db:
                self.db.execute('UPDATE jobs SET status=?,attempts=?,ready_at=?,error=? WHERE event_id=?',
                                (status, attempts, self.clock() + 2 ** attempts,
                                 type(exc).__name__, eid))
                self._audit(eid, status)
            return self.get(eid)
        serialized = json.dumps(proposal, sort_keys=True, ensure_ascii=False)
        digest = hashlib.sha256(serialized.encode()).hexdigest()
        with self.db:
            self.db.execute('''UPDATE jobs SET status='awaiting_review', attempts=?,
                proposal=?,proposal_hash=?,expires_at=?,error=NULL WHERE event_id=?''',
                (attempts, serialized, digest, self.clock() + self.approval_ttl, eid))
            self._audit(eid, 'draft_created')
        return self.get(eid)

    def tick(self) -> list[dict]:
        now = self.clock()
        with self.db:
            expired = self.db.execute("SELECT event_id FROM jobs WHERE status='awaiting_review' AND expires_at<=?",
                                      (now,)).fetchall()
            for row in expired:
                self.db.execute("UPDATE jobs SET status='expired' WHERE event_id=?", (row['event_id'],))
                self._audit(row['event_id'], 'expired')
        ids = self.db.execute("SELECT event_id FROM jobs WHERE status IN ('received','retry') AND ready_at<=? ORDER BY event_id LIMIT 100",
                              (now,)).fetchall()
        return [self.process(row['event_id']) for row in ids]

    def decide(self, eid: str, decision: str, reviewer: str, proposal_hash: str) -> dict:
        if decision not in {'approve', 'reject'} or reviewer != 'reviewer-demo':
            raise InvalidEvent('Décision ou identité du relecteur invalide')
        with self.db:
            job = self.get(eid)
            if proposal_hash != job['proposal_hash']:
                raise Conflict('La décision ne porte pas sur le brouillon courant')
            if job['status'] in {'published', 'rejected'}:
                if job['decision'] == decision and job['reviewer'] == reviewer:
                    return job
                raise Conflict('Une autre décision a déjà été appliquée')
            if job['status'] != 'awaiting_review':
                raise Conflict('Aucune validation en attente')
            if self.clock() >= job['expires_at']:
                raise Conflict('Validation expirée')
            status = 'published' if decision == 'approve' else 'rejected'
            if decision == 'approve':
                # Publication locale et transition dans la même transaction.
                # Ce mécanisme ne garantit rien pour un fournisseur externe.
                self.db.execute('INSERT INTO publications VALUES (?,?)',
                                (eid, job['proposal']['draft']))
            self.db.execute('UPDATE jobs SET status=?,decision=?,reviewer=? WHERE event_id=?',
                            (status, decision, reviewer, eid))
            self._audit(eid, status)
        return self.get(eid)

    def replay(self, eid: str) -> dict:
        with self.db:
            if self.get(eid)['status'] != 'dead_letter':
                raise Conflict('Seule une dead letter peut être rejouée')
            self.db.execute("UPDATE jobs SET status='received',attempts=0,ready_at=0,error=NULL WHERE event_id=?", (eid,))
            self._audit(eid, 'replayed')
        return self.get(eid)

    def metrics(self) -> dict:
        rows = self.db.execute('SELECT status,COUNT(*) AS total FROM jobs GROUP BY status')
        return {row['status']: row['total'] for row in rows}


def event(eid='evt-001', text='Je souhaite comprendre ma facture') -> dict:
    return {'event_id': eid, 'schema_version': 1, 'type': 'support.requested',
            'ticket_id': 'T-001', 'text': text}
