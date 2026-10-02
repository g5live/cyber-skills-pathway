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


class FoundationLibraryTests(unittest.TestCase):
    setUp = LearningTests.setUp
    token = LearningTests.token
    post = LearningTests.post

    def test_catalogue_has_complete_connected_content(self):
        from core.learning import lessons
        content = lessons()
        ids = {item['id'] for item in content}
        self.assertEqual(len(ids), 24)
        for path in ('foundations', 'security', 'network'):
            self.assertEqual(sum(item['path'] == path for item in content), 8)
        for item in content:
            with self.subTest(concept=item['id']):
                for key in ('learn','observe','practice','answer','reinforce','reinforce_answer',
                            'checkpoint','checkpoint_answer','practice_feedback','reinforce_feedback',
                            'checkpoint_feedback','connection','takeaways'):
                    self.assertTrue(item[key])
                self.assertTrue(set(item['prerequisites']) <= ids)
                self.assertNotIn(item['id'], item['prerequisites'])

    def test_every_lesson_renders_and_completes_all_five_stages(self):
        from core.learning import lessons
        for item in lessons():
            with self.subTest(concept=item['id']):
                url = '/learn/' + item['id']
                self.assertEqual(self.client.get(url).status_code, 200)
                for stage in range(1,6):
                    answer = item.get({3:'answer',4:'reinforce_answer',5:'checkpoint_answer'}.get(stage,''),'')
                    response = self.post(url, {'stage':str(stage),'answer':answer})
                    self.assertEqual(response.status_code, 302)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, 200)
                    if stage>=3:
                        self.assertIn(b'Why that fits:', response.data)
                self.assertEqual(progress(self.db)[item['id']], 5)

    def test_command_case_and_concept_whitespace(self):
        from core.learning import lessons, matches_answer
        content = {item['id']:item for item in lessons()}
        self.assertTrue(matches_answer(content['linux-files'],3,'  mkdir   reports  '))
        self.assertFalse(matches_answer(content['linux-files'],3,'MKDIR reports'))
        self.assertFalse(matches_answer(content['linux-files'],3,'mkdir REPORTS'))
        self.assertTrue(matches_answer(content['cia'],3,' CONFIDENTIALITY '))
        self.assertFalse(matches_answer(content['linux-files'],3,'mkdir reports; whoami'))

    def test_placement_remains_short_and_wrong_answers_do_not_advance(self):
        response = self.client.get('/placement?path=network')
        self.assertEqual(response.data.count(b'autocomplete="off" required'),4)
        for stage in (1,2):
            self.post('/learn/python-functions', {'stage':str(stage)})
        response = self.post('/learn/python-functions', {'stage':'3','answer':'6'})
        self.assertIn(b'Not quite.',response.data)
        self.assertEqual(progress(self.db)['python-functions'],2)
