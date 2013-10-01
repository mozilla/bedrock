# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render as django_render
from django.template import TemplateDoesNotExist

from funfactory.urlresolvers import split_path

from .dotlang import get_lang_path, get_translations
from .gettext import template_is_active


def render(request, template, context=None, **kwargs):
    """
    Same as django's render() shortcut, but with l10n template support.
    If used like this::

        return l10n_utils.render(request, 'myapp/mytemplate.html')

    ... this helper will render the following template::

        l10n/LANG/myapp/mytemplate.html

    if present, otherwise, it'll render the specified (en-US) template.
    """
    context = {} if context is None else context

    # Make sure we have a single template
    if isinstance(template, list):
        template = template[0]

    # Every template gets its own .lang file, so figure out what it is
    # and pass it in the context
    context['langfile'] = get_lang_path(template)

    # Get the available translation list of the current page
    context['translations'] = get_translations(context['langfile'])

    # Look for localized template if not default lang.
    if hasattr(request, 'locale') and request.locale != settings.LANGUAGE_CODE:

        # redirect to default lang if locale not active
        if not template_is_active(template, get_locale(request)):
            return HttpResponseRedirect('/' + '/'.join([
                settings.LANGUAGE_CODE,
                split_path(request.get_full_path())[1]
            ]))

        localized_tmpl = '%s/templates/%s' % (request.locale, template)
        try:
            return django_render(request, localized_tmpl, context, **kwargs)
        except TemplateDoesNotExist:
            # If not found, just go on and try rendering the parent template.
            pass

    return django_render(request, template, context, **kwargs)


def get_locale(request):
    return getattr(request, 'locale', settings.LANGUAGE_CODE)
