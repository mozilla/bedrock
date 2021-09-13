.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _contentful:

======================
Contentful Integration
======================

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

We have created a few different types of content models. Most are components that
correspond to components in our design system. The smallest create little bits of code
like buttons. The larger ones group together several entries for the smaller components
into a bigger component or an entire page.

For example: The *Page: General* model allows editors to include a hero entry, body
entry, and callout entry. The callout layout entry, in turn, includes a CTA
entry.

One advantage of storing the content in small chunks like this is that is can be
reused in many different pages. A callout which focuses on the privacy related reasons
to download Firefox could end up on the Private Browsing, Ad Tracker Blocking, and
Fingerprinter Blocking pages. If our privacy focused tagline changes from "Keep it
secret with Firefox" to "Keep it private with Firefox" it only needs to be updated in
one entry.

So, when looking at a page on the website that comes from Contentful you are typically
looking at several different entries combined together.

On the bedrock side, the data for all entries is periodically requested from the API
and stored in a database.

When a Contentful page is requested the code in `api.py` transforms the information
from the database into a group of Python dictionaries (these are like key/value pairs
or an object in JS).

This data is then passed to the page template (either Mozilla or for Firefox themed
as appropriate). The page template includes some files which take the data and feed
it into macros to create Protocol components. These are the same macros we use on
non-Contentful pages. There are also includes which will import the appropriate JS and
CSS files to support the components.

Once rendered the pages get cached on the CDN as usual.


Content Models
--------------

Emoji legend for content models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

🔗 this component is referenced by ID in bedrock (at the moment that is just the
homepage but could be used to connect single components for display on non-contentful
pages. For example: the latest feature box on /new)
📄 this component is a page, it will include meta data for the page, a folder, and slug
🎁 this is a layout wrapper for another component
✏️ this component includes editable content, not just layout config
♟ this component is suitable for inclusion as an inline entry in a rich text field
➡️ this component can be embedded without a layout wrapper


Naming conventions for content models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    For some fields it is important to be consistent because of how they are processed in
    bedrock. For all it is important to make the editor's jobs easier.

Name
    This is for the internal name of the entry. It should be set as the **Entry title**,
    required, and unique.

Preview (and Preview Title, Preview Blurb, Preview Image)
    These will be used in search results and social media sites. There's also the
    potential to use them for aggregate pages on our own sites. Copy configuration and
    validation from an existing page.

Heading (and Heading Level)
    Text on a page which provides context for information that follows it. Usually made
    into a H1-H4 in bedrock. Not: header, title, or name.

Image (and Image Size, Image Width)

    Not: picture, photo, logo, or icon (unless we are specifically talking about a logo or icon.)

Content
    Multi-reference

Product Icon
    Copy configuration and validation from an existing page.

Theme
    Copy configuration and validation from an existing page.

Body (Body Width, Body Vertical Alignment, Body Horizontal Alignment)
    Rich text field in a Component. Do not use this for multi reference fields, even if the only content on the page is other content entries.
    Do not use MarkDown for body fields, we can’t restrict the markup. Copy configuration and validation from an existing page.

CTA
    The button/link/dropdown that we want a user to interact with following some content. Most often appearing in Split and Callout components.




🔗 Connect
~~~~~~~~~~

These are the highest level component. They should be just a name and entry reference.

The purpose of the connect is to create a stable ID that can be referenced in bedrock
to be included in a jinja template. Right now we only do this for the homepage. This
is because the homepage has some conditional content above and below the Contentful
content.

Using a connect component to create the link between jinja template and the Contentful
Page entry means an entire new page can be created and proofed in Contentful before
the bedrock homepage begins pulling that content in.

In other contexts a connect content model could be created to link to entries where the
ID may change. For example: the "Latest Firefox Features: section of /new could be
moved to Contentful using a connect component which references 3 picto blocks.

Because the ID must be added to a bedrock by a dev, only devs should be able to make new
connect entries.

📄 Page
~~~~~~~

Pages in bedrock are created from page entries in Contentful. The three page types are
Homepage, Versatile, and General.

The homepage needs to be connected to bedrock using a Connect component and page meta
data like title, blurb, image, etc come from bedrock.

The versatile and general templates do not need bedrock configuration to be displayed.
Instead, they should appear automatically at the folder and slug specified in the entry.
These templates do include fields for meta data.

The versatile template can include any number of components in any order.

The general template is a hero, text, and callout. The simplified list and order of
components is intended to make it easier for editors to put a page together. Hopefully
more of these simplified content models will be created in the future.

🎁 Layout
~~~~~~~~~

These entries bring a group of components together. For example: 3 picto blocks in
a picto block layout. They also include layout and theme options which are applied to
all of the components they bring together. For example: centering the icons in all 3
picto blocks.

These correspond roughly to Protocol templates.

The one exception to the above is the Layout: Large Card, which exists to attach a large
display image to a regular card entry. The large card must still be included in the
Layout: 5 Cards.

✏️ Component
~~~~~~~~~~~~

We're using this term pretty loosely. It corresponds roughly to a Protocol atom,
molecule, or organism.

These entries include the actual content, the bits that people write and the images that
go with it.

If they do not require a layout wrapper there may also be some layout and theme options.
For example, the text components include options for width and alignment.

♟ Component
~~~~~~~~~~~

Should I have named these something else? Probably. I suggest either atom or piece if
someone wants to go to the trouble.

These components are always Protocol atoms and cannot be included in a page entry,
however, they don't have a specific layout wrapper either. They can go in any entry that
has a body field that is configured as rich text (picto, split, multi column text...)

Adding a new ✏️ Component
~~~~~~~~~~~~~~~~~~~~~~~~~

Example: Picto

#. Create the content model in Contentful.

   * *Follow the naming conventions*.
   * You may need two models if you are configuring layout separately.

#. Add the new content model to the list of allowed references in other content models (ATM this is just the "content" reference field on pages).
#. In bedrock create CSS and JS entries in static-bundles for the new component.
#. In api.py write a def for the component.
#. In api.py add the component name, def, and bundles to the CONTENT_TYPE_MAP.
#. Find or add the macro to macros-protocol.
#. Import the macro into all.html and add a call to it in the entries loop.

.. note::

  Tips:

  * can't define defaults in Contentful, so set those in your Python def.
  * for any optional fields make sure you check the field exists before referencing the content.


Adding a new ♟ Component
~~~~~~~~~~~~~~~~~~~~~~~~

Example: Wordmark.

#. Create the content model in Contentful.

   * *Follow the naming conventions*.

#. Add the new content model to rich text fields (like split and text).
#. In bedrock include the CSS in the Sass file for any component which may use it (yeah, this is not ideal, hopefully we will have better control in the future).
#. Add a def to api.py to render the piece (like ``_make_wordmark``).

.. note::

  Tips:

  * can't define defaults in Contentful, so set those in your Python def.
  * for any optional fields make sure you check the field exists before referencing the content.

Adding a rich text field in a component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Disable everything then enable: B, I, UL, OL, Link to URL, and Inline entry. You will
want to enable some some Headings as well, H1 should be enabled very rarely. Enable
H2-H4 using your best judgement.


Adding support for a new product icon, size, folder
---------------------------------------------------

Many content models have drop downs with identical content. For example: the Hero, Callout,
and Wordmark models all include a "product icon". The icon can be one of any of the
[supported logos in Protocol](https://protocol.mozilla.org/demos/logo.html). Other common
fields are width and folder.

There are two ways to keep these lists up to date to reflect Protocol updates:

#. By opening and editing the content models individually in Contentful
#. Scripting updates using the API

At the moment it's not too time consuming to do by hand, just make sure you are copy and
pasting to avoid introducing spelling errors.

We have not tried scripting updates with the API yet. One thing to keep in mind if
attempting this is that not all widths are available on all components. For example: the
"Text: Four columns" component cannot be displayed in small content widths.

Rich Text Rendering
-------------------

Contentful provides a helper library to transform the rich text fields in the API into
HTML content.

In places were we disagree with the rendering or want to enhance the rendering we can
provide our own renderers on the bedrock side. They can be as simple as changing `<b>` tags
to `<strong>` tags or as complex as inserting a component.

A list of our custom renderers is passed to the `RichTextRenderer` helper at the start of
the `ContentfulPage` class in api.py. The renderers themselves are also defined in api.py

L10N
----

Localization has no been finalized.

Here are three possible approaches for translation:

Smartling
~~~~~~~~~

When setting up a content model in Contentful fields can be designated as available for
translation. Individual users can be associated with different languages and when they edit
entries they see duplicate fields for each language they can translate into. These fields
can also be sent to Smartling to be translated there.

On the bedrock side, the translated content can be pulled from the appropriate fields and
inserted into the rendered page.

At the moment bedrock is capable of displaying the localized content but the Smartling
integration has not been set up.

This would be the "official" way of doing translations but would be limited to the locales
that we are paying to have active in Smartling.

Fluent
~~~~~~

Instead of using the language translation fields in Contentful to store translations we
could designate one of the locales to contain a fluent string ID. Bedrock could then
use the string IDs and the English content to create Fluent files for submission into our
current translation system.

Creation of the string IDs could be automated using Contentful's write API.

To give us the ability to use fallback strings the Contentful field could accept a comma
separated list of values.

This approach requires significant integration code on the bedrock side but comes with
the benefit of using our current translation system, including community contributions.

No English Equivalent
~~~~~~~~~~~~~~~~~~~~~

Components could be created in the language they are intended to display in. The localized
content would be written in the English content fields.

The down sides of this are that we do not know what language the components are written in
and could accidentally display the wrong language on any page. It also means that localized
content cannot be created automatically by English editors and translations would have to
be manually associated with URLs.

This is the  approach that will likely be used for the German and French homepages since
that content is not going to be used on English pages and creating a separate homepage
with different components is valuable to the German and French teams.

Assets
------

Images that are uploaded in Contentful will be served to site visitors from the Contentful
CDN. The cost of using the CDN are not by request so we don't have to worry about how
many times an image will be requested.

Using the Contentful CDN lets us use their [Images API](https://www.contentful.com/developers/docs/references/images-api/)
to format our images.

In theory, a large high quality image is uploaded in Contentful and then bedrock inserts
links to the CDN for images which are cropped to fit their component and resized to fit
their place on the page.

Because we cannot rely on the dimensions of the image uploaded to Contentful as a guide
for displaying the image - bedrock needs to be opinionated about what size images it requests
based on the component and its configuration. For example, hero images are fixed at 800px
wide. In the future this could be a user configurable option.


Preview
-------

Content previews are configured under *Settings* > *Content preview* on a per-content model
basis. At the moment previews are only configured for pages, and display on demo5.

Once the code is merged into bedrock they should be updated to use the dev server.

Specific URLs will only update every 5 minutes as the data is pulled from the API but pages
can be previewed up to the second at the `contentful-preview` URL. This preview will include
"changed" and "draft" changes (even if there is an error in the data) not just published changes.


Roles/Permissions
-----------------

In general we are trusting people to check their work before publishing and very few
guard rails have been installed.

One exception is the Connect component, only developers should have permission to create one.
It's not problematic to have them created by non developers, it's just that they won't work
without corresponding bedrock code.


Useful Contentful Docs
----------------------

https://www.contentful.com/developers/docs/references/images-api/#/reference/resizing-&-cropping/specify-focus-area

https://www.contentful.com/developers/docs/references/content-delivery-api/

https://contentful.github.io/contentful.py/#filtering-options

https://github.com/contentful/rich-text-renderer.py
https://github.com/contentful/rich-text-renderer.py/blob/a1274a11e65f3f728c278de5d2bac89213b7470e/rich_text_renderer/block_renderers.py











Assumptions
    - image sizes

