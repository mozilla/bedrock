# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.pocket.forms import NewsletterForm, newsletter_choices


def test_newsletter_choices():
    choices = newsletter_choices()
    assert choices == [("news", "news"), ("hits", "hits")]


def test_newsletter_form_uses_configured_choices():
    form = NewsletterForm()
    assert [x for x in form.fields["newsletter"].choices] == [("news", "news"), ("hits", "hits")]


def test_newsletter_form_required_fields__no_data():
    empty_form = NewsletterForm(data={})
    assert empty_form.is_valid() is False
    assert empty_form.errors == {
        "email": ["This field is required."],
        "newsletter": ["This field is required."],
    }


def test_newsletter_form_required_fields__sufficient_data():
    filled_form = NewsletterForm(
        data={
            "email": "test@example.com",
            "newsletter": "news",
        }
    )
    assert filled_form.is_valid()
