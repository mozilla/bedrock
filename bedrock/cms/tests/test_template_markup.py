import os
import re
from collections import defaultdict

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from django.conf import settings

from bedrock.cms.models.images import AUTOMATIC_RENDITION_FILTER_SPECS

wagtail_jinja_image_tag_regex_pattern = re.compile(r"(?<!_)image\(.*(?<!=)\"(?P<filter_spec>[\w\-]*)\".*\)")


def test_templates_only_contain_valid_image_tag_calls():
    """Because we have to pre-generate renditions of images, we must ensure
    that no template includes an image that is not an appropriate
    width - see cms.models.images.BedrockImage._pre_generate_expected_renditions
    for details.
    """

    # Gather all the templates
    template_config = settings.TEMPLATES[0]
    if template_config["BACKEND"] != "django_jinja.jinja2.Jinja2":
        # Be sure we're looking at the right dir
        assert False, "Template configuration has changed and this test is now misconfigured"

    template_dirs = template_config["DIRS"]

    template_names = []
    for dirname in template_dirs:
        for root, dirs, filenames in os.walk(dirname):
            for filename in filenames:
                if filename.endswith(".html"):
                    template_names.append(os.path.join(root, filename))

    failures = defaultdict(list)

    # now check each of them
    for template_name in template_names:
        with open(template_name) as fp:
            html = fp.read()
            matches = wagtail_jinja_image_tag_regex_pattern.findall(html)
            for match in matches:
                if match not in AUTOMATIC_RENDITION_FILTER_SPECS:
                    failures[template_name].append(match)

    expected_fail = failures.pop("bedrock/cms/templates/cms/for_tests/test_template__invalid_image_inclusion.html", None)
    if expected_fail is None:
        assert False, "Failed to detect deliberately invalid filter spec in image() call"
    if len(failures.keys()) > 0:
        assert False, f"Found templates with invalid image() helper parameters: {failures}"
