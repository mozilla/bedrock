.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _contentful:

===========
Contentful Integration
===========

Overview
--------

Contentful is a headless CMS. It stores content for our website in a structured
format. We request the content from Contentful using an API. Then the content
gets made into Protocol components for display on the site.

We define the structure Contentful uses to store the data in **content models**.
The content models are used to create a form for editors to fill out when they want
to enter new content. Each chunk of content is called an **entry**.

For example: we have a content model for our "card" component. That model creates a
form with fields like heading, link, blurb, and image. Each card that is created from
the model is its own entry.

We have created a few different types of content models. The smallest create little
bits of code like buttons. Most are components that correspond to components in our
design system. Some group together entries for the smaller components into a bigger
component or an entire page.

For example: The _Page: General_ model allows editors to include a hero entry, body
entry, and callout layout entry. The callout layout entry, in turn, includes a callout
entry.

One advantage of storing the content in small chunks like this is that is can be
reused in many different pages. A callout which focuses on the privacy related reasons
to download Firefox could end up on the Private Browsing, Ad Tracker Blocking, and
Fingerprinter Blocking pages. If our privacy focused tagline changes from "Keep it
secret with Firefox" to "Keep it safe with Firefox" it only needs to be updated in
one entry. But, each of those pages could display that content using different layouts.

So, when looking at a page on the website that comes from Contentful you are typically
looking at several different entries combined together.

On the bedrock side, the data for all entries is periodically requested from the API
and stored in a database.

When a Contentful page is requested the code in `api.py` transforms the information
from the database into a group of Python dictionaries (these are like key/value pairs
or an object in JS).

This data is then passed to the page template (either Mozilla or for Firefox themed
as appropriate). The page template includes some files which take the data and feed
it into macros to create Protocol components. The same macros we use on non-Contentful
pages. There are also includes which will import the appropriate JS and CSS files to
support the components.

Once rendered the pages get cached on the CDN as usual.

Content Model
⬇️
Entry
⬇️
API
⬇️
database

page request
⬇️
view
⬇️
page template
⬇️
api.py (⬅️ database)
⬇️
macro


Content Models
--------------

Approach to structure
    Page vs layout vs component vs piece

Rich text field config

Emoji legend
➡ this component can be embeded without a layout wrapper
🎁 this is a layout wrapper for another component
✏️ this component includes editable content, not just layout config
📄 this component is a page, it will include meta data for the page, a folder, and slug
♟ this component is suitable for inclusion as an inline entry in a rich text field


Adding a new component
----------------------

Example: Picto

#. Create a content model in Contentful
_Follow the naming conventions._
You may need two models if you are configuring layout separately.
#. Add the new content model to the list of allowed references in other content models
(ATM this is just the "content" reference field on pages).
#. Create CSS and JS entries in static-bundles for the new component.
#. In api.py write a def for the component
#. In api.py add the component name, def, and bundles to the CONTENT_TYPE_MAP
#. Find or add the macro to macros-protocol
#. Import the macro into all.html and add a call to it in the entries loop
#.

Tips:
- can't define defaults in Contentful, so set those in your Python def
- for any optional fields make sure you check the field exists before referencing the content



Adding a new 'piece'
--------------------

Example: Wordmark.

#. Create a content model (or models) in Contentful
_Follow the naming conventions._
#. Add the new content model to rich text fields (like split and text)
#. Include the piece CSS in the Sass file for any component which may use it.
(yeah, this is not ideal) (see logo/wordmark)
#. Add a def to api.py to render the piece (like _make_wordmark)
#.


Adding support for a new product icon, size, folder
---------------------------------------------------

Many content models have drop downs with identical content. For example: the Hero, Callout,
and Wordmark models all include a "product icon". The icon can be one of any of the [supported
logos in Protocol](https://protocol.mozilla.org/demos/logo.html). Other common fields
are width and folder.

There are two ways to keep these lists up to date to reflect Protocol updates:

#. By opening and editing the content models individually in Contentful
#. Scripting updates using the API

At the moment it's not too time consuming to do by hand, just make sure you are copy and pasting
to avoid introducing spelling errors.

We have not tried scripting updates with the API yet. One thing to keep in mind if attempting this
is that not all widths are available on all components. For example: the "Text: Four columns" component cannot
be displayed in small content widths.


Bedrock Integration
-------------------



Filters

Assumptions
    - image sizes

Defaults are in bedrock not contentful




Terminology

    Content Model

    Content/Entry



L10N

Assets

- hosting
- sizing
- API

Preview

- where/how configure
- uses demo5 now but will move to dev
- only works at contentful-preview URL, pages will still only update every 5 min
- Publish/Changed/Draft

Roles/Permissions

-

Branch/Spaces

-

Useful Contentful Docs

https://github.com/contentful/rich-text-renderer.py/blob/a1274a11e65f3f728c278de5d2bac89213b7470e/rich_text_renderer/block_renderers.py#L77

https://www.contentful.com/developers/docs/references/images-api/#/reference/resizing-&-cropping/specify-focus-area

https://www.contentful.com/developers/docs/references/content-delivery-api/

https://contentful.github.io/contentful.py/#filtering-options
