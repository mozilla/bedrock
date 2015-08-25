# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from bedrock.urls import urlpatterns
from bedrock.mozorg.util import page


# have to append these to existing site patterns
# because calls to e.g. {{ url('mozorg.home') }}
# in templates don't work otherwise.
urlpatterns += (
    page('trans-block-reload-test', 'trans_block_reload_test.html'),
    page('active-de-lang-file', 'active_de_lang_file.html'),
    page('inactive-de-lang-file', 'inactive_de_lang_file.html'),
    page('some-lang-files', 'some_lang_files.html'),
    page('state-of-mozilla', 'state_of_mozilla.html'),
    page('firefox/new', 'firefox/new.html'),
)
