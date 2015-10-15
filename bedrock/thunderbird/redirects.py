from bedrock.redirects.util import redirect


redirectpatterns = (
    # bug 1124038
    redirect(r'^thunderbird/organizations/(?:all-esr\.html|faq/?)$', 'thunderbird.organizations'),

    # bug 1124042
    redirect(r'^thunderbird/features/email_providers\.html$', 'thunderbird.email-providers'),

    # bug 1123399, 1150649
    redirect(r'^thunderbird/all\.html?$', 'thunderbird.latest.all'),
    redirect(r'^thunderbird/all-beta\.html?$', 'thunderbird.latest.all',
             to_kwargs={'channel': 'beta'}),
    redirect(r'^thunderbird/early_releases/downloads/?$', 'thunderbird.latest.all',
             to_kwargs={'channel': 'beta'}),
    redirect(r'^thunderbird/early_releases/?$', 'thunderbird.channel'),

    # bug 1081917, 1029829, 1029838
    redirect(r'^thunderbird/releases/(?P<version>0\.\d)\.html$',
             'http://website-archive.mozilla.org/www.mozilla.org/thunderbird_releasenotes'
             '/en-US/thunderbird/releases/{version}.html'),
    # should catch everything 1.* to 29.*
    redirect(r'^thunderbird/(?P<version>(?:\d|[12]\d)\.[^/]+)/'
             '(?P<page>firstrun|releasenotes|start|system-requirements|whatsnew)/$',
             'http://website-archive.mozilla.org/www.mozilla.org/thunderbird_releasenotes'
             '/en-US/thunderbird/{version}/{page}/'),
    # bug 1209720
    redirect(r'^thunderbird/releasenotes/?$', 'thunderbird.latest.notes'),
    # bug 1211007
    redirect(r'^thunderbird/download/?', 'thunderbird.index'),

    # bug 1133266
    redirect(r'^thunderbird/legal/privacy/?$', 'privacy.notices.thunderbird'),
    redirect(r'^thunderbird/about/privacy-policy/?$',
             'privacy.archive.thunderbird-2010-06'),

    # bug 1196578
    redirect(r'^thunderbird/about/legal/eula/?$', 'legal.eula'),
    redirect(r'^thunderbird/about/legal/eula/thunderbird2',
             'legal.eula.thunderbird-2-eula'),
    redirect(r'^thunderbird/about/legal/eula/thunderbird',
             'legal.eula.thunderbird-1.5-eula'),

    # bug 1204579
    redirect(r'^thunderbird/2.0.0.0/eula/?$', 'legal.eula.thunderbird-2-eula'),
    redirect(r'^thunderbird/about/legal/?$', 'legal.terms.mozilla'),
    redirect(r'^thunderbird/about(/mission)?/?$',
             'https://wiki.mozilla.org/Thunderbird'),
    redirect(r'^thunderbird/(about/(careers|contact|get-involved)|community)/?$',
             'https://wiki.mozilla.org/Thunderbird#Contributing'),
    redirect(r'^thunderbird/(?P<version>\d\.\d(?:a|b|rc)\d|[6-9]\.0beta)/?$',
             'http://website-archive.mozilla.org/www.mozilla.org/thunderbird'
             '/thunderbird/{version}/'),
    redirect(r'^thunderbird/about/(?P<page>board|press|staff)/',
             'http://website-archive.mozilla.org/www.mozilla.org/thunderbird'
             '/thunderbird/about/{page}/'),
)
