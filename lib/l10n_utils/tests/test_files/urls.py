from django.conf.urls.defaults import *
from mozorg.util import page


urlpatterns = patterns('',
    page('trans-block-reload-test', 'trans_block_reload_test.html'),
    page('active-de-lang-file', 'active_de_lang_file.html'),
    page('inactive-de-lang-file', 'inactive_de_lang_file.html'),
)
