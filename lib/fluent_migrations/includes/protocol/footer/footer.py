from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

footer = "footer.lang"
main = "main.lang"


def migrate(ctx):
    """Migrate bedrock/base/templates/includes/protocol/footer/footer.html, part {index}."""

    ctx.add_transforms(
        "footer.ftl",
        "footer.ftl",
        transforms_from(
            """
footer-firefox = { -brand-name-firefox }
footer-privacy = {COPY(main, "Privacy",)}
footer-press = {COPY(footer, "Press",)}
footer-brand-standards = {COPY(footer, "Brand Standards",)}
footer-browsers = {COPY(footer, "Browsers",)}
footer-desktop = {COPY(main, "Desktop",)}
footer-mobile = {COPY(main, "Mobile",)}
footer-reality = { -brand-name-reality }
footer-enterprise = { -brand-name-enterprise }
footer-products = {COPY(footer, "Products",)}
footer-lockwise = { -brand-name-lockwise }
footer-monitor = { -brand-name-monitor }
footer-send = { -brand-name-send }
footer-pocket = { -brand-name-pocket }
footer-join = {COPY(footer, "Join",)}
footer-sign-up = {COPY(footer, "Sign Up",)}
footer-sign-in = {COPY(footer, "Sign In",)}
footer-benefits = {COPY(footer, "Benefits",)}
footer-developers = {COPY(footer, "Developers",)}
footer-developer-edition = { -brand-name-developer-edition }
footer-beta = { -brand-name-beta }
footer-nightly = { -brand-name-nightly }
""",
            footer=footer,
            main=main,
        ),
    )

    ctx.add_transforms(
        "footer.ftl",
        "footer.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("footer-nightly-for-android"),
                value=REPLACE(
                    "footer.lang",
                    "Nightly for Android",
                    {
                        "Nightly": TERM_REFERENCE("brand-name-nightly"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("footer-beta-for-android"),
                value=REPLACE(
                    "footer.lang",
                    "Beta for Android",
                    {
                        "Beta": TERM_REFERENCE("brand-name-beta"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("footer-visit-mozilla-corporations"),
                value=REPLACE(
                    "footer.lang",
                    "Visit <a %(moco_link)s>Mozilla Corporation’s</a> not-for-profit parent, the <a %(mofo_link)s>Mozilla Foundation</a>.",
                    {
                        "%%": "%",
                        "%(moco_link)s": VARIABLE_REFERENCE("moco_link"),
                        "%(mofo_link)s": VARIABLE_REFERENCE("mofo_link"),
                        "Mozilla Corporation": TERM_REFERENCE("brand-name-mozilla-corporation"),
                        "Mozilla Foundation": TERM_REFERENCE("brand-name-mozilla-foundation"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("footer-portions-of-this-content"),
                value=REPLACE(
                    "footer.lang",
                    'Portions of this content are ©1998–%(current_year)s by individual mozilla.org contributors. Content available under a <a rel="license" href="%(url)s">Creative Commons license</a>.',
                    {
                        "%%": "%",
                        "%(current_year)s": VARIABLE_REFERENCE("current_year"),
                        "%(url)s": VARIABLE_REFERENCE("url"),
                        "Creative Commons": TERM_REFERENCE("brand-name-creative-commons"),
                    },
                ),
            ),
        ],
    )

    ctx.add_transforms(
        "footer.ftl",
        "footer.ftl",
        transforms_from(
            """
footer-mozilla = { -brand-name-mozilla }
footer-company = {COPY(footer, "Company",)}
footer-about = {COPY(main, "About",)}
footer-press-center = {COPY(main, "Press Center",)}
footer-careers = {COPY(footer, "Careers",)}
footer-test-new-features = {COPY(footer, "Test New Features",)}
footer-mdn-web-docs = { -brand-name-mdn-web-docs }
footer-tools = {COPY(footer, "Tools",)}
footer-resources = {COPY(footer, "Resources",)}
footer-contact = {COPY(footer, "Contact",)}
footer-product-help = {COPY(footer, "Product Help",)}
footer-support = {COPY(footer, "Support",)}
footer-file-a-bug = {COPY(footer, "File a Bug",)}
footer-community-participation-guidelines = {COPY(footer, "Community Participation Guidelines",)}
footer-websites-privacy-notice = {COPY(main, "Website Privacy Notice",)}
footer-websites-cookies = {COPY(main, "Cookies",)}
footer-websites-legal = {COPY(main, "Legal",)}
footer-language = {COPY(main, "Language",)}
footer-go = {COPY(main, "Go",)}
footer-twitter = { -brand-name-twitter }
footer-instagram = { -brand-name-instagram }
footer-youtube = { -brand-name-youtube }
""",
            footer=footer,
            main=main,
        ),
    )
