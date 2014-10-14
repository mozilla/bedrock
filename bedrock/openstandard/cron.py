import cronjobs

from .utils import delete_old_articles, update_from_category_feeds


@cronjobs.register
def update_openstandard():
    update_from_category_feeds()
    delete_old_articles()
