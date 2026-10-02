import hmac
import secrets
from flask import Blueprint, current_app, render_template, request, redirect, url_for, session, abort, flash
from core.learning import lessons, progress, advance, cards, preference, coverage, STAGES, matches_answer, PATHWAYS

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
    return {'csrf_token': csrf, 'stages': STAGES, 'pathway_names': {key: icon + ' ' + title for key, icon, title, _ in PATHWAYS}}


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
    sample = [item for item in lessons() if item['id'] in ('linux-navigation', 'python-data', 'permissions', 'integrity', 'dns', 'subnets') and item['path'] in ('foundations', selected)]
    recommendation = None
    if request.method == 'POST':
        correct = sum(matches_answer(item, 3, request.form.get(item['id'], '')) for item in sample)
        recommendation = selected if correct >= len(sample) - 1 else 'foundations'
        if selected == 'foundations' and correct == len(sample):
            recommendation = 'security'
        gaps = [item['title'] for item in sample if not matches_answer(item, 3, request.form.get(item['id'], ''))]
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
        if answer_key and not matches_answer(item, stage, request.form.get('answer', '')):
            message = 'Not quite. Review the lesson notes below and trace the example before trying again.'
        elif advance(database(), concept, stage):
            if answer_key:
                prefix = {3: 'practice', 4: 'reinforce', 5: 'checkpoint'}[stage]
                flash(item[prefix + '_feedback'], 'learning')
            return redirect(url_for('learning.lesson', concept=concept))
    content = lessons()
    related = [entry for entry in content if entry['id'] in item.get('prerequisites', [])]
    sequence = [entry for entry in content if entry['path'] == item['path']]
    index = next(i for i, entry in enumerate(sequence) if entry['id'] == concept)
    next_lesson = sequence[index + 1] if index + 1 < len(sequence) else None
    return render_template('learning_lesson.html', lesson=item, stage=stage, completed=completed,
                           message=message, related=related, next_lesson=next_lesson)


@learning.route('/coverage/<exam>')
def exam_coverage(exam):
    if exam not in ('security_plus', 'ccna'):
        abort(404)
    content = [item for item in lessons() if exam in item['exams']]
    records = progress(database())
    return render_template('coverage.html', exam='Security+' if exam == 'security_plus' else 'CCNA',
                           lessons=content, records=records, percent=coverage(records, content))


@learning.route('/pathway/<path>')
def pathway(path):
    card = next((item for item in cards(progress(database())) if item['key'] == path), None)
    if card is None:
        abort(404)
    content = [item for item in lessons() if item['path'] == path]
    return render_template('pathway.html', card=card, lessons=content, records=progress(database()))
