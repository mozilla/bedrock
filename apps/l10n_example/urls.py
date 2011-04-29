from django.conf.urls.defaults import patterns

import jingo


urlpatterns = patterns('',
    (r'^$', 'l10n_example.views.example'),
)
