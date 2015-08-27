from braceexpand import braceexpand
import requests


def get_abs_url(url, base_url):
    if url.startswith('/'):
        # urljoin messes with query strings too much
        return ''.join([base_url, url])

    return url


def url_test(url, location=None, status_code=301, req_headers=None, req_kwargs=None,
             resp_headers=None):
    """
    Function for producing a config dict for the redirect test.

    You can use simple bash style brace expansion in the `url` and `location`
    values. If you need the `location` to change with the `url` changes you must
    use the same number of expansions or the `location` will be treated as non-expandable.

    If you use brace expansion this function will return a list of dicts instead of a dict.
    You must use the `flatten` function provided to prepare your test fixture if you do this.

    example:

        url_test('/about/drivers{/,.html}', 'https://wiki.mozilla.org/Firefox/Drivers'),
        url_test('/projects/index.{de,fr,hr,sq}.html', '/{de,fr,hr,sq}/firefox/products/'),

    :param url: The URL in question (absolute or relative).
    :param location: If a redirect, the expected value of the "Location" header.
    :param status_code: Expected status code from the request.
    :param req_headers: Extra headers to send with the request.
    :param req_kwargs: Extra arguments to pass to requests.get()
    :param resp_headers: Dict of headers expected in the response.
    :return: dict or list of dicts
    """
    test_data = {
        'url': url,
        'location': location,
        'status_code': status_code,
        'req_headers': req_headers,
        'req_kwargs': req_kwargs,
        'resp_headers': resp_headers,
    }
    expanded_urls = list(braceexpand(url))
    num_urls = len(expanded_urls)
    if num_urls == 1:
        return test_data

    new_urls = []
    if location:
        expanded_locations = list(braceexpand(test_data['location']))
        num_locations = len(expanded_locations)

    for i, url in enumerate(expanded_urls):
        data = test_data.copy()
        data['url'] = url
        if location and num_urls == num_locations:
            data['location'] = expanded_locations[i]
        new_urls.append(data)

    return new_urls


def assert_valid_url(url, location, status_code, req_headers, req_kwargs,
                     resp_headers, base_url):
    """
    Define a test of a URL's response.
    :param url: The URL in question (absolute or relative).
    :param location: If a redirect, the expected value of the "Location" header.
    :param status_code: Expected status code from the request.
    :param req_headers: Extra headers to send with the request.
    :param req_kwargs: Extra arguments to pass to requests.get()
    :param resp_headers: Dict of headers expected in the response.
    :param base_url: Base URL for the site to test.
    """
    kwargs = {'allow_redirects': False}
    if req_headers:
        kwargs['headers'] = req_headers
    if req_kwargs:
        kwargs.update(req_kwargs)

    abs_url = get_abs_url(url, base_url)
    resp = requests.get(abs_url, **kwargs)
    assert resp.status_code == status_code
    if location:
        assert 'location' in resp.headers
        assert resp.headers['location'] == get_abs_url(location, base_url)

    if resp_headers:
        for name, value in resp_headers.items():
            print name, value
            assert name in resp.headers
            assert resp.headers[name].lower() == value.lower()


def flatten(urls_list):
    """Take a list of dicts which may itself contain some lists of dicts, and
       return a generator that will return just the dicts in sequence.

       Example:

       list(flatten([{'dude': 'jeff'}, [{'walter': 'walter'}, {'donny': 'dead'}]]))
       > [{'dude': 'jeff'}, {'walter': 'walter'}, {'donny': 'dead'}]
    """
    for url in urls_list:
        if isinstance(url, dict):
            yield url
        else:
            for sub_url in url:
                yield sub_url
