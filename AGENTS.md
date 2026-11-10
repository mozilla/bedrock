# Repository Guidelines

## Project Structure & Module Organization

Bedrock is a Django monolith: core apps, views, and templates live in `bedrock/`. Shared helpers sit in `lib/`, while automated checks and integration flows reside in `tests/`. Front-end source (Sass, JS, icons) lives under `media/`; webpack entry points are in `assets/`, and collected output is in `static/`. Infrastructure and localization assets are under `docker/`, `docs/`, and `l10n/`—update them when deployment or translation changes land.

## Architecture (big picture)

Bedrock is a Django monolith (~25 apps in `bedrock/`) that serves mozilla.org. A few cross-cutting systems are worth understanding before editing, because they span multiple files:

* **Templating is Jinja2, not Django templates.** Configured via `django_jinja` in `bedrock/settings/base.py` with the environment in `bedrock/jinja2.py`. Page templates extend `bedrock/base/templates/base-protocol.html`.
* **Localization of hard-coded templates for regular Django views (but not CMS-driven pages) flows through Fluent.** Source strings live in `l10n/en/*.ftl`; templates pull them with the `ftl('message-id')` global (optional `fallback=` to another message). The machinery is in `lib/l10n_utils/` (`fluent.py` loads resources, `templatetags/fluent.py` exposes the tag). `ftl_file_is_active('name')` gates whether a given `.ftl` file is translated enough to show — this is how alternate template variants are switched on (e.g. the footer renders `footer-refresh.html` only when both `navigation_refresh` and `footer-refresh` are active, otherwise the legacy `footer.html` markup). URL locale prefixes come from `bedrock_i18n_patterns` in `bedrock/urls.py`.
* **Front-end assets are bundled by webpack from named bundles.** `media/static-bundles.json` is the source of truth: it maps bundle names to lists of Sass/JS files in `media/`. `webpack.config.js` builds those into `assets/`; `webpack.static.config.js` copies images/fonts and the Protocol package. Templates include them with `css_bundle('name')` / `js_bundle('name')` (defined in `bedrock/base/templatetags/helpers.py`), which resolve cache-busted filenames via Django's manifest storage. Adding CSS/JS means editing `static-bundles.json`, not just the template.
* **Protocol is Mozilla's design system**, consumed as the `@mozilla-protocol/core` npm package. Its components use the `mzp-*` class prefix (`mzp-c-footer`, `mzp-c-button`, …). Bedrock layers overrides in `media/css/protocol/`; shared chrome (footer, nav) lives in `bedrock/base/templates/includes/protocol/`.
* **Wagtail CMS** powers editor-managed content and lives in `bedrock/cms/` (models, hooks, middleware). CMS pages are served through Wagtail's page hierarchy rather than `urls.py`, and content is translated via the Smartling plugin (`bedrock/cms/wagtail_localize_smartling/`).
* **Settings** are environment-driven via `everett` in `bedrock/settings/base.py` (`config(...)`), with `test.py` overrides for tests. `lib/` holds shared, app-agnostic helpers.

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
Use markers such as `cdn`, `download`, or `headless` to scope runs (e.g., `pytest -m "not cdn"`). `npm run jasmine` rebuilds assets via `webpack.test.config.js` and runs front-end unit coverage. `make test` is the containerized umbrella; browser flows in `tests/playwright/` require QA coordination before extending.

## Workflow guidelines

When working on a feature or fix, work on a dedicated branch whose name is prefixed with the relevant issue number (or nothing) and then is a kebab-cased short term for the branch. Ask for the issue ID and a short summary, turning "12345" and "Amend CSS shadows for nav" to "12345--amend-css-shadows-for-nav". Use the Issue ID to generate a URL for it (<https://github.com/mozmeao/bedrock/issues/ISSUE_ID>) and see if the descroption helps you work on the task. Always offer to run the tests after the work appears to be complete.

## Commit & Pull Request Guidelines

Keep commit titles short, imperative, and linked to issues when available (e.g., `Tighten hero metrics (#16595)`). Focus diffs and note migrations, toggles, or telemetry changes. Flag rollout considerations when touching configuration under `docker/`, `**/migrations/` or monitoring.

### Writing PR descriptions

Keep all four headings from `.github/PULL_REQUEST_TEMPLATE.md`. Answer one that does not
apply with `n/a` — one word is a complete answer, and inventing content to fill a heading is
worse than admitting it is empty. Don't end the description with "🤖 Generated with Claude
Code" or any other generated-by line.

A description directs the reviewer's attention. It does not restate the diff, and it does not
explain this codebase back to the team that owns it. Check what actually changed
(`git diff --stat main...`, plus a scan for migrations, fixtures, config, and deletions —
these are the categories most likely to hide a consequence a stat diff won't show) before
writing, so the description matches reality.

Take length out of describing the change.

**One-line summary.** One or two sentences: what the change does, and why where the title
does not already make that obvious. Compress rather than qualify. "Add compact-input class
for narrower input fields" beats "Add a reusable `.compact-input` CSS class to
narrow admin number fields that only ever hold a few digits, instead of rendering
full-width" — 21 words and two subordinate clauses to say less than eight.

**Significant changes and points to review.** Short bullets, most significant first, one
clause each. Nest a sub-bullet where a consequence needs one; never go past two levels. A
single sentence is right where the change is one idea, and a short paragraph is right
where the reviewer needs domain context the diff cannot give — mozmeao/springfield#1813 explains that editors
keep several "General" WNPs published at once, which is why the filter had to move off the
slug.

Name a file where the file is the point — "Remove the unused wagtail-admin.scss",
"Add regenerate_analytics_ids() to cms/blocks.py" — and prefer the bare
filename when it identifies the thing on its own.

Rejected — mozmeao/springfield#1791 as first drafted:

> - **Page-level validation** (`springfield/cms/models/base.py`) — every sample-rated
>   Conditional Display block on a page must share the same rate. **This is the most critical
>   part to review** — it's new validation that runs on every page save across the whole CMS.

Replacement — mozmeao/springfield#1791 as merged:

> - Adds sample_rate field on ConditionalDisplayBlock (DecimalBlock, 0.01-100%).
> - Multiple components can be displayed based on sample-rate but the sample rate must match.
>   - Page.clean() now rejects a save if two sample-rated blocks on the same page disagree.

- Say what changed. Add why only where the change does not already imply it.
- Do not rate your own change. No "low risk", "mechanical", "straightforward", "nothing here
  is riskier than a CSS tweak", and never a reflexive "this is the most critical part to
  review" — most PRs have no such thing, and a rating carries nothing a reviewer can act on.
- Do flag a change that is genuinely high-risk or wide blast radius, in one line, stating its
  reach as a fact rather than a rating: a data migration, a schema change, something hard to
  undo, or behaviour that reaches past the scope the summary names. "The copy hook now
  regenerates these fields on every page copy, of every page type" earns that line.
  Validation that only fires on the blocks this PR adds does not. When nothing qualifies,
  say nothing — silence is the normal case.
- A side-effect worth knowing about but not risky — a duplicate file deleted, a stray
  reference removed — is a plain bullet like everything else.
- Fold low-risk, mechanical fallout — updated fixtures, ported static pages, renamed CSS —
  into its own short item, kept brief and after the substantive bullets, so it doesn't crowd
  out what the reviewer actually needs to think about.
- Flag genuine uncertainty about your own work — "I'm not sure this handles the RTL case" —
  distinct from rating risk. Risk-rating is banned above; naming a real unknown is not, and
  is often the most useful sentence in the description.
- Never explain mechanics the team already knows: why no migration was generated, how this
  project's StreamField subclass behaves, what an existing template loop does.
- Never describe your own process. Not which approach you tried first, not what a review
  caught, not that the branch is stacked on another PR. Two things that look similar but are
  worth keeping: deliberately deferred scope — "Bare template changes for the new layouts
  (no styles yet)" — and a port's provenance — "Ported from mozmeao/springfield#1570".

**Issue / Bugzilla link.** The full GitHub issue, Jira or Bugzilla URL, or `n/a`. List all of them where a change
closes more than one, and give the context on a cross-reference: "Follow-up to
mozmeao/springfield#1813, fixing the issue pointed out by <comment URL>".

**Testing.** What a reviewer does by hand to check this. The one section worth expanding.

- Open with prerequisites where there are any: "Make sure you have GCP/DNT disabled", "get
  prod DB (or set up a referral hub page with an image on it locally)".
- Include setup commands a reviewer must run to see the change at all, such as
  `./manage.py migrate`. Leave out test and lint commands: `pytest`,
  `npm run jasmine` and `stylelint` only re-check what CI already checked.
- Give the URL to load. Deep-link to the specific fixture page where there is one, with the
  expected result after it.
- One step per thing to verify, phrased as a check — "Check an error displays when two blocks
  disagree on sample rate", not "set two blocks to different rates → save is rejected, error
  names both blocks". `- [ ]` checkboxes where the reviewer is working through a list.
- Ask plainly for a close look when you want one: "Look at this one pretty closely please, it
  changes the thanks page."

A complete example — mozmeao/springfield#1823, in full, as the shape to aim for:

> ## One-line summary
>
> Enforce good practices for image titles and descriptions.
>
> ## Significant changes and points to review
>
> - Add a new `is_decorative` field `SpringfieldImage`
> - Make the description field required when an image isn't decorative
> - Reject image titles that look like file names
> - Remove Wagtail's default behavior to use the image's file name as the title
> - Render an empty `alt` attribute for images flagged as decorative
>
> ## Issue / Bugzilla link
>
> https://mozilla-hub.atlassian.net/browse/WT-1715
>
> ## Testing
>
> - Edit any image and check the "Image is decorative" checkbox
> - Load a page that uses the image and verify that it renders an empty `alt` attribute
> - Upload a new image from a page editor and check that the form doesn't pre-fill the title
>   field with the image file name
> - Verify that the form rejects an empty description
> - Check the "Image is decorative" checkbox and verify that the form accepts an empty
>   description
> - Do the same on the multiple image upload form (`/cms-admin/images/multiple/add/`)

166 words. Five bullets, each one clause. Backticks on identifiers, none on prose. No bold,
no em-dashes, no repo paths, no risk rating, no test commands. Testing is six imperative
checks an editor could follow without reading the diff.

## Security & Configuration Tips

* Keep secrets out of version control.
* Use a 12-Factor App pattern and an .env file.
* Where necessary (eg JSON credential files) store machine-specific credentials in `local-credentials/`.
* Install the local git hooks via `make install-custom-git-hooks`.
* If a changeset includes a GitHub Action or Workflow, use [Zizmor](https://zizmor.sh/) to check it for security issues before considering the work complete.

## Wagtail CMS

* When planning Wagtail work, remember that <https://docs.wagtail.org/en/7.3/llms.txt> and the full version at <https://docs.wagtail.org/en/7.3/llms-full.txt> contain LLM-appropriate documentation.
* If the version of Wagtail (not counting patch releases) in `pyproject.toml` doesn't match the version in the LLM-appropriate URLs mentioned, please update this AGENTS.md then load the new info

## LLM assistance

* When committing code, do not list the LLM as a co-author - it is a tool, not a developer. All code committed is the responsibility of the human developer using the LLM. This is in line with <https://firefox-source-docs.mozilla.org/contributing/ai-coding.html>
