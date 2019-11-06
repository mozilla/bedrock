.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _fluent:

======================
L10n Fluent Conversion
======================

There are some tools that exist now but are only useful during our conversion
from .lang to .ftl files. This document will cover the usage of these.

If you've got a translated page you'd like to convert as-is to the Fluent system
then you can follow this procedure to get a big head start.

The key concept in converting a page to Fluent is a recipe. The recipe is a
piece of python code that can programmatically generate a Fluent file. It can
use existing Fluent files as templates, and .lang localizations as data sources.

All the functionality is provided by the ``fluent`` management command via
subcommands for each phase.

Create a recipe from a template
===============================

The first step is to create the recipe. Let's say you want to convert
``bedrock/mozorg/templates/mozorg/mission.html``, then you'll run


.. code-block:: bash

    $ make run-shell
    $ ./manage.py fluent recipe bedrock/mozorg/templates/mozorg/mission.html

This will parse all of the calls to ``_()`` and the ``trans`` blocks, process the strings in the
same way the old string extraction process did, and create new Fluent string IDs.
It will generate the recipe in ``lib/fluent_migrations/mozorg/mission.py``. The recipe name is based
on the template name after ``templates``.

Sanitize recipe
===============

The recipe creates migrations for each localizable string in the template,
with some possibly bad string IDs. At this point, you want to change
the IDs to be conforming with the best practices laid out in the l10n docs.
The existing recipe will already have the template name as prefix, though.

You can also choose to remove strings from the conversion, if you just
want to convert a subset of the strings.

Once you're happy with the recipe, you can create the Fluent files and the template.

Convert a .lang file to English .ftl
====================================

The next step is to convert an existing english .lang file into an equivalent
.ftl file in the ``en`` folder of the ``l10n`` directory in bedrock. Let's
continue with the example of ``mission.html``; you would run:

.. code-block:: bash

    $ make run-shell
    $ ./manage.py fluent ftl bedrock/mozorg/templates/mozorg/mission.html

This should create ``l10n/en/mozorg/mission.ftl`` which has all of the strings
in the order in which they appear in the template.

You want to sanitize this Fluent file by adding license headers, file comments
with staging URLs, as well as comments individual strings or groups of strings.

Convert the template
====================

With the recipe created in the first step, you'll do the following
(assuming your docker shell is still running):

.. code-block:: bash

    $ ./manage.py fluent template bedrock/mozorg/templates/mozorg/mission.html

This will reparse the template much in the same way it did when creating the recipe.
It will inspect the recipe to see which legacy strings map to which ID, that you've
chosen when you sanitized the recipe. It will then take this mapping of IDs and replace all of the old calls with new calls to ``ftl()``.
If there are any issues you should see warnings printed to your screen, but always inspect the new
template and give the page a test run to make sure all is working as expected.

Convert the View or URL
-----------------------

To get it working on the site you do have to do a bit more. The above step creates a new template
with a ``_ftl.html`` suffix instead of overwriting the old one so that you can compare them before
removing the old one. You can then either delete the old one and rename the new one with the original
name, or keep them both for a while if you may need to quickly switch back. You then need to specify
which .ftl file to use by passing it (or them) to the ``l10n_utils.render`` function in the view,
or the ``page()`` function in urls.py. See the :ref:`specifying_fluent_files` section for more details.

.. code-block:: python

    # urls.py
    urlpatterns = [
        page('mission', 'mozorg/mission.html', ftl_files=['mozorg/mission']),
    ]

    # views.py
    def mission_view(request):
        return l10n_utils.render(request, 'mozorg/mission.html', ftl_files=['mozorg/mission'])

.. note::

    If you are using the ``page()`` helper and switch to the new template name that will also change
    the name of the URL referenced by calls to ``url`` and ``reverse`` around the site. To avoid this
    you can pass the original name to the page function, e.g. ``url_name='mozorg.mission'``.

Port the translations
=====================

The remaining step is to port all of the existing translation in the .lang files over to .ftl
files in our fluent files repo.

.. code-block:: bash

    $ ./manage.py fluent ftl bedrock/mozorg/templates/mozorg/mission.html de it
    $ ./manage.py fluent ftl lib/fluent_migrations/mozorg/mission.py de it

This is the same command we used to create the original ``en`` Fluent file.
As you can see, you can specify both the template path here as well as the
recipe path.

Before you run this, make sure to update the local clones of your l10n repositories.

This command will use the Fluent file you edited as template, read the legacy translations
from ``locale`` and write the generated Fluent files for each locale into the ``git-repos/www-l10n/`` directory.

Commit
======

After that it's up to you to commit all of these changes and push them to where they need to be:
a pull request to bedrock for the template and English .ftl file changes, and a pull request
to the www-l10n repo for the translated .ftl files and activation metadata.
