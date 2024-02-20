# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.shortcuts import redirect
from django.utils.cache import add_never_cache_headers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page as WagtailBasePage

from lib import l10n_utils


@method_decorator(never_cache, name="serve_password_required_response")
class AbstractBedrockCMSPage(WagtailBasePage):
    """Base page class for all Wagtail pages within Bedrock

    Things we do to in particular are:

    * Use our l10n_utils.render() method so that templates can use Fluent string

    * Ensure private pages are not cached:
        By default, Wagtail is unopinionated about cache-control headers,
        so we need to be sure that pages with acecss restrictions are _not_
        cached anywhere in a shared resource (e.g. the CDN)
        Taking our lead from the relevant Wagtail issue
        https://github.com/wagtail/wagtail/issues/5072#issuecomment-949397013, we:
        1) Override the default `serve()` method with cache-control settings
        for pages with view restrictions.
        2) Apply `never_cache` headers to the `wagtail.Page` class's
        `serve_password_required_response` method, via the @method_decorator above
    """

    class Meta:
        abstract = True

    def _serve_with_fluent_string_support(self, request, *args, **kwargs):
        # Normally, Wagtail's serve() returns a TemplateResponse, so we
        # can swap that for our Fluent-compatible rendering method
        template = self.get_template(request, *args, **kwargs)
        context = self.get_context(request, *args, **kwargs)
        # We shouldn't need to spec any special ftl_files param for render()
        # here because the global spec is in settings.FLUENT_DEFAULT_FILES
        return l10n_utils.render(request, template, context)

    def serve(self, request, *args, **kwargs):
        # Need to replicate behaviour in https://github.com/wagtail/wagtail/blob/stable/5.2.x/wagtail/models/__init__.py#L1928
        request.is_preview = False
        response = self._serve_with_fluent_string_support(request, *args, **kwargs)
        response = super().serve(request, *args, **kwargs)
        if len(self.get_view_restrictions()):
            add_never_cache_headers(response)
        return response

    def serve_preview(self, request, *args, **kwargs):
        return self._serve_with_fluent_string_support(request, *args, **kwargs)


class StructuralPage(AbstractBedrockCMSPage):
    """A page used to create a folder-like structure within a page tree,
    under/in which other pages live.
    Not directly viewable - will redirect to its parent page if called"""

    # There are minimal fields on this model - only exactly what we need
    # `title` and `slug` fields come from Page->AbstractBedrockCMSPage
    is_structural_page = True
    # TO COME: guard rails on page heirarchy
    # subpage_types = []
    settings_panels = WagtailBasePage.settings_panels + [
        FieldPanel("show_in_menus"),
    ]
    promote_panels = []

    def serve_preview(self, request, mode_name="irrelevant"):
        # Regardless of mode_name, always redirect to the parent page
        return redirect(self.get_parent().get_full_url())

    def serve(self, request):
        return redirect(self.get_parent().get_full_url())


class SimpleRichTextPage(AbstractBedrockCMSPage):
    """Simple page that renders a rich-text field, using our broadest set of
    allowed rich-text features.

    Not intended to be commonly used, this is more a very simple reference
    implementation.
    """

    # 1. Define model fields
    # `title` and `slug` fields come from Page->AbstractBedrockCMSPage
    content = RichTextField(
        blank=True,
        features=settings.WAGTAIL_RICHEXT_FEATURES_FULL,
    )
    # Note there are no other custom fields here

    # 2. Define editing UI by extending the default field list
    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("content"),
    ]

    # 3. Specify HTML Template:
    # If not set, Wagtail will automatically choose a name for the template
    # in the format `<app_label>/<model_name_in_snake_case>.html`
    template = "cms/simple_rich_text_page.html"
