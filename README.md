# Cyber Skills Pathway

A personal, concept-led learning application for building connected Linux, Python, networking and security skills. The aim is understanding and practical judgement, not awarding certificates, professional registration or job qualifications. Certification coverage is an optional reference for learners who choose external assessment.

## Learning model

Every concept follows **1 Learn → 2 Observe → 3 Practice → 4 Reinforce → 5 Checkpoint**. Earlier knowledge should recur in later situations: navigating Linux supports file handling; permissions support least privilege; Python data handling supports automation; DNS and subnetting support investigation.

Start directly at a chosen area or take a short placement check based on your selected confidence. The app explains its recommendation and lets you confirm any available starting point. Placement never awards learning progress and a small sample cannot prove proficiency.

The design draws on the structure of the personal Obsidian Skills Concept Table: concept, branch, development stage, supporting evidence and next target. Personal scores and private learning records are not imported. The curriculum should eventually use prerequisite relationships and evidence to recommend the next useful concept rather than a sequence of isolated tool rooms.

## Dashboard and proposed pathway

Each tier has an icon and a red → amber → green progress bar. Shared concepts can contribute to multiple tiers. The current percentages use a fixed set of published starter concepts, including unseen concepts in the denominator. They measure activity completion, not knowledge confidence or likelihood of passing an exam. Higher-tier prerequisite progress is explicitly labelled; specialist content is not unlocked or claimed by completing basics.

| Tier | Current scope | Next development |
| --- | --- | --- |
| 🧱 Foundational Skills | Linux orientation, Python values, permissions | Shell/pipes, files, functions, Git, processes, troubleshooting |
| 🛡️ Security Basics | Least privilege, hashing/integrity, DNS crossover | CIA, authentication, threats, controls, risk, logs and response |
| 🌐 Network Basics | DNS records, IPv4 subnet scope, Python crossover | TCP/UDP, routing, switching, DHCP, VLANs and packet interpretation |
| 🔎 Security Practitioner | Shared prerequisites only | Connected Security+/CCNA-informed investigations |
| 🧭 Junior Pentester | Shared prerequisites only | Scoped enumeration, validation and reporting |
| 📋 Registered Pentester pathway | Planned | Professional assessment methodology; no registration awarded |
| ⚔️ Offensive Security | Planned | Controlled offensive investigations |
| 🎯 Red Team Ops | Planned | Authorised operational scenarios |
| 🧬 Exploit Developer | Planned | Specialist systems and exploit-development foundations |

These are learning areas, not a mandatory career ladder. Networking and security can develop alongside coding and system skills. Advanced areas remain future work. Initial development should stretch slightly beyond the owner's current Linux/Python/networking/security knowledge rather than attempt a complete professional curriculum.

## What works today

- A dashboard with shared-concept progress across tiers.
- Manual entry selection and an optional short placement check with user-confirmed recommendations.
- Six starter concepts: Linux navigation, Python data, permissions, integrity, DNS and IPv4 subnet scope.
- All five learning stages per starter concept; practical submissions are checked but never executed.
- Local SQLite persistence for one personal learner, surviving app restarts and browser-session changes.
- Security+ and CCNA starter relevance pages showing completed activities and unassessed evidence.
- The original 40 Basic/Standard command scenarios remain available under **Command practice**.

This is a small functional starter, not complete foundational, Security+ or CCNA courses. Original command exercises are retained as legacy practice rather than automatically counted as evidence on the new dashboard. Their simplified validation rules and content need further review.

## Evidence and certification coverage

Opening a lesson or completing an activity does not demonstrate independent retention. Current records track stage completion only; they cannot detect AI assistance, looked-up answers or copied commands. Same-session reinforcement and checkpoints are starter exercises, not delayed assessments. Future evidence should distinguish exposure, assisted practice, unaided application, repeated interpretation and unfamiliar delayed checks.

Security+/CCNA relevance tags are provisional. They are not full official-objective mappings, exam weightings or endorsed preparation materials. Future coverage pages should use an explicitly versioned syllabus with per-objective mappings, evidence dates, gaps and next practice. No exam-pass estimate is produced. The legacy 80% results threshold is an app practice target only.

## Run locally

Python 3.10+:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python cyber-skills-path.py
```

Open http://127.0.0.1:5000. In PyCharm use this project's `.venv/bin/python` and run `cyber-skills-path.py`.

A random browser-session secret is generated at startup unless `SECRET_KEY` is set. Learning records persist separately in ignored `progress.sqlite3`. Set `PROGRESS_DB` to use another writable SQLite file. The local database represents one learner shared by all browsers using this app; there are no user accounts or multi-user isolation. Keep the Flask development server local. Debug mode is opt-in with `FLASK_DEBUG=1`.

```bash
python -m unittest discover -s tests -v
```

## Next implementation slices

1. Expand foundations: Linux orientation → files → permissions → processes → shell pipelines; Python values → collections → functions → files → small utilities. Add meaningful output interpretation and contextual feedback.
2. Develop Security+ knowledge: controls, IAM, cryptography, logs, risk, incident response and governance. Connect foundational skills into practical reasoning.
3. Develop CCNA knowledge: addressing, TCP/IP, DNS/DHCP, switching/routing, VLANs, access controls and automation. Use diagrams, packet traces and simulated outputs.
4. Improve evidence: persist attempts, hints, assistance declarations and dates; add spaced revisits and unfamiliar checkpoints. Separate learning stage from demonstrated proficiency.
5. Add versioned certification mappings and objective-gap views. Review the original command questions before incorporating them into evidence.
6. Later add isolated, disposable practice environments and optional local environment verification. Installed software is not proof of skill or permission. Use explicitly scoped lab targets, controlled network access and resettable environments; do not execute learner code in the Flask process or expose a general-purpose host shell.

## Project structure

- `cyber-skills-path.py`: Flask setup and retained command-practice routes.
- `core/learning.py`: concept catalogue, starter mappings and SQLite progress.
- `core/learning_routes.py`: dashboard, orientation, placement, lesson and coverage routes.
- `data/learning.json`: six concept-led starter cycles.
- `core/engine.py` and the original JSON files: legacy command practice.
- `templates/`: learning views and original simulated terminal.
- `tests/`: route, progress and scenario regressions.

No live target interaction, shell execution or attack-box provisioning is implemented.
