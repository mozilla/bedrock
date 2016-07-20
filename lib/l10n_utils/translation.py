# mimic django's language activation machinery. it checks for .mo files
# and we don't need anything nearly as complex.

from _threading_local import local

from django.conf import settings


_active = local()


def activate(language):
    # coppied from Django
    _active.value = language


def get_language():
    # coppied from Django
    l = getattr(_active, "value", None)
    if l is None:
        return settings.LANGUAGE_CODE

    return l


def get_language_bidi():
    """
    Returns selected language's BiDi layout.

    * False = left-to-right layout
    * True = right-to-left layout
    """
    # coppied from Django
    base_lang = get_language().split('-')[0]
    return base_lang in settings.LANGUAGES_BIDI
