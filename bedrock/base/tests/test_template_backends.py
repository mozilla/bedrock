# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.template import TemplateDoesNotExist

import pytest

from bedrock.base.template.backends import SelectiveWagtailTemplateUsage


@pytest.mark.parametrize(
    "params, template_name, expect_template_match",
    (
        (
            {},
            "some_non_wagtail_template.html",
            False,
        ),
        (
            {},
            "wagtailadmin/admin_base.html",
            False,
        ),
        (
            {
                "CUSTOM_ALLOWED_DIRS": [
                    "wagtailadmin",
                    "wagtailcore",
                ],
            },
            "some_non_wagtail_template.html",
            False,
        ),
        (
            {
                "CUSTOM_ALLOWED_DIRS": [
                    "wagtailadmin",
                    "wagtailcore",
                ],
            },
            "wagtailadmin/admin_base.html",
            True,
        ),
    ),
    ids=[
        "no custom allowed dirs and no matching template specced, so no match",
        "no custom allowed dirs though a matching template specced, so no match",
        "custom allowed dirs, but no matching template specced, so no match",
        "custom allowed dirs and a matching template specced, so we get a match",
    ],
)
def test_selective_wagtail_template_usage(
    params,
    template_name,
    expect_template_match,
):
    params.update(
        **{
            "NAME": "test-setup",
            "OPTIONS": {},
            "DIRS": [],
            "APP_DIRS": True,
        }
    )
    backend = SelectiveWagtailTemplateUsage(params)

    try:
        backend.get_template(template_name)
    except TemplateDoesNotExist as te:
        if expect_template_match:
            # only complain if we are expecting a match
            raise te
