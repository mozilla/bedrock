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

Keep commit titles short, imperative, and linked to issues when available (e.g., `Tighten hero metrics (#16595)`). Focus diffs and note migrations, toggles, or telemetry changes. Pull requests should explain intent, list verification steps (`make test`, screenshots), and link to bugs. Flag rollout considerations when touching configuration under `docker/`, `**/migrations/` or monitoring.

## Security & Configuration Tips

* Keep secrets out of version control.
* Use a 12-Factor App pattern and an .env file.
* Where necessary (eg JSON credential files) store machine-specific credentials in `local-credentials/`.
* Install the local git hooks via `make install-custom-git-hooks`.
* If a changeset includes a GitHub Action or Workflow, use [Zizmor](https://zizmor.sh/) to check it for security issues before considering the work complete.

## Wagtail CMS

* When planning Wagtail work, remember that <https://docs.wagtail.org/en/7.3/llms.txt> and the full version at <https://docs.wagtail.org/en/7.3/llms-full.txt> contain LLM-appropriate documentation.
* If the version of Wagtail (not counting patch releases) in `pyproject.toml` doesn't match the version in the LLM-appropriate URLs mentioned, please update this AGENTS.md then load the new info

## m24 CMS blocks

Conventions for the m24 blocks in `bedrock/mozorg/blocks/common.py`, with templates in `bedrock/mozorg/templates/mozorg/cms/blocks/` and styles in `media/css/m24/`:

* Put a block's options in a `<Name>BlockSettings` StructBlock with `icon = "cog"`, `collapsed = True`, `label = "Settings"`, a `label_format` and `form_classname = "compact-form struct-block"`. Background color is a `background_color` ChoiceBlock whose values are theme classes: `""` for white, then `m24-t-dark`, `m24-t-green`, `m24-t-orange`, `m24-t-pink` and `m24-t-gray`.
* Block templates wrap the component in an outer element that carries the background class, then a `<div class="m24-c-content">` container (see `prose_block.html`).
* Headings follow `block_level` (`{% set heading_level = block_level if block_level else 2 %}`). Each page has exactly one `<h1>`, and every block after it starts at `<h2>`; see `freeform.html` for a page that promotes its first block's heading or falls back to a visually hidden `<h1>`.
* Freeform page StreamField block names end in `_block`.
* Class prefixes: `m24-c-` for components, `m24-l-` for layout variants, `m24-t-` for theme and size modifiers and `m24-u-` for utilities (e.g. `m24-u-lede`).
* Use the `$m24-color-*` variables, not the `$token-color-*` values. `.m24-t-dark` uses the `invert-colors` mixin, so colors written in light-theme terms flip without being redeclared for dark sections. An element with its own dark background can `@include invert-colors` so links and text inside it adapt.
* Grid helpers live in `vars/_grid.scss`: `grid($n)` only works inside a full-width container that has the container padding, `page-grid($n)` gives n columns of the page grid inside a full-width parent with no padding (e.g. `.m24-c-article`), and `sub-grid($n, $context)` gives n columns inside a context-column parent. Check the rendered widths in a browser, because nesting these changes what the percentages resolve against.
* Limit body text width with `$text-body-max-cols` (in `vars/_text.scss`) rather than a literal column count.
* Use the spacing tokens for vertical rhythm: `--section-spacing` between unconnected sections, `--group-spacing` to separate groups of related elements within a section, and `--item-spacing` between related elements. For example, the heading and subheading in an intro are separated by item spacing, the intro is separated from a group of tiles by group spacing, and the tiles inside that group are separated by item spacing.
* Build intros with the `m24_intro` macro in `macros-m24.html`, placed inside the background wrapper and `.m24-c-content`. Its `tag` defaults to `header`, for an intro that introduces the content after it; pass `tag="div"` for an intro that stands alone, as the intro block does.
* Blocks with a heading size setting share `HEADING_SIZE_CHOICES`.
* Rich text fields share feature lists from `common.py`: `RICHTEXT_BODY_FEATURES` for bodies that sit under a block's own heading field, and `ARTICLE_RICHTEXT_FEATURES` (`h2` and `h3` plus the body set) for article text.
* Wrap rendered rich text in `.m24-c-rich-text` to get the editor typography in `rich-text.scss`.
* Use logical properties (`border-inline-start`, `inset-inline-start`, `padding-inline-start`), because bedrock serves right-to-left locales.
* The browser support matrix is Safari 15.6+ and Firefox 115+. Check caniuse before using newer CSS.
* Keep the `sizes` value on `srcset_image` in step with the image's CSS widths, and re-check it whenever the layout changes.
* Image and mask URLs in m24 SCSS are absolute `/media/...` paths, because `STATIC_URL` is `/media/`.
* Wagtail serializes block definitions, including features, choices, `help_text` and `template`, into migrations, so changing any of them needs `makemigrations`.
* Don't keep lists of things in comments; they go out of date.

## LLM assistance

* When committing code, do not list the LLM as a co-author - it is a tool, not a developer. All code committed is the responsibility of the human developer using the LLM. This is in line with <https://firefox-source-docs.mozilla.org/contributing/ai-coding.html>
