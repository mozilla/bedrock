.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _redirects:

==================
Managing Redirects
==================

We have a redirects app in bedrock that makes it easier to add and manage
redirects. Due to the size, scope, and history of mozilla.org we have
quite a lot of redirects. If you need to add or manage redirects read on.

Add a redirect
--------------

You should add redirects in the app that makes the most sense. For example, if the source
url is ``/firefox/...`` then the ``bedrock.firefox`` app is the best place. Redirects
are added to a ``redirects.py`` file within the app. If the app you want to add redirects
to doesn't have such a file, you can create one and it will automatically be discovered
and used by bedrock as long as said app is in the ``INSTALLED_APPS`` setting (see
``bedrock/mozorg/redirects.py`` as an example).

Once you decide where it should go you can add your redirect. To do this you simply add
a call to the ``bedrock.redirects.util.redirect`` helper function in a list named
``redirectpatterns`` in ``redirects.py``. For example:

.. code-block:: python

    from bedrock.redirects.util import redirect


    redirectpatterns = [
        redirect(r'^rubble/barny/$', '/flintstone/fred/'),
    ]

This will make sure that requests to ``/rubble/barny/`` (or with the locale like
``/pt-BR/rubble/barny/``) will get a 301 response sending users to ``/flintstone/fred/``.

The ``redirect()`` function has several options. Its signature is as follows:

.. code-block:: python

    def redirect(pattern, to, permanent=True, locale_prefix=True, anchor=None, name=None,
                 query=None, vary=None, cache_timeout=12, decorators=None):
        """
        Return a url matcher suited for urlpatterns.

        pattern: the regex against which to match the requested URL.
        to: either a url name that `reverse` will find, a url that will simply be returned,
            or a function that will be given the request and url captures, and return the
            destination.
        permanent: boolean whether to send a 301 or 302 response.
        locale_prefix: automatically prepend `pattern` with a regex for an optional locale
            in the url. This locale (or None) will show up in captured kwargs as 'locale'.
        anchor: if set it will be appended to the destination url after a '#'.
        name: if used in a `urls.py` the redirect URL will be available as the name
            for use in calls to `reverse()`. Does _NOT_ work if used in a `redirects.py` file.
        query: a dict of query params to add to the destination url.
        vary: if you used an HTTP header to decide where to send users you should include that
            header's name in the `vary` arg.
        cache_timeout: number of hours to cache this redirect. just sets the proper `cache-control`
            and `expires` headers.
        decorators: a callable (or list of callables) that will wrap the view used to redirect
            the user. equivalent to adding a decorator to any other view.

        Usage:
        urlpatterns = [
            redirect(r'projects/$', 'mozorg.product'),
            redirect(r'^projects/seamonkey$', 'mozorg.product', locale_prefix=False),
            redirect(r'apps/$', 'https://marketplace.firefox.com'),
            redirect(r'firefox/$', 'firefox.new', name='firefox'),
            redirect(r'the/dude$', 'abides', query={'aggression': 'not_stand'}),
        ]
        """


Differences
-----------

This all differs from ``urlpatterns`` in ``urls.py`` files in some important ways. The first is
that these happen first. If something matches in a ``redirects.py`` file it will always win the
race if another url in a ``urls.py`` file would also have matched. Another is that these are
matched before any locale prefix stuff happens. So what you're matching against in the redirects
files is the original URL that the user requested. By default (unless you set ``locale_prefix=False``)
your patterns will match either the plain url (e.g. ``/firefox/os/``) or one with a locale
prefix (e.g. ``/fr/firefox/os/``). If you wish to include this locale in the destination URL
you can simply use python's string ``format()`` function syntax. It is passed to the ``format``
method as the keyword argument ``locale`` (e.g. ``redirect('^stuff/$', '{locale}whatnot/')``). If
there was no locale in the url the ``{locale}`` substitution will be an empty string. Similarly
if you wish to include a part of the original URL in the destination, just capture it with
the regex using a named capture (e.g. ``r'^stuff/(?P<rest>.*)$'`` will let you do
``'/whatnot/{rest}'``).

Utilities
---------

There are a couple of utility functions for use in the ``to`` argument of ``redirect`` that will
return a function to allow you to match something in an HTTP header.

ua_redirector
~~~~~~~~~~~~~

``bedrock.redirects.util.ua_redirector`` is a function to be used in the ``to`` argument that
will use a regex to match against the ``User-Agent`` HTTP header to allow you to decide where
to send the user. For example:

.. code-block:: python

    from bedrock.redirects.util import redirect, ua_redirector


    redirectpatterns = [
        redirect(r'^rubble/barny/$',
                 ua_redirector('firefox(os)?', '/firefox/', '/not-firefox/'),
                 vary='user-agent'),
    ]

You simply pass it a regex to match, the destination url (substitutions from the original URL do
work) if the regex matches, and another destination url if the regex does not match. The match is
not case sensitive unless you add the optional ``case_sensitive=True`` argument.

.. note::

    Be sure to include the header against which you're matching in the ``vary`` argument so that
    you won't be bitten by any caching proxies sending all users one way or the other.

header_redirector
~~~~~~~~~~~~~~~~~

This is basically the same as ``ua_redirector`` but works against any header. The arguments
are the same as above except that thre is an additional first argument for the name
of the header:

.. code-block:: python

    from bedrock.redirects.util import redirect, header_redirector


    redirectpatterns = [
        redirect(r'^rubble/barny/$',
                 header_redirector('cookie', 'been-here', '/firefox/', '/firefox/new/'),
                 vary='cookie'),
    ]
