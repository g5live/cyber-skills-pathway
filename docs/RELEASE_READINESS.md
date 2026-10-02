# Release readiness — cyber-skills-pathway

Review date: 2 October 2026. Proposed work, not an implementation or release announcement.

## Appropriate next functionality

- Improve layout/menu navigation and detailed skills pages for all nine headings, as recorded in the README roadmap.
- Add meaningful attempt/hint/assistance records, delayed checks, evidence dates and export/reset controls. Separate stage completion from independent skill evidence.
- Add versioned Security+/CCNA relevance mappings, clear unassessed gaps and more connected exercises.

## Before a first public release

- Keep the first supported release explicitly local and single-user. Provide a sample configuration, database backup/reset guidance and reproducible startup steps.
- Review CSRF protection across every state-changing route, session handling and validation before supporting network hosting. A hosted multi-user edition also needs accounts, ownership checks, migrations, privacy choices and a production deployment configuration.
- Add CI for route/content regressions and browser checks for navigation, keyboard access, mobile layouts and contrast. The current checks are not full accessibility or security verification.
- Do not add live command execution to the Flask process. Isolated practice infrastructure belongs in a separately reviewed later phase.

## Shared release preparation

Before publishing a tagged release, choose a project licence after reviewing tutorial and asset provenance; document installation, supported versions, examples and known limits; add a changelog, issue/PR templates, contribution guidance and a vulnerability-reporting policy; run CI on the claimed platforms and test a clean installation. Add dependency updates and appropriate repository security checks where supported. Provide tagged release notes and usable download assets where relevant. These are readiness recommendations, not GitHub certification or features already delivered.

GitHub references: [community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file) and [releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).
