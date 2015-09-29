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
    redirect(r'^thunderbird/releases/(?P<page>.+)$',
             'http://website-archive.mozilla.org/www.mozilla.org/thunderbird_releasenotes'
             '/en-US/thunderbird/releases/{page}'),
    # should catch everything 1.* to 29.*
    redirect(r'^thunderbird/(?P<version>(?:\d|[12]\d)\.[^/]+)/(?P<page>.*)$',
             'http://website-archive.mozilla.org/www.mozilla.org/thunderbird_releasenotes'
             '/en-US/thunderbird/{version}/{page}'),
    # bug 1209720
    redirect(r'^thunderbird/releasenotes/?$', 'thunderbird.latest.notes'),
)
