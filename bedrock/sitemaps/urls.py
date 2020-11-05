from django.urls import re_path

from bedrock.sitemaps.views import SitemapView


urlpatterns = (
    re_path(r'sitemap(?P<is_none>_none)?.xml', SitemapView.as_view()),
)
