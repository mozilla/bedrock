# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os

from django.http import Http404
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_safe

import commonware.log

from bedrock.base.waffle import switch
from lib import l10n_utils

log = commonware.log.getLogger("mozorg.util")


def page(name, tmpl, decorators=None, url_name=None, ftl_files=None, enabling_switch=None, **kwargs):
    """
    Define a bedrock page.

    The URL name is the template name, with the extension stripped and the
    slashes changed to dots. So if tmpl="path/to/template.html", then the
    page's URL name will be "path.to.template". Set the `url_name` parameter
    to override this name.

    @param name: The URL path. It is passed to `django.urls.path`.
    @param tmpl: The template name.  Also used to come up with the URL name.
    @param decorators: A decorator or an iterable of decorators that should
        be applied to the view.
    @param url_name: The value to use as the URL name, default is to coerce
        the template path into a name as described above.
    @param active_locales: A list of locale codes that should be active for this page
        regardless of the state of the lang files. Useful for pages with locale-
        specific templates or non-English text in the template. Ignores the lang
        file activation tags.
    @param add_active_locales: A list of locale codes that should be active for this page
        in addition to those from the lang or ftl files.
    @param ftl_files: A list of FTL files that combined contain the strings for this page.
    @param enabling_switch: An optional waffle switch name. When provided,
        the page returns 404 if the switch is disabled.
    @param kwargs: Any additional arguments are passed to l10n_utils.render
        as the context.
    """
    if url_name is None:
        # Set the name of the view to the template path replaced with dots
        (base, ext) = os.path.splitext(tmpl)
        url_name = base.replace("/", ".")

    @csrf_exempt
    @require_safe
    def _view(request):
        if enabling_switch and not switch(enabling_switch):
            raise Http404()
        kwargs.setdefault("urlname", url_name)
        return l10n_utils.render(request, tmpl, kwargs, ftl_files=ftl_files)

    # This is for graphite so that we can differentiate pages
    _view.page_name = url_name

    # Apply decorators
    if decorators:
        if callable(decorators):
            _view = decorators(_view)
        else:
            try:
                # Decorators should be applied in reverse order so that input
                # can be sent in the order your would write nested decorators
                # e.g. dec1(dec2(_view)) -> [dec1, dec2]
                for decorator in reversed(decorators):
                    _view = decorator(_view)
            except TypeError:
                log.exception("decorators not iterable or does not contain callable items")

    return path(name, _view, name=url_name)
