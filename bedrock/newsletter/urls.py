# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from django.urls import path, re_path

from bedrock.mozorg.util import page
from bedrock.newsletter import views

# A UUID looks like: f81d4fae-7dec-11d0-a765-00a0c91e6bf6
# Here's a regex to match a UUID:
uuid_regex = r"[0-Fa-f]{8}-[0-Fa-f]{4}-[0-Fa-f]{4}-[0-Fa-f]{4}-[0-Fa-f]{12}"


urlpatterns = (
    # view.existing allows a user who has a link including their token to
    # subscribe, unsubscribe, change their preferences. Each newsletter
    # includes that link for them.
    re_path("^newsletter/existing/(?P<token>[^/]*)/?$", views.existing, name="newsletter.existing.token"),
    # After submitting on the `existing` page, users end up on the
    # `updated` page.  There are optional query params; see the view.
    path("newsletter/updated/", views.updated, name="newsletter.updated"),
    # Confirm subscriptions
    re_path("^newsletter/confirm/(?P<token>%s)/$" % uuid_regex, views.confirm, name="newsletter.confirm"),
    # Update country
    re_path("^newsletter/country/(?P<token>%s)/$" % uuid_regex, views.set_country, name="newsletter.country"),
    # Request recovery message with link to manage subscriptions
    path("newsletter/recovery/", views.recovery, name="newsletter.recovery"),
    # Receives POSTs from all subscribe forms
    path("newsletter/", views.newsletter_subscribe, name="newsletter.subscribe"),
    # Welcome program out-out confirmation page (bug 1442129)
    path("newsletter/opt-out-confirmation/", views.recovery, name="newsletter.opt-out-confirmation"),
    # Branded signup pages for individual newsletters
    page("newsletter/mozilla/", "newsletter/mozilla.html", ftl_files=["mozorg/newsletters"]),
    page("newsletter/firefox/", "newsletter/firefox.html", ftl_files=["mozorg/newsletters"]),
    page("newsletter/developer/", "newsletter/developer.html", ftl_files=["mozorg/newsletters"]),
    page("newsletter/fxa-error/", "newsletter/fxa-error.html", ftl_files=["mozorg/newsletters"]),
    page("newsletter/knowledge-is-power/", "newsletter/knowledge-is-power.html", ftl_files=["mozorg/newsletters"]),
    page("newsletter/family/", "newsletter/family.html", ftl_files=["mozorg/newsletters"], active_locales=["en-US"]),
    path("newsletter/newsletter-strings.json", views.newsletter_strings_json, name="newsletter.strings"),
)
