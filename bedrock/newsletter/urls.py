# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from django.urls import path

from bedrock.mozorg.util import page
from bedrock.newsletter import views
from bedrock.utils.views import VariationTemplateView

# NOTE:
# URLs are defined with two variations for token handling. This dual approach allows flexibility in
# token passing, supporting both URL-based and cookie-based methods.
#
# 1. With <uuid:token> in the path:
#    - Used when the token is explicitly provided in the URL.
#    - Example: /newsletter/confirm/<uuid:token>/
#
# 2. Without <uuid:token> in the path:
#    - Used when the token is not in the URL.
#    - In this case, the view will attempt to retrieve the token from a cookie named 'nl-token'.
#    - Example: /newsletter/confirm/

urlpatterns = (
    # view.existing allows a user who has a link including their token to
    # subscribe, unsubscribe, change their preferences. Each newsletter
    # includes that link for them.
    path("newsletter/existing/<uuid:token>/", views.existing, name="newsletter.existing"),
    path("newsletter/existing/", views.existing, name="newsletter.existing.no-token"),
    # After submitting on the `existing` page, users end up on the
    # `updated` page.  There are optional query params; see the view.
    path("newsletter/updated/", views.updated, name="newsletter.updated"),
    # Confirm subscriptions
    path("newsletter/confirm/<uuid:token>/", views.confirm, name="newsletter.confirm"),
    path("newsletter/confirm/thanks/", views.confirm_thanks, name="newsletter.confirm.thanks"),
    # Update country
    path("newsletter/country/<uuid:token>/", views.set_country, name="newsletter.country"),
    path("newsletter/country/", views.set_country, name="newsletter.country.no-token"),
    # Request recovery message with link to manage subscriptions
    path("newsletter/recovery/", views.recovery, name="newsletter.recovery"),
    # Receives POSTs from all subscribe forms
    path("newsletter/", views.newsletter_subscribe, name="newsletter.subscribe"),
    # Welcome program opt-out confirmation page (bug 1442129)
    path("newsletter/opt-out-confirmation/", views.recovery, name="newsletter.opt-out-confirmation"),
    # Branded signup pages for individual newsletters
    page("newsletter/mozilla/", "newsletter/mozilla.html", ftl_files=["mozorg/newsletters"]),
    # Firefox newsletter A/B test. See issue 15075
    path(
        "newsletter/firefox/",
        VariationTemplateView.as_view(
            template_name="newsletter/firefox.html", template_context_variations=["1", "2"], ftl_files=["mozorg/newsletters"]
        ),
        name="newsletter.firefox",
    ),
    path("newsletter/firefox/confirm/<uuid:token>/", views.firefox_confirm, name="newsletter.firefox.confirm"),
    path("newsletter/firefox/confirm/", views.firefox_confirm, name="newsletter.firefox.confirm.no-token"),
    page("newsletter/developer/", "newsletter/developer.html", ftl_files=["mozorg/newsletters"]),
    page("newsletter/fxa-error/", "newsletter/fxa-error.html", ftl_files=["mozorg/newsletters"]),
    page("newsletter/family/", "newsletter/family.html", ftl_files=["mozorg/newsletters"], active_locales=["en-US"]),
    page("newsletter/security-and-privacy/", "newsletter/security-privacy-news.html", ftl_files=["mozorg/newsletters"]),
    page("newsletter/security-and-privacy/online-harassment/", "newsletter/online-harassment.html"),
    page("newsletter/ten-tabs/", "newsletter/ten-tabs.html", ftl_files=["mozorg/newsletters"]),
    page("newsletter/monitor-waitlist/", "newsletter/monitor-waitlist.html", ftl_files=["mozorg/newsletters"]),
    path("newsletter/newsletter-all.json", views.newsletter_all_json, name="newsletter.all"),
    path("newsletter/newsletter-strings.json", views.newsletter_strings_json, name="newsletter.strings"),
)
