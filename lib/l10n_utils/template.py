import uuid

from jinja2.ext import Environment, Extension, nodes


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
        body = parser.parse_statements(['name:else', 'name:endl10n'],
                                       drop_needle=False)

        # Translation fallback: If this is followed by an "else" tag, render
        # that block instead.
        end_tag = parser.stream.expect('name')  # Either else or endl10n.
        if end_tag.value == 'else':
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
    """ Create a special syntax for specifying additional lang files.
    It looks like this: {% lang_files "foo" "bar" %}. We convert it
    into a call to a helper method because it needs to context to load
    in the correct locale. As a result, this must be within a block. """

    tags = set(['lang_files'])

    def parse(self, parser):
        # Skip over the block name
        lineno = parser.stream.next().lineno

        # Grab all the args
        args = [parser.stream.expect('string').value]
        while parser.stream.current.type == 'string':
            args.append(parser.stream.current.value)
            parser.stream.next()

        # Since we are a block, we must emit a block too, so make a
        # random one that contains a call to the load function
        node = nodes.Block().set_lineno(lineno)
        node.name = '__loadlangs_%s__' % str(uuid.uuid4()).replace('-', '_')
        node.scoped = False
        node.body = [nodes.Output([nodes.Call(nodes.Name('lang_files', 'load'),
                                              [nodes.Const(x) for x in args], [],
                                              None, None).set_lineno(lineno)])]
        return node


# Makes for a prettier import in settings.py
l10n_blocks = L10nBlockExtension
lang_blocks = LoadLangExtension
