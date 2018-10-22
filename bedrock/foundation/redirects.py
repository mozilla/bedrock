from bedrock.redirects.util import redirect

redirectpatterns = (

    redirect(r'^foundation/trademarks/?$', '/foundation/trademarks/policy/'),
    redirect(r'^foundation/trademarks/faq/$', '/foundation/trademarks/policy/'),
    redirect(r'^foundation/documents/domain-name-license.pdf$', '/foundation/trademarks/policy/'),
    redirect(r'^about/partnerships/distribution/$', '/foundation/trademarks/distribution-policy/'),
    redirect(r'^foundation/trademarks/poweredby/faq/$', '/foundation/trademarks/policy/'),
    redirect(r'^foundation/trademarks/l10n-website-policy/$', '/foundation/trademarks/policy/')
)
