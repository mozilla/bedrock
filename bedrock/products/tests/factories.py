# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import factory
import wagtail_factories

from bedrock.products.models import VPNCallToActionSnippet, VPNResourceCenterDetailPage, VPNResourceCenterIndexPage


class VPNCallToActionSnippetFactory(factory.BaseDictFactory):
    heading = wagtail_factories.CharBlockFactory
    image = factory.SubFactory(wagtail_factories.ImageChooserBlockFactory)

    class Meta:
        model = VPNCallToActionSnippet


class VPNResourceCenterIndexPageFactory(wagtail_factories.PageFactory):
    title = "Test VPN Resource Center Index Page Title"
    live = True
    slug = "test"

    sub_title = wagtail_factories.CharBlockFactory

    class Meta:
        model = VPNResourceCenterIndexPage


class VPNResourceCenterDetailPageFactory(wagtail_factories.PageFactory):
    title = "Test VPN Resource Center Detail Page Title"
    live = True

    image = factory.SubFactory(wagtail_factories.ImageChooserBlockFactory)
    desc = wagtail_factories.CharBlockFactory
    content = wagtail_factories.CharBlockFactory

    class Meta:
        model = VPNResourceCenterDetailPage
