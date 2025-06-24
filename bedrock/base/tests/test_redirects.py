import pytest


@pytest.mark.parametrize(
    "path,expected_location,expected_status",
    [
        ("/en-US/firefox/", "https://www.firefox.com", 301),
        ("/en-US/firefox/releasenotes/", "https://www.firefox.com/firefox/releasenotes/", 301),
        ("/en-US/firefox/all/", "https://www.firefox.com/download/all/", 301),
        ("/en-US/firefox/installer-help/", "https://www.firefox.com/download/installer-help/", 301),
        ("/firefox/browsers/best-browser/", "https://www.firefox.com/more/best-browser/", 301),
        ("/firefox/features/adblocker/", "https://www.firefox.com/features/adblocker/", 301),
        ("/firefox/browsers/compare/ie/", None, 404),
        ("/firefox/browsers/quantum/", None, 404),
    ],
)
def test_redirect_patterns(client, path, expected_location, expected_status):
    response = client.get(path)
    assert response.status_code == expected_status
    if expected_status == 404:
        assert "Location" not in response.headers
    else:
        assert response.headers["Location"] == expected_location
