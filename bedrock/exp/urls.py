# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from bedrock.mozorg.util import page


urlpatterns = (
    page('opt-out', 'exp/opt-out.html'),
    page('firefox/new', 'exp/firefox/new/download.html', active_locales=['en-US', 'en-GB', 'en-CA', 'de']),
    page('firefox/accounts', 'exp/firefox/accounts-2019.html'),
)
