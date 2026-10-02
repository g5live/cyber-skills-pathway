import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MODULE_FILES = {
    "security_plus": DATA_DIR / "security_plus.json",
    "offensive_security": DATA_DIR / "offensive_security.json",
    "pentesting": DATA_DIR / "pentesting.json",
    "ethical_hacker": DATA_DIR / "ethical_hacker.json",
}
AVAILABLE_MODULES = frozenset(MODULE_FILES)
AVAILABLE_DIFFICULTIES = frozenset({"basic", "standard"})


def build_scenario_list(modules, difficulty):
    if difficulty not in AVAILABLE_DIFFICULTIES or not isinstance(modules, (list, tuple)):
        return []

    scenarios = []
    for module in dict.fromkeys(modules):
        file_path = MODULE_FILES.get(module)
        if file_path is None:
            continue

        with file_path.open(encoding="utf-8") as file:
            data = json.load(file)

        scenarios.extend(
            item for item in data
            if item.get("difficulty") == difficulty
        )

    return scenarios


def get_scenario_by_index(modules, difficulty, index):
    if type(index) is not int:
        return None

    scenarios = build_scenario_list(modules, difficulty)
    if 0 <= index < len(scenarios):
        return scenarios[index]
    return None


def validate_command(user_input, modules, difficulty, index):
    if not isinstance(user_input, str) or not user_input.strip():
        return {"correct": False, "message": "Enter a command before submitting."}

    scenario = get_scenario_by_index(modules, difficulty, index)
    if not scenario:
        return {"correct": False, "message": "Scenario not found."}

    val = scenario.get("validation", {})
    user_parts = user_input.strip().split()

    for forbidden in val.get("forbidden", []):
        if forbidden in user_parts:
            hint = val.get("hints", {}).get(forbidden, f"Remove the '{forbidden}' command.")
            return {"correct": False, "message": hint}

    if "192.168.1.0/24" not in user_parts and "192.168.1.0" in user_parts:
        return {"correct": False, "message": val.get("hints", {}).get("192.168.1.0", "Check your IP/CIDR.")}

    if "-sT" in user_parts:
        return {"correct": False, "message": val.get("hints", {}).get("-sT", "Wrong scan type.")}

    missing = [req for req in val.get("required", []) if req not in user_parts]
    if missing:
        return {"correct": False, "message": "[-] Error: Missing required flags, incorrect IP, or invalid syntax."}

    return {"correct": True, "message": "[+] Answer matches this simulated exercise. No command was executed."}
