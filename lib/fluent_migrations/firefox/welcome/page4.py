from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

page4 = "firefox/welcome/page4.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/welcome/page4.html, part {index}."""

    ctx.add_transforms(
        "firefox/welcome/page4.ftl",
        "firefox/welcome/page4.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("welcome-page4-download-the-firefox-browser"),
                value=REPLACE(
                    page4,
                    "Download the Firefox Browser on your Mobile for iOS and Android",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("welcome-page4-wallet-keys-phone-firefox"),
                value=REPLACE(
                    page4,
                    "Wallet. Keys. Phone. <strong>Firefox.</strong>",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page4-take-privacy-with-you-on-every = {COPY(page4, "Take privacy with you on every device — and leave the data trackers behind.",)}
""",
            page4=page4,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("welcome-page4-get-the-firefox-app"),
                value=REPLACE(
                    page4,
                    "Get the Firefox App",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("welcome-page4-get-firefox-on-your-phone"),
                value=REPLACE(
                    page4,
                    "Get Firefox on your Phone",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page4-send-the-download-link-right = {COPY(page4, "Send the download link right to your phone or email.",)}
""",
            page4=page4,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("welcome-page4-download-firefox-for-your"),
                value=REPLACE(
                    page4,
                    "Download Firefox for your smartphone and tablet.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("welcome-page4-firefox-private-safe-browser"),
                value=REPLACE(
                    page4,
                    "“Firefox: Private, Safe Browser” on iOS or Android.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page4-get-data-trackers-off-your = {COPY(page4, "Get data trackers off your trail",)}
""",
            page4=page4,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("welcome-page4-enhanced-tracking-protection"),
                value=REPLACE(
                    page4,
                    'Enhanced Tracking Protection <a href="%(privacy)s">blocks 2000+ trackers</a> from chasing you around the web.',
                    {
                        "%%": "%",
                        "%(privacy)s": VARIABLE_REFERENCE("privacy"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page4-leave-no-trace = {COPY(page4, "Leave no trace",)}
welcome-page4-automatically-clear-your-history = {COPY(page4, "Automatically clear your history and cookies with Private Browsing mode.",)}
welcome-page4-take-it-all-with-you = {COPY(page4, "Take it all with you",)}
welcome-page4-dont-walk-out-the-door-without = {COPY(page4, "Don’t walk out the door without your bookmarks, tabs, notes, and passwords.",)}
welcome-page4-why-am-i-seeing-this = {COPY(page4, "Why am I seeing this?",)}
""",
            page4=page4,
        ),
    )
