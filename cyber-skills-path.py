import os
import secrets
import time
from pathlib import Path
from core.learning_routes import learning
from core.learning import PATHWAYS

from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from core.engine import (
    AVAILABLE_DIFFICULTIES,
    AVAILABLE_MODULES,
    build_scenario_list,
    get_scenario_by_index,
    validate_command,
)


ALLOWED_TIME_LIMITS = frozenset({300, 600, 1200, 1800, 3600})
MAX_COMMAND_LENGTH = 500

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

app.config['PROGRESS_DB'] = os.environ.get('PROGRESS_DB') or str(Path(__file__).resolve().parent / 'progress.sqlite3')
app.register_blueprint(learning)


@app.route('/quickfire-reinforcement')
@app.route('/command-practice')
def home():
    return render_template('menu.html', pathways=PATHWAYS)


@app.route('/start', methods=['POST'])
def start_lab():
    difficulty = request.form.get('difficulty', '')
    try:
        time_limit = int(request.form.get('time_limit', ''))
    except (TypeError, ValueError):
        return "Invalid session timer.", 400

    selected_modules = request.form.getlist('modules')
    if not selected_modules:
        selected_modules = ['foundations']
    selected_modules = list(dict.fromkeys(selected_modules))

    if difficulty not in AVAILABLE_DIFFICULTIES:
        return "Invalid learning level selection.", 400
    if time_limit not in ALLOWED_TIME_LIMITS:
        return "Invalid session timer.", 400
    if any(module not in AVAILABLE_MODULES for module in selected_modules):
        return "Invalid training module.", 400

    session['difficulty'] = difficulty
    session['time_limit'] = time_limit
    session['modules'] = selected_modules

    scenarios = build_scenario_list(selected_modules, difficulty)
    session['total_questions'] = len(scenarios)
    session['solved'] = []
    session['end_time'] = time.time() + time_limit

    if session['total_questions'] == 0:
        return "Error: No scenarios found for this module/difficulty combination. Please add questions to the JSON files.", 400

    return redirect(url_for('scenario', index=0))


@app.route('/scenario/<int:index>')
def scenario(index):
    modules = session.get('modules')
    difficulty = session.get('difficulty')
    end_time = session.get('end_time')
    if not modules or difficulty not in AVAILABLE_DIFFICULTIES or end_time is None:
        return redirect(url_for('home'))
    if time.time() >= end_time:
        return redirect(url_for('results'))

    scenario_data = get_scenario_by_index(modules, difficulty, index)
    if not scenario_data:
        return redirect(url_for('results'))

    time_left = max(0, int(end_time - time.time()))

    next_index = index + 1 if (index + 1) < session['total_questions'] else None

    return render_template('index.html', scenario=scenario_data, index=index, next_index=next_index,
                           time_left=time_left)


@app.route('/api/validate', methods=['POST'])
def validate():
    if not all(key in session for key in ('modules', 'difficulty', 'total_questions', 'end_time')):
        return jsonify({"correct": False, "message": "Start a training session first."}), 400
    if time.time() >= session['end_time']:
        return jsonify({"correct": False, "message": "This training session has ended."}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"correct": False, "message": "Invalid request data."}), 400

    user_command = data.get('command')
    index = data.get('index')

    if not isinstance(user_command, str) or not user_command.strip():
        return jsonify({"correct": False, "message": "Enter a command before submitting."}), 400
    if len(user_command) > MAX_COMMAND_LENGTH:
        return jsonify({"correct": False, "message": "Command is too long."}), 400
    if type(index) is not int or not 0 <= index < session['total_questions']:
        return jsonify({"correct": False, "message": "Invalid scenario index."}), 400

    result = validate_command(user_command, session['modules'], session['difficulty'], index)

    if result.get('correct'):
        if index not in session.setdefault('solved', []):
            session['solved'].append(index)
            session.modified = True

    return jsonify(result)


@app.route('/results')
def results():
    if 'solved' not in session:
        return redirect(url_for('home'))

    score = len(session['solved'])
    total = session.get('total_questions', 0)
    pass_rate = round((score / total) * 100) if total else 0
    passed = pass_rate >= 80

    return render_template('results.html', score=score, total=total, pass_rate=pass_rate, passed=passed)


if __name__ == '__main__':
    debug_mode = os.environ.get("FLASK_DEBUG", "").lower() in {"1", "true", "yes"}
    app.run(debug=debug_mode)
