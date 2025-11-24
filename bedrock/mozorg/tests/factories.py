# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import factory
import wagtail_factories
from wagtail_link_block.blocks import LinkBlock

from bedrock.mozorg import models
from bedrock.mozorg.blocks import advertising, leadership, navigation


class LeadershipHeadshotBlockFactory(wagtail_factories.StructBlockFactory):
    image = factory.SubFactory(wagtail_factories.ImageChooserBlockFactory)
    image_alt_text = wagtail_factories.CharBlockFactory
    photos_link = wagtail_factories.CharBlockFactory

    class Meta:
        model = leadership.LeadershipHeadshotBlock


class LeadershipExternalLinkBlockFactory(wagtail_factories.StructBlockFactory):
    url = wagtail_factories.CharBlockFactory
    type = wagtail_factories.CharBlockFactory
    text = wagtail_factories.CharBlockFactory

    class Meta:
        model = leadership.LeadershipExternalLinkBlock


class LeadershipBioBlockFactory(wagtail_factories.StructBlockFactory):
    name = wagtail_factories.CharBlockFactory
    headshot = factory.SubFactory(LeadershipHeadshotBlockFactory)
    job_title = wagtail_factories.CharBlockFactory
    biography = wagtail_factories.CharBlockFactory
    external_links = wagtail_factories.ListBlockFactory(LeadershipExternalLinkBlockFactory)

    class Meta:
        model = leadership.LeadershipBioBlock


class LeadershipGroupBlockFactory(wagtail_factories.StructBlockFactory):
    title = wagtail_factories.CharBlockFactory
    leaders = wagtail_factories.ListBlockFactory(LeadershipBioBlockFactory)

    class Meta:
        model = leadership.LeadershipGroupBlock


class LeadershipSectionBlockFactory(wagtail_factories.StructBlockFactory):
    title = wagtail_factories.CharBlockFactory
    leadership_group = wagtail_factories.ListBlockFactory(LeadershipGroupBlockFactory)

    class Meta:
        model = leadership.LeadershipSectionBlock


class LeadershipPageFactory(wagtail_factories.PageFactory):
    title = "Test Leadership Page"
    live = True
    slug = "leadership"

    leadership_sections = wagtail_factories.StreamFieldFactory({"section": factory.SubFactory(LeadershipSectionBlockFactory)})

    class Meta:
        model = models.LeadershipPage


class ContactBannerSnippetFactory(factory.django.DjangoModelFactory):
    heading = "Contact Us"
    image = factory.SubFactory(wagtail_factories.ImageChooserBlockFactory)
    button_text = "Get in touch"
    button_link = "https://example.com/contact"

    class Meta:
        model = models.ContactBannerSnippet


class NotificationSnippetFactory(factory.django.DjangoModelFactory):
    notification_text = wagtail_factories.CharBlockFactory
    linkedin_link = "https://www.example.com/test"
    tiktok_link = "https://www.example.com/test"
    spotify_link = "https://www.example.com/test"
    twitter_link = "https://www.example.com/test"
    bluesky_link = "https://www.example.com/test"
    instagram_link = "https://www.example.com/test"
    youtube_link = "https://www.example.com/test"

    class Meta:
        model = models.NotificationSnippet


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
        model = advertising.AdvertisingHeroBlock


class SectionHeaderBlockFactory(wagtail_factories.StructBlockFactory):
    heading_text = wagtail_factories.CharBlockFactory

    class Meta:
        model = advertising.SectionHeaderBlock


class SectionSettingsFactory(wagtail_factories.StructBlockFactory):
    anchor_id = wagtail_factories.CharBlockFactory
    has_top_divider = False
    display_on_dark_background = False

    class Meta:
        model = advertising.SectionSettings


class RowTextAndLinkBlockFactory(wagtail_factories.StructBlockFactory):
    text = wagtail_factories.CharBlockFactory
    link_text = wagtail_factories.CharBlockFactory
    link = factory.SubFactory(LinkBlockFactory)

    class Meta:
        model = advertising.RowTextAndLinkBlock


class SectionBlockFactory(wagtail_factories.StructBlockFactory):
    settings = factory.SubFactory(SectionSettingsFactory)
    header = factory.SubFactory(SectionHeaderBlockFactory)
    content = []
    call_to_action = []

    class Meta:
        model = advertising.SectionBlock


class LinkWithIconFactory(wagtail_factories.StructBlockFactory):
    icon = wagtail_factories.CharBlockFactory
    link = factory.SubFactory(LinkBlockFactory)

    class Meta:
        model = advertising.LinkWithIcon


class NotificationBlockFactory(wagtail_factories.StructBlockFactory):
    notification_text = wagtail_factories.CharBlockFactory
    links = []

    class Meta:
        model = advertising.NotificationBlock


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
        model = advertising.ListItemBlock


class ListBlockFactory(wagtail_factories.StructBlockFactory):
    list_items = wagtail_factories.ListBlockFactory(ListItemBlockFactory)

    class Meta:
        model = advertising.ListBlock


class TwoColumnDetailBlockFactory(wagtail_factories.StructBlockFactory):
    heading_text = wagtail_factories.CharBlockFactory
    subheading = wagtail_factories.CharBlockFactory
    second_column = []

    class Meta:
        model = advertising.TwoColumnDetailBlock


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
