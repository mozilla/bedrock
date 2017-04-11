from django.test import override_settings

from bedrock.wordpress import api

import responses
from mock import patch


TEST_WP_BLOGS = {
    'firefox': {
        'url': 'https://blog.mozilla.org/firefox/',
        'name': 'The Firefox Frontier',
        'num_posts': 10,
    },
}


@patch.object(api, 'requests')
def test_limited_request(req_mock):
    api._request('some_url', limit=10)
    req_mock.get.assert_called_once_with('some_url',
                                         params={'per_page': 10, 'page': 1},
                                         timeout=5)


@responses.activate
def test_unlimited_request():
    api_url = api._api_url(TEST_WP_BLOGS['firefox']['url'], 'tags', None)
    responses.add(responses.GET,
                  api_url + '?per_page=100&page=1',
                  match_querystring=True,
                  json=[1],
                  adding_headers={'X-WP-TotalPages': '3'})
    responses.add(responses.GET,
                  api_url + '?per_page=100&page=2',
                  json=[2, 2],
                  match_querystring=True,
                  adding_headers={'X-WP-TotalPages': '3'})
    responses.add(responses.GET,
                  api_url + '?per_page=100&page=3',
                  json=[3, 3, 3],
                  match_querystring=True,
                  adding_headers={'X-WP-TotalPages': '3'})

    data = api._request(api_url, limit=None)
    assert data == [1, 2, 2, 3, 3, 3]
    assert len(responses.calls) == 3


def test_api_url():
    assert (api._api_url('https://moz.blog/', 'posts', 4) ==
            'https://moz.blog/wp-json/wp/v2/posts/4')
    assert (api._api_url('https://moz.blog/', 'tags', None) ==
            'https://moz.blog/wp-json/wp/v2/tags/')
    assert (api._api_url('https://moz.blog', 'media', 55) ==
            'https://moz.blog/wp-json/wp/v2/media/55')


@override_settings(WP_BLOGS=TEST_WP_BLOGS)
@patch.object(api, '_request')
def test_get_wp_data(req_mock):
    api.get_wp_data('firefox', 'posts')
    api_url = api._api_url(TEST_WP_BLOGS['firefox']['url'], 'posts', None)
    req_mock.assert_called_with(api_url, limit=10)

    api.get_wp_data('firefox', 'media', 75)
    api_url = api._api_url(TEST_WP_BLOGS['firefox']['url'], 'media', 75)
    req_mock.assert_called_with(api_url, limit=1)

    api.get_wp_data('firefox', 'tags')
    api_url = api._api_url(TEST_WP_BLOGS['firefox']['url'], 'tags', None)
    req_mock.assert_called_with(api_url, limit=None)
