from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

set_default_thanks = "firefox/set-default-thanks.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/set-as-default/thanks.html, part {index}."""

    ctx.add_transforms(
        "firefox/set-as-default/thanks.ftl",
        "firefox/set-as-default/thanks.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("set-as-default-thanks-set-as-default-thanks-for-choosing-firefox"),
                value=REPLACE(
                    set_default_thanks,
                    "Thanks for choosing Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("set-as-default-thanks-success-your-default-browser"),
                value=REPLACE(
                    set_default_thanks,
                    "Success! Your default browser is set to Firefox.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("set-as-default-thanks-looks-like-youre-using-a"),
                value=REPLACE(
                    set_default_thanks,
                    "Looks like you’re using a different browser right now. Make sure you have Firefox downloaded on your device.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("set-as-default-thanks-youre-almost-done-just-change"),
                value=REPLACE(
                    set_default_thanks,
                    "You’re almost done. Just change your default browser to Firefox in the settings panel on your screen.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
set-as-default-thanks-having-trouble-setting-your = {COPY(set_default_thanks, "Having trouble setting your default browser?",)}
""",
            set_default_thanks=set_default_thanks,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("set-as-default-thanks-heres-everything-you-need-android"),
                value=REPLACE(
                    set_default_thanks,
                    'Here’s everything you need to know about setting your default browser on <a href="%(android)s">Android devices</a>.',
                    {
                        "%%": "%",
                        "%(android)s": VARIABLE_REFERENCE("android"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("set-as-default-thanks-heres-everything-you-need-ios"),
                value=REPLACE(
                    set_default_thanks,
                    'Here’s everything you need to know about setting your default browser on <a href="%(ios)s">iOS devices</a>.',
                    {
                        "%%": "%",
                        "%(ios)s": VARIABLE_REFERENCE("ios"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
set-as-default-thanks-youre-all-set = {COPY(set_default_thanks, "You’re all set.",)}
""",
            set_default_thanks=set_default_thanks,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("set-as-default-thanks-get-firefox-for-mobile"),
                value=REPLACE(
                    set_default_thanks,
                    "Get Firefox for mobile",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
set-as-default-thanks-travel-the-internet-with = {COPY(set_default_thanks, "Travel the internet with protection on all your devices.",)}
set-as-default-thanks-download-the-app = {COPY(set_default_thanks, "Download the app",)}
""",
            set_default_thanks=set_default_thanks,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("set-as-default-thanks-join-firefox"),
                value=REPLACE(
                    set_default_thanks,
                    "Join Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
set-as-default-thanks-sign-up-for-a-free-account = {COPY(set_default_thanks, "Sign up for a free account and sync all your passwords, browsing history, and preferences across your devices.",)}
set-as-default-thanks-get-an-account = {COPY(set_default_thanks, "Get an Account",)}
set-as-default-thanks-having-trouble = {COPY(set_default_thanks, "Having trouble?",)}
""",
            set_default_thanks=set_default_thanks,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("set-as-default-thanks-heres-everything-you-need-android-desktop"),
                value=REPLACE(
                    set_default_thanks,
                    'Here’s everything you need to know about setting your default browser on <a href="%(android)s">Android devices</a> or <a href="%(desktop)s">desktop computers</a>.',
                    {
                        "%%": "%",
                        "%(android)s": VARIABLE_REFERENCE("android"),
                        "%(desktop)s": VARIABLE_REFERENCE("desktop"),
                    },
                ),
            ),
        ],
    )
