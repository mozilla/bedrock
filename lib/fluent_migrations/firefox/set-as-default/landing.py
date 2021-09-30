from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

whatsnew_73 = "firefox/whatsnew_73.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/set-as-default/landing-page.html, part {index}."""

    ctx.add_transforms(
        "firefox/set-as-default/landing.ftl",
        "firefox/set-as-default/landing.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("set-as-default-landing-make-firefox-your-default"),
                value=REPLACE(
                    whatsnew_73,
                    "Make Firefox your default browser",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
set-as-default-landing-make-sure-youre-protected = {COPY(whatsnew_73, "Make sure you’re protected, every time you get online",)}
""",
            whatsnew_73=whatsnew_73,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("set-as-default-landing-thanks-for-using-the"),
                value=REPLACE(
                    whatsnew_73,
                    "Thanks for using the latest Firefox browser. When you choose Firefox, you support a better web for you and everyone else. Now take the next step to protect yourself.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
set-as-default-landing-choose-automatic-privacy = {COPY(whatsnew_73, "Choose automatic privacy",)}
""",
            whatsnew_73=whatsnew_73,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("set-as-default-landing-companies-keep-finding"),
                value=REPLACE(
                    whatsnew_73,
                    "Companies keep finding new ways to poach your personal data. Firefox is the browser with a mission of finding new ways to protect you.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
set-as-default-landing-choose-freedom-on-every = {COPY(whatsnew_73, "Choose freedom on every device",)}
""",
            whatsnew_73=whatsnew_73,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("set-as-default-landing-firefox-is-fast-and"),
                value=REPLACE(
                    whatsnew_73,
                    "Firefox is fast and safe on Windows, iOS, Android, Linux…and across them all. You deserve choices in browsers and devices, instead of decisions made for you.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
set-as-default-landing-choose-corporate-independence = {COPY(whatsnew_73, "Choose corporate independence",)}
""",
            whatsnew_73=whatsnew_73,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("set-as-default-landing-firefox-is-the-only"),
                value=REPLACE(
                    whatsnew_73,
                    "Firefox is the only major independent browser. Chrome, Edge and Brave are all built on Google code, which means giving Google even more control of the internet.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Brave": TERM_REFERENCE("brand-name-brave"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("set-as-default-landing-the-internet-keeps"),
                value=REPLACE(
                    whatsnew_73,
                    "The internet keeps finding new ways to poach your personal data. Firefox is the only browser with a mission of finding new ways to protect you.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("set-as-default-landing-firefox-is-fast-no-interest"),
                value=REPLACE(
                    whatsnew_73,
                    "Firefox is fast and safe on Windows, iOS, Android, Linux...and across them all. We have no interest in locking you in or resetting your preferences.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("set-as-default-landing-firefox-is-the-only-major"),
                value=REPLACE(
                    whatsnew_73,
                    "Firefox is the only major independent browser. Chrome, Edge and Brave are all built with code from Google, the world’s largest ad network.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Brave": TERM_REFERENCE("brand-name-brave"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                    },
                ),
            ),
        ],
    )
