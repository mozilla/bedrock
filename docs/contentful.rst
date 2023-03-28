.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _contentful:

==============================================================
Contentful :abbr:`CMS (Content Management System)` Integration
==============================================================

Overview
--------

Contentful is a headless :abbr:`CMS (Content Management System)`. It stores content for our website in a structured
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
entry, and callout entry. The callout layout entry, in turn, includes a :abbr:`CTA (Call To Action)`
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

Once rendered the pages get cached on the :abbr:`CDN (Content Delivery Network)` as usual.

Contentful Apps
---------------

Installed on Environment level. Make sure you are in the environment you want to edit before accessing an app.
Use *Apps* link in top navigation of Contentful Web App to find an environment's installed apps.

Compose
~~~~~~~

`Compose <https://www.contentful.com/marketplace/contentful-app/compose/>`_ provides a nicer editing experience.
It creates a streamlined view of pages by combining multiple entries into a single edit screen and allowing field
groups for better organization.

Any changes made to Compose page entries in a specific environment are limited to that
environment. If you are in a sandbox environment, you should see an ``/environments/sandbox-name`` path at the end
of your Compose URL.

Known Limitations
^^^^^^^^^^^^^^^^^
* Comments are not available on Compose entries
* It is not possible to edit embedded entries in Rich Text fields in Compose app. Selecting the "edit" option in the dropdown opens the entry in the Contentful web app.

Merge
~~~~~

`Merge <https://www.contentful.com/marketplace/app/merge/>`_ provides a UI for comparing the state of Content Models across two environments. You can select what changes you would like to migrate to a new environment.

Known Limitations
^^^^^^^^^^^^^^^^^
* Does not migrate Help Text (under Appearance Tab)
* Does not migrate any apps used with those Content Models
* Does not migrate Content Entries or Assets
* It can identify when Content Models should be available in Compose, but it cannot migrate the field groups

Others
~~~~~~
* `Launch <https://www.contentful.com/marketplace/contentful-app/launch/>`_ allows creation of "releases", which can help coordinate publishing of multiple entries
* `Workflows <https://www.contentful.com/help/workflows-overview/>`_ standardizes process for a specific Content Model. You can specify steps and permissions to regulate how content moves from draft to published.

Content Models
--------------

Emoji legend for content models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 📄 this component is a page, it will include meta data for the page, a folder, and slug
* 🎁 this is a layout wrapper for another component
* ✏️ this component includes editable content, not just layout config
* ♟ this component is suitable for inclusion as an inline entry in a rich text field
* ➡️ this component can be embedded without a layout wrapper


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

Rich Text Content
    Rich text field in a Compose Page

:abbr:`CTA (Call To Action)`
    The button/link/dropdown that we want a user to interact with following some content. Most often appearing in Split and Callout components.



📄 Page
~~~~~~~

Pages in bedrock are created from page entries in Contentful's `Compose`_ App.

Homepage
    The homepage needs to be connected to bedrock using a Connect component (see `Legacy`_) and page meta
    data like title, blurb, image, etc come from bedrock.

General
    Includes hero, text, and callout. The simplified list and order of
    components is intended to make it easier for editors to put a page together.

Versatile
    No pre-defined template. These pages can be constructed from any combination of layout and
    component entries.

Resource Center
    Includes product, category, tags, and a rich text editor. These pages follow a recognizable
    format that will help orient users looking for more general product information (i.e. VPN).


The versatile and general templates do not need bedrock configuration to be displayed.
Instead, they should appear automatically at the folder and slug specified in the entry.
These templates do include fields for meta data.

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

♟ Embed
~~~~~~~~~~~

These pre-configured content pieces can go in rich text editors when allowed (picto, split, multi column text...).

Embeds are things like logos, where we want tightly coupled style and content that will be consistent across entries.
If a logo design changes, we only need to update it in one place, and all uses of that embed will be updated.

Adding a new 📄 Page
~~~~~~~~~~~~~~~~~~~~
* Create the content model

    * Ensure the content model name starts with page (i.e. pageProductJournalismStory)

    * Add an SEO reference field which requires the **SEO Metadata** content type

    * In Compose, go to Page Types and click “Manage Page Types” to make your new content model available to the Compose editor.

        * If you have referenced components, you can choose whether they will be displayed as expanded by default.

        * Select “SEO” field for “Page Settings” field

    * If the page is meant to be localised, ensure all fields that need localisation have the “Enable localization of this field” checkbox checked in content model field settings

* Update ``bedrock/contentful/constants``

    * Add content type constant

    * Add constant to default array

    * If page is for a single locale only, add to SINGLE_LOCALE_CONTENT_TYPES

    * If page is localised, add to LOCALISATION_COMPLETENESS_CHECK_CONFIG with an array of localised fields that need to be checked before the page’s translation can be considered complete

* Update ``bedrock/contentful/api.py``

    * If you’re adding new embeddable content types, expand list of renderer helpers configured for the RichTextRenderer in the ``ContentfulAPIWrapper``

    * Update ``ContentfulAPIWrapper.get_content()`` to have a clause to handle the new page type

* Create a `custom view </coding.html#writing-views>`_ to pass the Contentful data to a template

Adding a new ✏️ Component
~~~~~~~~~~~~~~~~~~~~~~~~~

Example: Picto

#. Create the content model in Contentful.

   * *Follow the naming conventions*.
   * You may need two models if you are configuring layout separately.

#. Add the new content model to the list of allowed references in other content models (At the moment this is just the "content" reference field on pages).
#. In bedrock create CSS and JS entries in static-bundles for the new component.
#. In api.py write a def for the component.
#. In api.py add the component name, def, and bundles to the CONTENT_TYPE_MAP.
#. Find or add the macro to macros-protocol.
#. Import the macro into all.html and add a call to it in the entries loop.

.. note::

  Tips:

  * can't define defaults in Contentful, so set those in your Python def.
  * for any optional fields make sure you check the field exists before referencing the content.


Adding a new ♟ Embed
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
and Wordmark models all include a "product icon". Other common fields are width and folder.

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

.. note::

  * Built-in nodes cannot be extended or customized: *Custom node types and marks are not allowed*. Embed entry types are required to extend rich text functionality. (i.e. if you need more than one style of blockquote)

L10N
----

Smartling - our selected approach
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When setting up a content model in Contentful, fields can be designated as available for
translation.

Individual users can be associated with different languages, so when they edit
entries they see duplicate fields for each language they can translate into.
In addition - and in the most common case - these fields are automatically sent to
Smartling to be translated there.

Once text for translation lands in Smartling, it is batched up into jobs for
human translation. When the work is complete, Smartling automatically updates
the relevant Contentful entries with the translations, in the appropriate fields.

Note that those translations are only visible in Contentful if you select to view
that locale's fields, but if they are present in Contentful's datastore (and
that locale is enabled in the API response) they will be synced down by Bedrock.

On the Bedrock side, the translated content is pulled down the same way as the
default locale's content is, and is stored in a locale-specific ContentfulEntry
in the database.

In terms of 'activation', or "Do we have all the parts to show this
Contentful content"?, Contentful content is not evaluated in the same way as
Fluent strings (where we will show a page in a given locale if 80% of its
Fluent strings have been translated, falling back to en-US where not).

Instead, we check that all of the required fields present in the translated
Entry have non-null data, and if so, then the entire page is viable to show in the
given locale. (ie, we look at fields, not strings. It's a coarser level of
granularity compared to Fluent, because the data is organised differently -
most of Contentful-sourced content will be rich text, not individual strings).

The check about whether or not a Contentful entry is 'active' or 'localisation complete'
happens during the main sync from Contentful. Note that there is no fallback
locale for Contentful content other than a redirect to the en-US version of the
page - either the page is definitely available in a locale, or it's not at all
available in that locale.

Notes:

    * The batching of jobs in Smartling is still manual, even though the data flow is automated. We need to keep an eye on how onerous this is, plus what the cost exposure could be like if we fully automate it.
    * The Smartling integration is currently only set to use Mozilla.org's 10 most popular locales, in addition to en-US.
    * No localisation of Contentful content happens via Pontoon.
    * The Smartling setup is most effectively leveraged with Compose-based pages rather than Connect-based components, and the latter may require some code tweaks.
    * Our Compose: SEO field in Contentful is configured for translation (and in use on the VPN Resource Center). All Compose pages require this field. If a Compose page type is *not* meant to be localised, we need to stop these SEO-related fields from going on to Smartling.


Fluent
~~~~~~

**NB: Not selected for use, but notes retained for reference**

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

**NB: Not selected for use, but notes retained for reference**

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
:abbr:`CDN (Content Delivery Network)`. The cost of using the CDN are not by request so we
don't have to worry about how many times an image will be requested.

Using the Contentful :abbr:`CDN (Content Delivery Network)` lets us use their
`Images API <https://www.contentful.com/developers/docs/references/images-api/>`_
to format our images.

In theory, a large high quality image is uploaded in Contentful and then bedrock inserts
links to the :abbr:`CDN (Content Delivery Network)` for images which are cropped to fit their
component and resized to fit their place on the page.

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

For previewing on localhost, see Development Practices, below.


Roles/Permissions
-----------------

In general we are trusting people to check their work before publishing and very few
guard rails have been installed. We have a few roles with different permissions.

Admin
    Organization

    * Define roles and permission
    * Manage users
    * Change master and sandbox environment aliases
    * Create new environments

    Master environment

    * Edit content model
    * Create, Edit, Publish, Archive, Delete content
    * Install/Uninstall apps

Developer
    Organization

    * Create new environments

    Master environment

    * Create, Edit, Publish, Archive content

    Sandbox environments (any non-master environment)

    * Edit content model
    * Create, Edit, Publish, Archive, Delete content
    * Install/Uninstall apps

Editor (WIP)
    Master environment (through Compose)

    * Create, Edit, Publish, Archive content


Development practices
---------------------

This section outlines tasks generally required if developing features against Contentful.

Get bedrock set up locally to work with Contentful
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In your ``.env`` file for Bedrock, make sure you have the followign environment variables
set up.

* ``CONTENTFUL_SPACE_ID`` - this is the ID of our Contentful integration
* ``CONTENTFUL_SPACE_KEY`` - this is the API key that allows you access to our space. Note that two types of key are available: a Preview key allows you to load in draft content; the Delivery key only loads published contnet. For local dev, you want a Preview key.
* ``SWITCH_CONTENTFUL_HOMEPAGE_DE`` should be set to ``True`` if you are working on the German Contentful-powered homepage
* ``CONTENTFUL_ENVIRONMENT`` Contentful has 'branches' which it calls environments. `master` is what we use in production, and `sandbox` is generally what we use in development. It's also possible to reference a specific environment - e.g. ``CONTENTFUL_ENVIRONMENT=sandbox-2021-11-02``

To get values for these vars, please check with someone on the backend team.

If you are working on the Contentful Sync backed by the message-queue (and if you don't know what this is, you don't need it for local dev), you will also need to set the following env vars:

* ``CONTENTFUL_NOTIFICATION_QUEUE_URL``
* ``CONTENTFUL_NOTIFICATION_QUEUE_REGION``
* ``CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID``
* ``CONTENTFUL_NOTIFICATION_QUEUE_SECRET_ACCESS_KEY``


How to preview your changes on localhost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When viewing a page in Contentful, it's possible to trigger a preview of the draft page. This is typically rendered on www-dev.allizom.org. However, that's only useful for code that's already in ``main``.
If you want to preview Contentful content on your local machine - e.g. you're working on a feature branch that isn't ready for merging - do the following:

Existing (master) Content Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In the right-hand sidebar of the editor page in Contentful:

* Find the Preview section
* Select ``Change`` and pick ``Localhost Preview``
* Click ``Open preview``

New (non-master) Content Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In bedrock:

* Update ``class ContentfulPreviewView(L10nTemplateView)`` in `Mozorg Views <https://github.com/mozilla/bedrock/blob/main/bedrock/mozorg/views.py>`_ with a render case for your new content type

In the right-hand sidebar of the editor page in Contentful:

* Click Info tab
* Find ``Entry ID`` section and copy the value

Manually create preview URL in browser:

* `http://localhost:8000/en-US/contentful-preview/{entry_id}/`

Note that previewing a page will require it to be pulled from Contentful's API, so you will need ``CONTENTFUL_SPACE_ID`` and ``CONTENTFUL_SPACE_KEY`` set in your ``.env``. It may take a few seconds to get the data.

Also note that when you select ``Localhost preview``, the choice sticks, so you should set it back to ``Preview on web`` when you're done.


How to update/refresh the sandbox environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It helps to think of Contentful 'environments' as simply branches of a git-like repo full of content. You can take a particular environment and branch off it to make a new environment for :abbr:`WIP (Work in Progress)` or experimental content, using the original one as your starting point.
On top of this, Contentful has the concept of aliases for environments and we use two aliases in our setup:

* ``master`` is used for production and is an alias currently pointing to the `V1` environment. It is pretty stable and access to it is limited.
* ``sandbox`` is used for development and more team members have access to edit content. Again, it's an alias and is pointed at an environment (think, branch) with a name in the format ``sandbox-YYYY-MM-DD``.


While updating ``master`` is something that we generally don't do (at the moment only a product owner and/or admin would do this), updating the sandbox happens more often, typically to populate it with data more recently added to master.
To do this:

* Go to ``Settings > Environments``
* Ensure we have at least one spare environment slot. If we don't delete the oldest ``sandbox-XXXX-XX-XX`` environment.
* Click the blue Add Environment button, to the right. Name it using the ``sandbox-YYYY-MM-DD`` pattern and base it on whatever environment is aliased to ``master`` - this will basically create a new 'branch' with the content currently in master.
* In the Environment Aliases section of the main page, find `sandbox` and click Change alias target, then select the ``sandbox-XXXX-XX-XX`` environment you just made.

Which environment is connected to where?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``master`` is the environment used in Bedrock production, stage, dev and test
``sandbox`` may, in the future, be made the default environment for dev. It's also the one we should use for local development.

If you develop a new feature that adds to Contentful (e.g. page or component) and you author it in the sandbox, you will need to re-create it in master before the corresponding bedrock changes hit production.


Troubleshooting
~~~~~~~~~~~~~~~

If you run into trouble on an issue, be sure to check in these places first and include the relevant information in requests for help (i.e. environment).

1. Contentful Content Model & Entries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* What environment are you using?
* Do you have the necessary permissions to make changes?
* Do you see all the entry fields you need? Do those fields have the correct value options?

2. `Bedrock API (api.py) <https://github.com/mozilla/bedrock/blob/main/bedrock/contentful/api.py>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* What environment are you using?
* Can you find a Python function definition for the content type you need?
* Does it structure data as expected?

.. code-block:: python

    # example content type def

    def get_section_data(self, entry_obj):
        fields = entry_obj.fields()
        # run `print(fields)` here to verify field values from Contentful

        data = {
            "component": "sectionHeading",
            "heading": fields.get("heading"),
        }

        # run `print(data)` here to verify data values from Bedrock API
        return data

3. `Bedrock Render (all.html) <https://github.com/mozilla/bedrock/blob/main/bedrock/contentful/templates/includes/contentful/all.html>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Can you find a render condition for the component you need?

.. code-block:: jinja

    /* example component condition */

    {% elif entry.component == 'sectionHeading' %}

* If the component calls a macro:
    * Does it have all the necessary parameters?
    * Is it passing the expected values as arguments?
* If the component is custom HTML:
    * Is the HTML structure correct?
    * Are Protocol-specific class names spelled correctly?
* Is the component `CSS <https://github.com/mozilla/bedrock/tree/main/media/css/contentful>`_ available?
* Is the component JS available?

.. note::

    Component CSS and JS are defined in a ``CONTENT_TYPE_MAP`` from the Bedrock API (``api.py``).

Useful Contentful Docs
----------------------

https://www.contentful.com/developers/docs/references/images-api/#/reference/resizing-&-cropping/specify-focus-area

https://www.contentful.com/developers/docs/references/content-delivery-api/

https://contentful.github.io/contentful.py/#filtering-options

https://github.com/contentful/rich-text-renderer.py
https://github.com/contentful/rich-text-renderer.py/blob/a1274a11e65f3f728c278de5d2bac89213b7470e/rich_text_renderer/block_renderers.py





Assumptions we still need to deal with
--------------------------------------

    - image sizes


Legacy
------

Since we decided to move forward the the Compose App, we no longer need the Connect content model.
The EN-US homepage is currently still using Connect. Documentation is here for reference.

* 🔗 this component is referenced by ID in bedrock (at the moment that is just the homepage but could be used to connect single components for display on non-contentful pages. For example: the latest feature box on /new)

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
