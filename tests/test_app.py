import importlib.util
import unittest
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
APP_PATH = PROJECT_ROOT / "cyber-skills-path.py"


def load_application():
    spec = importlib.util.spec_from_file_location("security_command_lab", APP_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SecurityCommandLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_application()
        cls.module.app.config.update(TESTING=True, SECRET_KEY="test-secret")

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.module.app.config['PROGRESS_DB'] = str(Path(self.directory.name) / 'test.sqlite3')
        self.client = self.module.app.test_client()

    def start_session(self):
        return self.client.post(
            "/start",
            data={
                "difficulty": "basic",
                "time_limit": "300",
                "modules": "security_plus",
            },
        )

    def test_menu_marks_professional_tier_as_planned(self):
        response = self.client.get("/command-practice")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'value="professional" disabled', response.data)

    def test_valid_session_opens_first_scenario(self):
        response = self.start_session()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/scenario/0")
        self.assertEqual(self.client.get("/scenario/0").status_code, 200)

    def test_start_rejects_invalid_inputs(self):
        cases = (
            {"difficulty": "professional", "time_limit": "300", "modules": "security_plus"},
            {"difficulty": "basic", "time_limit": "301", "modules": "security_plus"},
            {"difficulty": "basic", "time_limit": "300", "modules": "../../private"},
        )
        for data in cases:
            with self.subTest(data=data):
                self.assertEqual(self.client.post("/start", data=data).status_code, 400)

    def test_validation_requires_active_session_and_json(self):
        self.assertEqual(self.client.post("/api/validate", json={"command": "nmap", "index": 0}).status_code, 400)
        self.start_session()
        self.assertEqual(self.client.post("/api/validate", data="not-json").status_code, 400)

    def test_validation_rejects_empty_command_and_invalid_index(self):
        self.start_session()
        self.assertEqual(self.client.post("/api/validate", json={"command": "", "index": 0}).status_code, 400)
        self.assertEqual(self.client.post("/api/validate", json={"command": "nmap", "index": 99}).status_code, 400)

    def test_correct_command_is_recorded(self):
        self.start_session()
        response = self.client.post(
            "/api/validate",
            json={"command": "nmap -sS 192.168.1.0/24", "index": 0},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["correct"])
        with self.client.session_transaction() as training_session:
            self.assertEqual(training_session["solved"], [0])


if __name__ == "__main__":
    unittest.main()
