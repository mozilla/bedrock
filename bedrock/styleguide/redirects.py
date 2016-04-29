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
)
