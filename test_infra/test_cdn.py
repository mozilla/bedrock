import pytest
import requests


MLS_URL = 'https://location.services.mozilla.com/v1/country' \
          '?key=ec4d0c4b-b9ac-4d72-9197-289160930e14'


@pytest.mark.parametrize('url', (
    '/',
    '/firefox/',
    '/firefox/new/',
    '/about/',
))
@pytest.mark.nondestructive
def test_locale_redirect(url, base_url):
    resp = requests.get(f'{base_url}{url}',
                        allow_redirects=False,
                        headers={'accept-language': 'de'})
    assert resp.status_code == 301
    assert 'accept-language' in resp.headers['vary'].lower()
    assert resp.headers['location'].startswith('/de/')


@pytest.mark.parametrize('url', (
    # only in s3
    '/media/contentcards/img/home-en/card_2/card_2.73be009fe44e.jpg',
    # comes from bedrock
    '/media/protocol/img/logos/mozilla/black.40d1af88c248.svg',
))
@pytest.mark.nondestructive
def test_media(url, base_url):
    """Verify that media is well cached and loaded from s3"""
    url = f'{base_url}{url}'
    resp = requests.head(url)
    assert resp.status_code == 200
    assert resp.headers['cache-control'] == 'max-age=315360000, public, immutable'
    # this means it came from s3
    assert 'x-amz-version-id' in resp.headers
    # cloudfront
    assert 'x-cache' in resp.headers
    assert 'x-amz-cf-id' in resp.headers
    assert 'cloudfront' in resp.headers['x-cache']


@pytest.mark.nondestructive
def test_geo(base_url):
    """Make sure our geo results match MLS no matter where they're run"""
    cdn_url = f'{base_url}/country-code.json'
    mls_country = requests.get(MLS_URL).json()['country_code']
    cdn_country = requests.get(cdn_url).json()['country_code']
    assert cdn_country == mls_country
