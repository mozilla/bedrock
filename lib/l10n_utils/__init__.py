# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
from os.path import relpath, splitext

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render as django_render
from django.template import TemplateDoesNotExist, loader
from django.utils.translation.trans_real import parse_accept_lang_header
from django.views.generic import TemplateView

from bedrock.base.urlresolvers import split_path
from .dotlang import get_translations_native_names
from .fluent import fluent_l10n, get_active_locales as ftl_active_locales
from .gettext import translations_for_template
from .utils import get_l10n_path


def template_source_url(template):
    if template in settings.EXCLUDE_EDIT_TEMPLATES:
        return None

    try:
        absolute_path = loader.get_template(template).template.filename
    except TemplateDoesNotExist:
        return None

    relative_path = relpath(absolute_path, settings.ROOT)
    return '%s/tree/master/%s' % (settings.GITHUB_REPO, relative_path)


def render_to_string(template_name,
                     context=None,
                     request=None,
                     using=None,
                     ftl_files=None):
    if request:
        context = context or {}
        locale = get_locale(request)
        if ftl_files:
            if isinstance(ftl_files, str):
                ftl_files = [ftl_files]

            # do not use list.extend() or += here to avoid modifying
            # the original list passed to the function
            ftl_files = ftl_files + settings.FLUENT_DEFAULT_FILES

            context['fluent_l10n'] = fluent_l10n([locale, 'en'],
                                                        ftl_files)
        else:
            context['fluent_l10n'] = fluent_l10n([locale, 'en'],
                                             settings.FLUENT_DEFAULT_FILES)
    return loader.render_to_string(template_name, context, request, using)


def render(request,
           template,
           context=None,
           ftl_files=None,
           activation_files=None,
           **kwargs):
    """
    Same as django's render() shortcut, but with l10n template support.
    If used like this::

        return l10n_utils.render(request, 'myapp/mytemplate.html')

    ... this helper will render the following template::

        l10n/LANG/myapp/mytemplate.html

    if present, otherwise, it'll render the specified (en-US) template.
    """
    # use copy() here to avoid modifying the dict in a view that will then
    # be different on the next call to the view.
    context = context.copy() if context else {}
    l10n = None
    ftl_files = ftl_files or context.get('ftl_files')
    locale = get_locale(request)

    # is this a non-locale page?
    name_prefix = request.path_info.split('/', 2)[1]
    nonlocale = name_prefix in settings.SUPPORTED_NONLOCALES

    # Make sure we have a single template
    if isinstance(template, list):
        template = template[0]

    if ftl_files:
        if isinstance(ftl_files, str):
            ftl_files = [ftl_files]

        # do not use list.extend() or += here to avoid modifying
        # the original list passed to the function
        ftl_files = ftl_files + settings.FLUENT_DEFAULT_FILES

        context['fluent_l10n'] = l10n = fluent_l10n([locale, 'en'],
                                                    ftl_files)
    else:
        context['fluent_l10n'] = fluent_l10n([locale, 'en'],
                                             settings.FLUENT_DEFAULT_FILES)

    # Every template gets its own .lang file, so figure out what it is
    # and pass it in the context
    context['template'] = template
    context['langfile'] = get_l10n_path(template)
    context['template_source_url'] = template_source_url(template)

    # if `locales` is given use it as the full list of active translations
    if 'active_locales' in context:
        translations = context['active_locales']
        del context['active_locales']
    else:
        if activation_files:
            translations = set()
            for af in activation_files:
                if af.endswith('.html'):
                    translations.update(translations_for_template(af))
                else:
                    translations.update(ftl_active_locales(af))

            translations = sorted(translations)

        elif l10n:
            translations = l10n.active_locales
        else:
            translations = translations_for_template(template)

        # if `add_active_locales` is given then add it to the translations for the template
        if 'add_active_locales' in context:
            translations.extend(context['add_active_locales'])
            del context['add_active_locales']

    context['translations'] = get_translations_native_names(translations)

    # Look for localized template
    if not nonlocale and getattr(request, 'locale', None):
        # Redirect to one of the user's accept languages or the site's default
        # language (en-US) if the current locale not active
        if request.locale not in translations:
            lang = get_best_translation(translations, get_accept_languages(request))
            response = HttpResponseRedirect('/' + '/'.join([
                lang,
                split_path(request.get_full_path())[1]
            ]))
            # Add the Vary header to avoid wrong redirects due to a cache
            response['Vary'] = 'Accept-Language'
            return response

        # Render try #1: Look for l10n template in locale/{{ LANG }}/templates/
        l10n_tmpl = '%s/templates/%s' % (request.locale, template)
        try:
            return django_render(request, l10n_tmpl, context, **kwargs)
        except TemplateDoesNotExist:
            pass

        # Render try #2: Look for locale-specific template in app/templates/
        locale_tmpl = '.{}'.format(request.locale).join(splitext(template))
        try:
            return django_render(request, locale_tmpl, context, **kwargs)
        except TemplateDoesNotExist:
            pass

    # Render try #3: Render originally requested/default template
    return django_render(request, template, context, **kwargs)


def get_locale(request):
    return getattr(request, 'locale', settings.LANGUAGE_CODE)


def get_accept_languages(request):
    """
    Parse the user's Accept-Language HTTP header and return a list of languages
    """
    languages = []
    pattern = re.compile(r'^([A-Za-z]{2,3})(?:-([A-Za-z]{2})(?:-[A-Za-z0-9]+)?)?$')

    parsed = parse_accept_lang_header(request.META.get('HTTP_ACCEPT_LANGUAGE', ''))

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


def get_best_translation(translations, accept_languages):
    # Look for the user's Accept-Language HTTP header to find another
    # locale we can offer
    for lang in accept_languages:
        if lang in translations:
            return lang

    # Check for the fallback locales if the previous look-up doesn't
    # work. This is useful especially in the Spanish locale where es-ES
    # should be offered as the fallback of es, es-AR, es-CL and es-MX
    for lang in accept_languages:
        lang = settings.FALLBACK_LOCALES.get(lang)
        if lang in translations:
            return lang

    # If all the attempts failed, just use en-US, the default locale of
    # the site
    if settings.LANGUAGE_CODE in translations:
        return settings.LANGUAGE_CODE

    # fall back to just the first locale in the list
    return translations[0]


class LangFilesMixin:
    """Generic views mixin that uses l10n_utils to render responses."""
    active_locales = None
    add_active_locales = None
    # a list of ftl files to use or a single ftl filename
    ftl_files = None
    # a dict of template names to ftl files
    ftl_files_map = None
    # a list of ftl or template files to use to determine the full list of active locales
    # mostly useful during a redesign where multiple templates are used for a single URL
    activation_files = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.active_locales:
            ctx['active_locales'] = self.active_locales
        if self.add_active_locales:
            ctx['add_active_locales'] = self.add_active_locales

        return ctx

    def get_ftl_files(self, template_names):
        if self.ftl_files:
            return self.ftl_files

        if self.ftl_files_map:
            return self.ftl_files_map.get(template_names[0])

        return None

    def render_to_response(self, context, **response_kwargs):
        template_names = self.get_template_names()
        return render(self.request, template_names, context,
                      ftl_files=self.get_ftl_files(template_names),
                      activation_files=self.activation_files, **response_kwargs)


class L10nTemplateView(LangFilesMixin, TemplateView):
    pass
