from __future__ import unicode_literals

import pytest
from django.test import override_settings
from mock import call, patch, DEFAULT

from bedrock.utils import git


@patch.object(git, 'os')
@patch.object(git, 'check_output')
def test_git(co_mock, os_mock):
    os_mock.getcwd.return_value = 'olddir'
    co_mock.return_value = 'dude'
    g = git.GitRepo('new_repo')
    output = g.git('checkout', 'maude')
    co_mock.assert_called_with((git.GIT, 'checkout', 'maude'), stderr=git.STDOUT)
    os_mock.chdir.assert_has_calls([
        call(g.path_str),
        call('olddir'),
    ])
    assert output == 'dude'


def test_git_current_hash():
    g = git.GitRepo('.')
    with patch.object(g, 'git') as git_mock:
        g.current_hash

    git_mock.assert_called_with('rev-parse', 'HEAD')


def test_git_full_branch_name():
    g = git.GitRepo('.', branch_name='dude', remote_name='the')
    assert g.full_branch_name == 'the/dude'


def test_git_remote_names():
    g = git.GitRepo('.')
    with patch.object(g, 'git') as git_mock:
        git_mock.return_value = 'dude\nwalter'
        assert g.remote_names == ['dude', 'walter']


def test_git_has_remote():
    g = git.GitRepo('.', 'https://example.com', remote_name='walter')
    with patch.object(g, 'git') as git_mock:
        git_mock.return_value = 'dude\nwalter'
        assert g.has_remote()
        g.remote_name = 'donnie'
        assert not g.has_remote()


def test_git_add_remote():
    g = git.GitRepo('.')
    with pytest.raises(RuntimeError):
        g.add_remote()

    g = git.GitRepo('.', 'https://example.com', remote_name='dude')
    with patch.object(g, 'git') as git_mock:
        g.add_remote()

    git_mock.assert_called_with('remote', 'add', 'dude', 'https://example.com')


@override_settings(DEV=True)
def test_git_clone():
    g = git.GitRepo('.')
    with pytest.raises(RuntimeError):
        g.clone()

    g = git.GitRepo('.', 'https://example.com')
    with patch.multiple(g, git=DEFAULT, path=DEFAULT) as git_mock:
        g.clone()

    git_mock['path'].mkdir.assert_called_with(parents=True, exist_ok=True)
    git_mock['git'].assert_called_with('clone', '--origin', 'bedrock-dev', '--depth', '1',
                                       'https://example.com', '.')


@patch.object(git, 'rmtree')
def test_git_update(rmtree_mock):
    g = git.GitRepo('.', 'https://example.com')
    with patch.multiple(g, clone=DEFAULT, path=DEFAULT,
                        diff=DEFAULT, pull=DEFAULT) as git_mock:
        git_mock['path'].is_dir.return_value = False
        g.update()
        assert git_mock['clone'].called
        git_mock['pull'].assert_not_called()

    rmtree_mock.reset_mock()
    with patch.multiple(g, clone=DEFAULT, path=DEFAULT,
                        diff=DEFAULT, pull=DEFAULT) as git_mock:
        git_mock['path'].is_dir.return_value = True
        git_mock['path'].joinpath().is_dir.return_value = False
        g.update()
        rmtree_mock.assert_called_with(g.path_str, ignore_errors=True)
        assert git_mock['clone'].called
        git_mock['pull'].assert_not_called()

    rmtree_mock.reset_mock()
    with patch.multiple(g, clone=DEFAULT, path=DEFAULT,
                        diff=DEFAULT, pull=DEFAULT) as git_mock:
        git_mock['path'].is_dir.return_value = True
        git_mock['path'].joinpath().is_dir.return_value = True
        val = g.update()
        rmtree_mock.assert_not_called()
        git_mock['clone'].assert_not_called()
        assert git_mock['pull'].called
        assert git_mock['diff'].called
        assert val == git_mock['diff'].return_value
