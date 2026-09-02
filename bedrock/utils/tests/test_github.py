# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.test import override_settings

from bedrock.utils import github


@override_settings(FLUENT_REPO_AUTH="")
def test_get_client_no_auth_configured():
    github.GITHUB_CLIENT = None
    assert github.get_client() is None


@override_settings(FLUENT_REPO_AUTH="ghp_baretoken123")
def test_get_client_bare_token():
    github.GITHUB_CLIENT = None
    with patch.object(github, "Github") as GithubMock:
        client = github.get_client()
    GithubMock.assert_called_once_with("ghp_baretoken123")
    assert client is GithubMock.return_value
    github.GITHUB_CLIENT = None


@override_settings(FLUENT_REPO_AUTH="dude:abides")
def test_get_client_legacy_username_and_token():
    github.GITHUB_CLIENT = None
    with patch.object(github, "Github") as GithubMock:
        client = github.get_client()
    GithubMock.assert_called_once_with("abides")
    assert client is GithubMock.return_value
    github.GITHUB_CLIENT = None
