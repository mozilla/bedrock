# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
from functools import wraps

from django.conf import settings
from django.http import Http404

from wagtail.views import serve as wagtail_serve

from bedrock.base.i18n import remove_lang_prefix
from bedrock.cms.utils import path_exists_in_cms
from lib.l10n_utils.fluent import get_active_locales

from .utils import get_cms_locales_for_path

logger = logging.getLogger(__name__)


HTTP_200_OK = 200


def prefer_cms(
    view_func=None,
    fallback_ftl_files=None,
    fallback_lang_codes=None,
    fallback_callable=None,
):
    """
    A decorator that helps us migrate from pure Django-based views
    to CMS views, or support having _some_ locales served from the CMS and
    other / evergreen content in other locales coming from Django views .

    It will try to see if `wagtail.views.serve` can find a live CMS page for the
    URL path that matches the current Django view's path, and if so, will
    return that. If not, it will let the regular Django view run.

    Args:
        view_func - the function to wrap
        fallback_ftl_files (optional) - a list of the names of the Fluent files used by
            the Django view that's being wrapped. It's a little repetitive, but
            from those we can work out what locales the page is availble in
            across the CMS and Django views
        fallback_lang_codes (optional) - a list of strings of language codes that
            show what locales are available for the Django view being wrapped.
            This is useful if, for some reason, the Fluent files are not a reliable
            way to determine the available locales for a page
            (e.g. the Fluent files cover 20 locales for some strings which appear
            on the page, but the main localized content is only in two languages,
            because the contnet doesn't come from Fluent - such as Legal Docs,
            which comes from a git repo). This works best when all the pages
            for the decorated route are available in all the specified locales --
            if not, some of the footer language-selector options will 404.
        fallback_callable (optional) - a method or function that takes the same
            arguments as the URL path (if any) in order to return a list of appropriate
            locale language codes. This is intended for use if we can't reliably
            pass either fluent files or specific lang codes (e.g. the view being
            decorated is not consistently translated via whatever non-Fluent method
            is being used)

        Note that setting both fallback_lang_codes and fallback_ftl_files will cause
        an exception to be raised - only one should be set, not both.

    Workflow:

    1. This decorator is added to the target view that will be replaced with CMS content
    2. Code is deployed and initially serves the original Django page
    3. CMS content is added for /path/to/page/ -- and can be previewed and approved
       without affecting the existing Django page at all
    4. CMS Page is published and starts getting served as it is "preferred" over the Django page
    5. Later, in a second changeset, the Django view and relevant URLconf item can be removed

    Example for a function-based view:

        @prefer_cms(fallback_ftl_files=[...])  # or fallback_lang_codes or fallback_callable
        def some_path(request):
            ...

    Or, in a URLconf for a regular Django view:

        ...
        path("some/path/", prefer_cms(views.some_view, fallback_ftl_files=[...])),

        # or

        path("some/path/", prefer_cms(views.some_view, fallback_lang_codes=["fr", "pt-BR",])),

        ...

        # or

        path("some/path/", prefer_cms(views.some_view, fallback_callable=path.to.callable)),

        ...

    IMPORTANT: there's no support for bedrock.mozorg.util.page(), deliberately.

        Making prefer_cms work with our page() helper would have made that function
        more complex. Given that it's straightforward to convert a page()-based view to
        a dedicated TemplateView, which _can_ be decorated with prefer_cms at the
        URLConf level, that is the recommended approach if you are migrating a page()
        based view to the CMS, or need to have hybrid behaviour.

    """

    if len([x for x in [fallback_ftl_files, fallback_lang_codes, fallback_callable] if x]) > 1:
        raise RuntimeError(
            "The prefer_cms decorator can be configured with only one of fallback_ftl_files or fallback_lang_codes or fallback_callable."
        )

    fallback_ftl_files = fallback_ftl_files or []
    fallback_lang_codes = fallback_lang_codes or []

    def _get_django_locales_available(
        *,
        fallback_ftl_files,
        fallback_lang_codes,
        fallback_callable,
        kwargs,
    ):
        # Prefer explicit callable to get lang codes
        if fallback_callable:
            return fallback_callable(**kwargs)

        # Use explicit list of lang codes over fluent files
        if fallback_lang_codes:
            return fallback_lang_codes

        _ftl_files = kwargs.get("ftl_files", fallback_ftl_files)
        return get_active_locales(_ftl_files, force=True)

    def decorator(func):
        @wraps(func)
        def wrapped_view(request, *args, **kwargs):
            path = remove_lang_prefix(request.path_info)

            # Annotate the request with the Django/fallback locales, as we'll
            # need them for the language picket in the footer when rendering
            # the Wagtail response IF there is a Wagtail match

            request._locales_for_django_fallback_view = _get_django_locales_available(
                fallback_ftl_files=fallback_ftl_files,
                fallback_lang_codes=fallback_lang_codes,
                fallback_callable=fallback_callable,
                kwargs=kwargs,
            )

            try:
                # Does Wagtail have a route that matches this? If so, show that page
                wagtail_response = wagtail_serve(request, path)
                if wagtail_response.status_code == HTTP_200_OK:
                    return wagtail_response
            except Http404:
                pass

            # If the page does not exist in Wagtail, call the original view function and...
            #
            # 1) Un-mark this request as being for a CMS page (which happened
            # via wagtail_serve()) to avoid lib.l10n_utils.render() incorrectly
            # looking for available translations based on CMS data, rather than
            # Fluent files
            request.is_cms_page = False

            # 2) Make extra sure this request is still annotated with any CMS-backed
            # locale versions that are available, so that we can populate the
            # language picker appropriately. (The annotation also happened via
            # wagtail_serve() thanks to AbstractBedrockCMSPage._patch_request_for_bedrock
            request._locales_available_via_cms = getattr(
                request,
                "_locales_available_via_cms",
                get_cms_locales_for_path(request),
            )
            return func(request, *args, **kwargs)

        return wrapped_view

    # If view_func is None, the decorator was called with parameters
    if view_func is None:
        return decorator
    else:
        # Otherwise, apply the decorator directly to view_func
        return decorator(view_func)


def pre_check_for_cms_404(view):
    """
    Decorator intended to avoid going through the Wagtail's serve view
    for a route that we know will be a 404. How do we know? We have a
    pre-warmed cache of all the pages of _live_ pages known to Wagtail
    - see bedrock.cms.utils for that.

    This decorator can be skipped if settings.CMS_DO_PAGE_PATH_PRECHECK is
    set to False via env vars.
    """

    def wrapped_view(request, *args, **kwargs):
        _path_to_check = request.path
        if settings.CMS_DO_PAGE_PATH_PRECHECK:
            if not path_exists_in_cms(_path_to_check):
                logger.info(f"Raising early 404 for {_path_to_check} because it doesn't exist in the CMS")
                raise Http404

        # Proceed to the original view
        return view(request, *args, **kwargs)

    return wrapped_view
