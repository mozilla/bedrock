# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import factory
import wagtail_factories
from wagtail_link_block.blocks import LinkBlock

from bedrock.mozorg import models
from bedrock.mozorg.blocks import advertising, leadership


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


class LinkBlockFactory(wagtail_factories.StructBlockFactory):
    link_to = "custom_url"
    custom_url = wagtail_factories.CharBlockFactory
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


class AdvertisingIndexPageFactory(wagtail_factories.PageFactory):
    title = "Test Advertising Index Page"
    live = True
    slug = "advertising"

    content = wagtail_factories.StreamFieldFactory(
        {
            "advertising_hero_block": factory.SubFactory(AdvertisingHeroBlockFactory),
            "section_header_block": factory.SubFactory(SectionHeaderBlockFactory),
        }
    )

    notifications = wagtail_factories.StreamFieldFactory(
        {
            "notification_block": factory.SubFactory(NotificationBlockFactory),
        }
    )

    class Meta:
        model = models.AdvertisingIndexPage
