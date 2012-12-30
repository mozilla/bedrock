# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import *
from mozorg.hierarchy import PageNode, PageRoot

hierarchy = PageRoot('Home', children=(
    PageNode('Home', template='styleguide/home.html'),
    PageNode('Identity', path='identity', children=(
        PageNode('Mozilla', path='mozilla', children=(
            PageNode('Branding', path='branding', template='styleguide/identity/mozilla-branding.html'),
            PageNode('Color', path='color', template='styleguide/identity/mozilla-color.html'),
            PageNode('Innovations', path='innovations', template='styleguide/identity/mozilla-innovations.html'),
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
            PageNode('Branding', path='branding', template='styleguide/identity/firefoxos-branding.html'),
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
        PageNode('Firefox OS', path='firefoxos', children=(
            PageNode('Icons', path='icons', template='styleguide/products/firefox-os-icons.html'),
        )),
    )),
))

urlpatterns = hierarchy.as_urlpatterns()
