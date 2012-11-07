import jingo

from l10n_utils.helpers import gettext


# TODO: Fix tower and remove this.
class FixLangFileTranslationsMiddleware(object):
    """
    Middleware that will overwrite the gettext functions in the Jinja2 setup.
    tower.activate() called by LocaleURLMiddleware sets them to tower's own
    functions.

    Bug 808580
    """

    def process_request(self, request):
        jingo.env.install_gettext_callables(gettext, gettext)
