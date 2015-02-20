from __future__ import print_function

from django.conf import settings

from feedparser import parse

from bedrock.firefox.models import FirefoxOSFeedLink


def create_or_update_fxos_feed_link(locale, link, title):
    feed_link, created = FirefoxOSFeedLink.objects.get_or_create(
        locale=locale, link=link, defaults={'title': title}) 
    if not created and title != feed_link.title:
        feed_link.title = title
        feed_link.save(update_fields=['title'])


def create_or_update_fxos_feed_links(locale, parsed_feed):
    for entry in parsed_feed.get('entries', []):
        link = entry.get('link')
        title = entry.get('title')
        if link and title:
            create_or_update_fxos_feed_link(locale, link, title)


def run(*args):
    for locale, url in settings.FIREFOX_OS_FEEDS:
        try:
            parsed_feed = parse(url)
        except:
            print('Unable to fetch and parse ' + url)
        else:
            create_or_update_fxos_feed_links(locale, parsed_feed)
