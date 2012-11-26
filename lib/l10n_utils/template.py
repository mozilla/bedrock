# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from jinja2.ext import Extension, InternationalizationExtension, nodes
from tower import strip_whitespace


class I18nExtension(InternationalizationExtension):
    """
    Use this instead of `tower.template.i18n` because the override of `_`
    global was throwing errors.
    """
    def _parse_block(self, parser, allow_pluralize):
        ref, buffer = super(I18nExtension, self)._parse_block(parser,
                                                              allow_pluralize)
        return ref, strip_whitespace(buffer)


class L10nBlockExtension(Extension):
    """
    Add support for an L10n block that works like a regular "block" for now.
    """

    tags = set(['l10n'])

    def parse(self, parser):
        # Jump over first token ("l10n"), grab line number.
        lineno = parser.stream.next().lineno

        # Block name is mandatory.
        name = parser.stream.expect('name').value

        # Comma optional.
        parser.stream.skip_if('comma')

        # Add version if provided.
        if parser.stream.current.type == 'integer':
            version = int(parser.parse_expression().value)
        else:
            version = 0  # Default version for unversioned block.

        # Parse content.
        body = parser.parse_statements(['name:was', 'name:endl10n'],
                                       drop_needle=False)

        # Translation fallback: If this is followed by an "was" tag, render
        # that block instead.
        end_tag = parser.stream.expect('name')  # Either was or endl10n.
        if end_tag.value == 'was':
            body = parser.parse_statements(['name:endl10n'], drop_needle=True)

        # Build regular block node with special node name and remember version.
        node = nodes.Block()
        node.set_lineno(lineno)
        node.name = '__l10n__{0}'.format(name)
        node.version = version  # For debugging only, for now.
        node.body = body
        # I *think*, `true` would mean that variable assignments inside this
        # block do not persist beyond this block (like a `with` block).
        node.scoped = False

        return node


class LoadLangExtension(Extension):
    """Create a special syntax for specifying additional lang files.
    It looks like this: {% lang_files "foo" "bar" %}. We convert it
    into a call to a helper method because it needs to context to load
    in the correct locale. As a result, this must be within a block."""

    tags = set(['set_lang_files', 'add_lang_files'])

    def parse(self, parser):
        # Skip over the block name
        name = parser.stream.next()
        lineno = name.lineno

        # Grab all the args
        args = [parser.stream.expect('string').value]
        while parser.stream.current.type == 'string':
            args.append(parser.stream.current.value)
            parser.stream.next()

        # Make a node that calls the lang_files helper
        content_nodes = [nodes.Call(nodes.Name('lang_files', 'load'),
                                    [nodes.Const(x) for x in args], [],
                                    None, None)]

        if name == 'add_lang_files':
            # If we are adding files, we need to keep the parent
            # template's list of lang files as well
            content_nodes.insert(0, [nodes.Call(nodes.Name('super', 'load'),
                                                [], [], None, None)])

        # Since we are a block, we must emit a block too, so make a
        # random one that contains a call to the load function
        node = nodes.Block().set_lineno(lineno)
        node.name = '__langfiles__'
        node.scoped = False
        node.body = [nodes.Output(content_nodes)]
        node.set_lineno(lineno)
        return node


# Makes for a prettier import in settings.py
l10n_blocks = L10nBlockExtension
lang_blocks = LoadLangExtension
i18n = I18nExtension
