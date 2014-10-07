# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import unicode_literals

from datetime import datetime
import urllib

import jingo
from lib.l10n_utils.dotlang import _


@jingo.register.function
def format_tweet_body(tweet):
    """
    Return a tweet in an HTML format.

    @param tweet: A Tweepy Status object retrieved with the Twitter REST API.

    See the developer document for details:
    https://dev.twitter.com/docs/platform-objects/tweets
    """
    text = tweet.text
    entities = tweet.entities

    # Hashtags (#something)
    for hashtags in entities['hashtags']:
        hash = hashtags['text']
        text = text.replace('#' + hash,
                            ('<a href="https://twitter.com/search?q=%s&amp;src=hash"'
                             ' class="hash">#%s</a>' % ('%23' + urllib.quote(hash.encode('utf8')),
                                                        hash)))

    # Mentions (@someone)
    for user in entities['user_mentions']:
        name = user['screen_name']
        text = text.replace('@' + name,
                            ('<a href="https://twitter.com/%s" class="mention">@%s</a>'
                             % (urllib.quote(name.encode('utf8')), name)))

    # URLs
    for url in entities['urls']:
        text = text.replace(url['url'],
                            ('<a href="%s" title="%s">%s</a>'
                             % (url['url'], url['expanded_url'], url['display_url'])))

    # Media
    if entities.get('media'):
        for medium in entities['media']:
            text = text.replace(medium['url'],
                                ('<a href="%s" title="%s" class="media">%s</a>'
                                 % (medium['url'], medium['expanded_url'],
                                    medium['display_url'])))

    return text


@jingo.register.function
def format_tweet_timestamp(tweet):
    """
    Return an HTML time element filled with a tweet timestamp.

    @param tweet: A Tweepy Status object retrieved with the Twitter REST API.

    For a tweet posted within the last 24 hours, the timestamp label should be
    a relative format like "20s", "3m" or 5h", otherwise it will be a simple
    date like "6 Jun". See the Display Requirements for details:
    https://dev.twitter.com/terms/display-requirements
    """
    now = datetime.utcnow()
    created = tweet.created_at  # A datetime object
    diff = now - created  # A timedelta Object

    if diff.days == 0:
        if diff.seconds < 60:
            label = _('%ds') % diff.seconds
        elif diff.seconds < 60 * 60:
            label = _('%dm') % round(diff.seconds / 60)
        else:
            label = _('%dh') % round(diff.seconds / 60 / 60)
    else:
        label = created.strftime("%-d %b")

    full = created.strftime("%Y-%m-%d %H:%M")

    return ('<time datetime="%s" title="%s" itemprop="dateCreated">%s '
            '<span class="full">(%s)</span></time>'
            % (created.isoformat(), full, label, full))
