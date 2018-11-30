from django.test import override_settings

from bedrock.pocketfeed import api
from bedrock.pocketfeed.models import PocketArticle

import json
import pytest
import responses
from pathlib2 import Path


TEST_DATA = Path(__file__).with_name('test_data')


def get_test_file_content(filename):
    with TEST_DATA.joinpath(filename).open() as fh:
        return fh.read()


def setup_responses():
    responses.add(responses.POST, 'http://www.test.com', json=json.loads(get_test_file_content('articles.json')))
    # intercept any checks to the image_src (checked in api.py)
    responses.add(responses.GET, 'https://img-getpocket.cdn.mozilla.net/direct', status=200)


@responses.activate
@override_settings(POCKET_API_URL='http://www.test.com')
def test_get_articles_data():
    setup_responses()
    articles = api.get_articles_data()
    assert len(articles['recommendations']) == 4
    assert articles['recommendations'][0]['id'] == 2262198874
    assert articles['recommendations'][2]['id'] == 2248108002


@responses.activate
@pytest.mark.django_db
@override_settings(POCKET_API_URL='http://www.test.com')
def test_refresh_articles():
    setup_responses()
    updated, deleted = PocketArticle.objects.refresh()
    assert updated == 3
    assert deleted == 0
    articles = PocketArticle.objects.all()
    assert len(articles) == 3

    # this article has a valid image URL
    article = articles.get(pocket_id=2262198874)
    assert article.domain == 'blog.mozilla.org'
    assert article.url == 'https://blog.mozilla.org/blog/2018/07/18/mozilla-responds-to-european-commissions-google-android-decision'
    assert article.image_src.startswith('https://img-getpocket.cdn.mozilla.net')

    # this article's image_src is http (not https), so should be None
    article = articles.get(pocket_id=2248108002)
    assert article.image_src is None

    # this article has an empty image_src, so should be None
    article = articles.get(pocket_id=2262115700)
    assert article.image_src is None


@responses.activate
@pytest.mark.django_db
@override_settings(POCKET_API_URL='http://www.test.com')
def test_refresh_articles_with_dupes():
    setup_responses()
    updated, deleted = PocketArticle.objects.refresh()
    assert updated == 3
    assert deleted == 0

    # add dupes
    articles = api.get_articles_data()['recommendations']
    api.complete_articles_data((None, a) for a in articles)
    for article in articles:
        PocketArticle.objects.create(**article)

    assert PocketArticle.objects.count() == 7
    PocketArticle.objects.refresh()
    assert PocketArticle.objects.count() == 3
