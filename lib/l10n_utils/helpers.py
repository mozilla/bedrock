import jingo
import jinja2

def init_context_trans(ctx, locale, files=None):
    # If we have a translation object, we can load translations and
    # use them. This "box" is set with a context processor (see
    # /apps/mozorg/context_processors.py).
    trans = ctx.get('__trans')

    if trans and not trans.loaded:
        files = ['main']
        if ctx.get('langfile'):
            files.append(ctx.get('langfile'))
        trans.add(files, locale)        
    return trans
    

@jingo.register.function
@jinja2.contextfunction
def _(ctx, text, *args):
    """Translate a string, loading the translations for the locale if
    necessary."""

    locale = ctx['request'].locale
    trans = init_context_trans(ctx, locale)

    if trans:
        msg = trans.get(text, text)
        return jinja2.Markup(msg % args)
    else:
        return jinja2.Markup(text)


@jingo.register.function
@jinja2.contextfunction
def lang_files(ctx, *files):
    """Add more lang files to the translation object"""

    locale = ctx['request'].locale
    trans = init_context_trans(ctx, locale)
    # Filter out empty files
    files = filter(lambda x: x, files)

    if trans:
        trans.add(files, locale)
