# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import *
from mozorg.util import page
import views

urlpatterns = patterns('',
    page('research', 'research/research.html'),
    page('research/researchers', 'research/researchers.html'),
    page('research/projects', 'research/projects.html'),
    page('research/collaborations', 'research/collaborations.html'),
    page('research/publications', 'research/publications.html'),
)
