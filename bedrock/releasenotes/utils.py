from django.conf import settings
from django.core.cache import caches

from memoize import Memoizer

from bedrock.utils.git import GitRepo


def get_data_version():
    """Add the git ref from the repo to the cache keys.

    This will ensure that the cache is invalidated when the repo is updated.
    """
    repo = GitRepo(settings.RELEASE_NOTES_PATH,
                   settings.RELEASE_NOTES_REPO,
                   branch_name=settings.RELEASE_NOTES_BRANCH)
    git_ref = repo.get_db_latest()
    if git_ref is None:
        git_ref = 'default'

    return git_ref


class ReleaseMemoizer(Memoizer):
    """A memoizer class that uses the git hash as the version"""
    def __init__(self, version_timeout=300):
        self.version_timeout = version_timeout
        return super(ReleaseMemoizer, self).__init__(cache=caches['release-notes'])

    def _memoize_make_version_hash(self):
        return get_data_version()

    def _memoize_version(self, f, args=None, reset=False, delete=False, timeout=None):
        """Use a shorter timeout for the version so that we can refresh based on git hash"""
        return super(ReleaseMemoizer, self)._memoize_version(f, args, reset, delete, self.version_timeout)


memoizer = ReleaseMemoizer()
memoize = memoizer.memoize
