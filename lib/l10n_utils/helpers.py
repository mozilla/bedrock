import jingo
import jinja2

from django.conf import settings

from dotlang import translate


def install_lang_files(ctx):
    """Install the initial set of .lang files"""
    req = ctx['request']

    if not hasattr(req, 'langfiles'):
        files = list(settings.DOTLANG_FILES)
        if ctx.get('langfile'):
            files.append(ctx.get('langfile'))
        setattr(req, 'langfiles', files)


def add_lang_files(ctx, files):
    """Install additional .lang files"""
    req = ctx['request']

    if hasattr(req, 'langfiles'):
        req.langfiles = files + req.langfiles


@jingo.register.function
@jinja2.contextfunction
def _(ctx, text):
    """Translate a string, loading the translations for the locale if
    necessary."""
    install_lang_files(ctx)

    trans = translate(text, ctx['request'].langfiles)
    return jinja2.Markup(trans)


@jingo.register.function
@jinja2.contextfunction
def gettext(ctx, text):
    """Override the gettext call to pass through our system. This is
    hacky, but lets us use the trans blocks and other nice integration
    features of gettext. """
    return _(ctx, text)


@jingo.register.function
@jinja2.contextfunction
def lang_files(ctx, *files):
    """Add more lang files to the translation object"""
    # Filter out empty files
    install_lang_files(ctx)
    add_lang_files(ctx, [f for f in files if f])
