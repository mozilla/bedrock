import logging


__all__ = ['patch']

# Idempotence! http://en.wikipedia.org/wiki/Idempotence
_has_patched = False


def patch():
    global _has_patched
    if _has_patched:
        return

    # Import for side-effect: configures logging handlers.
    # pylint: disable-msg=W0611
    from . import log_settings  # noqa

    # Monkey-patch django forms to avoid having to use Jinja2's |safe
    # everywhere.
    try:
        import jingo.monkey
        jingo.monkey.patch()
    except ImportError:
        # If we can't import jingo.monkey, then it's an older jingo,
        # so we go back to the old ways.
        import safe_django_forms
        safe_django_forms.monkeypatch()
    logging.debug("Note: bedrock monkey patches executed in %s" % __file__)

    # prevent it from being run again later
    _has_patched = True
