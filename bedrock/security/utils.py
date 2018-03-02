# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import codecs
import re
from collections import OrderedDict
from datetime import date

import yaml
from django.template.loader import render_to_string
from markdown import markdown


FILENAME_RE = re.compile('mfsa(\d{4}-\d{2,3})\.(md|yml)$')


def mfsa_id_from_filename(filename):
    match = FILENAME_RE.search(filename)
    if match:
        return match.group(1)

    return None


def parse_md_front_matter(lines):
    """Return the YAML and MD sections.

    :param: lines iterator
    :return: str YAML, str Markdown
    """
    # fm_count: 0: init, 1: in YAML, 2: in Markdown
    fm_count = 0
    yaml_lines = []
    md_lines = []
    for line in lines:
        # first line we care about is FM start
        if fm_count < 2 and line.strip() == '---':
            fm_count += 1
            continue

        if fm_count == 1:
            yaml_lines.append(line)

        if fm_count == 2:
            md_lines.append(line)

    if fm_count < 2:
        raise ValueError('Front Matter not found.')

    return ''.join(yaml_lines), ''.join(md_lines)


def parse_md_file(file_name):
    """Return the YAML and MD sections for file_name."""
    with codecs.open(file_name, encoding='utf8') as fh:
        yamltext, mdtext = parse_md_front_matter(fh)

    data = yaml_ordered_safe_load(yamltext)
    if 'mfsa_id' not in data:
        mfsa_id = mfsa_id_from_filename(file_name)
        if mfsa_id:
            data['mfsa_id'] = mfsa_id
    return data, markdown(mdtext)


def parse_yml_file_base(file_name):
    with codecs.open(file_name, encoding='utf8') as fh:
        return yaml_ordered_safe_load(fh)


def parse_yml_file(file_name):
    data = parse_yml_file_base(file_name)
    if 'mfsa_id' not in data:
        mfsa_id = mfsa_id_from_filename(file_name)
        if mfsa_id:
            data['mfsa_id'] = mfsa_id

    return data, generate_yml_advisories_html(data)


def update_advisory_bugs(advisory):
    if advisory.get('bugs', None):
        for bug in advisory['bugs']:
            if not bug.get('desc', None):
                bug['desc'] = 'Bug %s' % bug['url']
            bug['url'] = parse_bug_url(bug['url'])


def generate_yml_advisories_html(data):
    html = []
    if data.get('description', None):
        html.append(markdown(data['description']))

    for cve, advisory in data['advisories'].items():
        advisory['id'] = cve
        advisory['impact_class'] = advisory['impact'].lower().split(None, 1)[0]
        update_advisory_bugs(advisory)
        html.append(render_to_string('security/partials/cve.html', advisory))

    return '\n\n'.join(html)


def parse_bug_url(url):
    """
    Take a bug number, list of bug numbers, or a URL and output a URL.

    url could be a bug number, a comma separated list of bug numbers, or a URL.
    """
    # could be an int
    url = str(url).strip()
    if re.match(r'^\d+$', url):
        url = 'https://bugzilla.mozilla.org/show_bug.cgi?id=%s' % url
    elif re.match(r'^[\d\s,]+$', url):
        url = re.sub(r'\s', '', url).replace(',', '%2C')
        url = 'https://bugzilla.mozilla.org/buglist.cgi?bug_id=%s' % url

    return url


def yaml_ordered_safe_load(stream, object_pairs_hook=OrderedDict):
    """
    Load YAML mappings as OrderedDicts

    from http://stackoverflow.com/a/21912744
    """
    class OrderedLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                                  construct_mapping)
    return yaml.load(stream, OrderedLoader)


def check_hof_data(data):
    """Check the HOF Data and raise ValueError if there's a problem."""
    if not data:
        raise ValueError('HOF Data is empty')

    if 'names' not in data:
        raise ValueError('Missing required key: names')

    if len(data['names']) < 100:
        raise ValueError('Suspiciously few names returned. File may be corrupted.')

    for name in data['names']:
        if 'name' not in name:
            raise ValueError('Key "name" required for every entry in "names"')
        if 'date' not in name:
            raise ValueError('Key "date" required for every entry in "names"')
        if not isinstance(name['date'], date):
            raise ValueError('Key "date" should be formatted as a date (YYYY-MM-DD): %s' % name['date'])
        if name['date'] < date(2004, 11, 9):
            raise ValueError('A date can\'t be set before the launch date of Firefox')
