import tempfile
import unittest
from pathlib import Path
from test_app import load_application
from core.learning import advance, progress, cards


class LearningTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = str(Path(self.temp.name) / 'progress.sqlite3')
        self.app = load_application().app
        self.app.config.update(TESTING=True, SECRET_KEY='testing', PROGRESS_DB=self.db)
        self.client = self.app.test_client()

    def token(self):
        self.client.get('/')
        with self.client.session_transaction() as session:
            return session['learning_csrf']

    def post(self, url, data):
        return self.client.post(url, data={**data, 'csrf': self.token()})

    def test_dashboard_and_coverage_render_without_exam_claims(self):
        for url in ('/', '/orientation', '/coverage/security_plus', '/coverage/ccna', '/placement?path=network'):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
        self.assertIn(b'prerequisite exposure', self.client.get('/').data)
        self.assertEqual(self.client.get('/coverage/unknown').status_code, 404)

    def test_progress_requires_order_and_persists_across_clients(self):
        self.assertFalse(advance(self.db, 'permissions', 3))
        self.assertTrue(advance(self.db, 'permissions', 1))
        self.assertFalse(advance(self.db, 'permissions', 1))
        second = self.app.test_client()
        self.assertIn(b'1/5 activities completed', second.get('/').data)
        values = {card['key']:card['percent'] for card in cards(progress(self.db))}
        self.assertGreater(values['foundations'], 0)
        self.assertGreater(values['security'], 0)
        self.assertGreater(values['junior'], 0)
        self.assertEqual(values['exploit'], 0)

    def test_lesson_flow_wrong_answer_replay_and_checkpoint(self):
        self.assertEqual(self.client.post('/learn/linux-navigation', data={'stage':'1'}).status_code, 400)
        for stage in (1, 2):
            self.assertEqual(self.post('/learn/linux-navigation', {'stage':str(stage)}).status_code, 302)
        self.assertEqual(self.post('/learn/linux-navigation', {'stage':'1'}).status_code, 400)
        self.post('/learn/linux-navigation', {'stage':'3','answer':'rm -rf /'})
        self.assertEqual(progress(self.db)['linux-navigation'], 2)
        for stage, answer in ((3,'pwd'), (4,'cd ..'), (5,'cd /tmp')):
            self.assertEqual(self.post('/learn/linux-navigation', {'stage':str(stage),'answer':answer}).status_code, 302)
        self.assertIn(b'Starter cycle completed', self.client.get('/learn/linux-navigation').data)
        self.assertEqual(self.post('/learn/linux-navigation', {'stage':'5','answer':'cd /tmp'}).status_code, 400)
        self.assertEqual(self.client.get('/learn/unknown').status_code, 404)

    def test_placement_recommends_but_does_not_award_progress(self):
        response = self.post('/placement', {'path':'network', 'linux-navigation':'wrong', 'python-data':'wrong'})
        self.assertIn(b'Suggested entry: foundations', response.data)
        self.assertEqual(progress(self.db), {})
        response = self.post('/placement', {'path':'foundations','linux-navigation':'pwd','python-data':'22'})
        self.assertIn(b'Suggested entry: security', response.data)
        self.assertEqual(self.post('/orientation', {'path':'network'}).status_code, 302)
        self.assertIn(b'Selected entry: network', self.client.get('/').data)
        self.assertEqual(self.post('/orientation', {'path':'exploit'}).status_code, 400)
