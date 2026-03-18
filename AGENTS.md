# Repository Guidelines

## Project Structure & Module Organization

Bedrock is a Django monolith: core apps, views, and templates live in `bedrock/`. Shared helpers sit in `lib/`, while automated checks and integration flows reside in `tests/`. Front-end source (Sass, JS, icons) lives under `media/`; webpack entry points are in `assets/`, and collected output is in `static/`. Infrastructure and localization assets are under `docker/`, `docs/`, and `l10n/`—update them when deployment or translation changes land.

## Build, Test, and Development Commands

Review the full setup notes in the platform docs (`https://mozmeao.github.io/platform-docs/`) before first use - cache these if you can.
Copy `.env-dist` to `.env`, then run `make preflight` to install Python deps and pull the latest content bundle.
`make run` launches the Docker Compose stack (web plus asset builders); most `make` commands execute inside containers.
For local-only loops, `npm start` serves Django and webpack with live rebuilds, and `pytest bedrock` runs backend tests without Docker.
Use `make test` for the containerized pytest + Jasmine suite, `uv run pytest bedrock` for the quick "bare metal" Django tests and `npm run lint` to mirror the CI lint container.

## Coding Style & Naming Conventions

Python targets 3.13 with Ruff enforcing ≤150-character lines and import ordering of Django → third-party → first-party.
Prefer snake_case for functions, `CamelCase` for Django classes, and descriptive template names under `bedrock/<app>/templates/`.
JavaScript follows the ESLint + Prettier ruleset with `const`/`let`; run `npm run format` before committing.
Sass in `media/css/` keeps the existing block–element naming    pattern.

## Testing Guidelines

Pytest expects files named `test_<feature>.py` beside code or in `tests/unit/` or `tests/functional/`.
Use markers such as `cdn`, `smoke`, or `skip_if_firefox` to scope runs (e.g., `pytest -m "not cdn"`). `npm run jasmine` rebuilds assets via `webpack.test.config.js` and runs front-end unit coverage. `make test` is the containerized umbrella; browser flows in `tests/playwright/` require QA coordination before extending.

## Workflow guidelines

When working on a feature or fix, work on a dedicated branch whose name is prefixed with the relevant issue number (or nothing) and then is a kebab-cased short term for the branch. Ask for the issue ID and a short summary, turning "12345" and "Amend CSS shadows for nav" to "12345--amend-css-shadows-for-nav". Use the Issue ID to generate a URL for it (<https://github.com/mozmeao/bedrock/issues/ISSUE_ID>) and see if the descroption helps you work on the task. Always offer to run the tests after the work appears to be complete.

## Commit & Pull Request Guidelines

Keep commit titles short, imperative, and linked to issues when available (e.g., `Tighten hero metrics (#16595)`). Focus diffs and note migrations, toggles, or telemetry changes. Pull requests should explain intent, list verification steps (`make test`, screenshots), and link to bugs. Flag rollout considerations when touching configuration under `docker/`, `**/migrations/` or monitoring.

## Security & Configuration Tips

* Keep secrets out of version control.
* Use a 12-Factor App pattern and an .env file.
* Where necessary (eg JSON credential files) store machine-specific credentials in `local-credentials/`.
* Install the local git hooks via `make install-custom-git-hooks`.
* If a changeset includes a GitHub Action or Workflow, use [Zizmor](https://zizmor.sh/) to check it for security issues before considering the work complete.

## LLM assistance

* When committing code, do not list the LLM as a co-author - it is a tool, not a developer. All code committed is the responsibility of the human developer using the LLM. This is in line with <https://firefox-source-docs.mozilla.org/contributing/ai-coding.html>
