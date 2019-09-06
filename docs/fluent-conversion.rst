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

Convert a .lang file to English .ftl
====================================

The first step is to convert an existing english .lang file into an equivalent
.ftl file in the ``en`` folder of the ``l10n`` directory in bedrock. Let's say
for example you have a file called ``mozorg/mission.lang``; you would run:

.. code-block:: bash

    $ make run-shell
    $ ./manage.py lang_to_ftl mozorg/mission

This should create ``l10n/en/mozorg/mission.ftl`` which has all of the strings,
generated string IDs, and a comment above each one containing the md5 hash
of the original string ID so that we can later match the new string IDs to the
proper places in the template. After you've run this and created the new file
you should inspect the file for any problems and tweak the new Fluent string
IDs to adhere to any standards you want or to make more sense.

Convert a template
==================

Once you have your new .ftl file you'll want to convert the template that used
the original .lang file to use the new system. To do that you'll do the following
(assuming your docker shell is still running):

.. code-block:: bash

    $ ./manage.py template_to_ftl mozorg/mission bedrock/mozorg/templates/mozorg/mission.html

This will parse all of the calls to ``_()`` and the ``trans`` blocks, process the strings in the
same way the old string extraction process did, and match them to the new Fluent string IDs. It
will then take this mapping of IDs and replace all of the old calls with new calls to ``ftl()``.
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

    $ ./manage.py port_lang_translations mozorg/mission

This will do several things:

1. Update the local repos for .lang files and .ftl files.
2. Find and port all of the .lang files in all locale directories
   into .ftl files in the ``git-repos/www-l10n/`` directory.
3. Look up which locales are currently active via the .lang files
   and record that info into a metadata file for the particular
   .ftl file e.g. ``git-repos/www-l10n/metadata/mozorg/mission.json``.

Clean up
========

Once all of that is done and you're happy with the results you need to remove the porting artifacts.
This is mainly the string ID hash comments from the new "en" .ftl files. To clean them you run the
``clean_ftl`` command.

.. code-block:: bash

    $ ./manage.py clean_ftl mozorg/mission

You can specify more than one file. By default it looks in the ``l10n/en/`` folder, but if you give a full
or relative path to an existing file it will clean that one.

Commit
======

After that it's up to you to commit all of these changes and push them to where they need to be:
a pull request to bedrock for the template and English .ftl file changes, and a pull request
to the www-l10n repo for the translated .ftl files and activation metadata.
