import os
from itertools import groupby

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone as tz

import dateutil.parser
import requests
from bs4 import BeautifulSoup
from feedparser import parse

from .models import Article, ArticleImage


# temporary default
CATEGORY_FEEDS = getattr(
    settings,
    'OPENSTANDARD_CATEGORY_FEEDS',
    (('live', 'https://openstandard.allizom.org/category/live/feed/'),
     ('learn', 'https://openstandard.allizom.org/category/learn/feed/'),
     ('innovate', 'https://openstandard.allizom.org/category/innovate/feed/'),
     ('engage', 'https://openstandard.allizom.org/category/engage/feed/'),
     ('opinion', 'https://openstandard.allizom.org/category/opinion/feed/')))

IMAGE_DIR = getattr(settings, 'OPENSTANDARD_IMAGE_DIR', 'openstandard')


def copy_image(src):
    try:
        response = requests.get(src, stream=True, timeout=10)
    except:
        return
    if response.status_code != 200:
        return

    local_path = os.path.join(IMAGE_DIR, src.split('/')[-1])
    filename = os.path.join(settings.MEDIA_ROOT, local_path)
    # TODO: check for existing file and generate new one if not identical image
    with open(filename, 'wb') as image_file:
        for chunk in response.iter_content(1024):
            image_file.write(chunk)

    return local_path


def get_or_maybe_create_article_image(soup):
    image_soup = soup.find('img')
    if not image_soup:
        return
    src = image_soup.attrs.get('src')
    if not src:
        return
    try:
        return ArticleImage.objects.get(original=src)
    except ArticleImage.DoesNotExist:
        local_path = copy_image(src)
        if local_path:
            return ArticleImage.objects.create(
                original=src, local_path=local_path,
                alt=image_soup.attrs.get('alt', ''))


def maybe_update(model_instance, data):
    update_fields = [key for key, value in data.items() if
                     getattr(model_instance, key, None) != value]
    if update_fields:
        for field in update_fields:
            setattr(model_instance, field, data[field])
        model_instance.save(update_fields=update_fields)


def parse_datetime(text, use_tz=settings.USE_TZ, timezone=settings.TIME_ZONE):
    try:
        parsed = dateutil.parser.parse(text)
    except:
        return
    else:
        if use_tz and tz.is_naive(parsed):
            return tz.make_aware(parsed, tz.get_current_timezone())
        elif not use_tz and tz.is_aware(parsed):
            return tz.make_naive(parsed, tz.get_current_timezone())
        return parsed


def get_validated_article_data(entry, category, use_tz=settings.USE_TZ):
    for key in ('author', 'link', 'title', 'summary', 'published'):
        if not entry.get(key):
            return
    try:
        soup = BeautifulSoup(entry['summary'])
    except:
        return
    published = parse_datetime(entry['published'])
    if published:
        return {
            'author': entry['author'],
            'category': category,
            'image': get_or_maybe_create_article_image(soup),
            'link': entry['link'],
            'title': entry['title'],
            'summary': soup.get_text(),
            'published': published}


def create_or_maybe_update_article(entry, category):
    article_data = get_validated_article_data(entry, category)
    if not article_data:
        return
    try:
        article = Article.objects.get(link=article_data['link'])
    except:
        return Article.objects.create(**article_data)
    else:
        return maybe_update(article, article_data)


def update_from_category_feeds(category_feeds=CATEGORY_FEEDS):
    for category, feed_url in category_feeds:
        try:
            parsed_feed = parse(feed_url)
        except:
            continue
        for entry in parsed_feed.get('entries', []):
            create_or_maybe_update_article(entry, category)


def categorized_articles(
        cache_timeout=None, cache_key='openstandard_articles',
        force_cache_refresh=False, per_category_limit=4):

    if not force_cache_refresh:
        cached = cache.get(cache_key)
        if cached:
            return cached

    # This is faster than the equivalent SQL for a small table size,
    # which we will ensure with a cron job running delete_old_articles
    categorized = dict((category, list(articles)[:per_category_limit])
                       for category, articles in
                       groupby(Article.objects.select_related(),
                               lambda a: a.category))
    cache.set(cache_key, categorized, cache_timeout)
    return categorized


def delete_old_articles():
    'TODO'
