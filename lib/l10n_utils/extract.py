# mostly borrowed from tower

from babel.messages.extract import extract_python as babel_extract_py
from jinja2 import ext

from lib.l10n_utils.utils import strip_whitespace


def add_context(context, message):
    # \x04 is a magic gettext number.
    return u"%s\x04%s" % (context, message)


def tweak_message(message):
    """We piggyback on jinja2's babel_extract() (really, Babel's extract_*
    functions) but they don't support some things we need so this function will
    tweak the message.  Specifically:

        1) We strip whitespace from the msgid.  Jinja2 will only strip
            whitespace from the ends of a string so linebreaks show up in
            your .po files still.

        2) Babel doesn't support context (msgctxt).  We hack that in ourselves
            here.
    """
    if isinstance(message, str):
        message = strip_whitespace(message)
    elif isinstance(message, tuple):
        # A tuple of 2 has context, 3 is plural, 4 is plural with context
        if len(message) == 2:
            message = add_context(message[1], message[0])
        elif len(message) == 3:
            if all(isinstance(x, str) for x in message[:2]):
                singular, plural, num = message
                message = (strip_whitespace(singular),
                           strip_whitespace(plural),
                           num)
        elif len(message) == 4:
            singular, plural, num, ctxt = message
            message = (add_context(ctxt, strip_whitespace(singular)),
                       add_context(ctxt, strip_whitespace(plural)),
                       num)
    return message


def extract_python(fileobj, keywords, comment_tags, options):
    for lineno, funcname, message, comments in \
            list(babel_extract_py(fileobj, keywords, comment_tags, options)):

        message = tweak_message(message)

        yield lineno, funcname, message, comments


def extract_jinja2(fileobj, keywords, comment_tags, options):
    for lineno, funcname, message, comments in \
            list(ext.babel_extract(fileobj, keywords, comment_tags, options)):

        message = tweak_message(message)

        yield lineno, funcname, message, comments
