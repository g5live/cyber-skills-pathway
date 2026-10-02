![G5LIVE — Build · Understand · Apply](assets/brand/g5live.svg)

# Cyber Skills Pathway

A personal, concept-led learning application for building connected Linux, Python, networking and security skills. The aim is understanding and practical judgement, not awarding certificates, professional registration or job qualifications. Certification coverage is an optional reference for learners who choose external assessment.

## Learning model

Every concept follows **1 Learning → 2 Observing → 3 Practising → 4 Reinforcing → 5 Checking**. Earlier knowledge should recur in later situations: navigating Linux supports file handling; permissions support least privilege; Python data handling supports automation; DNS and subnetting support investigation.

Start directly at a chosen area or take a short placement check based on your selected confidence. The app explains its recommendation and lets you confirm any available starting point. Placement never awards learning progress and a small sample cannot prove proficiency.

The design draws on the structure of the personal Obsidian Skills Concept Table: concept, branch, development stage, supporting evidence and next target. Personal scores and private learning records are not imported. The curriculum should eventually use prerequisite relationships and evidence to recommend the next useful concept rather than a sequence of isolated tool rooms.

## Dashboard and proposed pathway

Each tier has an icon and a red → amber → green progress bar. Shared concepts can contribute to multiple tiers. The current percentages use a fixed set of published starter concepts, including unseen concepts in the denominator. They measure activity completion, not knowledge confidence or likelihood of passing an exam. Higher-tier prerequisite progress is explicitly labelled; specialist content is not unlocked or claimed by completing basics.

| Tier | Current scope | Next development |
| --- | --- | --- |
| 🧱 Foundational Skills | Eight concepts: Linux navigation/files, shell streams, processes, Python data/control flow/functions/files | Deeper shell fluency, Git, practical utilities and error handling |
| 🛡️ Security Basics | Eight concepts: CIA, permissions, identity, MFA, phishing, integrity, risk, logs/recovery | Broader Security+ knowledge and connected evidence-led scenarios |
| 🌐 Network Basics | Eight concepts: network roles, subnets, TCP/UDP, DNS, DHCP, gateways, HTTP/TLS, troubleshooting | Switching, routing, VLANs, packet interpretation and deeper CCNA learning |
| 🔎 Security Practitioner | Evidence-led triage starter plus shared prerequisites | Connected investigations and proportionate response decisions |
| 🧭 Junior Pentester | Scope-before-tools starter plus shared prerequisites | Scoped enumeration, validation and reporting |
| 📋 Registered Pentester | Engagement-planning starter | Professional assessment methodology; no registration awarded |
| ⚔️ Offensive Security | Trust-boundary reasoning starter | Controlled offensive investigations |
| 🎯 Red Team Ops | Exercise-objectives starter | Authorised operational scenarios and debriefing |
| 🧬 Exploit Developer | Input-bounds and failure-reasoning starter | Specialist systems and memory-model foundations |

These are learning areas, not a mandatory career ladder. Networking and security can develop alongside coding and system skills. Each advanced area has an introductory concept; full specialist curricula remain future work. Initial development should stretch slightly beyond the owner's current Linux/Python/networking/security knowledge rather than attempt a complete professional curriculum.

## What works today

- A dashboard with shared-concept progress across tiers.
- Manual entry selection and an optional short placement check with user-confirmed recommendations.
- 30 starter concepts across all nine areas, with suggested preparation links, worked examples, answer explanations and next-lesson navigation.
- All five learning stages per starter concept; practical submissions are checked but never executed.
- Local SQLite persistence for one personal learner, surviving app restarts and browser-session changes.
- Security+ and CCNA starter relevance pages showing completed activities and unassessed evidence.
- Quickfire Reinforcement provides timed recall across all nine topics and five learning levels. The original 40 command scenarios remain archived in their JSON files.

This is an expanded foundation library, not complete foundational, Security+ or CCNA courses. Original command exercises are retained as archived content rather than automatically counted as evidence on the new dashboard. Their simplified validation rules and content need further review.

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

1. Deepen the existing foundations with connected Linux/Python tasks, small utilities, error handling and more demanding output interpretation.
2. Develop Security+ knowledge: controls, IAM, cryptography, logs, risk, incident response and governance. Connect foundational skills into practical reasoning.
3. Develop CCNA knowledge: addressing, TCP/IP, DNS/DHCP, switching/routing, VLANs, access controls and automation. Use diagrams, packet traces and simulated outputs.
4. Improve evidence: persist attempts, hints, assistance declarations and dates; add spaced revisits and unfamiliar checkpoints. Separate learning stage from demonstrated proficiency.
5. Add versioned certification mappings and objective-gap views. Review the original command questions before incorporating them into evidence.
6. Later improve layout and menu navigation: consistent page structure, clear topic grouping, breadcrumbs, visible current topic/stage, predictable back/next controls, accessible keyboard/focus behaviour and responsive layouts. Keep starting-point selection, learning, coverage and Quickfire easy to distinguish. Review usability before adding more menu complexity.
7. Later develop detailed skills pages for **all nine headings**: explain the area and intended outcomes, prerequisites, concepts and subskills, a recommended learning sequence, worked examples, practical use, links to related areas, completed activities, supporting evidence, gaps and next practice. Separate assisted exposure from independent application and retained understanding. Add versioned certification relevance where appropriate without implying certification, registration or a job qualification.
8. Later add isolated, disposable practice environments and optional local environment verification. Installed software is not proof of skill or permission. Use explicitly scoped lab targets, controlled network access and resettable environments; do not execute learner code in the Flask process or expose a general-purpose host shell.

## Project structure

- `cyber-skills-path.py`: Flask setup and retained command-practice routes.
- `core/learning.py`: concept catalogue, starter mappings and SQLite progress.
- `core/learning_routes.py`: dashboard, orientation, placement, lesson and coverage routes.
- `data/learning.json`: 30 concept-led starter cycles.
- `core/engine.py`: five-level Quickfire answer checking; the original JSON files retain archived command exercises.
- `templates/`: learning views and original simulated terminal.
- `tests/`: route, progress and scenario regressions.

No live target interaction, shell execution or attack-box provisioning is implemented.

## Foundation library

| Area | Suggested lesson sequence |
| --- | --- |
| Foundational Skills | Linux navigation → files and paths → pipes/redirection → processes/services → Python data → conditions/loops → functions → files/environments |
| Security Basics | CIA objectives → permissions → authentication/authorisation → passwords/MFA → phishing → hashes/integrity → threats/risk/controls → logs/recovery |
| Network Basics | Hosts/switches/routers → IPv4 subnet scope → TCP/UDP/ports → DNS → DHCP → gateways → HTTP/TLS → evidence-led troubleshooting |

Every lesson includes Learn/Observe material and three applied checks, for 150 learning activities across the library. Prerequisites are recommendations, not locks. Successful checks explain why the answer fits; notes remain available for assisted practice. Text answers support whitespace normalisation and case-insensitive concept terms; commands and paths retain case sensitivity. This is still bounded answer checking, not semantic evaluation of free-form explanations.

The quick placement check intentionally retains its original two-to-four-question sample rather than expanding into a full course test. Existing concept IDs and database records remain valid. Adding material expands the progress denominator: percentages can decrease while completed activities stay unchanged. That reflects curriculum coverage, not loss of ability.

Technical further-reading links are included where appropriate, using the GNU Bash manual, Python tutorial, CISA/NIST guidance and IETF protocol specifications. Examples use simulated systems and documentation addresses; no submissions are executed.

## All nine topic pages and Quickfire Reinforcement

Each dashboard heading opens its topic page. The six later topics now include one five-stage starter concept each: evidence-led triage, scope before tools, engagement planning, trust boundaries, exercise objectives, and input bounds. These are introductory material, not full specialist training.

Quickfire Reinforcement uses the same concept library across all nine topics. Its five levels are Learning (with notes), Observing (with worked examples), Practising (practice questions), Reinforcing (different recall questions), and Checking (checkpoint questions). They are learning modes rather than professional difficulty ratings. Timers are 5, 10, 20, 30 or 60 minutes; longer values are rejected by the server. Quickfire completion does not advance persistent learning progress. The former command-practice URL remains a compatibility alias.

UI prose uses UK English and pages declare en-GB. Executable commands, protocol names, programming keywords and CSS/API identifiers keep their required spelling.

## Progress snapshot — 2 October 2026

The application has moved from its original command-recall prototype to a concept-led personal learning app: nine clickable topic pages, 30 concepts/150 learning activities, persistent local progress, provisional Security+/CCNA relevance pages, and Quickfire Reinforcement across all nine topics and five levels. The current suite has 21 passing tests, including every topic/level combination and the 5–60-minute timer bounds.

The topic pages are currently simple starter listings. Improved layout/navigation and comprehensive informative skills pages are deliberately recorded as later-stage work above, not features already delivered. Advanced topics contain introductory primers only. Progress bars record starter activity completion; they are not mastery or exam-readiness scores.

## Shared brand and release preparation

Part of the G5LIVE app family. See the [shared brand guide](assets/brand/BRAND.md) and [project-specific release-readiness review](docs/RELEASE_READINESS.md) for proposed functionality and public-release preparation.
