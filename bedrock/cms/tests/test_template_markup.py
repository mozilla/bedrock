# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import re
from collections import defaultdict

from django.conf import settings

from wagtail.images.models import Filter

from bedrock.cms.models.images import AUTOMATIC_RENDITION_FILTER_SPECS

wagtail_jinja_image_tag_regex_pattern = re.compile(
    r"(?:(?<!_)image|srcset_image)\("  # `image(` or `srcset_image(`, but not other `*_image(` calls such as
    # macros like hero_image(). Deliberately excludes `picture(`: every `picture(` call in the codebase is
    # the unrelated, locally-defined `url=`/`sources=` helper, not Wagtail's image-filterspec `picture()`.
    r".*?"  # anything, such as the dot-pattern to get hold of the image on a block; non-greedy so this
    # stops at the first quoted arg instead of skipping past it to a later one (calls span multiple
    # lines, so DOTALL is needed for this to cross line breaks at all)
    r"(?<!=)\"([\w\-{},.|]+)\""  # a filter spec pattern as an arg (eg "fill-200x200", "width-1200", or the
    # brace-expanded "fill-{400x200,600x300}"), but not a key=value attr pair. Required to be non-empty so a
    # call with no literal spec (e.g. a variable) can't match an unrelated quoted string later in the file.
    r".*?\)",  # any other optional args to the image() call and its closing paren
    re.DOTALL,
)


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
                for spec in Filter.expand_spec(match):
                    if spec not in AUTOMATIC_RENDITION_FILTER_SPECS:
                        failures[template_name].append(spec)

    expected_fail = failures.pop("bedrock/cms/templates/cms/for_tests/test_template__invalid_image_inclusion.html", None)
    if expected_fail is None:
        assert False, "Failed to detect deliberately invalid filter spec in image() call"
    if len(failures.keys()) > 0:
        assert False, f"Found templates with invalid image() helper parameters: {failures}"
