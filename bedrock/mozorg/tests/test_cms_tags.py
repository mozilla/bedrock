# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from bedrock.mozorg.templatetags.cms_tags import add_utm_parameters


@pytest.fixture
def utm_context():
    """Context with UTM parameters as would be provided by HomePage."""
    return {
        "utm_parameters": {
            "utm_source": "www.mozilla.org",
            "utm_medium": "referral",
            "utm_campaign": "homepage",
        }
    }


@pytest.fixture
def empty_context():
    """Context without UTM parameters."""
    return {}


class TestAddUtmParameters:
    """Tests for the add_utm_parameters template filter."""

    def test_adds_utm_to_mozilla_subdomain(self, utm_context):
        """Should add UTM parameters to Mozilla subdomains."""
        url = "https://blog.mozilla.org/some-article/"
        result = add_utm_parameters(utm_context, url)
        assert "utm_source=www.mozilla.org" in result
        assert "utm_medium=referral" in result
        assert "utm_campaign=homepage" in result

    def test_adds_utm_to_mozillafoundation_org(self, utm_context):
        """Should add UTM parameters to mozillafoundation.org URLs."""
        url = "https://www.mozillafoundation.org/donate/"
        result = add_utm_parameters(utm_context, url)
        assert "utm_source=www.mozilla.org" in result
        assert "utm_medium=referral" in result
        assert "utm_campaign=homepage" in result

    def test_adds_utm_to_firefox_com(self, utm_context):
        """Should add UTM parameters to firefox.com URLs."""
        url = "https://relay.firefox.com/"
        result = add_utm_parameters(utm_context, url)
        assert "utm_source=www.mozilla.org" in result
        assert "utm_medium=referral" in result
        assert "utm_campaign=homepage" in result

    def test_excludes_www_mozilla_org(self, utm_context):
        """Should NOT add UTM parameters to www.mozilla.org (same site)."""
        url = "https://www.mozilla.org/firefox/"
        result = add_utm_parameters(utm_context, url)
        assert result == url
        assert "utm_source" not in result

    def test_excludes_bare_mozilla_org(self, utm_context):
        """Should NOT add UTM parameters to bare mozilla.org (same site)."""
        url = "https://mozilla.org/about/"
        result = add_utm_parameters(utm_context, url)
        assert result == url
        assert "utm_source" not in result

    def test_excludes_external_domains(self, utm_context):
        """Should NOT add UTM parameters to non-Mozilla domains."""
        url = "https://example.com/page/"
        result = add_utm_parameters(utm_context, url)
        assert result == url
        assert "utm_source" not in result

    def test_excludes_youtube(self, utm_context):
        """Should NOT add UTM parameters to YouTube URLs."""
        url = "https://www.youtube.com/watch?v=abc123"
        result = add_utm_parameters(utm_context, url)
        assert result == url
        assert "utm_source" not in result

    def test_preserves_existing_query_params(self, utm_context):
        """Should preserve existing query parameters when adding UTM."""
        url = "https://blog.mozilla.org/article/?foo=bar"
        result = add_utm_parameters(utm_context, url)
        assert "foo=bar" in result
        assert "utm_source=www.mozilla.org" in result

    def test_handles_empty_url(self, utm_context):
        """Should return empty string for empty URL."""
        result = add_utm_parameters(utm_context, "")
        assert result == ""

    def test_handles_none_url(self, utm_context):
        """Should return None for None URL."""
        result = add_utm_parameters(utm_context, None)
        assert result is None

    def test_handles_relative_url(self, utm_context):
        """Should return relative URLs unchanged (no host to match)."""
        url = "/en-US/firefox/"
        result = add_utm_parameters(utm_context, url)
        assert result == url

    def test_handles_missing_utm_parameters_in_context(self, empty_context):
        """Should return URL unchanged when context has no UTM parameters."""
        url = "https://blog.mozilla.org/article/"
        result = add_utm_parameters(empty_context, url)
        assert result == url

    def test_handles_protocol_relative_url(self, utm_context):
        """Should handle protocol-relative URLs."""
        url = "//blog.mozilla.org/article/"
        result = add_utm_parameters(utm_context, url)
        assert "utm_source=www.mozilla.org" in result

    def test_case_insensitive_domain_matching(self, utm_context):
        """Should match domains case-insensitively."""
        url = "https://BLOG.MOZILLA.ORG/article/"
        result = add_utm_parameters(utm_context, url)
        assert "utm_source=www.mozilla.org" in result

    def test_deeply_nested_subdomain_not_matched(self, utm_context):
        """Should NOT add UTM to deeply nested subdomains (regex only matches one level)."""
        url = "https://something.blog.mozilla.org/article/"
        result = add_utm_parameters(utm_context, url)
        # The regex only matches single-level subdomains like blog.mozilla.org
        assert result == url
