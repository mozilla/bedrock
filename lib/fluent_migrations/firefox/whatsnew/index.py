from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

index = "firefox/whatsnew/index.lang"
whatsnew = "firefox/whatsnew.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/whatsnew/index.html, part {index}."""

    ctx.add_transforms(
        "firefox/whatsnew/whatsnew-s2d.ftl",
        "firefox/whatsnew/whatsnew-s2d.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("whatsnew-s2d-download-firefox-for-android"),
                value=REPLACE(
                    whatsnew,
                    "Download Firefox for Android and iOS",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
whatsnew-s2d-want-privacy-on-every-device = {COPY(whatsnew, "Want privacy on every device?",)}
""",
            whatsnew=whatsnew,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("whatsnew-s2d-you-got-it-get-firefox-for"),
                value=REPLACE(
                    whatsnew,
                    "You got it. Get Firefox for mobile.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("whatsnew-s2d-send-firefox-to-your-phone"),
                value=REPLACE(
                    whatsnew, "Send Firefox to your phone<br> and unleash your Internet.", {"Firefox": TERM_REFERENCE("brand-name-firefox")}
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("whatsnew-s2d-download-firefox-for-your"),
                value=REPLACE(
                    whatsnew,
                    "Download Firefox for your smartphone and tablet.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ],
    )
