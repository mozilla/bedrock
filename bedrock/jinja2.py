# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from jinja2 import Environment

from bedrock.anonym.templatetags.anonym_tags import case_studies


def bedrock_environment(**options):
    env = Environment(**options)
    env.globals["anonym_case_studies"] = case_studies

    return env
