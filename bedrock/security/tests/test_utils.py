# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from textwrap import dedent
from cStringIO import StringIO

from mock import patch, call
from nose.tools import eq_

from bedrock.security.utils import (
    generate_yml_advisories_html,
    mfsa_id_from_filename,
    parse_bug_url,
    parse_md_front_matter,
    yaml_ordered_safe_load,
)


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
    eq_(mfsa_id_from_filename('announce/2014/mfsa2014-01.md'), '2014-01')
    eq_(mfsa_id_from_filename('announce/2014/mfsa2014-101.md'), '2014-101')
    eq_(mfsa_id_from_filename('announce/2016/mfsa2016-42.yml'), '2016-42')
    assert mfsa_id_from_filename('dude.txt') is None


def test_parse_bug_url():
    assert parse_bug_url('8675309') == 'https://bugzilla.mozilla.org/show_bug.cgi?id=8675309'
    assert parse_bug_url('1234,5678, 9012') == 'https://bugzilla.mozilla.org/buglist.cgi?' \
                                               'bug_id=1234%2C5678%2C9012'
    assert parse_bug_url('http://example.com/1234') == 'http://example.com/1234'


@patch('bedrock.security.utils.render_to_string')
def test_generate_yml_advisories_html(rts_mock):
    rts_mock.return_value = 'html'
    data = yaml_ordered_safe_load(StringIO(YML_ADVISORY))
    html = generate_yml_advisories_html(data)
    assert html.startswith('<p>Some <strong>HTML</strong> that relates '
                           'to the whole lot of em.</p>')
    rts_mock.assert_has_calls([
        call('security/partials/cve.html', {
            'id': 'CVE-2016-2827',
            'impact': 'Low',
            'impact_class': 'low',
            'title': 'A sample title for a CVE here',
            'reporter': 'Reporty McReporterface',
            'description': 'Short description <strong>with HTML</strong> and multiple lines!\n\n'
                           'Can also have full breaks and ***markdown***!\n',
            'bugs': [
                {'url': 'https://bugzilla.mozilla.org/show_bug.cgi?id=1289085',
                 'desc': 'Bug 1289085'},
                {'url': 'https://bugzilla.mozilla.org/buglist.cgi?bug_id=1289085%2C1289087',
                 'desc': 'stuff about the bugs'},
            ]
        }),
        call('security/partials/cve.html', {
            'id': 'CVE-2016-5270',
            'impact': 'High',
            'impact_class': 'high',
            'title': 'Another sampile title, this time with more length!',
            'reporter': 'A Nameless Evilcorp Employee',
            'description': 'Another short description',
            'bugs': [
                {'url': 'https://example.com/warning.html',
                 'desc': 'A different site that is totally not bugzilla'},
            ]
        }),
    ])


@patch('bedrock.security.utils.render_to_string')
def test_generate_yml_advisories_missing_things(rts_mock):
    rts_mock.return_value = 'html'
    data = yaml_ordered_safe_load(StringIO(YML_ADVISORY_MISSING_THINGS))
    generate_yml_advisories_html(data)
    rts_mock.assert_has_calls([
        call('security/partials/cve.html', {
            'id': 'CVE-2016-2827',
            'impact': 'Low',
            'impact_class': 'low',
            'title': 'A sample title for a CVE here',
            'reporter': 'Reporty McReporterface',
            'description': 'Short description <strong>with HTML</strong> and multiple lines!\n\n'
                           'Can also have full breaks and ***markdown***!\n',
        }),
        call('security/partials/cve.html', {
            'id': 'CVE-2016-5270',
            'impact': 'High',
            'impact_class': 'high',
            'title': 'Another sampile title, this time with more length!',
            'reporter': 'A Nameless Evilcorp Employee',
            'description': 'Another short description',
            'bugs': [
                {'url': 'https://bugzilla.mozilla.org/show_bug.cgi?id=1289085',
                 'desc': 'Bug 1289085'},
            ]
        }),
    ])


YML_ADVISORY = dedent("""\
    announced: September 13, 2016
    fixed_in:
      - Firefox 49
    title: Security vulnerabilities fixed in Firefox 49
    description: Some **HTML** that relates to the whole lot of em.
    advisories:
      CVE-2016-2827:
        title: A sample title for a CVE here
        impact: Low
        reporter: Reporty McReporterface
        description: |
          Short description <strong>with HTML</strong> and multiple lines!

          Can also have full breaks and ***markdown***!
        bugs:
          - url: 1289085
          - url: 1289085, 1289087
            desc: stuff about the bugs
      CVE-2016-5270:
        title: Another sampile title, this time with more length!
        impact: High
        reporter: A Nameless Evilcorp Employee
        description: Another short description
        bugs:
          - url: https://example.com/warning.html
            desc: A different site that is totally not bugzilla
    """)

YML_ADVISORY_MISSING_THINGS = dedent("""\
    announced: September 13, 2016
    fixed_in:
      - Firefox 49
    title: Security vulnerabilities fixed in Firefox 49
    description:
    advisories:
      CVE-2016-2827:
        title: A sample title for a CVE here
        impact: Low
        reporter: Reporty McReporterface
        description: |
          Short description <strong>with HTML</strong> and multiple lines!

          Can also have full breaks and ***markdown***!
      CVE-2016-5270:
        title: Another sampile title, this time with more length!
        impact: High
        reporter: A Nameless Evilcorp Employee
        description: Another short description
        bugs:
          - url: 1289085
            desc:
    """)
