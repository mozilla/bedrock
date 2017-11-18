from django.test import override_settings

from bedrock.wordpress import api
from bedrock.wordpress import models

import pytest
import responses
from pathlib2 import Path


TEST_DATA = Path(__file__).with_name('test_data')
TEST_WP_BLOGS = {
    'firefox': {
        'url': 'https://blog.mozilla.org/firefox/',
        'name': 'The Firefox Frontier',
        'num_posts': 10,
    },
    'hacks': {
        'url': 'https://hacks.mozilla.org/',
        'name': 'Hacks',
    },
}


def get_test_file_content(filename):
    with TEST_DATA.joinpath(filename).open() as fh:
        return fh.read()


def setup_responses(blog='firefox'):
    posts_url = api._api_url(TEST_WP_BLOGS[blog]['url'], 'posts', None)
    tags_url = api._api_url(TEST_WP_BLOGS[blog]['url'], 'tags', None)
    media_url = api._api_url(TEST_WP_BLOGS[blog]['url'], 'media', 75)
    media_url_404 = api._api_url(TEST_WP_BLOGS[blog]['url'], 'media', 42)
    responses.add(responses.GET, posts_url, body=get_test_file_content('posts.json'))
    responses.add(responses.GET, tags_url, body=get_test_file_content('tags.json'))
    responses.add(responses.GET, media_url, body=get_test_file_content('media_75.json'))
    responses.add(responses.GET, media_url_404, status=404)


@responses.activate
@override_settings(WP_BLOGS=TEST_WP_BLOGS)
def test_get_posts_data():
    setup_responses()
    posts = api.get_posts_data('firefox')
    tags = api.get_feed_tags('firefox')
    for post in posts:
        post['tags'] = [tags[t] for t in post['tags']]
        api.update_post_media('firefox', post)
    assert posts[0]['tags'] == ['browser', 'fastest']
    assert posts[0]['featured_media'] == {}
    assert posts[1]['featured_media'] == {}
    assert posts[2]['featured_media']['id'] == 75
    assert len(responses.calls) == 4


@responses.activate
@override_settings(WP_BLOGS=TEST_WP_BLOGS)
@pytest.mark.django_db
def test_refresh_posts():
    setup_responses('firefox')
    models.BlogPost.objects.refresh('firefox')
    setup_responses('hacks')
    models.BlogPost.objects.refresh('hacks')
    blog = models.BlogPost.objects.filter_by_blogs('firefox')
    assert len(blog) == 3
    bp = blog.get(wp_id=10)
    assert bp.tags == ['browser', 'fastest']
    assert bp.wp_blog_slug == 'firefox'
    bp = blog.get(wp_id=74)
    assert bp.tags == ['fastest', 'privacy', 'programming', 'rust', 'security']
    assert bp.featured_media['id'] == 75
    assert bp.get_featured_image_url('large').endswith('Put-Your-Trust-in-Rust-600x315.png')
    blog = models.BlogPost.objects.filter_by_blogs('firefox', 'hacks')
    assert len(blog) == 6


@responses.activate
@override_settings(WP_BLOGS=TEST_WP_BLOGS)
@pytest.mark.django_db
def test_refresh_posts_missing_media():
    setup_responses()
    models.BlogPost.objects.refresh('firefox')
    blog = models.BlogPost.objects.filter_by_blogs('firefox')
    bp = blog.get(wp_id=10)
    assert bp.get_featured_image_url('large') is None


@responses.activate
@override_settings(WP_BLOGS=TEST_WP_BLOGS)
@pytest.mark.django_db
def test_filter_by_tags():
    setup_responses()
    models.BlogPost.objects.refresh('firefox')
    blog = models.BlogPost.objects.filter_by_blogs('firefox')
    assert len(blog.filter_by_tags('browser')) == 1
    assert len(blog.filter_by_tags('fastest')) == 3
    assert len(blog.filter_by_tags('browser', 'jank')) == 2


@responses.activate
@override_settings(WP_BLOGS=TEST_WP_BLOGS)
@pytest.mark.django_db
def test_featured_tag():
    setup_responses()
    models.BlogPost.objects.refresh('firefox')
    blog = models.BlogPost.objects.filter_by_blogs('firefox')
    p = blog.filter_by_tags('browser')[0]
    assert p.get_featured_tag(['browser', 'dude']) == 'browser'
    p = blog.filter_by_tags('browser', 'jank')[0]
    assert p.get_featured_tag(['browser', 'jank', 'dude']) in ['browser', 'jank']
    assert p.get_featured_tag(['dude']) == ''
