---
name: create-block
description: Create a new Wagtail CMS block
argument-hint: "<description of the block to build>"
---

## Blocks

Bedrock has no single centralized block registry. Two conventions exist, split by app:

- A single flat file, e.g. `bedrock/anonym/blocks.py`, defining every StreamField block class for that app.
- A package split by content domain, e.g. `bedrock/mozorg/blocks/` (`common.py`, `advertising.py`, `leadership.py`, `navigation.py`, ...).

Follow whichever convention the target app already uses. If the app has no blocks yet, start a single `blocks.py`.
Shared, cross-app utility blocks (not page content) live in `bedrock/cms/blocks.py` (e.g. `UUIDBlock`, `regenerate_analytics_ids`) — only put something there if multiple apps need it, not for new page-content blocks.
StreamField definitions themselves stay on the page model in the app's `models.py` (e.g. `AnonymIndexPage.content`), not in a separate file.

If the instructions don't say which app the block belongs to, ask before starting.

## Templates

Bedrock uses Jinja2, not Django templates or `django-includecontents` — there is no component library.

Each block sets `Meta.template` and gets exactly one template, at `bedrock/<app>/templates/<app>/blocks/<name>.html` (mozorg nests further by section, e.g. `mozorg/cms/advertising/blocks/`).

Before writing new markup:
- For nested/child StreamField values, use Wagtail's `{% include_block %}` tag rather than hand-rolling recursion.
- For reusable non-block fragments, check the app's existing templates and `bedrock/base/templates/includes/` for something to `{% include %}` (pass "props" via `{% with %}`). Don't invent a formal component system — reuse an existing include/macro if one already covers the markup, otherwise write the template inline.

## Fixtures

Fixtures are plain Python, not JSON dumps. In `bedrock/<app>/fixtures/block_fixtures.py`, write one function per block returning a `list[dict]` in StreamField JSON shape (`{"type": ..., "value": {...}, "id": ...}`), e.g. `get_figure_block_variants()`. Add enough variants to cover the block's options — not every combination.
Use the block's text fields (headings, content) to describe its options and behaviors. Be concise; use more descriptive text where a field is meant for longer copy.

When the new block nests other blocks that already have fixtures, reuse their variant functions instead of duplicating literal values (e.g. pull buttons from the existing button fixtures).

If the app composes full pages from block fixtures (`bedrock/<app>/fixtures/page_fixtures.py`, see anonym), add the new block's variants there too. If the app also has a fixture-loading management command for seeding real pages into the Wagtail admin for manual QA (e.g. `load_anonym_fixtures.py`), extend it — but only add one if the app doesn't have one and it's actually wanted; mozorg's fixtures are consumed only from tests and have no such command.

## Tests

Follow whichever convention the app already uses: a dedicated `test_blocks.py` (mozorg) or block tests alongside `test_models.py` (anonym).

Testing idiom: build/load a page via fixtures, use pytest's `rf` (RequestFactory) and `minimal_site` fixtures, call `page.serve(request)` (or `serve_preview`), and parse `response.text` with BeautifulSoup. Assert on classes, text, and attributes.

Every field on the block must be verified end-to-end: not just that an element exists, but that its content matches the fixture data. If the block sets a data attribute (e.g. analytics attributes below), assert that attribute's value too. When asserting headings, select by the specific heading tag (`h1`/`h2`/...) to confirm the hierarchy is correct, not just that a heading with the right text exists somewhere.

## Reuse before building

Before writing new markup or fixtures, check whether an existing shared include, macro, or block fixture already covers what's needed (see Templates and Fixtures above) rather than duplicating it.

## Important considerations

Bedrock has no `block_position`/`block_text` equivalent. Heading hierarchy is tracked with `block_level`, a plain Jinja template variable (not a block field) set in the parent page template before calling `{% include_block %}`, e.g. `bedrock/anonym/templates/anonym/anonym_content_sub_page.html`:

```jinja
{% set block_level = 1 if ns.headings == 0 else 2 %}
{% include_block block %}
```

and consumed by the block's own template (`bedrock/anonym/templates/anonym/blocks/section.html`): `<h{{ block_level }} class="mzan-heading">`. Any block that renders a heading and can contain child blocks with their own headings must set/increment `block_level` before including them.

Analytics attributes are `data-cta-text` and `data-cta-uid`, not `data-cta-position`. `data-cta-uid` comes from a `UUIDBlock`-backed `analytics_id` field (auto-generated, excluded from translation — see `bedrock/cms/blocks.py`); `data-cta-text` is just the link/button's own label. For rich text fields where attributes can't be set at block-definition time, use the `add_cta_analytics` Jinja filter (`bedrock/base/templatetags/helpers.py`) to inject both attributes onto every rendered `<a>`.

## Steps

Use the instructions to build the block: $ARGUMENTS

Follow these steps to do it:

1. Determine which app the block belongs to, and match that app's existing `blocks.py`/`blocks/` convention.
2. Check for reusable includes/macros/block fixtures before writing new markup (see Reuse before building).
3. Create the block (block class + template).
4. Create testing fixtures (and page fixtures / fixture-loading command, if the app uses them).
5. Create unit tests.

First present the plan to the user with a simple explanation of what will be done. Allow the user to give feedback before starting the implementation.
