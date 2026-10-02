import hmac
import secrets
from flask import Blueprint, current_app, render_template, request, redirect, url_for, session, abort
from core.learning import lessons, progress, advance, cards, preference, coverage, STAGES

learning = Blueprint('learning', __name__)
PATHS = ('foundations', 'security', 'network')


def database():
    return current_app.config['PROGRESS_DB']


def csrf():
    if 'learning_csrf' not in session:
        session['learning_csrf'] = secrets.token_hex(24)
    return session['learning_csrf']


@learning.before_request
def protect_forms():
    csrf()
    if request.method == 'POST' and not hmac.compare_digest(request.form.get('csrf', ''), csrf()):
        abort(400, 'Invalid form token. Reload the page and try again.')


@learning.context_processor
def template_helpers():
    return {'csrf_token': csrf, 'stages': STAGES}


@learning.route('/')
def dashboard():
    records = progress(database())
    selected = preference(database())
    content = sorted(lessons(), key=lambda item: item['path'] != selected)
    return render_template('dashboard.html', cards=cards(records), lessons=content, records=records,
                           selected=selected)


@learning.route('/orientation', methods=['GET', 'POST'])
def orientation():
    if request.method == 'POST':
        path = request.form.get('path')
        if path not in PATHS:
            abort(400)
        preference(database(), path)
        return redirect(url_for('learning.dashboard'))
    return render_template('orientation.html')


@learning.route('/placement', methods=['GET', 'POST'])
def placement():
    selected = request.values.get('path', 'foundations')
    if selected not in PATHS:
        abort(400)
    # A small sample informs entry advice, never progress or certification scores.
    sample = [item for item in lessons() if item['path'] in ('foundations', selected)]
    recommendation = None
    if request.method == 'POST':
        correct = sum(request.form.get(item['id'], '').strip().casefold() == item['answer'].casefold() for item in sample)
        recommendation = selected if correct >= len(sample) - 1 else 'foundations'
        if selected == 'foundations' and correct == len(sample):
            recommendation = 'security'
        gaps = [item['title'] for item in sample if request.form.get(item['id'], '').strip().casefold() != item['answer'].casefold()]
        return render_template('placement.html', sample=sample, selected=selected, recommendation=recommendation,
                               correct=correct, gaps=gaps)
    return render_template('placement.html', sample=sample, selected=selected, recommendation=None)


@learning.route('/learn/<concept>', methods=['GET', 'POST'])
def lesson(concept):
    item = next((item for item in lessons() if item['id'] == concept), None)
    if item is None:
        abort(404)
    completed = progress(database()).get(concept, 0)
    stage = min(completed + 1, 5)
    message = None
    if request.method == 'POST':
        if request.form.get('stage') != str(stage) or completed == 5:
            abort(400, 'This stage has already changed. Reload the lesson.')
        answer_key = {3: 'answer', 4: 'reinforce_answer', 5: 'checkpoint_answer'}.get(stage)
        if answer_key and request.form.get('answer', '').strip().casefold() != item[answer_key].casefold():
            message = 'That answer does not match this exercise. Revisit the explanation and try again; this is practice, not a pass/fail judgement.'
        elif advance(database(), concept, stage):
            return redirect(url_for('learning.lesson', concept=concept))
    return render_template('learning_lesson.html', lesson=item, stage=stage, completed=completed, message=message)


@learning.route('/coverage/<exam>')
def exam_coverage(exam):
    if exam not in ('security_plus', 'ccna'):
        abort(404)
    content = [item for item in lessons() if exam in item['exams']]
    records = progress(database())
    return render_template('coverage.html', exam='Security+' if exam == 'security_plus' else 'CCNA',
                           lessons=content, records=records, percent=coverage(records, content))
