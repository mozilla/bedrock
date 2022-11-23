# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import date
from itertools import groupby

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils import feedgenerator

from bedrock.careers.models import Position


class LatestPositionsFeed(Feed):
    feed_type = feedgenerator.Rss201rev2Feed
    title = "Current Mozilla job openings"
    description = "The current list of job openings, available internships and contract opportunities at Mozilla."
    feed_copyright = (
        f"Portions of this content are ©1998–{date.today().year} by individual "
        "mozilla.org contributors. Content available under a Creative Commons license."
    )

    def link(self):
        return reverse("careers.listings")

    def feed_url(self):
        return reverse("careers.feed")

    def categories(self):
        return Position.categories()

    def items(self):
        return [list(g)[0] for k, g in groupby(Position.objects.all().order_by("internal_job_id", "job_id"), key=lambda p: p.internal_job_id)]

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
