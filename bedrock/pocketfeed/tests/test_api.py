from django.test import override_settings
from django.utils.timezone import make_aware, utc

from bedrock.pocketfeed import api

import datetime
from mock import patch


@override_settings(POCKET_API_URL='test_url', POCKET_CONSUMER_KEY='1234',
                   POCKET_ACCESS_TOKEN='5678')
@patch.object(api, 'requests')
def test_get_articles_data(req_mock):
    expected_payload = {
        'consumer_key': '1234',
        'access_token': '5678',
        'count': 7,
        'detailType': 'complete',
    }

    api.get_articles_data(count=7)

    req_mock.post.assert_called_once_with('test_url',
                                         json=expected_payload,
                                         timeout=5)


@patch.object(api, 'requests')
def test_complete_articles_data(req_mock):
    articles = [
        (
            None,
            {
                'id': '12345',
                'comment': 'test comment',
                'excerpt': 'test excerpt',
                'quote': 'test quote',
                'time_shared': '1531937658',
                'image_src': 'https://www.test.com/test.png',
            }
        )
    ]

    api.complete_articles_data(articles)

    # article should have new key 'pocket_id' equal to value from 'id'
    assert articles[0][1]['pocket_id'] == '12345'

    # unnecessary keys should be removed
    assert 'id' not in articles[0][1]
    assert 'comment' not in articles[0][1]
    assert 'excerpt' not in articles[0][1]
    assert 'quote' not in articles[0][1]

    # 'time_shared' should be converted to a datetime value
    assert articles[0][1]['time_shared'] == make_aware(datetime.datetime(2018, 7, 18, 11, 14, 18), utc)

    # should have attempted to GET request against image_src
    req_mock.get.assert_called_once_with('https://www.test.com/test.png')
