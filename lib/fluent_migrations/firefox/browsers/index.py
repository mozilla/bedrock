from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

browsers = "firefox/browsers.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/browsers/index.html, part {index}."""

    ctx.add_transforms(
        "firefox/browsers.ftl",
        "firefox/browsers.ftl",
        transforms_from(
            """
firefox-browsers-get-the-browsers-that-put = {COPY(browsers, "Get the browsers that put your privacy first — and always have",)}
""",
            browsers=browsers,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-browsers-get-the-privacy-you-deserve"),
                value=REPLACE(
                    browsers,
                    "Get the privacy you deserve. Enhanced Tracking Protection is automatic in every Firefox browser.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-browsers-get-the-browsers-strong = {COPY(browsers, "Get the <strong>browsers</strong> that put your privacy first — and always have",)}
firefox-browsers-desktop = {COPY(browsers, "Desktop",)}
""",
            browsers=browsers,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-browsers-seriously-private-browsing"),
                value=REPLACE(
                    browsers,
                    "Seriously private browsing. Firefox automatically blocks 2000+ online trackers from collecting information about what you do online.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-browsers-download-for-desktop = {COPY(browsers, "Download for Desktop",)}
firefox-browsers-mobile = {COPY(browsers, "Mobile",)}
firefox-browsers-take-the-same-level-of-privacy = {COPY(browsers, "Take the same level of privacy — plus your passwords, search history, open tabs and more — with you wherever you go.",)}
firefox-browsers-download-for-mobile = {COPY(browsers, "Download for Mobile",)}
firefox-browsers-send-me-a-link = {COPY(browsers, "Send me a link",)}
""",
            browsers=browsers,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-browsers-enterprise"),
                value=REPLACE(
                    browsers,
                    "Enterprise",
                    {
                        "Enterprise": TERM_REFERENCE("brand-name-enterprise"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-browsers-get-unmatched-data-protection = {COPY(browsers, "Get unmatched data protection with support cycles tailored to suit your company’s needs.",)}
""",
            browsers=browsers,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-browsers-enterprise-packages"),
                value=REPLACE(
                    browsers,
                    "Enterprise packages",
                    {
                        "Enterprise": TERM_REFERENCE("brand-name-enterprise"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-browsers-reality"),
                value=REPLACE(
                    browsers,
                    "Reality",
                    {
                        "Reality": TERM_REFERENCE("brand-name-reality"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-browsers-go-beyond-two-dimensions-and = {COPY(browsers, "Go beyond two dimensions and enjoy the best immersive content from around the web.",)}
""",
            browsers=browsers,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-browsers-build-sites-and-refine-your"),
                value=REPLACE(
                    browsers,
                    "Build sites and refine your code with Firefox <strong>DevTools</strong>",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "DevTools": TERM_REFERENCE("brand-name-devtools"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-browsers-learn-more-about-devtools"),
                value=REPLACE(
                    browsers,
                    "Learn more about DevTools",
                    {
                        "DevTools": TERM_REFERENCE("brand-name-devtools"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-browsers-join-firefox-and-get-the-most"),
                value=REPLACE(
                    browsers,
                    "Join Firefox and get the most out of every product — across every device.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-browsers-already-have-an-account-sign"),
                value=REPLACE(
                    browsers,
                    "Already have an account? <a %(fxa_attr)s>Sign In</a> or <a %(accounts_attr)s>learn more</a> about joining Firefox.",
                    {
                        "%%": "%",
                        "%(fxa_attr)s": VARIABLE_REFERENCE("fxa_attr"),
                        "%(accounts_attr)s": VARIABLE_REFERENCE("accounts_attr"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-browsers-android = { -brand-name-android }
firefox-browsers-ios = { -brand-name-ios }
firefox-browsers-developer-edition = { -brand-name-developer-edition }
""",
            browsers=browsers,
        ),
    )
