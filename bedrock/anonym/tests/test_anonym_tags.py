# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from bedrock.anonym.models import AnonymCaseStudyItemPage
from bedrock.anonym.templatetags.anonym_tags import case_studies

pytestmark = [
    pytest.mark.django_db,
]


def test_should_use_simple_auth(anonym_index_page):
    """Test the case_studies template tag."""
    # When there are no AnonymCaseStudyItemPages, case_studies() returns an empty QuerySet.
    assert len(case_studies()) == 0

    # Create a live AnonymCaseStudyItemPage.
    case_study_live = AnonymCaseStudyItemPage(
        slug="test-case-study-page-live",
        title="Test Case Study Page Live",
    )
    anonym_index_page.add_child(instance=case_study_live)
    case_study_live.save_revision().publish()
    # Create a draft AnonymCaseStudyItemPage.
    case_study_draft = AnonymCaseStudyItemPage(
        slug="test-case-study-page-draft",
        title="Test Case Study Page Draft",
        live=False,
    )
    anonym_index_page.add_child(instance=case_study_draft)

    # case_studies() should return only the case_study_live.
    assert list(case_studies()) == [case_study_live]
