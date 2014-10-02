import logging
import os
import traceback

from django.conf import settings

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
        return logging.debug(
            'unable to get {}: {}'.format(
                src, traceback.format_exc()))
    if response.status_code != 200:
        return logging.debug(
            'status code {} for {}'.format(
                response.status_code, src))

    local_path = os.path.join(IMAGE_DIR, src.split('/')[-1])
    filename = os.path.join(settings.MEDIA_ROOT, local_path)
    with open(filename, 'wb') as image_file:
        for chunk in response.iter_content(1024):
            image_file.write(chunk)

    return local_path


def get_or_create_article_image(image):
    src = image.get('src')
    if not src:
        return logging.debug('no src for img')
    try:
        return ArticleImage.objects.get(original=src)
    except ArticleImage.DoesNotExist:
        local_path = copy_image(src)
        if local_path:
            return ArticleImage.objects.create(
                original=src, local_path=local_path,
                alt=image.get('alt', ''))


def get_or_create_article(category, link, summary):
    try:
        soup = BeautifulSoup(summary)
    except:
        return logging.debug(
            'unable to make soup from {}: {}'.format(
                summary, traceback.format_exc()))

    try:
        article = Article.objects.get(link=link)
    except:
        article = Article(link=link)
    article.summary = soup.get_text()
    article.category = category

    image_soup = soup.find('img')
    if image_soup:
        article.image = get_or_create_article_image(image_soup.attrs)
    else:
        article.image = None
    article.save()
    return article


def store_categorized_article_summaries(category, parsed_feed):
    for entry in parsed_feed.get('entries', []):
        summary = entry.get('summary')
        if not summary:
            logging.debug(
                'category {}: entry without summary'.format(category))
            continue

        link = entry.get('link')
        if not link:
            logging.debug(
                'category {}: entry without link'.format(category))
            continue

        get_or_create_article(category, link, summary)


def parse_category_feeds(category_feeds=CATEGORY_FEEDS):
    for category, feed_url in category_feeds:
        try:
            parsed_feed = parse(feed_url)
        except:
            logging.debug(
                'unable to parse {} for open standard category {}: {}'.format(
                    feed_url, category, traceback.format_exc()))
        else:
            store_categorized_article_summaries(category, parsed_feed)
