# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import jingo
import jinja2

from django.conf import settings

from dotlang import translate


def install_lang_files(ctx):
    """Install the initial set of .lang files"""
    req = ctx['request']

    if not hasattr(req, 'langfiles'):
        files = list(settings.DOTLANG_FILES)
        if ctx.get('langfile'):
            files.append(ctx.get('langfile'))
        setattr(req, 'langfiles', files)


def add_lang_files(ctx, files):
    """Install additional .lang files"""
    req = ctx['request']

    if hasattr(req, 'langfiles'):
        req.langfiles = files + req.langfiles


# TODO: make an ngettext compatible function. The pluaralize clause of a
#       trans block won't work untill we do.
@jinja2.contextfunction
def gettext(ctx, text):
    """Translate a string, loading the translations for the locale if
    necessary."""
    install_lang_files(ctx)

    trans = translate(text, ctx['request'].langfiles)
    return jinja2.Markup(trans)


@jingo.register.function
@jinja2.contextfunction
def lang_files(ctx, *files):
    """Add more lang files to the translation object"""
    # Filter out empty files
    install_lang_files(ctx)
    add_lang_files(ctx, [f for f in files if f])


# backward compatible for imports
_ = gettext


# Once tower is fixed and we only need to install the above `gettext` function
# into Jinja2 once, we should do it here. The call is simply:
# jingo.env.install_gettext_callables(gettext, gettext)
