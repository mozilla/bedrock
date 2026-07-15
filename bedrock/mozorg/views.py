# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.http import Http404
from django.shortcuts import render as django_render
from django.views.decorators.http import require_safe
from django.views.generic import TemplateView

from product_details import product_details

from bedrock.mozorg.credits import CreditsFile
from bedrock.mozorg.models import WebvisionDoc
from bedrock.newsletter.forms import NewsletterFooterForm
from lib import l10n_utils
from lib.l10n_utils import L10nTemplateView, RequireSafeMixin
from lib.l10n_utils.fluent import ftl_file_is_active

credits_file = CreditsFile("credits")


@require_safe
def credits_view(request):
    """Display the names of our contributors."""
    ctx = {"credits": credits_file}
    # not translated
    return django_render(request, "mozorg/credits.html", ctx)


@require_safe
def forums_view(request):
    """Display our mailing lists and newsgroups."""
    return l10n_utils.render(request, "mozorg/about/forums/forums.html")


class Robots(RequireSafeMixin, TemplateView):
    template_name = "mozorg/robots.txt"
    content_type = "text/plain"

    def get_context_data(self, **kwargs):
        hostname = self.request.get_host()
        return {"disallow_all": not hostname == "www.mozilla.org"}


class SecurityDotTxt(RequireSafeMixin, TemplateView):
    # https://github.com/mozilla/bedrock/issues/14173
    # served under .well-known/security.txt
    template_name = "mozorg/security.txt"
    content_type = "text/plain"


class GpcDotJson(RequireSafeMixin, TemplateView):
    # https://github.com/mozilla/bedrock/issues/14213
    # served under .well-known/gpc.json
    template_name = "mozorg/gpc.json"
    content_type = "application/json"


NAMESPACES = {
    "addons-bl": {
        "namespace": "http://www.mozilla.org/2006/addons-blocklist",
        "standard": "Add-ons Blocklist",
        "docs": "https://wiki.mozilla.org/Extension_Blocklisting:Code_Design",
    },
    "em-rdf": {
        "namespace": "http://www.mozilla.org/2004/em-rdf",
        "standard": "Extension Manifest",
        "docs": "https://developer.mozilla.org/Add-ons/Distribution",
    },
    "microsummaries": {
        "namespace": "http://www.mozilla.org/microsummaries/0.1",
        "standard": "Microsummaries",
        "docs": "https://wiki.mozilla.org/Microsummaries",
    },
    "mozsearch": {
        "namespace": "http://www.mozilla.org/2006/browser/search/",
        "standard": "MozSearch plugin format",
        "docs": "https://web.archive.org/web/20061116161614/http://developer.mozilla.org/en/docs/Creating_MozSearch_plugins",
    },
    "update": {
        "namespace": "http://www.mozilla.org/2005/app-update",
        "standard": "Software Update Service",
        "docs": "https://wiki.mozilla.org/Software_Update:Testing",
    },
    "xbl": {
        "namespace": "http://www.mozilla.org/xbl",
        "standard": "XML Binding Language (XBL)",
        "docs": "https://www.w3.org/TR/xbl/",
    },
    "xforms-type": {
        "namespace": "http://www.mozilla.org/projects/xforms/2005/type",
        "standard": "XForms mozType extension",
        "docs": "https://wiki.mozilla.org/XForms",
    },
    "xul": {
        "namespace": "http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul",
        "standard": "XML User Interface Language (XUL)",
        "docs": "https://en.wikipedia.org/wiki/XUL",
    },
}


@require_safe
def locales(request):
    context = {"languages": product_details.languages}
    return l10n_utils.render(request, "mozorg/locales.html", context)


@require_safe
def namespaces(request, namespace):
    context = NAMESPACES[namespace]
    context["slug"] = namespace
    template = "mozorg/namespaces.html"
    return django_render(request, template, context)


class HomeView(L10nTemplateView):
    m24_template_name = "mozorg/home/home-m24.html"
    template_name = "mozorg/home/home-new.html"
    old_template_name = "mozorg/home/home-old.html"
    activation_files = ["mozorg/home-m24", "mozorg/home-new", "mozorg/home"]

    ftl_files_map = {old_template_name: ["mozorg/home"], template_name: ["mozorg/home-new"], m24_template_name: ["mozorg/home-m24"]}

    # place expected ?v= values in this list
    variations = ["a", "b", "c"]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({"is_homepage": True})
        variant = self.request.GET.get("v", None)

        # ensure variant matches pre-defined value
        if variant not in self.variations:
            variant = None

        ctx["variant"] = variant
        return ctx

    def get_template_names(self):
        experience = self.request.GET.get("xv", None)

        if ftl_file_is_active("mozorg/home-m24") and experience not in ["quantum", "trailhead"]:
            return [self.m24_template_name]
        elif ftl_file_is_active("mozorg/home-new") and experience != "quantum":
            return [self.template_name]

        return [self.old_template_name]


class AboutView(L10nTemplateView):
    m24_template_name = "mozorg/about/index-m24.html"
    template_name = "mozorg/about/index.html"
    activation_files = ["mozorg/about", "mozorg/about-m24"]

    ftl_files_map = {template_name: ["mozorg/about"], m24_template_name: ["mozorg/about-m24"]}

    def get_template_names(self):
        if ftl_file_is_active("mozorg/about-m24"):
            return [self.m24_template_name]

        return [self.template_name]


class WebvisionDocView(RequireSafeMixin, TemplateView):
    """
    Generic view for loading a webvision doc and displaying it with a template.

    Class attributes in addition to standard Django TemplateView:

    * doc_name: The name of the file in the webvision repo.
    * doc_context_name: (default 'doc') template variable name for doc.

    """

    doc_name = None
    doc_context_name = "doc"

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault("content_type", self.content_type)
        return l10n_utils.render(self.request, self.get_template_names()[0], context, **response_kwargs)

    def get_context_data(self, **kwargs):
        try:
            doc = WebvisionDoc.objects.get(name=self.doc_name)
        except WebvisionDoc.DoesNotExist:
            raise Http404("Webvision doc not found")

        context = super().get_context_data(**kwargs)
        context[self.doc_context_name] = doc.content
        return context


@require_safe
def anti_harassment_tool_view(request):
    locale = l10n_utils.get_locale(request)
    newsletter_form = NewsletterFooterForm("antiharassment-waitlist", locale=locale)
    action = settings.BASKET_SUBSCRIBE_URL

    ctx = {"action": action, "newsletter_form": newsletter_form}

    return l10n_utils.render(request, "mozorg/antiharassment-tool.html", ctx)


@require_safe
def advertising_landing_view(request):
    context = {}
    template = "mozorg/advertising/landing.html"
    return l10n_utils.render(request, template, context)


@require_safe
def advertising_solutions_view(request):
    context = {}
    template = "mozorg/advertising/solutions.html"
    return l10n_utils.render(request, template, context)


@require_safe
def advertising_principles_view(request):
    context = {}
    template = "mozorg/advertising/principles.html"
    return l10n_utils.render(request, template, context)


@require_safe
def advertising_impact_view(request):
    context = {}
    template = "mozorg/advertising/impact.html"
    return l10n_utils.render(request, template, context)
