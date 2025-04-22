---
render_macros: true
---

# CMS

From 2024, Bedrock's CMS will be powered by [Wagtail CMS](https://wagtail.org/).

This page is currently a skeleton for documentation to be added as the work evolves.

## High-level summary

Wagtail CMS will be used to make either entire pages or portions of pages (let's call them 'surfaces') content-editable on www.mozilla.org. It is not a free-for-all add-any-page-you-like approach, but rather a careful rollout of surfaces with appropriate guard rails that helps ensure the integrity, quality and security of www.mozilla.org.

Surfaces will be authored via a closed 'Editing' deployment and when those changes are published they will become visible on the main www.mozilla.org 'Web' deployment.

If you are new to Wagtail, it is recommended that you read the official docs and/or complete an online course to get a better understanding of how Wagtail works.

Useful resources:

-   [Wagtail Editor Guide](https://guide.wagtail.org/en-latest/).
-   [Wagtail Docs](https://docs.wagtail.org/).
-   [The Ultimate Wagtail Developers Course](https://learnwagtail.com/courses/the-ultimate-wagtail-developers-course/).

## Accessing the CMS on your local machine

### SSO authentication setup

1.  Become a member of `bedrock_cms_local_dev-access` on people.mozilla.org. Make sure you remember to accept the email invitation.
2.  Extend your `.env` file with the development OIDC credentials that have been supplied to you. (make sure your `.env` file is based on a recent copy of `.env-dist` as several new variables exist).
3.  In your `.env` file set the following variables:
    -   `USE_SSO_AUTH=True`
    -   `WAGTAIL_ENABLE_ADMIN=TRUE`
    -   `WAGTAIL_ADMIN_EMAIL=YOUR_MOZILLA_LDAP_EMAIL@mozilla.com`
4.  Run `make preflight` to update bedrock with the latest DB version. As part of this step, the make file will also create a local admin user for you, using the Mozilla LDAP email address you added in the previous step. **If you do not want to overwrite your local database, run** `make preflight -- --retain-db` **instead.**
5.  Start bedrock running via `npm start` (for local dev) or `make build run` (for Docker).
6.  Go to `http://localhost:8000/cms-admin/` and you should see a button to login with SSO. Click it and you should go through the OAuth flow and end up in the Wagtail admin.

### Non-SSO authentication

1.  In your `.env` file set `USE_SSO_AUTH=False`, and `WAGTAIL_ENABLE_ADMIN=TRUE`.
2.  Run `make preflight` to update bedrock with the latest DB version. **If you do not want to overwrite your local database, run** `make preflight -- --retain-db` **instead.**
3.  Create a local admin user with `./manage.py createsuperuser`, setting both the username, email and password to whatever you choose (note: these details will only be stored locally on your device).
4.  Alternatively, if you define `WAGTAIL_ADMIN_EMAIL=YOUR_MOZILLA_LDAP_EMAIL@mozilla.com` and `WAGTAIL_ADMIN_PASSWORD=somepassword` in your `.env.` file, `make preflight` will automatically create a non-SSO superuser for you
5.  Start bedrock running via `npm start` (for local dev) or `make build run` (for Docker).
6.  Go to `http://localhost:8000/cms-admin/` and you should see a form for logging in with a username and password. Use the details you created in the previous step.

## Fetching the latest CMS data for local work

!!! note
**TL;DR version:**

1.  Get the DB with `make preflight`
2.  If you need the images that the DB expects to exist, use `python manage.py download_media_to_local`
::::

The CMS content exists in hosted cloud database and a trimmed-down version of this data is exported to a sqlite DB for use in local development and other processes. The exported database contains all the same content, but deliberately omits sensitive info like user accounts, unpublished drafts and outmoded versions of pages.

The DB export is generated twice a day and is put into the same public cloud buckets we've used for years. Your local Bedrock install will just download the ``bedrock-dev`` one as part of `make preflight`.

The DB will contain a table that knows the relative paths of the images uploaded to the CMS, but not the actual images. Those are in a cloud storage bucket, and if you want your local machine to have them available after you download the DB that expects them to be present, you can run `python manage.py download_media_to_local` which will sync down any images you don't already have.

!!! note
By default, `make preflight` and `./bin/run-db-download.py` will download a database file based on `bedrock-dev`. If you want to download from stage or prod, which are also available in sanitised form, you need to tell Bedrock which environment you want by prefixing the command with `AWS_DB_S3_BUCKET=bedrock-db-stage` or `AWS_DB_S3_BUCKET=bedrock-db-prod`.

`AWS_DB_S3_BUCKET=bedrock-db-stage make preflight`

`python manage.py download_media_to_local --environment=stage`
::::

## Editing current content surfaces

In terms of managing the content of an existing surface, please see the general [Wagtail Editor Guide](https://guide.wagtail.org/en-latest/) for now.

If you want to change the code-defined behaviour of an existing surface, that's similar to adding a new content surface, covered below. You may also find the [Wagtail Docs](https://docs.wagtail.org/) and [The Ultimate Wagtail Developers Course](https://learnwagtail.com/courses/the-ultimate-wagtail-developers-course/) useful if you don't have experience of building with Wagtail yet.

## Adding new content surfaces

This is an introduction to creating new content surfaces in the CMS. It is not a comprehensive guide, but rather a starting point to get you up and running with the basics.

The page types that you see in the CMS admin are defined as regular models in Django. As such, you can define new page types in the same way you would define any other Django model, using Wagtail's field types and panels to define the data that can be entered into the page.

When it comes to structuring CMS page models, there are some general guidelines to try and follow:

-   Models and templates should be defined in the same Django app that corresponds to where the URL exists in Bedrock's information architecture (IA) hierarchy, similar to what we do for regular Jinja templates already. For example, a Mozilla themed page should be defined in `/bedrock/mozorg/models.py`, and a Firefox themed page model should be in `/bedrock/firefox/models.py`.
-   Global `Page` models and `StreamField` blocks that are shared across many pages throughout the site should be defined in `/bedrock/cms/`.

Structuring code in this way should hopefully help to keep things organized and migrations in a manageable state.

### Creating a new page model

Let's start by creating a new Wagtail page model called `TestPage` in `bedrock/mozorg/models.py`.

``` python
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
```

Some key things to note here:

-   `TestPage` is a subclass of `AbstractBedrockCMSPage`, which is a common base class for all Wagtail pages in bedrock. Inheriting from `AbstractBedrockCMSPage` allows CMS pages to use features that exist outside of Wagtail, such as rendering Fluent strings and other L10n methods.
-   The `TestPage` model defines two database field called `heading` and `body`. The `heading` field is a `CharField` (the most simple text entry field type), and `body` is a `RichTextField`. The HTML tags and elements that a content editor can enter into a rich text field are defined in `settings.WAGTAIL_RICHTEXT_FEATURES_FULL`.
-   There is also a `title` field on the page model, which from `AbstractBedrockCMSPage` (which in turn comes from `wagtail.models.Page`). This doesn't make `heading` redundant, but it's worth knowing where `title` comes from.
-   Both fields are added to the CMS admin panel by adding each as a `FieldPanel` to `content_panels`. If you forget to do this, that's usually why you don't see the field in the CMS admin.
-   Finally, the template used to render the page type can be found at `mozorg/test_page.html`.
-   If you don't set a custom template name, Wagtail will infer it from the model's name: `<app_label>/<model_name (in snake case)>.html`
-   All new models must be added to the config for the DB exporter script. If you do not, the page will not be correctly exported for local development and will break for anyone using that DB export file. See ``Add your new model to the DB export``, below.

### Django model migrations

Once you have your model defined, it's then time to run create and run migrations to set up a database table for it:

``` shell
./manage.py makemigrations
```

You can then run migrations using:

``` shell
./manage.py migrate
```

Many times when you make changes to a model, it will also mean that the structure of the database table has changed. So as a general rule it's good to form a habit of running the above steps after making changes to your model. Each migration you make will add a new migration file to the `/migrations` directory. When doing local development for a new page you might find yourself doing this several times, so to help reduce the number of migration files you create you can also squash / merge them.

-   [Django migrations docs](https://docs.djangoproject.com/en/4.2/topics/migrations/).
-   [Squashing migrations](https://docs.djangoproject.com/en/4.2/topics/migrations/).

### Rendering data in templates

This is a good time to test out your page model by adding data to it to see how it renders in your template.

The data can be rendered in `mozorg/test_page.html` as follows:

``` jinja
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
```

Note the `|richtext` filter applied to the `page.body` field. This is a Wagtail-provided Jinja2 filter that will render the rich text field as HTML.
We use a custom `wagtailcore/shared/richtext.html` template to slot in our own Protocol CSS at the last minute.

### Previewing pages in the CMS admin

Next, restart your local server and log in to the CMS admin. Browse to a page and use the `+` icon or similar to add a new "child page". You should now see your new page type in the list of available pages. Create a new page using the `TestPage` type, give the page a title of `Test Page` and a slug of `test`, and then enter some data for the fields you defined. When you click the preview icon in the top right of the CMS page, you should hopefully see your template and data rendered successfully!

### Using advanced page models, fields, and blocks

The example above was relatively simple in terms of data, but not very flexible. Now that you have the basics covered, the next step is to start thinking about your page requirements, and how to better structure your data models.

At this point, deep diving into the [Wagtail Docs](https://docs.wagtail.org/) is very much recommended. In particular, reading up on more advanced concepts such as [Stream Fields](https://docs.wagtail.org/en/stable/topics/streamfield.html) and [Custom Block types](https://docs.wagtail.org/en/stable/advanced_topics/customisation/streamfield_blocks.html#custom-streamfield-blocks) will make it possible to make much more advanced CMS page types.

This is also a good time to start thinking about guardrails for your page and data. Some common things to consider:

-   Are there rules around the type of content that should be allowed on the page, such as the minimum or maximum number of items in a block?
-   Should there be a set order to content in a page, or can it be flexible?
-   Are there rules that should be applied at the page level, such as where it should live in the site hierarchy?
-   Should there be a limit to the number of instances of that page type? (e.g. it would be confusing to have more than one home page or contact page).

### Writing tests

When it comes to testing CMS page models, [wagtail_factories](https://github.com/wagtail/wagtail-factories) can be used to create mock data for tests to render. This can often be the trickiest part when testing more complex page models, so it takes some practice.

Factories for your page models and blocks should be defined in a `factories.py` file for your tests to import:

``` python
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
```

In your `test_models.py` file, you can then import the factory for your test and give it some data to render:

``` python
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
    page_content = resp.text
    assert "Test Heading" in page_content
    assert "Test Body" in page_content
```

### Add your new model to the DB export

When you add a new model, you must update the script that generates the sqlite DB export of our data, so that the model is included in the export. (It's an allowlist pattern, as requested by Mozilla Security).

**If you do not, the page will not be correctly exported for local development and will break for anyone using that DB export file.**

(It's down to Wagtail's multi-table inheritance pattern: if you don't specify your new model for export, Wagtail's core metadata `Page` is exported, but not the actual new data model that holds the content that's linked to that `Page`)

The script is `bin/export-db-to-sqlite.sh` and you need to add your new model to the list of models being exported. Search for `MAIN LIST OF MODELS BEING EXPORTED` and add your model (in the format `appname.ModelName`) there.

### The `CMS_ALLOWED_PAGE_MODELS` setting

When you add a new page to the CMS, it will be available to add as a new child page immediately if `DEV=True`. This means it'll be on Dev (www-dev), but not in Staging or Prod.

So if you ship a page that needs to be used immediately in Production (which will generally be most cases), you must remember to add it to `CMS_ALLOWED_PAGE_MODELS` in Bedrock's settings. If you do not, it will not be selectable as a new Child Page in the CMS.

#### Why do we have this behaviour?

Two reasons:

1.  This setting allows us to complete initial/eager work to add a new page type, but stop it being used in Production until we are ready for it (e.g. a special new campaign page type that we wanted to get ready in good time). While there will be guard rails and approval workflows around publishing, without this it could still be possible for part of the org to start using a new page without us realising it was off-limits, and possibly before it is allowed to be released.
2.  This approach allows us to gracefully deprecate pages: if a page is removed in `settings.CMS_ALLOWED_PAGE_MODELS`, that doesn't mean it disappears from Prod or can't be edited - it just stops a NEW one being added in Prod.

### Migrating Django pages to the CMS

!!! note
    This is initial documentation, noting relevant things that exist already, but much fuller recommendations will follow


Migrating a surface to Wagtail is very similar to adding a new one, but some extra thought needs to be given to the switchover between old hardcoded content and new CMS-backed content.

#### The `@prefer_cms` decorator

If you have an existing Django-based page that you want to move to be a CMS-driven page, you are faced with a quandry.

Let's say the page exists at `/some/path/`; you can create it in the CMS with a branch of pages that mirror the same slugs (a parent page with a slug of `some` and a child page with a slug of `path`). However, in order for anyone to see the published page, you would have to remove the reference to the Django view from the URLconf, so that Wagtail would get a chance to render it (because Wagtail's page-serving logic comes last in all URLConfs). **BUT\...** how can you enter content into the CMS fast enough replace the just-removed Django page? (Note: we could use a data migraiton here, but that gets complicated when there are images involved)

Equally, you may have a situation where the content for certain paths needs to be managed in the CMS for certain locales, while other locales (with rarely changing 'evergreen' content) may only exist as Django-rendered views drawing strings from Fluent.

The answer here is to use the `bedrock.cms.decorators.prefer_cms` decorator/helper.

A Django view decorated with `prefer_cms` will check if a live CMS page has been added that matches the same overall, relative path as the Django view. If it finds one, it will show the user ``that`` CMS page instead. If there is no match in the CMS, then the original Django view will be used.

The result is a graceful handover flow that allows us to switch to the CMS page without needing to remove the Django view from the URLconf, or to maintain a hybrid approach to page management. It doesn't affect previews, so the review of draft pages before publishing can continue with no changes. Once the CMS is populated with a live version of the replacement page, that's when a later changeset can remove the deprecated Django view if it's no longer needed.

The `prefer_cms` decorator can be used directly on function-based views, or can wrap views in the URLconf. It should not used with `bedrock.mozorg.util.page` due to the complexity of passing through what locales are involved, but instead the relevant URL route should be refactored as a regular Django view, and then decorated with `prefer_cms`

For more details, please see the docstring on `bedrock.cms.decorators.prefer_cms`.

## Generating URLs for CMS pages in non-CMS templates

Pages in the CMS don't appear in the hard-coded URLConfs in Bedrock. Normally, this means there's no way to use ``url()`` to generate a path to it.

However, if there's a page in the CMS you need to generate a URL for using the `url()` template tag, ``and you know what its path will be``, Bedrock contains a solution.

`bedrock.cms.cms_only_urls` is a special URLConf that only gets loaded during the call to the `url()` helper. If you expand it with a named route definition that matches the path you know will/should exist in the CMS (and most of our CMS-backed pages ``do`` have carefully curated paths), the `url()` helper will give you a path that points to that page, even though it doesn't really exist as a static Django view.

See the example in the `bedrock.cms.cms_only_urls.py` file.

!!! note
    Moving a URL route to `cms_only_urls.py` is a natural next step after you've migrated a page to the CMS using the `@prefer_cms` decorator and now want to remove the old view without breaking all the calls to ``url('some.view')`` or ``reverse('some.view')``.


## Images

### Using editor-uploaded images in templates

Images may be uploaded into Wagtail's Image library and then included in content-managed surfaces that have fields/spaces for images.

Images are stored in the same media bucket that fixed/hard-coded Bedrock images get put in, and coexist alongside them, being namespaced into a directory called `custom-media/`.

If a surface uses an image, images use must be made explicit via template markup --- we need to state both *where* and *how* an image will be used in the template, including specifying the size the image will be. This is because --- by design and by default --- Wagtail can generate any size version that the template mentions by providing a "filter spec" e.g.

``` jinja
{% set the_image=image(page.product_image, "width-1200") %}
<img class="some-class" src="{{ the_image.url }})"/>
```

(More examples are available in the [Wagtail Images docs](https://docs.wagtail.org/en/stable/topics/images.html).)

When including an image in a template we ONLY use filter specs between 2400px down to 200px in 200px steps, plus 100px.

Laying them out, these are the **only** filter specs allowed. **Using alternative ones will trigger an error in production.**

-   `width-100`
-   `width-200`
-   `width-400`
-   `width-600`
-   `width-800`
-   `width-1000`
-   `width-1200`
-   `width-1400`
-   `width-1600`
-   `width-1800`
-   `width-2000`
-   `width-2200`
-   `width-2400`

### Why are we limiting filter-specs to that set?

In a line: to balance infrastructure security constraints with site flexiblity, we have to pre-generate a known set of renditions.

Normally, if that `product_image` is not already available in `1024x1024`, Wagtail will resize the original image to suit, on the fly, and store this "rendition" (a resized version, basically) in the cloud bucket. It will also add a reference to the database so that Wagtail knows that the rendition already exists.

In production, the "Web" deployment has **read-only** access to the DB and to the cloud storage, so it will not be able to generate new renditions on the fly. Instead, we pre-generate those renditions when the image is saved.

This approach will not be a problem if we stick to image filter-specs from the 'approved' list. Note that extending the list of filter-specs is possible, if we need to.

### I've downloaded a fresh DB and the images are missing!

That's expected: the images don't live in the DB, only references to them live there. CMS images are destined for public consumption, and Dev, Stage and Prod all store their images in a publicly-accessible cloud bucket.

We have a tool to help you sync down the images from the relevant bucket.

By default, the sqlite DB you can download to run bedrock locally is based on the data in Bedrock Dev. To get images from the cloud bucket for dev, run:

``` shell
./manage.py download_media_to_local
```

This will look at your local DB, find the image files that it says should be available locally, copy them down to your local machine, then trigger the versions/renditions of them that should also exist.

The command will only download images you don't already have locally. You can use the `--redownload` option to force a redownload of all images.

If you have a DB from Stage you can pass the `--environment=stage` option to get the images from the Stage bucket instead. Same goes for Production.

## L10N and Translation Management

:::: important
!!! title "Important"


Localization via Wagtail is something we are ramping up on, so please do not assume the following notes are final, or that the workflows are currently all rock-solid. We're learning as we go.
::::

### Page-tree concept

Our Wagtail setup uses the official [wagtail-localize](https://wagtail-localize.org/) package to manage localization of pages.

This package supports page-level localization rather than field-level localization, which means that each locale has its own distinct tree of pages, rather than each page having a stack of duplicate fields, one per destination language.

These language-specific trees can be "synchronised" with the default `en-US` page tree, so would have the same page structure, field by field) --- or they can not be synchronised, so can have their own extra pages, or some specific pages in the tree can be made not "synchronised", while others are.

Basically, there is plenty of flexibility. The flipside of that flexibility is we may also create an edge-case situation that `wagtail-localize` won't work with, but we'll have to see and deal with it.

!!! note
    It's worth investing 15 mins in watching the [Wagtail Localize original demo](https://www.youtube.com/watch?v=mEzQcOMUzoc) to get a good feel of how it can work.


### Locale configuration within Wagtail

While the list of available overall locales is defined in code in `settings.base.WAGTAIL_CONTENT_LANGUAGES`, any locale also needs enabling via the Wagtail Admin UI before it can be used.

When you go to `Settings > Locales` in the Wagtail fly-out menu, you will see which locales are currenly enabled. You can add new ones via the `+` icon.

:::: warning
!!! title "Warning"


When you add/edit a Locale in this part of the admin, you will see an option to enable syncronisation between locales. **Do not enable this**. If it is enabled, for every new page added in `en-US`, it will auto-create page aliases in every other enabled locale and these will deliver the `en-US` content under locale-specific paths, which is not what we want.
::::

### Localization process

### Manual updates

At its most basic, there's nothing stopping us using copy-and-paste to enter translations into lang-specific pages, which might work well if we have a page in just one non-en-US lang and an in-house colleague doing the translation.

### Automated via Smartling

However, we also have automation available to send source strings to translation vendor Smartling. This uses the `wagtail-localize-smartling` package.

Here's the overall workflow:

1.  CMS page "MyPage" is created in the default lang (`en-US`)

2.  The "Translate this page" option is triggered for MyPage, and relevant langs are selected from the configured langs that Smartling supports. (We don't have to translate into all of them)

3.  A translation Job is created in Smartling, awaiting authorization by our L10N team.

4.  A L10N team colleague authorizes the Job and selects the relevant translation workflow(s) for the relevant lang(s)

    > -   ⚠️ Note that one Wagtail Page (or one Wagtail Snippet) creates one single Job, so if you select mutiple target languages for that Job and submit it, you won't get it back from Smartling until ``all`` languages involved are submitted by translators. One way around this is to submit each language as a separate Job, but that creates more work for our L10N team to coordinate. (We are looking to refine that experience in the future and to make it better for everyone.)

5.  Once the job is completed, the localised strings flow back to Wagtail and populate a ``draft`` version of each language-specific page.

6.  A human reviews these draft pages and publishes them

    > -   ⚠️ When a translation flows back, by default the relevant pages are ``not`` automatically published. At the moment, CMS admins are emailed for each language in a Job when it is synced back from Smartling, reminding them of this. (We may well move this to in-dashboard Wagtail `Tasks` for better UX.)
    > -   The CMS admin sidebar has a link to `Smartling Jobs`. You can use this to see what translations have landed, and also follow the link to the localized version of the page, which you can then Preview, visually check, then Publish like a regular page.

**Notes:**

-   Smartling/`wagtail-localize-smartling` will only translate pages from the base lang (`en-US`) to another lang - it won't treat, say, a Page in `fr` as a source-language document.
-   If a string is received from Smartling into the CMS and then manually edited on the CMS side, the change will ``not`` be overwritten by subsequent Smartling syncs and the manual edit needs to be added on the Smartling side for consistency and stability.
-   If a page is translated from `en-US` once, then has new `en-US` content added that is sent for translation, that will trigger a new Smartling Job. When that job is complete, it ``will`` overwrite any manual edits made to a translation within the CMS. This is why it's important to make sure Smartling contains any manual tweaks done to translations in the CMS.

### Automated via Pontoon

It should also be possible to use [Pontoon](https://pontoon.mozilla.org/) with ``wagtail-localize``. (There are notes on the [Pontoon integration](https://wagtail-localize.org/stable/how-to/integrations/pontoon/) here, but we have not yet tried to enable this alongside ``wagtail-localize-smartling``).

Additionally using Pontoon would let us benefit from community translations across a broad range of languages. However, we have yet to try to set this up and would need to agree which parts of the site do and do not use Pontoon.

## Infrastructure notes

### SSO authentication setup

When the env vars `OIDC_RP_CLIENT_ID` and `OIDC_RP_CLIENT_SECRET` are present and `USE_SSO_AUTH` is set to True in settings, Bedrock will use Mozilla SSO instead of Django's default username + password approach to sign in. The deployed sites will have these set, but we also have credentials available for using SSO locally if you need to develop something that needs it - see our password vault.

Note that Bedrock in SSO mode will ``not`` support 'drive by' user creation even if they have an `@mozilla.com` identity. Only users who already exist in the Wagtail admin as a User will be allowed to log in. You can create new users using Django's [createsuperuser](https://docs.djangoproject.com/en/5.0/ref/django-admin/#createsuperuser) command, setting both the username and email to be your `flast@mozilla.com` LDAP address

### Non-SSO authentication for local builds

If you just want to use a username and password locally, you can - ensure those env vars above are not set, and use Django's [createsuperuser](https://docs.djangoproject.com/en/5.0/ref/django-admin/#createsuperuser) command to make an admin user in your local build.
