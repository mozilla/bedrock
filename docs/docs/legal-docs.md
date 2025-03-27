---
render_macros: true
---

# Legal Docs {: #legaldocs }

Privacy notices and their applicable translations are markdown files managed by the legal team in the [legal-docs](https://github.com/mozilla/legal-docs) repository.

When the markdown files are imported into bedrock they are parsed using the default python markdown library and [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/). BeautifulSoup allows content selection and manipulation using [CSS selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors).

For example the code:

``` jinja
{{ doc.select('body > section > [datetime] ~ p')|join|safe }}
```

means something like:

From the document, find the `body` element, then find the `section` element that is its direct descendant, then look for a direct descendant with a `datetime` attribute, select all `p` that are its siblings. Join that array of data, and then print it without filtering it for unsafe characters.

If you would like to see the structure of the html you're working with, you can print it all to the page with `{{ doc.select('body') }}`.

## Templates

There are three templates:

-   base-notice
-   base-notice-headings
-   base-notice-paragraphs

### base-notice

This is a basic template that will extract a lead-in section and add the appropriate classes to style lists. It will print the rest of the privacy notice un-altered.

### base-notice-headings

This template is preferred for longer privacy notices. It collapses content under h3 headings.

The [V1.2 subscription services](https://github.com/mozilla/legal-docs/blob/21c1e31ea5092565d7e3eff8aecd2612395e8497/en/subscription_services_privacy_notice.md) notice is a good example of this template. It prefers content formatted like:

``` markdown
# Start the document with an h1, it will be used for the page title and first heading

Version 1.2, Effective February 5, 2024
{: datetime="2024-02-05" }

## The first heading will be the heading in the lead-in section

Paragraphs after the first heading but before later headings will be displayed as part of the lead-in section.

A line will appear under the last paragraph of the lead-in.

## This will be displayed as an h2 heading and the sibling elements will not be collapsed until an h3 is encountered

This paragraph will be visible

### This will be displayed as an h3 heading and will serve as a toggle for all its siblings until the next h3 {: provide-an-id }

* This will be a bulleted list that is collapsed under the h3 heading

This will be a paragraph that is collapsed under the h3 heading

### Footnote {: footnote }

If a section contains a heading with an ID of `footnote` the section will be extracted and output as the last thing on the page.

None of the elements in this section will be collapsed.
```

### base-notice-paragraphs

This is an older style template that we would like to phase out in favour of the heading template. It assumes the notice will be formatted in a series of sections each with an introductory paragraph and then bulleted lists of further information. When the notice is rendered, the bulleted lists are collapsed behind a "learn more" button.
