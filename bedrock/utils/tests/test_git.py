# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import base64
from unittest.mock import DEFAULT, call, patch

from django.test import override_settings

import pytest

from bedrock.utils import git


@patch.object(git, "os")
@patch.object(git, "check_output")
def test_git(co_mock, os_mock):
    os_mock.getcwd.return_value = "olddir"
    co_mock.return_value = "dude"
    g = git.GitRepo("new_repo")
    output = g.git("checkout", "maude")
    co_mock.assert_called_with((git.GIT, "checkout", "maude"), stderr=git.STDOUT)
    os_mock.chdir.assert_has_calls(
        [
            call(g.path_str),
            call("olddir"),
        ]
    )
    assert output == "dude"


def test_git_current_hash():
    g = git.GitRepo(".")
    with patch.object(g, "git") as git_mock:
        g.current_hash

    git_mock.assert_called_with("rev-parse", "HEAD")


@pytest.mark.django_db
def test_git_db_latest():
    g = git.GitRepo(".", "https://example.com/repo.git", "master")
    assert g.db_latest_key == "33ff0192f06306345030004c92533017b466e16489d4c762eab69ad8142ddae4"
    assert g.get_db_latest() is None
    g.set_db_latest("deadbeef")
    assert g.get_db_latest() == "deadbeef"
    g.set_db_latest("deadbeef1234")
    assert g.get_db_latest() == "deadbeef1234"


@pytest.mark.django_db
def test_git_db_latest_methods():
    g = git.GitRepo(".", "https://example.com/repo.git", "master", "dude")
    g.set_db_latest("deadbeef")
    assert g.get_db_latest() == "deadbeef"
    gobj = git.GitRepoState.objects.get(repo_id=g.db_latest_key)
    assert gobj.repo_name == "dude"
    assert gobj.commit_url == "https://example.com/repo/commit/deadbeef"


@pytest.mark.django_db
def test_git_db_latest_auto_name():
    # name should be the last bit of the path, and the repo URL can deal with a trailing slash
    g = git.GitRepo("hollywood-star-lanes/the-dude", "https://example.com/repo/", "master")
    g.set_db_latest("deadbeef")
    assert g.get_db_latest() == "deadbeef"
    gobj = git.GitRepoState.objects.get(repo_id=g.db_latest_key)
    assert gobj.repo_name == "the-dude"
    assert gobj.commit_url == "https://example.com/repo/commit/deadbeef"


@pytest.mark.parametrize(
    "repo_url,expected",
    [
        ("https://github.com/mozilla/foundation-security-advisories-private", True),
        ("https://github.com/mozilla/bedrock", False),
        ("", False),
    ],
)
def test_git_repo_state_is_private(repo_url, expected):
    state = git.GitRepoState(repo_url=repo_url, latest_ref="deadbeef")
    assert state.is_private is expected


@override_settings(DEV=True)
def test_git_clone():
    g = git.GitRepo(".")
    with pytest.raises(RuntimeError):
        g.clone()

    g = git.GitRepo(".", "https://example.com")
    with patch.multiple(g, git=DEFAULT, path=DEFAULT) as git_mock:
        g.clone()

    git_mock["path"].mkdir.assert_called_with(parents=True, exist_ok=True)
    git_mock["git"].assert_called_with("clone", "--depth", "1", "--branch", "main", "https://example.com", ".")


def test_git_split_auth():
    g = git.GitRepo(".")
    assert g._split_auth() == (None, None)

    g.auth = "bare-token"
    assert g._split_auth() == ("x-access-token", "bare-token")

    g.auth = "testserviceaccount:supersecret"
    assert g._split_auth() == ("testserviceaccount", "supersecret")

    # missing username falls back to the default
    g.auth = ":supersecret"
    assert g._split_auth() == ("x-access-token", "supersecret")


def test_git_auth_env_no_auth_yields_none():
    g = git.GitRepo(".")
    with g._auth_env() as env:
        assert env is None


def test_git_auth_env_with_auth():
    g = git.GitRepo(".", "https://github.com/mozilla/repo.git", auth="testserviceaccount:supersecret")
    with g._auth_env() as env:
        assert env is not None
        assert env["GIT_CONFIG_COUNT"] == "1"
        # Config key is scoped to the remote host so the Authorization header
        # won't follow off-host redirects or LFS fetches.
        assert env["GIT_CONFIG_KEY_0"] == "http.https://github.com/.extraheader"
        assert env["GIT_TERMINAL_PROMPT"] == "0"

        header = env["GIT_CONFIG_VALUE_0"]
        assert header.startswith("AUTHORIZATION: Basic ")
        decoded = base64.b64decode(header.removeprefix("AUTHORIZATION: Basic ")).decode("ascii")
        assert decoded == "testserviceaccount:supersecret"


def test_git_auth_env_falls_back_to_global_key_for_non_https_remote():
    """If we somehow have auth but no usable HTTPS remote, fall back to the
    unscoped `http.extraheader` rather than producing a malformed key."""
    g = git.GitRepo(".", "git@github.com:foo/bar.git", auth="user:tok")
    with g._auth_env() as env:
        assert env["GIT_CONFIG_KEY_0"] == "http.extraheader"

    g = git.GitRepo(".", auth="user:tok")  # no remote_url at all
    with g._auth_env() as env:
        assert env["GIT_CONFIG_KEY_0"] == "http.extraheader"


def test_git_auth_env_bare_token_uses_default_username():
    g = git.GitRepo(".", auth="bare-token")
    with g._auth_env() as env:
        decoded = base64.b64decode(env["GIT_CONFIG_VALUE_0"].removeprefix("AUTHORIZATION: Basic ")).decode("ascii")
        assert decoded == "x-access-token:bare-token"


def test_git_clone_with_auth_keeps_token_out_of_argv_and_url():
    g = git.GitRepo(".", "https://example.com/repo.git", auth="testserviceaccount:supersecret")
    with patch.multiple(g, git=DEFAULT, path=DEFAULT) as mocks:
        g.clone()

    call_args = mocks["git"].call_args
    # URL is plain — no username, no token.
    assert call_args.args == (
        "clone",
        "--depth",
        "1",
        "--branch",
        "main",
        "https://example.com/repo.git",
        ".",
    )
    # Token must not appear in any positional arg.
    for a in call_args.args:
        assert "supersecret" not in str(a)
    # Auth travels via env vars setting host-scoped http.extraheader.
    assert "env" in call_args.kwargs
    env = call_args.kwargs["env"]
    assert env["GIT_CONFIG_KEY_0"] == "http.https://example.com/.extraheader"
    assert env["GIT_TERMINAL_PROMPT"] == "0"


def test_git_pull_with_auth_only_authenticates_fetch():
    g = git.GitRepo(".", "https://example.com/repo.git", auth="testserviceaccount:supersecret")
    with patch.object(g, "git") as git_mock:
        git_mock.return_value = "deadbeef"
        g.pull()

    fetch_calls = [c for c in git_mock.call_args_list if c.args and c.args[0] == "fetch"]
    assert len(fetch_calls) == 1
    fetch_call = fetch_calls[0]
    # Token never appears in argv.
    for a in fetch_call.args:
        assert "supersecret" not in str(a)
    # URL is plain.
    assert "https://example.com/repo.git" in fetch_call.args
    # Auth env is set on the fetch call (host-scoped).
    assert fetch_call.kwargs["env"]["GIT_CONFIG_KEY_0"] == "http.https://example.com/.extraheader"

    # The checkout step does not need auth.
    checkout_calls = [c for c in git_mock.call_args_list if c.args and c.args[0] == "checkout"]
    assert len(checkout_calls) == 1
    assert checkout_calls[0].kwargs == {}


def test_git_call_passes_env_when_provided():
    """The base git() helper merges the supplied env on top of os.environ."""
    with patch.object(git, "os") as os_mock, patch.object(git, "check_output") as co_mock:
        os_mock.getcwd.return_value = "olddir"
        os_mock.environ = {"PATH": "/usr/bin", "EXISTING": "keep"}
        co_mock.return_value = "ok"
        g = git.GitRepo("new_repo")
        g.git("fetch", "origin", env={"GIT_ASKPASS": "/tmp/x", "EXISTING": "override"})

    _, kwargs = co_mock.call_args
    assert kwargs["stderr"] == git.STDOUT
    assert kwargs["env"] == {
        "PATH": "/usr/bin",
        "EXISTING": "override",
        "GIT_ASKPASS": "/tmp/x",
    }


@patch.object(git, "rmtree")
def test_git_update(rmtree_mock):
    g = git.GitRepo(".", "https://example.com")
    with patch.multiple(g, clone=DEFAULT, path=DEFAULT, diff=DEFAULT, pull=DEFAULT) as git_mock:
        git_mock["path"].is_dir.return_value = False
        g.update()
        assert git_mock["clone"].called
        git_mock["pull"].assert_not_called()

    rmtree_mock.reset_mock()
    with patch.multiple(g, clone=DEFAULT, path=DEFAULT, diff=DEFAULT, pull=DEFAULT) as git_mock:
        git_mock["path"].is_dir.return_value = True
        git_mock["path"].joinpath().is_dir.return_value = False
        g.update()
        rmtree_mock.assert_called_with(g.path_str, ignore_errors=True)
        assert git_mock["clone"].called
        git_mock["pull"].assert_not_called()

    rmtree_mock.reset_mock()
    with patch.multiple(g, clone=DEFAULT, path=DEFAULT, diff=DEFAULT, pull=DEFAULT) as git_mock:
        git_mock["path"].is_dir.return_value = True
        git_mock["path"].joinpath().is_dir.return_value = True
        val = g.update()
        rmtree_mock.assert_not_called()
        git_mock["clone"].assert_not_called()
        assert git_mock["pull"].called
        assert val == git_mock["pull"].return_value


def test_git_diff():
    g = git.GitRepo(".", "https://example.com")
    with patch.object(g, "git") as git_mock:
        git_mock.return_value = GIT_DIFF_TEST_DATA
        modified, deleted = g.diff("abcd", "ef12")
        git_mock.assert_called_with("diff", "--name-status", "abcd", "ef12")

    assert modified == {
        "media/css/mozorg/home/home.scss",
        "lib/l10n_utils/tests/test_template.py",
        "docs/mozilla-traffic-cop.rst",
        "lib/l10n_utils/management/commands/l10n_update.py",
        "media/css/mozorg/home/home-variant.scss",
        "media/css/pebbles/base/_elements.scss",
        "media/css/newsletter/newsletter-mozilla.scss",
        "media/css/pebbles/components/_buttons-download.scss",
        "media/css/mozorg/technology.less",
        "lib/l10n_utils/tests/test_commands.py",
        "media/css/pebbles/base/elements/_document.scss",
        "media/css/pebbles/base/elements/_typography.scss",
        "media/css/pebbles/base/elements/_links.scss",
        "docs/javascript-libs.rst",
        "docker/run.sh",
        "media/css/pebbles/components/_masthead.scss",
        "media/css/pebbles/components/_footer.scss",
        "media/css/pebbles/components/_modal.scss",
        "media/css/pebbles/base/oldIE.scss",
        "etc/supervisor_available/cron_db.conf",
        "media/css/mozorg/leadership.scss",
        "media/css/pebbles/components/_buttons.scss",
        "media/css/pebbles/base/elements/_lists.scss",
        "etc/supervisor_available/cron_l10n.conf",
        "media/css/pebbles/base/elements/_reset.scss",
        "media/css/pebbles/base/elements/_tables.scss",
        "media/css/pebbles/components/_sections.scss",
        "media/css/firefox/firstrun/ravioli.less",
        "media/css/pebbles/elements/forms.less",
        "media/css/pebbles/base/elements/_forms.scss",
        "media/css/pebbles/components/_base-button.scss",
        "media/css/newsletter/newsletter-firefox.scss",
    }
    assert deleted == {
        "media/css/mozorg/leadership.less",
        "media/css/pebbles/base.less",
        "media/css/pebbles/reset.less",
        "media/css/newsletter/newsletter-mozilla.less",
        "media/css/pebbles/components/footer.less",
        "media/css/pebbles/components/modal.less",
        "media/css/mozorg/home/home.less",
        "etc/supervisor_available/cron.conf",
        "media/css/newsletter/newsletter-firefox.less",
        "media/css/pebbles/oldIE.less",
    }


# real output from git against the bedrock repo
GIT_DIFF_TEST_DATA = """\
A       docker/run.sh
M       docs/javascript-libs.rst
A       docs/mozilla-traffic-cop.rst
R072    etc/supervisor_available/cron.conf      etc/supervisor_available/cron_db.conf
A       etc/supervisor_available/cron_l10n.conf
M       lib/l10n_utils/management/commands/l10n_update.py
M       lib/l10n_utils/tests/test_commands.py
M       lib/l10n_utils/tests/test_template.py
A       media/css/firefox/firstrun/ravioli.less
A       media/css/mozorg/home/home-variant.scss
R059    media/css/mozorg/home/home.less media/css/mozorg/home/home.scss
R081    media/css/mozorg/leadership.less        media/css/mozorg/leadership.scss
A       media/css/mozorg/technology.less
R059    media/css/newsletter/newsletter-firefox.less    media/css/newsletter/newsletter-firefox.scss
R063    media/css/newsletter/newsletter-mozilla.less    media/css/newsletter/newsletter-mozilla.scss
D       media/css/pebbles/base.less
A       media/css/pebbles/base/_elements.scss
A       media/css/pebbles/base/elements/_document.scss
C080    media/css/pebbles/elements/forms.less   media/css/pebbles/base/elements/_forms.scss
A       media/css/pebbles/base/elements/_links.scss
A       media/css/pebbles/base/elements/_lists.scss
R100    media/css/pebbles/reset.less    media/css/pebbles/base/elements/_reset.scss
A       media/css/pebbles/base/elements/_tables.scss
A       media/css/pebbles/base/elements/_typography.scss
R064    media/css/pebbles/oldIE.less    media/css/pebbles/base/oldIE.scss
A       media/css/pebbles/components/_base-button.scss
A       media/css/pebbles/components/_buttons-download.scss
A       media/css/pebbles/components/_buttons.scss
R067    media/css/pebbles/components/footer.less        media/css/pebbles/components/_footer.scss
A       media/css/pebbles/components/_masthead.scss
R080    media/css/pebbles/components/modal.less media/css/pebbles/components/_modal.scss
A       media/css/pebbles/components/_sections.scss
D       media/css/pebbles/base.less
"""
