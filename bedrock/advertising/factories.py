# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import factory
import wagtail_factories
from wagtail_link_block.blocks import LinkBlock

from bedrock.advertising import blocks, models
from bedrock.mozorg.blocks import navigation


class LinkBlockFactory(wagtail_factories.StructBlockFactory):
    link_to = "custom_url"
    new_window = False

    class Meta:
        model = LinkBlock


class AdvertisingHeroBlockFactory(wagtail_factories.StructBlockFactory):
    heading_text = wagtail_factories.CharBlockFactory
    primary_cta_text = wagtail_factories.CharBlockFactory
    primary_cta_link = factory.SubFactory(LinkBlockFactory)
    supporting_text = wagtail_factories.CharBlockFactory
    secondary_cta_text = wagtail_factories.CharBlockFactory
    secondary_cta_link = factory.SubFactory(LinkBlockFactory)

    class Meta:
        model = blocks.AdvertisingHeroBlock


class SectionHeaderBlockFactory(wagtail_factories.StructBlockFactory):
    heading_text = wagtail_factories.CharBlockFactory

    class Meta:
        model = blocks.SectionHeaderBlock


class SectionSettingsFactory(wagtail_factories.StructBlockFactory):
    anchor_id = wagtail_factories.CharBlockFactory
    has_top_divider = False
    display_on_dark_background = False

    class Meta:
        model = blocks.SectionSettings


class RowTextAndLinkBlockFactory(wagtail_factories.StructBlockFactory):
    text = wagtail_factories.CharBlockFactory
    link_text = wagtail_factories.CharBlockFactory
    link = factory.SubFactory(LinkBlockFactory)

    class Meta:
        model = blocks.RowTextAndLinkBlock


class SectionBlockFactory(wagtail_factories.StructBlockFactory):
    settings = factory.SubFactory(SectionSettingsFactory)
    header = factory.SubFactory(SectionHeaderBlockFactory)
    content = []
    call_to_action = []

    class Meta:
        model = blocks.SectionBlock


class NavigationLinkBlockFactory(wagtail_factories.StructBlockFactory):
    link_text = wagtail_factories.CharBlockFactory
    link = factory.SubFactory(LinkBlockFactory)
    has_button_appearance = False

    class Meta:
        model = navigation.NavigationLinkBlock


class AdvertisingIndexPageFactory(wagtail_factories.PageFactory):
    title = "Test Advertising Index Page"
    live = True
    slug = "advertising"

    hero = wagtail_factories.StreamFieldFactory(
        {
            "advertising_hero_block": factory.SubFactory(AdvertisingHeroBlockFactory),
        }
    )

    sections = wagtail_factories.StreamFieldFactory(
        {
            "section": factory.SubFactory(SectionBlockFactory),
        }
    )

    sub_navigation = wagtail_factories.StreamFieldFactory(
        {
            "link": factory.SubFactory(NavigationLinkBlockFactory),
        }
    )

    class Meta:
        model = models.AdvertisingIndexPage


class ListItemBlockFactory(wagtail_factories.StructBlockFactory):
    heading_text = wagtail_factories.CharBlockFactory
    supporting_text = wagtail_factories.CharBlockFactory

    class Meta:
        model = blocks.ListItemBlock


class ListBlockFactory(wagtail_factories.StructBlockFactory):
    list_items = wagtail_factories.ListBlockFactory(ListItemBlockFactory)

    class Meta:
        model = blocks.ListBlock


class TwoColumnDetailBlockFactory(wagtail_factories.StructBlockFactory):
    heading_text = wagtail_factories.CharBlockFactory
    subheading = wagtail_factories.CharBlockFactory
    second_column = []

    class Meta:
        model = blocks.TwoColumnDetailBlock


class AdvertisingTwoColumnSubpageFactory(wagtail_factories.PageFactory):
    title = "Test Two Column Subpage"
    live = True
    slug = "two-column-subpage"

    content = wagtail_factories.StreamFieldFactory(
        {
            "two_column_block": factory.SubFactory(TwoColumnDetailBlockFactory),
        }
    )

    class Meta:
        model = models.AdvertisingTwoColumnSubpage


class ContentSubpageFactory(wagtail_factories.PageFactory):
    title = "Test Content Subpage"
    live = True
    slug = "content-subpage"

    sections = wagtail_factories.StreamFieldFactory(
        {
            "section": factory.SubFactory(SectionBlockFactory),
        }
    )

    class Meta:
        model = models.ContentSubpage
