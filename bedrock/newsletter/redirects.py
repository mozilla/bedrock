from bedrock.redirects.util import redirect


redirectpatterns = (
    # bug 926629
    redirect(r'^newsletter/about_mobile(?:/(?:index.html)?)?$', 'newsletter.subscribe'),
    redirect(r'^newsletter/about_mozilla(?:/(?:index.html)?)?$', 'mozorg.contribute.index'),
    redirect(r'^newsletter/new(?:/(?:index.html)?)?$', 'newsletter.subscribe'),
    redirect(r'^newsletter/ios(?:/(?:index.html)?)?$', 'firefox.mobile'),
)
