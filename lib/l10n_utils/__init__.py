from django.conf import settings

from dotlang import get_lang_path
import jingo
from jinja2.exceptions import TemplateNotFound


def render(request, template, context={}, **kwargs):
    """
    Same as jingo's render() shortcut, but with l10n template support.
    If used like this::

        return l10n_utils.render(request, 'myapp/mytemplate.html')

    ... this helper will render the following template::

        l10n/LANG/myapp/mytemplate.html

    if present, otherwise, it'll render the specified (en-US) template.
    """
    # Look for localized template if not default lang.
    if request.locale != settings.LANGUAGE_CODE:
        localized_tmpl = '%s/templates/%s' % (request.locale, template)
        try:
            return jingo.render(request, localized_tmpl, context, **kwargs)
        except TemplateNotFound:
            # If not found, just go on and try rendering the parent template.
            pass

    # Every template gets its own .lang file, so figure out what it is
    # and pass it in the context
    context['langfile'] = get_lang_path(template)

    return jingo.render(request, template, context, **kwargs)
