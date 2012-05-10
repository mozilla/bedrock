from django.conf.urls.defaults import *
from mozorg.util import page
import views

urlpatterns = patterns('',
    page('research', 'research/research.html'),
    page('research/people', 'research/people.html'),
    page('research/emscripten', 'research/emscripten.html'),
    page('research/rust', 'research/rust.html'),
    page('research/servo', 'research/servo.html'),
    page('research/shumway', 'research/shumway.html'),
)
