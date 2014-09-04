# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render as django_render
from django.template import TemplateDoesNotExist
from django.utils.translation.trans_real import parse_accept_lang_header

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

    # skip l10n if path exempt
    if template.partition('/')[0] in settings.SUPPORTED_NONLOCALES:
        return django_render(request, template, context, **kwargs)

    # Every template gets its own .lang file, so figure out what it is
    # and pass it in the context
    context['langfile'] = get_lang_path(template)

    # Get the available translation list of the current page
    context['translations'] = get_translations(context['langfile'])

    # Look for localized template if not default lang.
    if hasattr(request, 'locale') and request.locale != settings.LANGUAGE_CODE:

        # Redirect to one of the user's accept languages or the site's default
        # language (en-US) if the current locale not active
        if not template_is_active(template, get_locale(request)):
            matched = None

            for lang in get_accept_languages(request):
                if template_is_active(template, lang):
                    matched = lang
                    break

            response = HttpResponseRedirect('/' + '/'.join([
                matched or settings.LANGUAGE_CODE,
                split_path(request.get_full_path())[1]
            ]))

            # Add the Vary header to avoid wrong redirects due to a cache
            response['Vary'] = 'Accept-Language'

            return response

        localized_tmpl = '%s/templates/%s' % (request.locale, template)
        try:
            return django_render(request, localized_tmpl, context, **kwargs)
        except TemplateDoesNotExist:
            # If not found, just go on and try rendering the parent template.
            pass

    return django_render(request, template, context, **kwargs)


def get_locale(request):
    return getattr(request, 'locale', settings.LANGUAGE_CODE)


def get_accept_languages(request):
    """
    Parse the user's Accept-Language HTTP header and return a list of languages
    """
    languages = []
    pattern = re.compile(r'^([A-Za-z]{2,3})(?:-([A-Za-z]{2})(?:-[A-Za-z0-9]+)?)?$')

    try:
        parsed = parse_accept_lang_header(request.META.get('HTTP_ACCEPT_LANGUAGE', ''))
    except ValueError:  # see https://code.djangoproject.com/ticket/21078
        return languages

    for lang, priority in parsed:
        m = pattern.match(lang)

        if not m:
            continue

        lang = m.group(1).lower()

        # Check if the shorter code is supported. This covers obsolete long
        # codes like fr-FR (should match fr) or ja-JP (should match ja)
        if m.group(2) and lang not in settings.PROD_LANGUAGES:
            lang += '-' + m.group(2).upper()

        if lang not in languages:
            languages.append(lang)

    return languages
