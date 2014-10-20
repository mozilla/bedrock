import cronjobs

from .utils import (delete_old_articles, update_from_category_feeds,
                    update_on_homepage)


@cronjobs.register
def update_openstandard_on_homepage():
    update_on_homepage()


@cronjobs.register
def update_openstandard_feeds():
    update_from_category_feeds()


@cronjobs.register
def delete_old_openstandard_articles():
    delete_old_articles()
