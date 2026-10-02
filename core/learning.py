"""Concept-led learning and local single-user progress, independent of exam claims."""
import json
from contextlib import contextmanager
import sqlite3
from pathlib import Path

STAGES = ('Learn', 'Observe', 'Practice', 'Reinforce', 'Checkpoint')
PATHWAYS = [
    ('foundations', '🧱', 'Foundational Skills', False),
    ('security', '🛡️', 'Security Basics', False),
    ('network', '🌐', 'Network Basics', False),
    ('practitioner', '🔎', 'Security Practitioner', True),
    ('junior', '🧭', 'Junior Pentester', True),
    ('registered', '📋', 'Registered Pentester pathway', True),
    ('offensive', '⚔️', 'Offensive Security', True),
    ('redteam', '🎯', 'Red Team Ops', True),
    ('exploit', '🧬', 'Exploit Developer', True),
]


def lessons():
    return json.loads((Path(__file__).resolve().parents[1] / 'data/learning.json').read_text())


@contextmanager
def connect(database):
    db = sqlite3.connect(database)
    db.execute('CREATE TABLE IF NOT EXISTS progress (concept TEXT PRIMARY KEY, stage INTEGER NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS preferences (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
    try:
        with db:
            yield db
    finally:
        db.close()


def progress(database):
    with connect(database) as db:
        return dict(db.execute('SELECT concept, stage FROM progress'))


def advance(database, concept, stage):
    with connect(database) as db:
        current = db.execute('SELECT stage FROM progress WHERE concept = ?', (concept,)).fetchone()
        completed = current[0] if current else 0
        if stage != completed + 1 or not 1 <= stage <= 5:
            return False
        db.execute('INSERT INTO progress VALUES (?, ?) ON CONFLICT(concept) DO UPDATE SET stage=excluded.stage', (concept, stage))
        return True


def preference(database, value=None):
    with connect(database) as db:
        if value is not None:
            db.execute("INSERT INTO preferences VALUES ('path', ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (value,))
        row = db.execute("SELECT value FROM preferences WHERE key='path'").fetchone()
        return row[0] if row else 'foundations'


def coverage(records, concepts):
    # Fixed published starter scope: unseen concepts remain in the denominator.
    return round(sum(records.get(item['id'], 0) for item in concepts) / (5 * len(concepts)) * 100) if concepts else 0


def cards(records):
    content = lessons()
    result = []
    for key, icon, title, planned in PATHWAYS:
        mapped = [item for item in content if key in item['tiers']]
        result.append(dict(key=key, icon=icon, title=title, planned=planned,
                           percent=coverage(records, mapped), count=len(mapped)))
    return result


def matches_answer(item, stage, answer):
    key = {3: 'answer', 4: 'reinforce_answer', 5: 'checkpoint_answer'}[stage]
    candidate = ' '.join(answer.strip().split())
    expected = ' '.join(item[key].strip().split())
    if not item.get('case_sensitive', False):
        candidate, expected = candidate.casefold(), expected.casefold()
    alternatives = item.get(key + '_alternatives', [])
    return candidate == expected or any(candidate == (' '.join(value.split()) if item.get('case_sensitive') else ' '.join(value.split()).casefold()) for value in alternatives)
