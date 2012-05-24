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
