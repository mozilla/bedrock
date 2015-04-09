# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings

from bedrock.mozorg.hierarchy import PageNode, PageRoot
from bedrock.mozorg.util import page


all_children = [
    PageNode('Home', template='styleguide/home.html'),
    PageNode('Identity', path='identity', children=(
        PageNode('Mozilla', path='mozilla', children=(
            PageNode('Branding', path='branding', template='styleguide/identity/mozilla-branding.html'),
            PageNode('Color', path='color', template='styleguide/identity/mozilla-color.html'),
        )),
        PageNode('Firefox Family', path='firefox-family', children=(
            PageNode('Overview', path='overview', template='styleguide/identity/firefox-family-overview.html'),
            PageNode('Platform', path='platform', template='styleguide/identity/firefox-family-platform.html'),
        )),
        PageNode('Firefox Browser', path='firefox', children=(
            PageNode('Branding', path='branding', template='styleguide/identity/firefox-branding.html'),
            PageNode('Channels', path='channels', template='styleguide/identity/firefox-channels.html'),
            PageNode('Wordmarks', path='wordmarks', template='styleguide/identity/firefox-wordmarks.html'),
            PageNode('Color', path='color', template='styleguide/identity/firefox-color.html'),
        )),
        PageNode('Firefox OS', path='firefoxos', children=(
            PageNode('Overview', path='overview', template='styleguide/identity/firefoxos-overview.html'),
            PageNode('Branding', path='branding', template='styleguide/identity/firefoxos-branding.html'),
            PageNode('Partners', path='partners', template='styleguide/identity/firefoxos-partners.html'),
            PageNode('Community', path='community', template='styleguide/identity/firefoxos-community.html'),
            PageNode('Typography', path='typography', template='styleguide/identity/firefoxos-typography.html'),
            PageNode('Usage', path='usage', template='styleguide/identity/firefoxos-usage.html'),
            PageNode('Color', path='color', template='styleguide/identity/firefoxos-color.html'),
            # PageNode('Promo Materials', path='promo', template='styleguide/identity/firefoxos-promo-materials.html'),
        )),
        PageNode('Marketplace', path='marketplace', children=(
            PageNode('Branding', path='branding', template='styleguide/identity/marketplace-branding.html'),
            PageNode('Color', path='color', template='styleguide/identity/marketplace-color.html'),
        )),
        PageNode('Webmaker', path='webmaker', children=(
            PageNode('Branding', path='branding', template='styleguide/identity/webmaker-branding.html'),
            PageNode('Color', path='color', template='styleguide/identity/webmaker-color.html'),
        )),
        PageNode('Thunderbird', path='thunderbird', children=(
            PageNode('Logo', path='logo', template='styleguide/identity/thunderbird-logo.html'),
            PageNode('Channels', path='channels', template='styleguide/identity/thunderbird-channels.html'),
            PageNode('Wordmarks', path='wordmarks', template='styleguide/identity/thunderbird-wordmarks.html'),
            PageNode('Color', path='color', template='styleguide/identity/thunderbird-color.html'),
        )),
    )),
    PageNode('Websites', path='websites', children=(
        PageNode('Sandstone', path='sandstone', children=(
            PageNode('Overview', template='styleguide/websites/sandstone-intro.html'),
            PageNode('Buttons', path='buttons', template='styleguide/websites/sandstone-buttons.html'),
            PageNode('Colors', path='colors', template='styleguide/websites/sandstone-colors.html'),
            PageNode('Forms', path='forms', template='styleguide/websites/sandstone-forms.html'),
            PageNode('Grids', path='grids', template='styleguide/websites/sandstone-grids.html'),
            PageNode('Tables & Lists', path='tables', template='styleguide/websites/sandstone-tables.html'),
            PageNode('Tabzilla', path='tabzilla', template='styleguide/websites/sandstone-tabzilla.html'),
            PageNode('Typefaces', path='typefaces', template='styleguide/websites/sandstone-typefaces.html'),
            PageNode('Examples', path='examples', template='styleguide/websites/sandstone-examples.html'),
        )),
        PageNode('Community sites', path='community/overview', template='styleguide/websites/community-overview.html'),
        PageNode('Domain strategy', path='domains/overview', template='styleguide/websites/domains-overview.html'),
    )),
    PageNode('Communications', path='communications', children=(
        PageNode('Presentations', path='presentations', template='styleguide/communications/presentations.html'),
        PageNode('Video', path='video', template='styleguide/communications/video.html'),
        PageNode('Typefaces', path='typefaces', template='styleguide/communications/typefaces.html'),
        PageNode('Copy tone', path='copy-tone', template='styleguide/communications/copy-tone.html'),
        PageNode('Copy rules', path='copy-rules', template='styleguide/communications/copy-rules.html'),
        PageNode('Translation', path='translation', template='styleguide/communications/translation.html'),
    )),
    PageNode('Products', path='products', children=(
        PageNode('Firefox OS', path='firefox-os', children=(
            PageNode('Guidelines', template='styleguide/products/firefox-os/guidelines.html'),
            PageNode('Color Palette', path='color', template='styleguide/products/firefox-os/color.html'),
            PageNode('Typeface', path='typeface', template='styleguide/products/firefox-os/typeface.html'),
            PageNode('Headers', path='headers', template='styleguide/products/firefox-os/headers.html'),
            PageNode('Backgrounds', path='backgrounds', template='styleguide/products/firefox-os/backgrounds.html'),
            PageNode('Lists', path='lists', template='styleguide/products/firefox-os/lists.html'),
            PageNode('Buttons', path='buttons', template='styleguide/products/firefox-os/buttons.html'),
            PageNode('Tab Bars', path='tab-bars', template='styleguide/products/firefox-os/tab-bars.html'),
            PageNode('Input Areas', path='input-areas', template='styleguide/products/firefox-os/input-areas.html'),
            PageNode('Switches', path='switches', template='styleguide/products/firefox-os/switches.html'),
            PageNode('Action Icons', path='actionicons', template='styleguide/products/firefox-os/action-icons.html'),
            PageNode('App Icons', path='icons', template='styleguide/products/firefox-os/icons.html'),
        )),
    )),
]

if settings.DEV:
    all_children.extend((
        PageNode('All Buttons', path='all-download-buttons',
                 template='styleguide/websites/sandstone-all-download-buttons.html'),
        PageNode('Docs', path='docs', children=(
            PageNode('Mozilla Pager JS', path='mozilla-pager',
                    template='styleguide/docs/mozilla-pager.html'),
            PageNode('Mozilla Accordion JS', path='mozilla-accordion',
                    template='styleguide/docs/mozilla-accordion.html'),
            PageNode('Send to Device widget', path='send-to-device',
                    template='styleguide/docs/send-to-device.html'),
        )),
    ))

urlpatterns = PageRoot('Home', children=tuple(all_children)).as_urlpatterns()

urlpatterns += [page('identity/mozilla/logo-prototype', 'styleguide/identity/logo-prototype.html')]
