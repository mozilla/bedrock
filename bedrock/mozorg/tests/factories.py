# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import factory
import wagtail_factories
from wagtail_link_block.blocks import LinkBlock

from bedrock.mozorg import models
from bedrock.mozorg.blocks import advertising, common, navigation


class LeadershipProfileSnippetFactory(factory.django.DjangoModelFactory):
    name = "Test Leadership Person"
    image = factory.SubFactory(wagtail_factories.ImageChooserBlockFactory)
    press_photos_link = "https://example.com/photos.zip"
    biography = "<p>Test biography text.</p>"

    class Meta:
        model = models.LeadershipProfileSnippet


class OrganizationLeadershipIndexPageFactory(wagtail_factories.PageFactory):
    title = "Test Organization Leadership Page"
    live = True
    slug = "organization-leadership"

    class Meta:
        model = models.OrganizationLeadershipIndexPage


class OrganizationLeadershipSubpageFactory(wagtail_factories.PageFactory):
    title = "Test Organization Leadership Subpage"
    live = True
    slug = "org-subpage"
    leadership_groups = []

    class Meta:
        model = models.OrganizationLeadershipSubpage


class ContactBannerSnippetFactory(factory.django.DjangoModelFactory):
    heading = "Contact Us"
    image = factory.SubFactory(wagtail_factories.ImageChooserBlockFactory)
    button_text = "Get in touch"
    button_link = "https://example.com/contact"

    class Meta:
        model = models.ContactBannerSnippet


class NotificationSnippetFactory(factory.django.DjangoModelFactory):
    notification_text = "<p>Follow Mozilla Ads for the latest advertising trends.</p>"
    linkedin_link = "https://www.example.com/test"
    tiktok_link = "https://www.example.com/test"
    spotify_link = "https://www.example.com/test"
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


class SpringboardItemBlockFactory(wagtail_factories.StructBlockFactory):
    url = "https://example.com/article"
    link_attributes = ""
    type = "Article"
    icon = "article"
    topic = "News"
    author = "Test Author"
    preview = "Test preview text"

    class Meta:
        model = common.SpringboardItemBlock


class SpringboardBlockSettingsFactory(wagtail_factories.StructBlockFactory):
    anchor_id = ""
    background_color = ""

    class Meta:
        model = common.SpringboardBlockSettings


class SpringboardBlockFactory(wagtail_factories.StructBlockFactory):
    settings = factory.SubFactory(SpringboardBlockSettingsFactory)
    heading = "Latest Resources"
    column_one = "Type"
    column_two = "Author"
    column_three = "Topic"
    column_four = "Preview"
    springboard_items = wagtail_factories.ListBlockFactory(SpringboardItemBlockFactory)

    class Meta:
        model = common.SpringboardBlock


class DonateBlockSettingsFactory(wagtail_factories.StructBlockFactory):
    background_color = "gray"
    anchor_id = ""

    class Meta:
        model = common.DonateBlockSettings


class DonateBlockFactory(wagtail_factories.StructBlockFactory):
    settings = factory.SubFactory(DonateBlockSettingsFactory)
    heading = "Support Mozilla"
    body = "<p>Help us build a better internet.</p>"
    image = factory.SubFactory(wagtail_factories.ImageChooserBlockFactory)
    image_alt = ""
    cta_text = "Donate"
    cta_link = factory.SubFactory(LinkBlockFactory)

    class Meta:
        model = common.DonateBlock


class ShowcaseBlockSettingsFactory(wagtail_factories.StructBlockFactory):
    background_color = ""
    anchor_id = ""

    class Meta:
        model = common.ShowcaseBlockSettings


class ShowcaseBlockFactory(wagtail_factories.StructBlockFactory):
    settings = factory.SubFactory(ShowcaseBlockSettingsFactory)
    heading = "State of Mozilla"
    body = "<p>Read our annual report.</p>"
    image = factory.SubFactory(wagtail_factories.ImageChooserBlockFactory)
    image_alt = ""
    sub_heading = "Supporting a healthy internet"
    cta_text = "Read the report"
    cta_link = factory.SubFactory(LinkBlockFactory)

    class Meta:
        model = common.ShowcaseBlock


class HomePageFactory(wagtail_factories.PageFactory):
    title = "Test Home Page"
    live = True
    slug = "home"

    content = wagtail_factories.StreamFieldFactory(
        {
            "donate_block": factory.SubFactory(DonateBlockFactory),
            "springboard_block": factory.SubFactory(SpringboardBlockFactory),
            "showcase_block": factory.SubFactory(ShowcaseBlockFactory),
        }
    )

    class Meta:
        model = models.HomePage


class ShowcaseGalleryImageBlockFactory(wagtail_factories.StructBlockFactory):
    image = wagtail_factories.ImageChooserBlockFactory
    image_alt = ""

    class Meta:
        model = common.ShowcaseGalleryImageBlock


class ShowcaseGalleryBlockSettingsFactory(wagtail_factories.StructBlockFactory):
    anchor_id = ""
    background_color = ""

    class Meta:
        model = common.ShowcaseGalleryBlockSettings


class ShowcaseGalleryBlockFactory(wagtail_factories.StructBlockFactory):
    settings = factory.SubFactory(ShowcaseGalleryBlockSettingsFactory)
    heading = "Working at Mozilla"
    tiles = wagtail_factories.ListBlockFactory(ShowcaseGalleryImageBlockFactory)
    body = "Join a team that believes the internet is for everyone."
    cta_text = "See open roles"
    cta_link = factory.SubFactory(LinkBlockFactory)

    class Meta:
        model = common.ShowcaseGalleryBlock


class AboutUsPageFactory(wagtail_factories.PageFactory):
    title = "Test About Us Page"
    live = True
    slug = "about-us"

    content = wagtail_factories.StreamFieldFactory(
        {
            "showcase_gallery_block": factory.SubFactory(ShowcaseGalleryBlockFactory),
        }
    )

    class Meta:
        model = models.AboutUsPage
