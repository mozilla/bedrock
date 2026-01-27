# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import factory
import wagtail_factories
from wagtail_link_block.blocks import LinkBlock

from bedrock.mozorg import models
from bedrock.mozorg.blocks import common, leadership


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


class HomePageFactory(wagtail_factories.PageFactory):
    title = "Test Home Page"
    live = True
    slug = "home"

    content = wagtail_factories.StreamFieldFactory(
        {
            "donate_block": factory.SubFactory(DonateBlockFactory),
        }
    )

    class Meta:
        model = models.HomePage
