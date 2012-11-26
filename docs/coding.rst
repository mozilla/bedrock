.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _coding:

=====================
Developing on Bedrock
=====================

Writing URL Patterns
--------------------

URL patterns should be as strict as possible. It should begin with a
`^` and end with `/$` to make sure it only matches what you specifiy.
It also forces a trailing slash. You should also give the URL a name
so that other pages can reference it instead of hardcoding the URL.
Example::

    url(r'^channel/$', channel, name='mozorg.channel')

Bedrock comes with a handy shortcut to automate all of this::

    from mozorg.util import page
    page('channel', 'mozorg/channel.html')

You don't even need to create a view. It will serve up the specified
template at the given URL (the first parameter). You can also pass
template data as keyword arguments:

    page('channel', 'mozorg/channel.html',
         latest_version=product_details.firefox_versions['LATEST_FIREFOX_VERSION'])

The variable `latest_version` will be available in the template.

Writing Views
-------------

You should rarely need to write a view for mozilla.org. Most pages are
static and you should use the `page` expression documented above.

If you need to write a view and the page has a newsletter signup form
in the footer (most do), make sure to handle this in your view.
Bedrock comes with a function for doing this automatically::

    from mozorg.util import handle_newsletter
    from django.views.decorators.csrf import csrf_exempt
    
    @csrf_exempt
    def view(request):
        ctx = handle_newsletter(request)
        return l10n_utils.render(request, 'app/template.html', ctx)

You'll notice a few other things in there. You should use the
`l10n_utils.render` function to render templates because it handles
special l10n work for us. Since we're handling the newsletter form
post, you also need the `csrf_exempt` decorator.

Make sure to namespace your templates by putting them in a directory
named after your app, so instead of templates/template.html they would
be in templates/blog/template.html if `blog` was the name of your app.
