from bedrock.redirects.util import redirect

redirectpatterns = (

    redirect(r'^foundation/$', 'https://foundation.mozilla.org/en/'),
    redirect(r'^foundation/about/$', 'https://foundation.mozilla.org/en/about/'),
    redirect(r'^foundation/documents/$', 'https://foundation.mozilla.org/en/about/public-records/'),
    redirect(r'^foundation/issues/$', 'https://foundation.mozilla.org/en/initiatives/'),
    redirect(r'^foundation/leadership-network/$', 'https://foundation.mozilla.org/en/'),
    redirect(r'^foundation/advocacy/$', 'https://foundation.mozilla.org/en/'),
    redirect(r'^foundation/trademarks/?$', '/foundation/trademarks/policy/'),
    redirect(r'^foundation/trademarks/faq/$', '/foundation/trademarks/policy/'),
    redirect(r'^foundation/documents/domain-name-license.pdf$', '/foundation/trademarks/policy/'),
    redirect(r'^about/partnerships/distribution/$', '/foundation/trademarks/distribution-policy/'),
    redirect(r'^foundation/trademarks/poweredby/faq/$', '/foundation/trademarks/policy/'),
    redirect(r'^foundation/trademarks/l10n-website-policy/$', '/foundation/trademarks/policy/')
)
