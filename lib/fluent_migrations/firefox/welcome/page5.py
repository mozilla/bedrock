from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

page5 = "firefox/welcome/page5.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/welcome/page5.html, part {index}."""

    ctx.add_transforms(
        "firefox/welcome/page5.ftl",
        "firefox/welcome/page5.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("welcome-page5-firefox-lockwise-password"),
                value=REPLACE(
                    page5,
                    "Firefox Lockwise — password manager — take your passwords everywhere",
                    {
                        "Firefox Lockwise": TERM_REFERENCE("brand-name-firefox-lockwise"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page5-theres-an-easier-way-to-deal = {COPY(page5, "There’s an easier way to deal with your passwords",)}
""",
            page5=page5,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("welcome-page5-let-firefox-save-them-for"),
                value=REPLACE(
                    page5,
                    "Let Firefox save them for you. Then use Firefox Lockwise to safely access your passwords across all your apps, on all of your devices.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Firefox Lockwise": TERM_REFERENCE("brand-name-firefox-lockwise"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("welcome-page5-get-the-lockwise-app"),
                value=REPLACE(
                    page5,
                    "Get the Lockwise App",
                    {
                        "Lockwise": TERM_REFERENCE("brand-name-lockwise"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("welcome-page5-get-firefox-lockwise-on-your"),
                value=REPLACE(
                    page5,
                    "Get Firefox Lockwise on your Phone",
                    {
                        "Firefox Lockwise": TERM_REFERENCE("brand-name-firefox-lockwise"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page5-send-the-download-link-right = {COPY(page5, "Send the download link right to your phone or email.",)}
""",
            page5=page5,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("welcome-page5-download-firefox-lockwise"),
                value=REPLACE(
                    page5,
                    "Download Firefox Lockwise for your smartphone and tablet.",
                    {
                        "Firefox Lockwise": TERM_REFERENCE("brand-name-firefox-lockwise"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page5-scan-this-qr-code = {COPY(page5, "Scan this QR code",)}
welcome-page5-firefox-lockwise = { -brand-term-firefox-lockwise }
welcome-page5-sync-up-safely = {COPY(page5, "Sync up safely",)}
welcome-page5-with-256-bit-encryption-your = {COPY(page5, "With 256-bit encryption, your passwords always travel to your devices securely.",)}
welcome-page5-no-more-making-up-new-passwords = {COPY(page5, "No more making up new passwords",)}
""",
            page5=page5,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("welcome-page5-lockwise-will-recommend-new"),
                value=REPLACE(
                    page5,
                    "Lockwise will recommend new, strong passwords whenever you set up a new login.",
                    {
                        "Lockwise": TERM_REFERENCE("brand-name-lockwise"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page5-help-during-a-breach = {COPY(page5, "Help during a breach",)}
""",
            page5=page5,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("welcome-page5-lockwise-will-let-you-know"),
                value=REPLACE(
                    page5,
                    "Lockwise will let you know if your saved logins have been part of a corporate data breach, so you can change them asap.",
                    {
                        "Lockwise": TERM_REFERENCE("brand-name-lockwise"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page5-why-am-i-seeing-this = {COPY(page5, "Why am I seeing this?",)}
""",
            page5=page5,
        ),
    )
