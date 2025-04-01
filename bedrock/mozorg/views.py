# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import Http404
from django.shortcuts import render as django_render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_safe
from django.views.generic import TemplateView

from jsonview.decorators import json_view
from product_details import product_details

from bedrock.contentful.api import ContentfulPage
from bedrock.mozorg.credits import CreditsFile
from bedrock.mozorg.forms import MiecoEmailForm
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

        if ftl_file_is_active("mozorg/home-m24") and experience != "legacy":
            return [self.m24_template_name]
        elif ftl_file_is_active("mozorg/home-new") and experience != "legacy":
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


@method_decorator(never_cache, name="dispatch")
class ContentfulPreviewView(L10nTemplateView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        content_id = ctx["content_id"]
        page = ContentfulPage(self.request, content_id)
        ctx.update(page.get_content())
        return ctx

    def render_to_response(self, context, **response_kwargs):
        page_type = context["page_type"]
        theme = context["info"]["theme"]
        if page_type == "pagePageResourceCenter":
            template = "products/vpn/resource-center/article.html"
        elif theme == "firefox":
            template = "firefox/contentful-all.html"
        else:
            template = "mozorg/contentful-all.html"

        return l10n_utils.render(self.request, template, context, **response_kwargs)


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


MIECO_EMAIL_SUBJECT = {"mieco": "MIECO Interest Form", "innovations": "Innovations Interest Form"}
MIECO_EMAIL_SENDER = settings.DEFAULT_FROM_EMAIL
MIECO_EMAIL_TO = {
    "mieco": ["mieco@mozilla.com"],
    "innovations": ["innovations@mozilla.com"],
}


@json_view
def mieco_email_form(request):
    """
    This form accepts a POST request from future.mozilla.org/mieco and will send
    an email with the data included in the email.
    """
    CORS_HEADERS = {
        "Access-Control-Allow-Origin": "https://future.mozilla.org",
        "Access-Control-Allow-Headers": "accept, accept-encoding, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with",
    }

    if request.method == "OPTIONS":
        return {}, 200, CORS_HEADERS

    if request.method != "POST":
        return {"error": 400, "message": "Only POST requests are allowed"}, 400, CORS_HEADERS

    try:
        json_data = json.loads(request.body.decode("utf-8"))
    except json.decoder.JSONDecodeError:
        return {"error": 400, "message": "Error decoding JSON"}, 400, CORS_HEADERS

    form = MiecoEmailForm(
        {
            "email": json_data.get("email", ""),
            "name": json_data.get("name", ""),
            "interests": json_data.get("interests", ""),
            "description": json_data.get("description", ""),
            "message_id": json_data.get("message_id", ""),
        }
    )

    if not form.is_valid():
        return {"error": 400, "message": "Invalid form data"}, 400, CORS_HEADERS

    message_id = form.cleaned_data.pop("message_id") or "mieco"
    email_to = MIECO_EMAIL_TO[message_id]
    email_msg = render_to_string("mozorg/emails/mieco-email.txt", {"data": form.cleaned_data}, request=request)
    email_sub = MIECO_EMAIL_SUBJECT[message_id]

    email = EmailMessage(email_sub, email_msg, MIECO_EMAIL_SENDER, email_to)

    try:
        email.send()
    except Exception as e:
        return {"error": 400, "message": str(e)}, 400, CORS_HEADERS

    return {"status": "ok"}, 200, CORS_HEADERS


@require_safe
def anti_harassment_tool_view(request):
    locale = l10n_utils.get_locale(request)
    newsletter_form = NewsletterFooterForm("antiharassment-waitlist", locale=locale)
    action = settings.BASKET_SUBSCRIBE_URL

    ctx = {"action": action, "newsletter_form": newsletter_form}

    return l10n_utils.render(request, "mozorg/antiharassment-tool.html", ctx)
