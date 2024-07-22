.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _cms:

====================
CMS capability (WIP)
====================

From 2024, Bedrock's CMS will be powered by `Wagtail CMS`_.

This page is currently a skeleton for documentation to be added as the work evolves.

High-level summary
==================

Wagtail CMS will be used to make either entire pages or portions of pages (let's
call them 'surfaces') content-editable on www.mozilla.org. It is not a free-for-all
add-any-page-you-like approach, but rather a careful rollout of surfaces with
appropriate guard rails that helps ensure the integrity, quality and security of
www.mozilla.org.

Surfaces will be authored via a closed 'Editing' deployment and when those changes
are published they will become visible on the main www.mozilla.org 'Web' deployment.

If you are new to Wagtail, it is recommended that you read the official docs
and/or complete an online course to get a better understanding of how Wagtail works.

Useful resources:

- `Wagtail Editor Guide`_.
- `Wagtail Docs`_.
- `The Ultimate Wagtail Developers Course`_.

Accessing the CMS
=================

SSO authentication setup
------------------------

#. Become a member of ``bedrock_cms_local_dev-access`` on people.mozilla.org. Make
   sure you remember to accept the email invitation.
#. Extend your ``.env`` file with the development OIDC credentials that have been
   supplied to you. (make sure your ``.env`` file is based on a recent copy of
   ``.env-dist`` as several new variables exist).
#. In your ``.env`` file set the following variables:

   - ``USE_SSO_AUTH=True``
   - ``WAGTAIL_ENABLE_ADMIN=TRUE``
   - ``WAGTAIL_ADMIN_EMAIL=YOUR_MOZILLA_LDAP_EMAIL@mozilla.com``

#. Run ``make preflight`` to update bedrock with the latest DB version. As part of
   this step, the make file will also create a local admin user for you, using the
   Mozilla LDAP email address you added in the previous step.
#. Start bedrock running via ``npm start`` (for local dev) or ``make build run``
   (for Docker).
#. Go to ``http://localhost:8000/cms-admin/`` and you should see a button to login
   with SSO. Click it and you should go through the OAuth flow and end up in the
   Wagtail admin.

Non-SSO authentication
----------------------

#. In your ``.env`` file set ``USE_SSO_AUTH=False``, and ``WAGTAIL_ENABLE_ADMIN=TRUE``.
#. Run ``make preflight`` to update bedrock with the latest DB version.
#. Create a local admin user with ``./manage.py createsuperuser``, setting both the
   username, email and password to whatever you choose (note: these details will only
   be stored locally on your device).
   #. Alternatively, if you define ``WAGTAIL_ADMIN_EMAIL=YOUR_MOZILLA_LDAP_EMAIL@mozilla.com`` and ``WAGTAIL_ADMIN_PASSWORD=somepassword`` in your ``.env.`` file, ``make preflight`` will automatically create a non-SSO superuser for you
#. Start bedrock running via ``npm start`` (for local dev) or ``make build run``
   (for Docker).
#. Go to ``http://localhost:8000/cms-admin/`` and you should see a form for logging in
   with a username and password. Use the details you created in the previous step.

Adding new content surfaces
===========================

This is an introduction to creating new content surfaces in the CMS. It is not a
comprehensive guide, but rather a starting point to get you up and running with the
basics.

The page types that you see in the CMS admin are defined as regular models in
Django. As such, you can define new page types in the same way you would define any
other Django model, using Wagtail's field types and panels to define the data that
can be entered into the page.

When it comes to structuring CMS page models, there are some general guidelines to
try and follow:

- Models and templates should be defined in the same Django app that corresponds
  to where the URL exists in Bedrock’s information architecture (IA) hierarchy, similar to what we do for
  regular Jinja templates already. For example, a Mozilla themed page should be
  defined in ``/bedrock/mozorg/models.py``, and a Firefox themed page model should
  be in ``/bedrock/firefox/models.py``.
- Global ``Page`` models and ``StreamField`` blocks that are shared across many pages throughout the site should
  be defined in ``/bedrock/cms/``.

Structuring code in this way should hopefully help to keep things organized and
migrations in a manageable state.

Creating a new page model
-------------------------

Let’s start by creating a new Wagtail page model called ``TestPage``
in ``bedrock/mozorg/models.py``.

.. code-block:: python

    from django.db import models

    from wagtail.admin.panels import FieldPanel
    from wagtail.fields import RichTextField

    from bedrock.cms.models.base import AbstractBedrockCMSPage

    class TestPage(AbstractBedrockCMSPage):
        heading = models.CharField(max_length=255, blank=True)
        body = RichTextField(
            blank=True,
            features=settings.WAGTAIL_RICHTEXT_FEATURES_FULL,
        )

        content_panels = AbstractBedrockCMSPage.content_panels + [
            FieldPanel("heading"),
            FieldPanel("body"),
        ]

        template = "mozorg/test_page.html"

Some key things to note here:

- ``TestPage`` is a subclass of ``AbstractBedrockCMSPage``, which is a common base
  class for all Wagtail pages in bedrock. Inheriting from ``AbstractBedrockCMSPage``
  allows CMS pages to use features that exist outside of Wagtail, such as rendering
  Fluent strings and other L10n methods.
- The ``TestPage`` model defines two database field called ``heading`` and ``body``.
  The ``heading`` field is a ``CharField`` (the most simple text entry field type),
  and ``body`` is a ``RichTextField``. The HTML tags and elements that a content
  editor can enter into a rich text field are defined in
  ``settings.WAGTAIL_RICHTEXT_FEATURES_FULL``.
- There is also a ``title`` field on the page model, which from ``AbstractBedrockCMSPage`` (which in turn comes from ``wagtail.models.Page``). This doesn't make ``heading`` redundant, but it's worth knowing where ``title`` comes from.
- Both fields are added to the CMS admin panel by adding each as a ``FieldPanel`` to
  ``content_panels``. If you forget to do this, that's usually why you don't see the
  field in the CMS admin.
- Finally, the template used to render the page type can be found at
  ``mozorg/test_page.html``.
  If you don't set a custom template name, Wagtail will infer it from the model's name: ``<app_label>/<model_name (in snake case)>.html``

Django model migrations
-----------------------

Once you have your model defined, it’s then time to run create and run migrations to
set up a database table for it:

.. code-block:: shell

    ./manage.py makemigrations

You can then run migrations using:

.. code-block:: shell

    ./manage.py migrate

Many times when you make changes to a model, it will also mean that the structure of
the database table has changed. So as a general rule it’s good to form a habit of
running the above steps after making changes to your model. Each migration you make
will add a new migration file to the ``/migrations`` directory. When doing local
development for a new page you might find yourself doing this several times, so to help
reduce the number of migration files you create you can also squash / merge them.

INSERT LINK TO ARTICLE ON SQUASHING / MERGING?

Rendering data in templates
---------------------------

This is a good time to test out your page model by adding data to it to see how it
renders in your template.

The data can be rendered in ``mozorg/test_page.html`` as follows:

.. code-block:: jinja

    {% extends "base-protocol-mozilla.html" %}

    {% block page_title %}{{ page.title }}{% endblock %}

    {% block content %}
        <header>
        <h1>{{ page.heading }}</h1>
        <div class="w-rich-text">
            {{ page.body|richtext }}
        </div>
        </header>
    {% endblock %}

Note the ``|richtext`` filter applied to the ``page.body`` field. This is a
Wagtail-provided Jinja2 filter that will render the rich text field as HTML.

Previewing pages in the CMS admin
---------------------------------

Next, restart your local server and log in to the CMS admin. 
Browse to a page and use the ``+`` icon or similar to add a new "child page".
You should now see
your new page type in the list of available pages. Create a new page using the
``TestPage`` type, give the page a title of ``Test Page`` and a slug of ``test``,
and then enter some data for the fields you defined. When you click the preview icon
in the top right of the CMS page, you should hopefully see your template and data
rendered successfully!

Using advanced page models, fields, and blocks
----------------------------------------------

The example above was relatively simple in terms of data, but not very flexible. Now
that you have the basics covered, the next step is to start thinking about your page
requirements, and how to better structure your data models.

At this point, deep diving into the `Wagtail Docs`_ is very much recommended. In
particular, reading up on more advanced concepts such as `Stream Fields`_ and `Custom
Block types`_ will make it possible to make much more advanced CMS page types.

This is also a good time to start thinking about guardrails for your page and data.
Some common things to consider:

- Are there rules around the type of content that should be allowed on the page, such
  as the minimum or maximum number of items in a block?
- Should there be a set order to content in a page, or can it be flexible?
- Are there rules that should be applied at the page level, such as where it should
  live in the site hierarchy?
- Should there be a limit to the number of instances of that page type? (e.g. it
  would be confusing to have more than one home page or contact page).

Writing tests
-------------

When it comes to testing CMS page models, `wagtail_factories`_ can be used to create
mock data for tests to render. This can often be the trickiest part when testing more
complex page models, so it takes some practice.

Factories for your page models and blocks should be defined in a ``factories.py`` file
for your tests to import:

.. code-block:: python

    import factory
    import wagtail_factories

    from bedrock.mozorg import TestPage

    class TestPageFactory(wagtail_factories.PageFactory):
        title = "Test Page"
        live = True
        slug = "test"

        heading = wagtail_factories.CharBlockFactory
        body = wagtail_factories.CharBlockFactory

        class Meta:
            model = models.TestPage

In your ``test_models.py`` file, you can then import the factory for your test and
give it some data to render:

.. code-block:: python

    import pytest
    from wagtail.rich_text import RichText

    from bedrock.cms.tests.conftest import minimal_site  # noqa
    from bedrock.mozorg.tests import factories

    pytestmark = [
        pytest.mark.django_db,
    ]

    @pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
    def test_page(minimal_site, rf, serving_method):  # noqa
        root_page = minimal_site.root_page

        test_page = factories.TestPageFactory(
            parent=root_page,
            heading="Test Heading",
            body=RichText("Test Body"),
        )

        test_page.save()

        _relative_url = test_page.relative_url(minimal_site)
        assert _relative_url == "/en-US/test/"
        request = rf.get(_relative_url)

        resp = getattr(test_page, serving_method)(request)
        page_content = str(resp.content)
        assert "Test Heading" in page_content
        assert "Test Body" in page_content

Editing current content surfaces
================================

`Wagtail Editor Guide`_.

Bedrock-specific details to come.

Migrating Django pages to the CMS
=================================

.. note::
    This is initial documentation, noting relevant things that exist already, but
    much fuller recommendations will follow

The ``@prefer_cms`` decorator
-----------------------------

If you have an existing Django-based page that you want to move to be a CMS-driven
page, you are faced with a quandry.

Let's say the page exists at ``/some/path/``;  you can create it in the CMS with a
branch of pages that mirror the same slugs (a parent page with a slug of ``some``
and a child page with a slug of ``path``). However, in order for anyone to see the
published page, you would have to remove the reference to the Django view from the
URLconf, so that Wagtail would get a chance to render it (because Wagtail's
page-serving logic comes last in all URLConfs). **BUT...** how can you enter content
into the CMS fast enough replace the just-removed Django page? (Note: we could use a
data migraiton here, but that gets complicated when there are images involved)

The answer here is to use the ``bedrock.cms.decorators.prefer_cms`` decorator/helper.

A Django view decorated with ``prefer_cms`` will check if a live CMS page has been
added that matches the same overall, relative path as the Django view. If it finds
one, it will show the user `that` CMS page instead. If there is no match in the CMS,
then the original Django view will be used.

The result is a graceful handover flow that allows us to switch to the CMS page
without needing to remove the Django view from the URLconf. It doesn't affect
previews, so the review of draft pages before publishing can continue with no changes.
Once the CMS is populated with a live version of the replacement page, that's when a
later changeset can remove the deprecated Django view.

The ``prefer_cms`` decorator can be used directly on function-based views, or can wrap
views in the URLconf. It can also be passed to our very handy
``bedrock.mozorg.util.page`` as one of the list of ``decorator`` arguments.

For more details, please see the docstring on ``bedrock.cms.decorators.prefer_cms``.

Images
======

Using editor-uploaded images in templates
-----------------------------------------

Images may be uploaded into Wagtail's Image library and then included in
content-managed surfaces that have fields/spaces for images.

Images are stored in the same media bucket that fixed/hard-coded Bedrock
images get put in, and coexist alongside them, being namespaced into a
directory called ``custom-media/``.

If a surface uses an image, images use must be made explicit via template markup
— we need to state both *where* and *how* an image will be used in the template,
including specifying the size the image will be. This is because — by design
and by default — Wagtail can generate any size version that the template
mentions by providing a "filter spec" e.g.

.. code-block:: jinja

    {% set the_image=image(page.product_image, "max-1024x1024") %}
    <img class="some-class" src="{{ the_image.url }})"/>

(More examples are available in the `Wagtail Images docs`_.)

When including an image in a template we ONLY use filter specs between
2400px down to 200px in 200px steps, plus 100px.

Laying them out, these are the **only** filter specs allowed.
**Using alternative ones will trigger an error in production.**

* ``width-100``
* ``width-200``
* ``width-400``
* ``width-600``
* ``width-800``
* ``width-1000``
* ``width-1200``
* ``width-1400``
* ``width-1600``
* ``width-1800``
* ``width-2000``
* ``width-2200``
* ``width-2400``

Why are we limiting filter-specs to that set?
---------------------------------------------

In a line: to balance infrastructure security constraints with site flexiblity,
we have to pre-generate a known set of renditions.

Normally, if that ``product_image`` is not already available in ``1024x1024``,
Wagtail will resize the original image to suit, on the fly, and store this
"rendition" (a resized version, basically) in the cloud bucket. It will also add
a reference to the database so that Wagtail knows that the rendition already exists.

In production, the "Web" deployment has **read-only** access to the DB and
to the cloud storage, so it will not be able to generate new renditions on the fly.
Instead, we pre-generate those renditions when the image is saved.

This approach will not be a problem if we stick to image filter-specs from the
'approved' list. Note that extending the list of filter-specs is possible, if
we need to.

Infrastructure notes
====================

SSO authentication setup
------------------------

When the env vars ``OIDC_RP_CLIENT_ID`` and ``OIDC_RP_CLIENT_SECRET`` are present
and ``USE_SSO_AUTH`` is set to True in settings, Bedrock will use Mozilla SSO instead
of Django's default username + password approach to sign in. The deployed sites will
have these set, but we also have credentials available for using SSO locally if you
need to develop something that needs it - see our password vault.

Note that Bedrock in SSO mode will `not` support 'drive by' user creation even if
they have an ``@mozilla.com`` identity. Only users who already exist in the Wagtail
admin as a User will be allowed to log in. You can create new users using Django's
`createsuperuser`_ command, setting both the username and email to be your
``flast@mozilla.com`` LDAP address

Non-SSO authentication for local builds
---------------------------------------

If you just want to use a username and password locally, you can - ensure those env
vars above are not set, and use Django's `createsuperuser`_ command to make an
admin user in your local build.

.. _Wagtail CMS: https://wagtail.org/
.. _Wagtail Docs: https://docs.wagtail.org/
.. _Wagtail Editor Guide: https://guide.wagtail.org/en-latest/
.. _Wagtail Images docs: https://docs.wagtail.org/en/stable/topics/images.html
.. _createsuperuser: https://docs.djangoproject.com/en/5.0/ref/django-admin/#createsuperuser
.. _The Ultimate Wagtail Developers Course: https://learnwagtail.com/courses/the-ultimate-wagtail-developers-course/
.. _wagtail_factories: https://github.com/wagtail/wagtail-factories
.. _Stream Fields: https://docs.wagtail.org/en/stable/topics/streamfield.html
.. _Custom Block types: https://docs.wagtail.org/en/stable/advanced_topics/customisation/streamfield_blocks.html#custom-streamfield-blocks
