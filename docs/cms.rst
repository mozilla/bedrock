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
------------------

Wagtail CMS will be used to make either entire pages or portions of pages (let's
call them 'surfaces') content-editable on www.mozilla.org. It is not a free-for-all
add-any-page-you-like approach, but rather a careful rollout of surfaces with
appropriate guard rails that helps ensure the integrity, quality and security of
www.mozilla.org.

Surfaces will be authored via a closed 'Editing' deployment and when those changes
are published they will become visible on the main www.mozilla.org 'Web' deployment.

Accessing the CMS
-----------------

Details to come


Editing current content surfaces
--------------------------------

Official `Editor Guide`_.

Bedrock-specific details to come.



Adding new content surfaces
---------------------------

Official `Editor Guide`_.

Bedrock-specific details to come.


Images
------

Using editor-uploaded images in templates
=========================================

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

Laying them out, these are
the **only** filter specs allowed. **Using alternative ones will trigger an error in production.**

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
--------------------

SSO authentication setup
========================

When the env vars ``OIDC_RP_CLIENT_ID`` and ``OIDC_RP_CLIENT_SECRET`` are present and ``USE_SSO_AUTH`` is set to True in settings, Bedrock will use Mozilla SSO instead of Django's default username + password approach to sign in. The deployed sites will have these set, but we also have credentials available for using SSO locally if you need to develop something that needs it - see our password vault.

Note that Bedrock in SSO mode will `not` support 'drive by' user creation even if they have an ``@mozilla.com`` identity. Only users who already exist in the Wagtail admin as a User will be allowed to log in. You can create new users using Django's `createsuperuser`_ command, setting both the username and email to be your ``flast@mozilla.com`` LDAP address

Non-SSO authentication for local builds
=======================================
If you just want to use a username and password locally, you can - ensure those env vars above are not set, and use Django's `createsuperuser`_ command to make an admin user in your local build.


.. _Wagtail CMS: https://wagtail.org/
.. _Editor Guide: https://guide.wagtail.org/en-latest/
.. _Wagtail Images docs: https://docs.wagtail.org/en/stable/topics/images.html
.. _createsuperuser: https://docs.djangoproject.com/en/5.0/ref/django-admin/#createsuperuser
