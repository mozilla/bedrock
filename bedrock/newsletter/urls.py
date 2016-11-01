# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.conf.urls import url

from bedrock.newsletter import views
from bedrock.mozorg.util import page

# A UUID looks like: f81d4fae-7dec-11d0-a765-00a0c91e6bf6
# Here's a regex to match a UUID:
uuid_regex = r'[0-Fa-f]{8}-[0-Fa-f]{4}-[0-Fa-f]{4}-[0-Fa-f]{4}-[0-Fa-f]{12}'


urlpatterns = (
    # view.existing allows a user who has a link including their token to
    # subscribe, unsubscribe, change their preferences. Each newsletter
    # includes that link for them.

    url('^newsletter/existing/(?P<token>[^/]*)/?$',
        views.existing,
        name='newsletter.existing.token'),

    # After submitting on the `existing` page, users end up on the
    # `updated` page.  There are optional query params; see the view.
    url('^newsletter/updated/$',
        views.updated,
        name='newsletter.updated'),

    # Confirm subscriptions
    url('^newsletter/confirm/(?P<token>' + uuid_regex + ')/$',
        views.confirm,
        name='newsletter.confirm'),

    # Request recovery message with link to manage subscriptions
    url('^newsletter/recovery/',
        views.recovery,
        name='newsletter.recovery'),

    # Receives POSTs from all subscribe forms
    url('^newsletter/$',
        views.newsletter_subscribe,
        name='newsletter.subscribe'),

    # Branded signup pages for individual newsletters
    page('newsletter/mozilla', 'newsletter/mozilla.html'),
    page('newsletter/firefox', 'newsletter/firefox.html'),
    page('newsletter/developer', 'newsletter/developer.html'),
)
