from builtins import str
from builtins import range
from django.conf import settings

import requests
from raven.contrib.django.raven_compat.models import client as sentry_client


def _request(api_url, limit=None, page=1):
    # 100 is max per page from WP
    per_page = limit or 100
    resp = requests.get(api_url, params={'per_page': per_page, 'page': page}, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    if limit is None and page == 1:
        num_pages = int(resp.headers.get('x-wp-totalpages', 1))
        if num_pages > 1:
            for i in range(2, num_pages + 1):
                data.extend(_request(api_url, page=i))

    return data


def _api_url(feed_url, data_type, data_id):
    api_url = '{}/wp-json/wp/v2/{}/'.format(feed_url.rstrip('/'), data_type)
    if data_id:
        api_url += str(data_id)
    return api_url


def get_wp_data(feed_id, data_type, data_id=None, limit=None):
    try:
        feed_config = settings.WP_BLOGS[feed_id]
        if data_type == 'posts' and limit is None:
            limit = feed_config.get('num_posts', 20)
        api_url = _api_url(feed_config['url'], data_type, data_id)
        if data_id:
            data = _request(api_url, limit=1)
        else:
            data = _request(api_url, limit=limit)

        return data
    except Exception:
        sentry_client.captureException()
        return None


def get_posts_data(feed_id, num_posts=None):
    posts = get_wp_data(feed_id, 'posts', limit=num_posts)
    if not posts:
        return None

    return posts


def complete_posts_data(blog_slug, posts):
    # posts will be a list of tuples (db obj or None, post data dict)
    tags = get_feed_tags(blog_slug)
    for _, post in posts:
        post['tags'] = [tags[t] for t in post['tags']]
        update_post_media(blog_slug, post)


def get_feed_tags(feed_id):
    tags = get_wp_data(feed_id, 'tags')
    return {t['id']: t['slug'] for t in tags}


def update_post_media(feed_id, post):
    """Fill out posts with featured media info"""
    # some blogs set featured_media to 0 when none is set
    if 'featured_media' in post:
        if post['featured_media']:
            media = get_wp_data(feed_id, 'media', post['featured_media'])
            if media:
                post['featured_media'] = media
                return

        # blank featured_media value if anything went wrong
        post['featured_media'] = {}
