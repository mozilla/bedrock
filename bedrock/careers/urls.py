from django.conf.urls import url

from . import views
from .feeds import LatestPositionsFeed

urlpatterns = [
    url(r"^$", views.HomeView.as_view(), name="careers.home"),
    url(r"^position/(?P<source>[\w]+)/(?P<job_id>[\w]+)/$", views.PositionDetailView.as_view(), name="careers.position"),
    url(r"^feed/$", LatestPositionsFeed(), name="careers.feed"),
    url(r"^listings/$", views.PositionListView.as_view(), name="careers.listings"),
    url(r"^internships/$", views.InternshipsView.as_view(), name="careers.internships"),
    url(r"^benefits/$", views.BenefitsView.as_view(), name="careers.benefits"),
]
