# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import *
from mozorg.util import page


urlpatterns = patterns('',
    page('trans-block-reload-test', 'trans_block_reload_test.html'),
    page('active-de-lang-file', 'active_de_lang_file.html'),
    page('inactive-de-lang-file', 'inactive_de_lang_file.html'),
)
