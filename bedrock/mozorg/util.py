# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.conf import settings
from django.conf.urls.defaults import url
from django.views.decorators.csrf import csrf_exempt

import commonware.log
from lib import l10n_utils
from lib.l10n_utils.dotlang import lang_file_has_tag

try:
    import newrelic.agent
except ImportError:
    newrelic = False


log = commonware.log.getLogger('mozorg.util')


def page(name, tmpl, decorators=None, **kwargs):
    """
    Define a bedrock page.

    The URL name is the template name, with the extension stripped and the
    slashes changed to dots. So if tmpl="path/to/template.html", then the
    page's URL name will be "path.to.template".

    @param name: The URL regex pattern.  If not empty, a trailing slash is
        added automatically, so it shouldn't be included in the parameter
        value.
    @param tmpl: The template name.  Also used to come up with the URL name.
    @param decorators: A decorator or an iterable of decorators that should
        be applied to the view.
    @param kwargs: Any additional arguments are passed to l10n_utils.render
        after the request and the template name.
    """
    pattern = r'^%s/$' % name if name else r'^$'

    # Set the name of the view to the template path replaced with dots
    (base, ext) = os.path.splitext(tmpl)
    name = base.replace('/', '.')

    # we don't have a caching backend yet, so no csrf (it's just a
    # newsletter form anyway)
    @csrf_exempt
    def _view(request, **kwargs):
        if newrelic:
            # Name this in New Relic to differentiate pages
            newrelic.agent.set_transaction_name(
                'mozorg.util.page:' + name.replace('.', '_'))
        kwargs.setdefault('urlname', name)
        return l10n_utils.render(request, tmpl, kwargs)

    # This is for graphite so that we can differentiate pages
    _view.page_name = name

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
                log.exception('decorators not iterable or does not contain '
                              'callable items')

    return url(pattern, _view, kwargs, name=name)


def hide_contrib_form(lang):
    """
    If the lang file for a locale exists and has the correct comment returns
    True, and False otherwise.
    :param lang: the language code
    :return: bool
    """
    return lang_file_has_tag("mozorg/contribute", lang, "hide_form")


def get_fb_like_locale(request_locale):
    """
    Returns the most appropriate locale from the list of supported Facebook
    Like button locales. This can either be the locale itself if it's
    supported, the next matching locale for that language if any or failing
    any of that the default `en_US`.
    Ref: https://www.facebook.com/translations/FacebookLocales.xml

    Adapted from the facebookapp get_best_locale() util
    """

    lang = request_locale.replace('-', '_')

    if lang not in settings.FACEBOOK_LIKE_LOCALES:
        lang_prefix = lang.split('_')[0]

        try:
            lang = next(locale for locale in settings.FACEBOOK_LIKE_LOCALES
                        if locale.startswith(lang_prefix))
        except StopIteration:
            lang = 'en_US'

    return lang
