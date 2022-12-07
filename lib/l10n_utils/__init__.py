# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from os.path import relpath, splitext

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render as django_render
from django.template import TemplateDoesNotExist, loader
from django.utils.translation.trans_real import parse_accept_lang_header
from django.views.generic import TemplateView

from product_details import product_details

from bedrock.base.urlresolvers import _get_language_map, split_path

from .fluent import fluent_l10n, get_active_locales as ftl_active_locales


def template_source_url(template):
    if template in settings.EXCLUDE_EDIT_TEMPLATES:
        return None

    try:
        absolute_path = loader.get_template(template).template.filename
    except TemplateDoesNotExist:
        return None

    relative_path = relpath(absolute_path, settings.ROOT)
    return f"{settings.GITHUB_REPO}/tree/master/{relative_path}"


def render_to_string(template_name, context=None, request=None, using=None, ftl_files=None):
    if request:
        context = context or {}
        locale = get_locale(request)
        if ftl_files:
            if isinstance(ftl_files, str):
                ftl_files = [ftl_files]

            # do not use list.extend() or += here to avoid modifying
            # the original list passed to the function
            ftl_files = ftl_files + settings.FLUENT_DEFAULT_FILES

            context["fluent_l10n"] = fluent_l10n([locale, "en"], ftl_files)
        else:
            context["fluent_l10n"] = fluent_l10n([locale, "en"], settings.FLUENT_DEFAULT_FILES)

        context["fluent_files"] = ftl_files or settings.FLUENT_DEFAULT_FILES
    return loader.render_to_string(template_name, context, request, using)


def redirect_to_best_locale(request, translations):
    # Strict only for the root URL.
    strict = request.path_info == "/" and request.headers.get("Accept-Language") is None
    # Note that translations is list of locale strings (eg ["en-GB", "ru", "fr"])
    locale = get_best_translation(translations, get_accept_languages(request), strict)
    if locale:
        return redirect_to_locale(request, locale)
    return locale_selection(request, translations)


def redirect_to_locale(request, locale, permanent=False):
    redirect_class = HttpResponsePermanentRedirect if permanent else HttpResponseRedirect
    response = redirect_class("/" + "/".join([locale, split_path(request.get_full_path())[1]]))
    # Add the Vary header to avoid wrong redirects due to a cache
    response["Vary"] = "Accept-Language"
    return response


def locale_selection(request, available_locales=None):
    # We want the root path to return a 200 and slightly adjusted content for search engines.
    is_root = request.path_info == "/"
    has_header = request.headers.get("Accept-Language") is not None
    # If `settings.DEV` is true, make `available_locales` all available locales for l10n testing.
    # Or if empty, set it to at least en-US.
    if not available_locales:
        available_locales = ["en-US"]
    if settings.DEV:
        available_locales = settings.DEV_LANGUAGES

    context = {
        "is_root": is_root,
        "has_header": has_header,
        "fluent_l10n": fluent_l10n(["en"], settings.FLUENT_DEFAULT_FILES),
        "languages": product_details.languages,
        "available_locales": sorted(set(available_locales)),
    }
    return django_render(request, "404-locale.html", context, status=200 if is_root else 404)


def render(request, template, context=None, ftl_files=None, activation_files=None, **kwargs):
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
    ftl_files = ftl_files or context.get("ftl_files")
    locale = get_locale(request)

    # is this a non-locale page?
    name_prefix = request.path_info.split("/", 2)[1]
    non_locale_url = name_prefix in settings.SUPPORTED_NONLOCALES or request.path_info in settings.SUPPORTED_LOCALE_IGNORE

    # Make sure we have a single template
    if isinstance(template, list):
        template = template[0]

    if ftl_files:
        if isinstance(ftl_files, str):
            ftl_files = [ftl_files]

        # do not use list.extend() or += here to avoid modifying
        # the original list passed to the function
        ftl_files = ftl_files + settings.FLUENT_DEFAULT_FILES

        context["fluent_l10n"] = l10n = fluent_l10n([locale, "en"], ftl_files)
    else:
        context["fluent_l10n"] = fluent_l10n([locale, "en"], settings.FLUENT_DEFAULT_FILES)

    context["fluent_files"] = ftl_files or settings.FLUENT_DEFAULT_FILES
    context["template"] = template
    context["template_source_url"] = template_source_url(template)

    # if `active_locales` is given use it as the full list of active translations
    translations = []
    if "active_locales" in context:
        translations = context["active_locales"]
        del context["active_locales"]
    else:
        if activation_files:
            translations = set()
            for af in activation_files:
                translations.update(ftl_active_locales(af))
            translations = sorted(translations)  # `sorted` returns a list.
        elif l10n:
            translations = l10n.active_locales

        # if `add_active_locales` is given then add it to the translations for the template
        if "add_active_locales" in context:
            translations.extend(context["add_active_locales"])
            del context["add_active_locales"]

        if not translations:
            translations = [settings.LANGUAGE_CODE]

    context["translations"] = get_translations_native_names(translations)

    # Ensure the path requires a locale prefix.
    if not non_locale_url:
        # If the requested path's locale is different from the best matching
        # locale stored on the `request`, and that locale is one of the active
        # translations, redirect to it. Otherwise we need to find the best
        # matching locale.

        # Does that path's locale match the request's locale?
        if locale in translations:
            # Redirect to the locale if:
            # - The URL is the root path but is missing the trailing slash OR
            # - The locale isn't in current prefix in the URL.
            if request.path == f"/{locale}" or locale != request.path.lstrip("/").partition("/")[0]:
                return redirect_to_locale(request, locale)
        else:
            return redirect_to_best_locale(request, translations)

        # Look for locale-specific template in app/templates/
        locale_tmpl = f".{locale}".join(splitext(template))
        try:
            return django_render(request, locale_tmpl, context, **kwargs)
        except TemplateDoesNotExist:
            pass

    # Render originally requested/default template
    return django_render(request, template, context, **kwargs)


def get_locale(request):
    return getattr(request, "locale", settings.LANGUAGE_CODE)


def get_accept_languages(request):
    """
    Parse the user's Accept-Language HTTP header and return a list of languages in ranked order.
    """
    ranked = parse_accept_lang_header(request.headers.get("Accept-Language", ""))
    return [lang for lang, rank in ranked]


def get_best_translation(translations, accept_languages, strict=False):
    """
    Return the best translation available comparing the accept languages against available translations.

    This attempts to find a matching translation for each accept language. It
    compares each accept language in full, and also the root. For example,
    "en-CA" looks for "en-CA" as well as "en", which maps to "en-US".

    If none found, it returns the first language code for the first available translation.

    """
    lang_map = _get_language_map()
    # translations contains mixed-case items e.g. "en-US" while the keys
    # of `lang_map` are all lowercase. But this works because the values
    # of the `lang_map` dict are mixed-case like translations and the
    # comparison below is with the values.
    valid_lang_map = {k: v for k, v in lang_map.items() if v in translations}
    for lang in accept_languages:
        lang.lower()
        if lang in valid_lang_map:
            return valid_lang_map[lang]
        pre = lang.split("-")[0]
        if pre in valid_lang_map:
            return valid_lang_map[pre]

    if settings.IS_MOZORG_MODE:
        if strict:
            # We couldn't find a best locale to return so we return `None`.
            return None
        else:
            # Use the default locale if it is an available translation.
            if settings.LANGUAGE_CODE in translations:
                return settings.LANGUAGE_CODE

            # In the rare case the default language isn't in the list,
            # return the first translation in the valid_lang_map.
            return list(valid_lang_map.values())[0]
    else:
        return settings.LANGUAGE_CODE


def get_translations_native_names(locales):
    """
    Return a dict of locale codes and native language name strings.

    Returned dict is suitable for use in view contexts and is filtered to only codes in PROD_LANGUAGES.

    :param locales: list of locale codes
    :return: dict, like {'en-US': 'English (US)', 'fr': 'Français'}
    """
    translations = {}
    for locale in locales:
        if locale in settings.PROD_LANGUAGES:
            language = product_details.languages.get(locale)
            translations[locale] = language["native"] if language else locale

    return translations


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
            ctx["active_locales"] = self.active_locales
        if self.add_active_locales:
            ctx["add_active_locales"] = self.add_active_locales

        return ctx

    def get_ftl_files(self, template_names):
        if self.ftl_files:
            return self.ftl_files

        if self.ftl_files_map:
            return self.ftl_files_map.get(template_names[0])

        return None

    def render_to_response(self, context, **response_kwargs):
        template_names = self.get_template_names()
        return render(
            self.request,
            template_names,
            context,
            ftl_files=self.get_ftl_files(template_names),
            activation_files=self.activation_files,
            **response_kwargs,
        )


class RequireSafeMixin:
    http_method_names = ["get", "head"]


class L10nTemplateView(LangFilesMixin, RequireSafeMixin, TemplateView):
    pass
