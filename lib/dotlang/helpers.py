import jingo
import jinja2
from translate import translate


@jingo.register.function
@jinja2.contextfunction
def ___(ctx, text):
    locale = ctx['request'].locale
    return jinja2.Markup(translate(locale, text))
