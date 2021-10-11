from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

home_master = "firefox/home-master.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/home/index-master.html, part {index}."""

    ctx.add_transforms(
        "firefox/home.ftl",
        "firefox/home.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("firefox-home-firefox-protect-your"),
                value=REPLACE(
                    home_master,
                    "Firefox - Protect your life online with privacy-first products",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-home-firefox-is-more-than"),
                value=REPLACE(
                    home_master,
                    "Firefox is more than a browser. Learn more about Firefox products that handle your data with respect and are built for privacy anywhere you go online.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-home-the-browser-is-just = {COPY(home_master, "The browser is just the beginning",)}
firefox-home-meet-our-family-of = {COPY(home_master, "Meet our family of products",)}
""",
            home_master=home_master,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-home-get-trackers-off"),
                value=REPLACE(
                    home_master,
                    "Get 2,000+ trackers off your trail — including Facebook",
                    {
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-home-know-when-hackers-strike = {COPY(home_master, "Know when hackers strike — and stay a step ahead",)}
firefox-home-start-getting-breach = {COPY(home_master, "Start getting breach reports",)}
firefox-home-keep-your-passwords = {COPY(home_master, "Keep your passwords safe on every device",)}
""",
            home_master=home_master,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-home-learn-more-about-lockwise"),
                value=REPLACE(
                    home_master,
                    "Learn more about Lockwise",
                    {
                        "Lockwise": TERM_REFERENCE("brand-name-lockwise"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-home-get-the-respect-you = {COPY(home_master, "Get the <strong>respect</strong> you deserve",)}
""",
            home_master=home_master,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-home-every-single-firefox"),
                value=REPLACE(
                    home_master,
                    "Every single Firefox product honors our Personal Data Promise: <strong>Take less. Keep it safe. No secrets.</strong>",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-home-share-large-files-without = {COPY(home_master, "Share large files without prying eyes",)}
firefox-home-start-sending-files = {COPY(home_master, "Start sending files safely",)}
firefox-home-trade-clickbait-for = {COPY(home_master, "Trade clickbait for quality content",)}
""",
            home_master=home_master,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-home-learn-more-about-pocket"),
                value=REPLACE(
                    home_master,
                    "Learn more about Pocket",
                    {
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-home-one-login-all-your = {COPY(home_master, "One login. All your devices. A family of products that respect your <strong>privacy</strong>.",)}
""",
            home_master=home_master,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-home-learn-more-about-joining"),
                value=REPLACE(
                    home_master,
                    "Learn more about joining Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-home-get-the-browser-extension = {COPY(home_master, "Get the browser extension",)}
""",
            home_master=home_master,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-home-get-the-facebook-container"),
                value=REPLACE(
                    home_master,
                    "Get the Facebook Container extension",
                    {
                        "Facebook Container": TERM_REFERENCE("brand-name-facebook-container"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-home-download-the-browser = {COPY(home_master, "Download the browser",)}
firefox-home-download-the-app = {COPY(home_master, "Download the app",)}
firefox-home-desktop = {COPY(home_master, "Desktop",)}
firefox-home-browsers = {COPY(home_master, "Browsers",)}
firefox-home-android = { -brand-name-android }
firefox-home-ios = { -brand-name-ios }
firefox-home-monitor = { -brand-name-monitor }
firefox-home-lockwise = { -brand-name-lockwise }
firefox-home-send = { -brand-name-send }
firefox-home-mozilla = { -brand-name-mozilla }
firefox-home-firefox-browser = { -brand-name-firefox-browser }
firefox-home-firefox-monitor = { -brand-name-firefox-monitor }
firefox-home-firefox-lockwise = { -brand-name-firefox-lockwise }
firefox-home-firefox-send = { -brand-name-firefox-send }
firefox-home-pocket = { -brand-name-pocket }
""",
            home_master=home_master,
        ),
    )
