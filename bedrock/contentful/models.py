# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import models
from django.db.models.query_utils import Q
from django.utils.timezone import now

from django_extensions.db.fields.json import JSONField

from bedrock.contentful.constants import CONTENT_TYPE_CONNECT_HOMEPAGE


class ContentfulEntryManager(models.Manager):
    """
    The key distinction here is that get_page_* returns a JSONDict of page data, while
    get_entry_* and get_entries_* returns a QuerySet of ContentfulEntry records.
    """

    def get_page_by_id(self, content_id, locale=None):
        kwargs = {"contentful_id": content_id}
        if locale:
            kwargs["locale"] = locale

        return self.get(**kwargs).data

    def get_entry_by_slug(self, slug, locale, content_type, classification=None):
        kwargs = dict(
            slug=slug,
            locale=locale,
            content_type=content_type,
        )
        if classification:
            kwargs["classification"] = classification
        return self.get(**kwargs)

    def get_page_by_slug(self, slug, locale, content_type, classification=None):
        # Thin wrapper that gets back only the JSON data
        return self.get_entry_by_slug(
            slug,
            locale,
            content_type,
            classification,
        ).data

    def get_entries_by_type(
        self,
        content_type,
        locale,
        classification=None,
        order_by="last_modified",
    ):
        """Get multiple appropriate ContentfulEntry records, not just the JSON data.

        Args:
            content_type (str): the Contentful content type
            locale (str): eg 'fr', 'en-US'
            classification ([str], optional): specific type of content, used when have
                a single content_type used for different areas of the site. Defaults to None.
            order_by (str, optional): Sorting key for the queryset. Defaults to "last_modified".

        Returns:
            QuerySet[ContentfulEntry]: the main ContenfulEntry models, not just their JSON data
        """

        kwargs = dict(
            content_type=content_type,
            locale=locale,
        )
        if classification:
            kwargs["classification"] = classification

        return self.filter(**kwargs).order_by(order_by)

    def get_homepage(self, locale):
        return self.get(
            content_type=CONTENT_TYPE_CONNECT_HOMEPAGE,
            locale=locale,
        ).data


class ContentfulEntry(models.Model):
    contentful_id = models.CharField(max_length=20)
    content_type = models.CharField(max_length=20)
    locale = models.CharField(max_length=5)
    last_modified = models.DateTimeField(default=now)
    url_base = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=255, blank=True)
    data_hash = models.CharField(max_length=64)
    data = JSONField()
    # Fields we may need to query by
    classification = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Some pages may have custom fields on them, distinct from their content type - eg: pagePageResourceCenter has a 'Product' field",
    )
    category = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Some pages may have a category",
    )
    tags = JSONField(
        blank=True,
        help_text="Some pages may have tags",
    )

    objects = ContentfulEntryManager()

    class Meta:
        unique_together = ["contentful_id", "locale"]

    def __str__(self) -> str:
        return f"ContentfulEntry {self.content_type}:{self.contentful_id}[{self.locale}]"

    def get_related_entries(self, order_by="last_modified"):
        """Find ContentfulEntry records that:
        * are for the same content_type
        * are for the same classification
        * share at least one tag with `self`

        Returns:
            QuerySet[ContentfulEntry]
        """

        if not self.tags:
            return ContentfulEntry.objects.none()

        _base_qs = ContentfulEntry.objects.filter(
            locale=self.locale,
            content_type=self.content_type,
            classification=self.classification,  # eg same Product/project/area of the site
        ).exclude(
            id=self.id,
        )

        # Tags are stored in a JSONField, but we can query it as text by quoting them
        q_obj = Q()
        for _tag in self.tags:
            q_obj |= Q(tags__contains=f'"{_tag}"')
        return _base_qs.filter(q_obj).order_by(order_by).distinct()
