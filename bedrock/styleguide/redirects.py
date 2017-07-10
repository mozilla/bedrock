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
)
