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
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.http import require_safe
from django.views.generic import TemplateView

from commonware.decorators import xframe_allow
from jsonview.decorators import json_view
from product_details import product_details
from sentry_sdk import capture_exception

from bedrock.base.geo import get_country_from_request
from bedrock.base.waffle import switch
from bedrock.contentcards.models import get_page_content_cards
from bedrock.contentful.api import ContentfulPage
from bedrock.contentful.models import ContentfulEntry
from bedrock.mozorg.credits import CreditsFile
from bedrock.mozorg.forms import MeicoEmailForm
from bedrock.mozorg.models import WebvisionDoc
from bedrock.pocketfeed.models import PocketArticle
from lib import l10n_utils
from lib.l10n_utils import L10nTemplateView, RequireSafeMixin

credits_file = CreditsFile("credits")
TECH_BLOG_SLUGS = ["hacks", "cd", "futurereleases"]


def csrf_failure(request, reason=""):
    template_vars = {"reason": reason}
    return l10n_utils.render(request, "mozorg/csrf-failure.html", template_vars, status=403)


@xframe_allow
def hacks_newsletter(request):
    return l10n_utils.render(request, "mozorg/newsletter/hacks.mozilla.org.html")


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


NAMESPACES = {
    "addons-bl": {
        "namespace": "http://www.mozilla.org/2006/addons-blocklist",
        "standard": "Add-ons Blocklist",
        "docs": "https://wiki.mozilla.org/Extension_Blocklisting:Code_Design",
    },
    "em-rdf": {
        "namespace": "http://www.mozilla.org/2004/em-rdf",
        "standard": "Extension Manifest",
        "docs": "https://developer.mozilla.org/en/Install_Manifests",
    },
    "microsummaries": {
        "namespace": "http://www.mozilla.org/microsummaries/0.1",
        "standard": "Microsummaries",
        "docs": "https://developer.mozilla.org/en/Microsummary_XML_grammar_reference",
    },
    "mozsearch": {
        "namespace": "http://www.mozilla.org/2006/browser/search/",
        "standard": "MozSearch plugin format",
        "docs": "https://developer.mozilla.org/en/Creating_MozSearch_plugins",
    },
    "update": {
        "namespace": "http://www.mozilla.org/2005/app-update",
        "standard": "Software Update Service",
        "docs": "https://wiki.mozilla.org/Software_Update:Testing",
    },
    "xbl": {
        "namespace": "http://www.mozilla.org/xbl",
        "standard": "XML Binding Language (XBL)",
        "docs": "https://developer.mozilla.org/en/XBL",
    },
    "xforms-type": {
        "namespace": "http://www.mozilla.org/projects/xforms/2005/type",
        "standard": "XForms mozType extension",
        "docs": "https://developer.mozilla.org/en/XForms/Custom_Controls",
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


@require_safe
def home_view(request):
    locale = l10n_utils.get_locale(request)
    country = get_country_from_request(request)
    donate_params = settings.DONATE_COUNTRY_CODES.get(country, settings.DONATE_COUNTRY_CODES["US"])

    # presets are stored as a string but, for the home banner
    # we need it as a list.
    donate_params["preset_list"] = donate_params["presets"].split(",")
    ctx = {
        "donate_params": donate_params,
        "pocket_articles": PocketArticle.objects.all()[:4],
        "ftl_files": ["mozorg/home", "mozorg/home-mr2-promo"],
        "add_active_locales": ["de", "fr"],
    }

    if locale.startswith("en-"):
        if switch("contentful-homepage-en"):
            try:
                template_name = "mozorg/home/home-contentful.html"
                # TODO: use a better system to get the pages than the ID
                ctx.update(ContentfulEntry.objects.get_page_by_id(content_id=settings.CONTENTFUL_HOMEPAGE_LOOKUP["en-US"]))
            except Exception as ex:
                capture_exception(ex)
                # if anything goes wrong, use the rest-of-world home page
                template_name = "mozorg/home/home.html"
        else:
            template_name = "mozorg/home/home.html"
    elif locale == "de":
        if switch("contentful-homepage-de"):
            try:
                template_name = "mozorg/home/home-contentful.html"
                ctx.update(ContentfulEntry.objects.get_page_by_id(content_id=settings.CONTENTFUL_HOMEPAGE_LOOKUP["de"]))
            except Exception as ex:
                capture_exception(ex)
                # if anything goes wrong, use the old page
                template_name = "mozorg/home/home-de.html"
                ctx["page_content_cards"] = get_page_content_cards("home-de", "de")
        else:
            template_name = "mozorg/home/home-de.html"
            ctx["page_content_cards"] = get_page_content_cards("home-de", "de")
    elif locale == "fr":
        template_name = "mozorg/home/home-fr.html"
        ctx["page_content_cards"] = get_page_content_cards("home-fr", "fr")
    else:
        template_name = "mozorg/home/home.html"

    return l10n_utils.render(request, template_name, ctx)


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
        if page_type == "pageHome":
            template = "mozorg/home/home-contentful.html"
        elif page_type == "pagePageResourceCenter":
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

    This view automatically adds the `cache_page` decorator. The default timeout
    is 10 minutes, configurable by setting the `WEBVISION_DOCS_CACHE_TIMEOUT` setting to change
    the default for all views, or the `cache_timeout` property for an single instance.

    """

    doc_name = None
    doc_context_name = "doc"
    cache_timeout = settings.WEBVISION_DOCS_CACHE_TIMEOUT

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

    @classmethod
    def as_view(cls, **initkwargs):
        cache_timeout = initkwargs.pop("cache_timeout", cls.cache_timeout)
        return cache_page(cache_timeout)(super().as_view(**initkwargs))


MEICO_EMAIL_SUBJECT = "MEICO Interest Form"
MEICO_EMAIL_SENDER = "Mozilla.com <noreply@mozilla.com>"
MEICO_EMAIL_TO = ["meico@mozilla.com"]


@json_view
def meico_email_form(request):
    """
    This form accepts a POST request from future.mozilla.org/meico and will send
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

    form = MeicoEmailForm(
        {
            "email": json_data.get("email", ""),
            "name": json_data.get("name", ""),
            "interests": json_data.get("interests", ""),
            "description": json_data.get("description", ""),
        }
    )

    if not form.is_valid():
        return {"error": 400, "message": "Invalid form data"}, 400, CORS_HEADERS

    email_msg = render_to_string("mozorg/emails/meico-email.txt", {"data": form.cleaned_data}, request=request)

    email = EmailMessage(MEICO_EMAIL_SUBJECT, email_msg, MEICO_EMAIL_SENDER, MEICO_EMAIL_TO)

    try:
        email.send()
    except Exception as e:
        return {"error": 400, "message": str(e)}, 400, CORS_HEADERS

    return {"status": "ok"}, 200, CORS_HEADERS
