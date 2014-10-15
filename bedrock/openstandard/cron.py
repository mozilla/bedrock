import cronjobs

from .utils import (
    categorized_articles, delete_old_articles, update_from_category_feeds)


@cronjobs.register
def update_openstandard_cache():
    categorized_articles(force_cache_refresh=True)


@cronjobs.register
def update_openstandard():
    update_from_category_feeds()
    delete_old_articles()
