from bedrock.redirects.util import redirect


redirectpatterns = (
    # bug 1255785
    redirect(r'^styleguide/identity/mozilla/logo-prototype/?$', 'styleguide.home'),

    # bug 1268847
    redirect(r'^styleguide/websites/sandstone/buttons/?$',
             'styleguide.websites.sandstone-intro'),
    redirect(r'^styleguide/websites/sandstone/forms/?$',
             'styleguide.websites.sandstone-intro'),
    redirect(r'^styleguide/websites/sandstone/tabzilla/?$',
             'styleguide.websites.sandstone-intro'),

    # Bug 1329931
    redirect(r'^styleguide/products/firefox-os(/.*)?$',
             'https://developer.mozilla.org/docs/Archive/Firefox_OS'),

    # Bug 1329931 & 1342043
    redirect(r'^styleguide/identity/firefoxos(/.*)?$',
             'https://developer.mozilla.org/docs/Archive/Firefox_OS'),

    # Bug 1365076
    redirect(r'^styleguide/identity/mozilla/branding/?$',
             'https://designlanguage.mozilla.org/'),
    redirect(r'^styleguide/identity/mozilla/color/?$',
             'https://designlanguage.mozilla.org/'),

    # Bug 1404926
    redirect(r'^styleguide/identity/firefox-family(/.*)?$',
            'http://design.firefox.com/photon/visuals/product-identity-assets.html'),
    redirect(r'^styleguide/identity/firefox/branding/?$',
            'http://design.firefox.com/photon/visuals/product-identity-assets.html'),
    redirect(r'^styleguide/identity/firefox/channels/?$',
            'http://design.firefox.com/photon/visuals/product-identity-assets.html#channel-variations'),
    redirect(r'^styleguide/identity/firefox/wordmarks/?$',
            'http://design.firefox.com/photon/visuals/product-identity-assets.html#using-icons-with-firefox-wordmarks-or-logos'),
    redirect(r'^styleguide/identity/firefox/color/?$',
            'http://design.firefox.com/photon/visuals/color.html'),
)
