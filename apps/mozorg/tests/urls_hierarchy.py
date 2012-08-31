from django.conf.urls.defaults import *

from mozorg.hierarchy import node, nodeview
from mozorg.util import page

hierarchy = node('ventilo',
    node('Identity',
        node('Mozilla',
            nodeview('Branding', 'identity/mozilla/brand', 'mozilla/brand.html'),
            nodeview('Color', 'identity/mozilla/color', 'mozilla/color.html'),
        ),
        nodeview('Firefox Family', 'firefoxfamily', 'firefoxfamily/index.html',
            nodeview('Overview', 'firefoxfamily/overview', 'firefoxfamily/overview.html'),
            nodeview('Platform', 'firefoxfamily/platform', 'firefoxfamily/platform.html'),
        ),
    ),
    node('Websites',
        node('Sandstone',
            nodeview('Overview', 'websites/sandstone/overview', 'sandstone/template.html'),
        ),
        nodeview('Community Sites', 'websites/community', 'websites/community.html'),
        nodeview('Domain strategy', 'websites/domain', 'websites/domain.html'),
    ),
)
urlpatterns = hierarchy.as_urlpattern()

ref_urlpatterns = patterns('',
    page('identity/mozilla/brand', 'brand.html'),
    page('identity/mozilla/color', 'color.html'),
    page('firefoxfamily', 'firefoxfamily/index.html'),
    page('firefoxfamily/overview', 'overview.html'),
    page('firefoxfamily/platform', 'platform.html'),
    page('websites/sandstone/overview', 'template.html'),
    page('websites/community', 'community.html'),
    page('websites/domain', 'domain.html'),
)
