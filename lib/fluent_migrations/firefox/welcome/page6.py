from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

page6 = "firefox/welcome/page6.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/welcome/page6.html, part {index}."""

    ctx.add_transforms(
        "firefox/welcome/page6.ftl",
        "firefox/welcome/page6.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("welcome-page6-make-firefox-your-default"),
                value=REPLACE(
                    page6,
                    "Make Firefox your default browser",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page6-make-sure-youre-protected = {COPY(page6, "Make sure you’re protected, every time you get online",)}
""",
            page6=page6,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("welcome-page6-when-you-choose-firefox-you"),
                value=REPLACE(
                    page6,
                    "When you choose Firefox, you support a better web for you and everyone else. Now take the next step to protect yourself.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("welcome-page6-get-the-firefox-app"),
                value=REPLACE(
                    page6,
                    "Get the Firefox App",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("welcome-page6-get-firefox-on-your-phone"),
                value=REPLACE(
                    page6,
                    "Get Firefox on your Phone",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page6-scan-the-qr-code-to-get-started = {COPY(page6, "Scan the QR code to get started",)}
""",
            page6=page6,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("welcome-page6-qr-code-to-scan-for-firefox"),
                value=REPLACE(
                    page6,
                    "QR code to scan for Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page6-choose-automatic-privacy = {COPY(page6, "Choose automatic privacy",)}
""",
            page6=page6,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("welcome-page6-companies-keep-finding-new"),
                value=REPLACE(
                    page6,
                    "Companies keep finding new ways to poach your personal data. Firefox is the browser with a mission of finding new ways to protect you.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page6-choose-freedom-on-every-device = {COPY(page6, "Choose freedom on every device",)}
""",
            page6=page6,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("welcome-page6-firefox-is-fast-and-safe-on"),
                value=REPLACE(
                    page6,
                    "Firefox is fast and safe on Windows, iOS, Android, Linux… and across them all. You deserve choices in browsers and devices, instead of decisions made for you.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page6-choose-corporate-independence = {COPY(page6, "Choose corporate independence",)}
""",
            page6=page6,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("welcome-page6-firefox-is-the-only-major"),
                value=REPLACE(
                    page6,
                    "Firefox is the only major independent browser. Chrome, Edge and Brave are all built on Google code, which means giving Google even more control of the internet.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Brave": TERM_REFERENCE("brand-name-brave"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page6-why-am-i-seeing-this = {COPY(page6, "Why am I seeing this?",)}
""",
            page6=page6,
        ),
    )
