# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re


def migration_name(template):
    'Derive migration name from template name'
    for parent in template.parents:
        if parent.name == 'templates':
            break
    return template.relative_to(parent).with_suffix('')


ADD_LANG_RE = re.compile(r'{% add_lang_files (.*?) %}')
GETTEXT_RE = re.compile(r'\b_\([\'"](?P<string>.+?)[\'"]\)'
                        r'(\s*\|\s*format\((?P<args>\w.+?)\))?', re.S)
TRANS_BLOCK_RE = re.compile(r'{%-?\s+trans\s+((?P<args>\w.+?)\s+)?-?%\}\s*'
                            r'(?P<string>.+?)'
                            r'\s*{%-?\s+endtrans\s+-?%\}', re.S)
