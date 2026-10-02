import unittest

from core.engine import AVAILABLE_MODULES, MODULE_FILES, build_scenario_list, get_scenario_by_index, validate_command


class ScenarioEngineTests(unittest.TestCase):
    def test_current_library_contains_40_valid_scenarios(self):
        scenario_count = 0
        for module in MODULE_FILES:
            for difficulty in ("basic", "standard"):
                scenarios = build_scenario_list([module], difficulty)
                self.assertEqual(len(scenarios), 5)
                scenario_count += len(scenarios)

                for scenario in scenarios:
                    self.assertTrue(scenario.get("scenario"))
                    self.assertTrue(scenario.get("objective"))
                    self.assertTrue(scenario.get("explanation"))
                    self.assertTrue(scenario.get("validation", {}).get("required"))

        self.assertEqual(scenario_count, 40)

    def test_invalid_module_and_difficulty_return_no_scenarios(self):
        self.assertEqual(build_scenario_list(["../../private"], "basic"), [])
        self.assertEqual(build_scenario_list(["security_plus"], "professional"), [])

    def test_invalid_index_returns_no_scenario(self):
        self.assertIsNone(get_scenario_by_index(["security_plus"], "basic", "0"))
        self.assertIsNone(get_scenario_by_index(["security_plus"], "basic", 99))

    def test_empty_command_returns_feedback(self):
        result = validate_command(None, ["security_plus"], "basic", 0)
        self.assertFalse(result["correct"])
        self.assertIn("Enter a command", result["message"])


if __name__ == "__main__":
    unittest.main()
