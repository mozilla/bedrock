# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import date

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils import feedgenerator

from bedrock.careers.models import Position


class LatestPositionsFeed(Feed):
    feed_type = feedgenerator.Rss201rev2Feed
    title = "Current Mozilla job openings"
    description = "The current list of job openings, available internships and contract opportunities at Mozilla."
    feed_copyright = (
        "Portions of this content are ©1998–%s by individual "
        "mozilla.org contributors. Content available under a "
        "Creative Commons license." % date.today().year
    )

    def link(self):
        return reverse("careers.listings")

    def feed_url(self):
        return reverse("careers.feed")

    def categories(self):
        return Position.categories()

    def items(self):
        return Position.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_pubdate(self, item):
        return item.updated_at

    def item_categories(self, item):
        categories = []
        categories.append(item.department)
        categories += item.location_list
        if "Remote" in item.location_list:
            categories.append("Worldwide")
        return categories
