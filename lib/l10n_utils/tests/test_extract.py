# taken and modified from tower tests

from builtins import str
from io import StringIO

from babel.messages.catalog import Catalog
from babel.messages.extract import extract
from babel.messages.pofile import write_po
from puente.commands import generate_options_map
from puente.settings import get_setting


def test_extract_python():
    fileobj = StringIO(TEST_PO_INPUT)
    method = 'lib.l10n_utils.extract.extract_python'
    output = fake_extract_command(filename="filename", fileobj=fileobj,
                                  method=method)

    # god help you if these are ever unequal
    assert TEST_PO_OUTPUT == output


def test_extract_jinja2():
    fileobj = StringIO(TEST_TEMPLATE_INPUT)
    method = 'lib.l10n_utils.extract.extract_jinja2'
    output = fake_extract_command(filename="filename", fileobj=fileobj,
                                  method=method)

    # god help you if these are ever unequal
    assert TEST_TEMPLATE_OUTPUT == output


def fake_extract_command(filename, fileobj, method,
                         options=generate_options_map(),
                         keywords=get_setting('KEYWORDS'),
                         comment_tags=get_setting('COMMENT_TAGS')):
    catalog = Catalog(charset='utf-8')
    extracted = fake_extract_from_dir(filename, fileobj, method, options, keywords, comment_tags)
    for filename, lineno, msg, cmts, ctxt in extracted:
        catalog.add(msg, None, [(filename, lineno)], auto_comments=cmts,
                    context=ctxt)

    po_out = StringIO()
    write_po(po_out, catalog, width=80, omit_header=True)
    return str(po_out.getvalue())


def fake_extract_from_dir(filename, fileobj, method, options, keywords, comment_tags):
    """We use Babel's exctract_from_dir() to pull out our gettext
    strings.  In the tests, I don't have a directory of files, I have StringIO
    objects.  So, we fake the original function with this one."""
    for lineno, message, comments, context in extract(method, fileobj, keywords,
                                                      comment_tags, options):

        yield filename, lineno, message, comments, context


TEST_PO_INPUT = """
_('fligtar')
# Make sure several uses collapses to one
ngettext('a fligtar', 'many fligtars', 1)
ngettext('a fligtar', 'many fligtars', 3)
ngettext('a fligtar', 'many fligtars', 5)
# Test comments
# L10N: Turn up the volume
_('fligtar    \\n\\n\\r\\t  talking')
# Test comments w/ plural and context
# l10n: Turn down the volume
ngettext('fligtar', 'many fligtars', 5)
# Test lazy strings are extracted
_lazy('a lazy string')
"""

TEST_PO_OUTPUT = """\
#. l10n: Turn down the volume
#: filename:2 filename:12
msgid "fligtar"
msgid_plural "many fligtars"
msgstr[0] ""
msgstr[1] ""

#: filename:4 filename:5 filename:6
msgid "a fligtar"
msgid_plural "many fligtars"
msgstr[0] ""
msgstr[1] ""

#. L10N: Turn up the volume
#: filename:9
msgid "fligtar talking"
msgstr ""

#: filename:14
msgid "a lazy string"
msgstr ""

"""

TEST_TEMPLATE_INPUT = """
  {{ _('sunshine') }}
  {# Regular comment, regular gettext #}
  {% trans %}
    I like pie.
  {% endtrans %}
  {# l10N: How many hours? #}
  {% trans plural=4, count=4 %}
    {{ count }} hour left
  {% pluralize %}
    {{ count }} hours left
  {% endtrans %}
  {{ ngettext("one", "many", 5) }}
  {# L10n: This string has a hat. #}
  {% trans %}
  Let me tell you about a string
  who spanned
  multiple lines.
  {% endtrans %}
"""

TEST_TEMPLATE_OUTPUT = """\
#: filename:2
msgid "sunshine"
msgstr ""

#: filename:4
msgid "I like pie."
msgstr ""

#. How many hours?
#: filename:8
#, python-format
msgid "%(count)s hour left"
msgid_plural "%(count)s hours left"
msgstr[0] ""
msgstr[1] ""

#: filename:13
msgid "one"
msgid_plural "many"
msgstr[0] ""
msgstr[1] ""

#. This string has a hat.
#: filename:15
msgid "Let me tell you about a string who spanned multiple lines."
msgstr ""

"""
