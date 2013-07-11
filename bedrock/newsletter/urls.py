# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.conf.urls import patterns, url

from bedrock.newsletter import views

# A UUID looks like: f81d4fae-7dec-11d0-a765-00a0c91e6bf6
# Here's a regex to match a UUID:
uuid_regex = r'[0-Fa-f]{8}-[0-Fa-f]{4}-[0-Fa-f]{4}-[0-Fa-f]{4}-[0-Fa-f]{12}'


urlpatterns = patterns('',
    # view.existing allows a user who has a link including their token to
    # subscribe, unsubscribe, change their preferences. Each newsletter
    # includes that link for them.

    # There's more than one 'url' here because Django seems to have
    # trouble reversing a regex with multiple optional parts.  All
    # of these go to the same view method, they just pass different
    # arguments.

    url('^newsletter/existing/(?P<token>' + uuid_regex + ')/$',
        views.existing,
        name='newsletter.existing.token'),

    url('^newsletter/existing/$',
        views.existing,
        name='newsletter.existing'),

    # After submitting on the `existing` page, users end up on the
    # `updated` page.  There are optional query params; see the view.
    url('^newsletter/updated/$',
        views.updated,
        name='newsletter.updated'),

    # This particular view is used inside a frame somewhere else, so it
    # has its own view and doesn't work like the rest of these newsletter
    # signup pages.
    url('^newsletter/hacks\.mozilla\.org/$',
        views.hacks_newsletter,
        name='mozorg.hacks_newsletter'),

    # Page to subscribe to 'mozilla-and-you' newsletter
    url('^newsletter/$',
        views.one_newsletter_signup,
        name='newsletter.mozilla-and-you',
        kwargs={'template_name': 'newsletter/mozilla-and-you.html'}),
)
