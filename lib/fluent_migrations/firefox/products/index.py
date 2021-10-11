from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

products = "firefox/products.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/products/index.html, part {index}."""

    ctx.add_transforms(
        "firefox/products.ftl",
        "firefox/products.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("firefox-products-firefox-is-more-than-a-browser"),
                value=REPLACE(
                    products,
                    "Firefox is more than a browser",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-products-its-a-whole-family-of-products = {COPY(products, "It’s a whole family of products designed to keep you safer and smarter online.",)}
""",
            products=products,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-products-firefox-is-more-than-a-browser-emphasis"),
                value=REPLACE(
                    products,
                    "Firefox is <strong>more</strong> than a browser",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-products-firefox-monitor = { -brand-name-firefox-monitor }
firefox-products-see-if-your-personal-information = {COPY(products, "See if your personal information has been compromised in a corporate data breach, and sign up for future alerts.",)}
firefox-products-check-for-breaches = {COPY(products, "Check for breaches",)}
firefox-products-sign-up-for-breach-alerts = {COPY(products, "Sign up for breach alerts",)}
""",
            products=products,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-products-firefox-browsers"),
                value=REPLACE(
                    products,
                    "Firefox browsers",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-products-get-the-browsers-that-block"),
                value=REPLACE(
                    products,
                    "Get the browsers that block 2000+ data trackers automatically. Enhanced Tracking Protection comes standard in every Firefox browser.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-products-desktop = {COPY(products, "Desktop",)}
firefox-products-android = { -brand-name-android }
firefox-products-ios = { -brand-name-ios }
firefox-products-see-all-browsers = {COPY(products, "See all browsers",)}
firefox-products-firefox-lockwise = { -brand-name-firefox-lockwise }
firefox-products-keep-your-passwords-safe-and = {COPY(products, "Keep your passwords safe, and access them across all your synced devices.",)}
""",
            products=products,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-products-download-lockwise"),
                value=REPLACE(
                    products,
                    "Download Lockwise",
                    {
                        "Lockwise": TERM_REFERENCE("brand-name-lockwise"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-products-open-in-firefox"),
                value=REPLACE(
                    products,
                    "Open in Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-products-learn-more-about-lockwise"),
                value=REPLACE(
                    products,
                    "Learn more about Lockwise",
                    {
                        "Lockwise": TERM_REFERENCE("brand-name-lockwise"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-products-firefox-send = { -brand-name-firefox-send }
firefox-products-send-your-large-files-and = {COPY(products, "Send your large files and sensitive documents safely, up to 2.5G.",)}
firefox-products-send-a-file = {COPY(products, "Send a file",)}
firefox-products-pocket = { -brand-name-pocket }
firefox-products-discover-the-best-content = {COPY(products, "Discover the best content on the web — and consume it wherever and whenever you want.",)}
""",
            products=products,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-products-get-pocket"),
                value=REPLACE(
                    products,
                    "Get Pocket",
                    {
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-products-learn-more-about-pocket"),
                value=REPLACE(
                    products,
                    "Learn more about Pocket",
                    {
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-products-join-firefox-and-get-the-most"),
                value=REPLACE(
                    products,
                    "Join Firefox and get the most out of every product — across every device.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-products-already-have-an-account-sign"),
                value=REPLACE(
                    products,
                    "Already have an account? <a %(fxa_attr)s>Sign In</a> or <a %(accounts_attr)s>learn more</a> about joining Firefox.",
                    {
                        "%%": "%",
                        "%(fxa_attr)s": VARIABLE_REFERENCE("fxa_attr"),
                        "%(accounts_attr)s": VARIABLE_REFERENCE("accounts_attr"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ],
    )
