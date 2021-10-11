from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

thank_you = "firefox/retention/thank-you.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/retention/thank-you.html, part {index}."""

    ctx.add_transforms(
        "firefox/retention/thank-you.ftl",
        "firefox/retention/thank-you.ftl",
        transforms_from(
            """
thank-you-thank-you = {COPY(thank_you, "Thank You",)}
thank-you-thank-you-page = {COPY(thank_you, "Thank you page.",)}
thank-you-its-all-thanks-to-you = {COPY(thank_you, "It’s all thanks to you",)}
""",
            thank_you=thank_you,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("thank-you-choosing-firefox-helps"),
                value=REPLACE(
                    thank_you,
                    "Choosing Firefox helps Mozilla make the Internet a better place. Here’s what you can do next:",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("thank-you-make-firefox-your-default"),
                value=REPLACE(
                    thank_you,
                    "Make Firefox your default browser",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
thank-you-1-min-action = {COPY(thank_you, "1 min action",)}
thank-you-set-as-your-default = {COPY(thank_you, "Set as your default",)}
""",
            thank_you=thank_you,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("thank-you-get-firefox-on-your-phone"),
                value=REPLACE(
                    thank_you,
                    "Get Firefox on your phone",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
thank-you-2-min-install = {COPY(thank_you, "2 min install",)}
""",
            thank_you=thank_you,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("thank-you-download-firefox"),
                value=REPLACE(
                    thank_you,
                    "Download Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("thank-you-tell-your-friends-about"),
                value=REPLACE(
                    thank_you,
                    "Tell your friends about Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
thank-you-1-min-share = {COPY(thank_you, "1 min share",)}
""",
            thank_you=thank_you,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("thank-you-join-me-in-the-fight-for"),
                value=REPLACE(
                    thank_you,
                    "Join me in the fight for an open web by choosing Firefox!",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
thank-you-send-a-tweet = {COPY(thank_you, "Send a tweet",)}
thank-you-make-the-internet-a-safer = {COPY(thank_you, "Make the Internet a safer place",)}
thank-you-4-min-read = {COPY(thank_you, "4 min read",)}
thank-you-stay-in-touch-for-more = {COPY(thank_you, "Stay in touch for more cool stuff",)}
""",
            thank_you=thank_you,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("thank-you-get-the-latest-greatest"),
                value=REPLACE(
                    thank_you,
                    "Get the latest & greatest from Firefox delivered straight to your inbox.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ],
    )
