# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import codecs

from django.conf import settings
from django.conf.urls.defaults import url
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

import commonware.log
from lib import l10n_utils

try:
    import newrelic.agent
except ImportError:
    newrelic = False


log = commonware.log.getLogger('mozorg.util')


def page(name, tmpl, decorators=None, **kwargs):
    # The URL pattern is the name with a forced trailing slash if not
    # empty
    pattern = r'^%s/$' % name if name else r'^$'

    # Set the name of the view to the template path replaced with dots
    (base, ext) = os.path.splitext(tmpl)
    name = base.replace('/', '.')

    # we don't have a caching backend yet, so no csrf (it's just a
    # newsletter form anyway)
    @csrf_exempt
    def _view(request):
        if newrelic:
            # Name this in New Relic to differentiate pages
            newrelic.agent.set_transaction_name(
                'mozorg.util.page:' + name.replace('.', '_'))
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

    return url(pattern, _view, name=name)


def hide_contrib_form(lang):
    """
    If the lang file for a locale exists and has the correct comment returns
    True, and False otherwise.
    :param lang: the language code
    :return: bool
    """
    rel_path = os.path.join('locale', lang, 'mozorg/contribute.lang')
    cache_key = 'hide:%s' % rel_path
    hide_form = cache.get(cache_key)
    if hide_form is None:
        hide_form = False
        fpath = os.path.join(settings.ROOT, rel_path)
        try:
            with codecs.open(fpath, 'r', 'utf-8', errors='replace') as lines:
                for line in lines:
                    # Filter out Byte order Mark
                    line = line.replace(u'\ufeff', '')
                    if line.startswith('##'):
                        if line.startswith('## hide_form ##'):
                            hide_form = True
                    else:
                        break
        except IOError:
            pass

        cache.set(cache_key, hide_form, settings.DOTLANG_CACHE)

    return hide_form
