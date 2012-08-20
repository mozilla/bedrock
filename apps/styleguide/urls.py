from django.conf.urls.defaults import *
from mozorg.util import page

urlpatterns = patterns('',
    page('', 'styleguide/home.html'),
    page('sandstone', 'styleguide/sandstone-intro.html'),
    page('sandstone/grids', 'styleguide/sandstone-grids.html'),
)
