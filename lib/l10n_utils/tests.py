import unittest

from l10n_utils.management.commands.l10n_check import list_templates, L10nParser

class TestL10nCheck(unittest.TestCase):

    def test_list_templates(self):
        tmpls = filter(lambda tmpl: 'mozorg/channel.html' in tmpl,
                       list_templates())
        print list(list_templates())
        assert tmpls

    def test_parse_templates(self):
        parser = L10nParser()
        blocks = parser.parse('foo bar bizzle what? '
                              '{% l10n baz, 20110914 %}'
                              'mumble'
                              '{% else %}'
                              'elsed'
                              '{% endl10n %}'
                              'qux')
        baz = blocks['baz']

        self.assertEqual(baz['main_content'], 'mumble')
        self.assertEqual(baz['else_content'], 'elsed')
        self.assertEqual(baz['version'], 20110914)

        blocks = parser.parse('foo bar bizzle what? '
                              '{% l10n baz, 20110914 %}'
                              'mumble'
                              '{% endl10n %}'
                              'qux')
        baz = blocks['baz']
        self.assertEqual(baz['main_content'], 'mumble')
