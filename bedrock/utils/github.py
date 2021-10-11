from django.conf import settings

from github import Github

GITHUB_CLIENT = None


def get_client():
    global GITHUB_CLIENT
    if GITHUB_CLIENT is not None:
        return GITHUB_CLIENT

    if settings.FLUENT_REPO_AUTH:
        auth_token = settings.FLUENT_REPO_AUTH.split(":")[1]
        GITHUB_CLIENT = Github(auth_token)

    return GITHUB_CLIENT
