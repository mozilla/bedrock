import unittest

from l10n_utils.management.commands.l10n_check import list_templates, L10nParser


class TestL10nCheck(unittest.TestCase):
    def _get_block(blocks, name):
        """Out of all blocks, grab the one with the specified name."""
        try:
            return filter(lambda b: b['name'] == name, blocks)[0]
        except IndexError:
            return None

    def test_list_templates(self):
        tmpls = filter(lambda tmpl: 'mozorg/channel.html' in tmpl,
                       list_templates())
        assert tmpls

    def test_parse_templates(self):
        """Make sure the parser grabs the l10n block content
        correctly."""

        parser = L10nParser()
        blocks = parser.parse('foo bar bizzle what? '
                              '{% l10n baz, 20110914 %}'
                              'mumble'
                              '{% else %}'
                              'elsed'
                              '{% endl10n %}'
                              'qux',
                              only_blocks=True)

        baz = self._get_block(blocks, 'baz')

        self.assertEqual(baz['main'], 'mumble')
        self.assertEqual(baz['else'], 'elsed')
        self.assertEqual(baz['version'], 20110914)

        blocks = parser.parse('foo bar bizzle what? '
                              '{% l10n baz, 20110914 %}'
                              'mumble'
                              '{% endl10n %}'
                              'qux',
                              only_blocks=True)

        baz = self._get_block(blocks, 'baz')
        self.assertEqual(baz['main'], 'mumble')

    def test_content_halt(self):
        """Make sure the parser will halt on the content block if told
        to do so."""

        parser = L10nParser()
        content_str = 'foo bar {% block content %}baz{% endblock %} hello'
        last_token = None

        for token in parser.parse(content_str, halt_on_content=True):
            last_token = token

        self.assertEqual(last_token, False)

    # I need help writing tests for copy_template and update_template,
    # which read files from the filesystem and write to it. I think I
    # need to mock those somehow.
