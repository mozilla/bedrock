import jingo
import jinja2
import dotlang

@jingo.register.function
@jinja2.contextfunction
def ___(ctx, text):
    locale = ctx['request'].locale
    return jinja2.Markup(dotlang.translate(locale, text))
