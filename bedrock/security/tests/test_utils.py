# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from textwrap import dedent
from cStringIO import StringIO
from nose.tools import eq_

from bedrock.security.utils import mfsa_id_from_filename, parse_md_front_matter


def test_parse_front_matter():
    """Should return front matter and MD separately."""
    lines = StringIO(dedent("""
        ---
        dude: abiding
        walter: angry
        donny: oblivious
        ---

        Let's go bowling.
    """))
    yaml, md = parse_md_front_matter(lines)
    eq_(yaml, dedent("""\
        dude: abiding
        walter: angry
        donny: oblivious
    """))
    eq_(md, "\nLet's go bowling.\n")


def test_parse_front_matter_only():
    """Should not care about any other --- lines."""
    lines = StringIO(dedent("""
        ---
        dude: abiding
        walter: angry
        ---

        Art
        ---

        Maude's thing.
    """))
    yaml, md = parse_md_front_matter(lines)
    eq_(yaml, 'dude: abiding\nwalter: angry\n')
    eq_(md, "\nArt\n---\n\nMaude's thing.\n")


def test_mfsa_id_from_filename():
    eq_(mfsa_id_from_filename('announce/2014/mfsa2014-01.md'),
        '2014-01')
    eq_(mfsa_id_from_filename('announce/2014/mfsa2014-101.md'),
        '2014-101')
    assert mfsa_id_from_filename('dude.txt') is None
