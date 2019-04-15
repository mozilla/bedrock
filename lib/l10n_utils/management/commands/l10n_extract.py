from __future__ import print_function
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
from textwrap import dedent

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from babel.messages.catalog import Catalog
from babel.messages.extract import extract_from_file
from babel.messages.pofile import write_po
from babel.util import pathmatch
from puente.commands import generate_options_map
from puente.settings import get_setting

from lib.l10n_utils.gettext import pot_to_langfiles


DOMAIN = 'django'
METHODS = settings.PUENTE['DOMAIN_METHODS'][DOMAIN]


def gettext_extract():
    call_command('extract', create=True)


def extract_callback(filename, method, options):
    if method != 'ignore':
        print("  %s" % filename)


def extract_from_files(filenames,
                       method_map=METHODS,
                       options_map=generate_options_map(),
                       keywords=get_setting('KEYWORDS'),
                       comment_tags=get_setting('COMMENT_TAGS'),
                       callback=extract_callback,
                       strip_comment_tags=False):
    """Extract messages from any source files found in the given iterable.

    This function generates tuples of the form:

        ``(filename, lineno, message, comments)``

    Which extraction method is used per file is determined by the `method_map`
    parameter, which maps extended glob patterns to extraction method names.
    For example, the following is the default mapping:

    >>> method_map = [
    ...     ('**.py', 'python')
    ... ]

    This basically says that files with the filename extension ".py"
    should be processed by the "python" extraction
    method. Files that don't match any of the mapping patterns are ignored. See
    the documentation of the `pathmatch` function for details on the pattern
    syntax.

    The following extended mapping would also use the "genshi" extraction
    method on any file in "templates" subdirectory:

    >>> method_map = [
    ...     ('**/templates/**.*', 'genshi'),
    ...     ('**.py', 'python')
    ... ]

    The dictionary provided by the optional `options_map` parameter augments
    these mappings. It uses extended glob patterns as keys, and the values are
    dictionaries mapping options names to option values (both strings).

    The glob patterns of the `options_map` do not necessarily need to be the
    same as those used in the method mapping. For example, while all files in
    the ``templates`` folders in an application may be Genshi applications, the
    options for those files may differ based on extension:

    >>> options_map = {
    ...     '**/templates/**.txt': {
    ...         'template_class': 'genshi.template:TextTemplate',
    ...         'encoding': 'latin-1'
    ...     },
    ...     '**/templates/**.html': {
    ...         'include_attrs': ''
    ...     }
    ... }

    :param filenames: an iterable of filenames relative to the ROOT of
                      the project
    :param method_map: a list of ``(pattern, method)`` tuples that maps of
                       extraction method names to extended glob patterns
    :param options_map: a dictionary of additional options (optional)
    :param keywords: a dictionary mapping keywords (i.e. names of functions
                     that should be recognized as translation functions) to
                     tuples that specify which of their arguments contain
                     localizable strings
    :param comment_tags: a list of tags of translator comments to search for
                         and include in the results
    :param callback: a function that is called for every file that message are
                     extracted from, just before the extraction itself is
                     performed; the function is passed the filename, the name
                     of the extraction method and and the options dictionary as
                     positional arguments, in that order
    :param strip_comment_tags: a flag that if set to `True` causes all comment
                               tags to be removed from the collected comments.
    :return: an iterator over ``(filename, lineno, funcname, message)`` tuples
    :rtype: ``iterator``
    :see: `pathmatch`
    """
    # adapted from babel.messages.extract.extract_from_dir
    for filename in filenames:
        matched = False
        for pattern, method in method_map:
            if pathmatch(pattern, filename):
                matched = True
                filepath = os.path.join(settings.ROOT, filename)
                if not os.path.exists(filepath):
                    print('! %s does not exist!' % filename)
                    break
                options = {}
                for opattern, odict in list(options_map.items()):
                    if pathmatch(opattern, filename):
                        options = odict
                if callback:
                    callback(filename, method, options)
                for lineno, message, comments, context in\
                    extract_from_file(method, filepath,
                                      keywords=keywords,
                                      comment_tags=comment_tags,
                                      options=options,
                                      strip_comment_tags=strip_comment_tags):
                    yield filename, lineno, message, comments, context
                break
        if not matched:
            print('! %s does not match any domain methods!' % filename)


class Command(BaseCommand):
    help = dedent("""
        Extracts a .lang file with new translations from all source files.
        If <filename>s are provided only extract from those files.
    """).strip()

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('filenames', nargs='*')

    def handle(self, *args, **options):
        filenames = options['filenames']
        if filenames:
            # mimics puente.management.commands.extract for a list of files
            outputdir = os.path.join(settings.ROOT, 'locale', 'templates',
                                     'LC_MESSAGES')
            if not os.path.isdir(outputdir):
                os.makedirs(outputdir)

            catalog = Catalog(
                header_comment='',
                project=get_setting('PROJECT'),
                version=get_setting('VERSION'),
                msgid_bugs_address=get_setting('MSGID_BUGS_ADDRESS'),
                charset='utf-8',
            )

            for filename, lineno, msg, cmts, ctxt in extract_from_files(filenames):
                catalog.add(msg, None, [(filename, lineno)], auto_comments=cmts,
                            context=ctxt)

            with open(os.path.join(outputdir, '%s.pot' % DOMAIN), 'wb') as fp:
                write_po(fp, catalog, width=80)
        else:
            # This is basically a wrapper around the puente extract
            # command, we might want to do some things around this in the
            # future
            gettext_extract()
        pot_to_langfiles(DOMAIN)
