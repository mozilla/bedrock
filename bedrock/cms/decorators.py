# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from functools import wraps

from django.http import Http404

from wagtail.views import serve as wagtail_serve

from bedrock.base.i18n import remove_lang_prefix

HTTP_200_OK = 200


def prefer_cms(view_func):
    """
    A decorator that helps us migrate from pure Django-based views
    to CMS views.

    It will try to see if `wagtail.views.serve` can find a live CMS page for the
    URL path that matches the current Django view's path, and if so, will
    return that. If not, it will let the regular Django view run.

    Workflow:

    1. This decorator is added to the target view that will be replaced with CMS content
    2. Code is deployed and initially serves the original Django page
    3. CMS content is added for /path/to/page/ -- and can be previewed and approved
       without affecting the existing Django page at all
    4. CMS Page is published and starts getting served as it is "preferred" over the Django page
    5. Later, in a second changeset, the Django view and relevant URLconf item can be removed

    Example for a function-based view:

        @prefer_cms
        def some_path(request):
            ...

    Or, in a URLconf for a regular Django view:

        ...
        path("some/path/", prefer_cms(views.some_view)),
        ...

    Or, in a URLconf with Bedrock's page() helper:
        page(
            "about/leadership/",
            "mozorg/about/leadership/index.html",
            decorators=[prefer_cms],
        )

    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        path = remove_lang_prefix(request.path_info)
        try:
            # Does Wagtail have a route that matches this? If so, show that page
            wagtail_response = wagtail_serve(request, path)
            if wagtail_response.status_code == HTTP_200_OK:
                return wagtail_response
        except Http404:
            pass

        # If not, call the original view function
        return view_func(request, *args, **kwargs)

    return wrapped_view
