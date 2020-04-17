from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

all_unified = "firefox/all-unified.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/all-unified.html, part {index}."""

    ctx.add_transforms(
        "firefox/all.ftl",
        "firefox/all.ftl",
        transforms_from("""
firefox-all-check-the-system-requirements = {COPY(all_unified, "Check the system requirements",)}
firefox-all-release-notes = {COPY(all_unified, "Release notes",)}
firefox-all-source-code = {COPY(all_unified, "Source code",)}
firefox-all-need-help = {COPY(all_unified, "Need help?",)}
firefox-all-which-browser-would = {COPY(all_unified, "Which browser would you like to download?",)}
firefox-all-get-help = {COPY(all_unified, "Get help",)}
firefox-all-you-are-about-to-download = {COPY(all_unified, "You are about to download:",)}
firefox-all-browser = {COPY(all_unified, "Browser:",)}
firefox-all-platform = {COPY(all_unified, "Platform:",)}
firefox-all-language = {COPY(all_unified, "Language:",)}
firefox-all-sorry-we-couldnt-find = {COPY(all_unified, "Sorry, we couldn’t find the download you’re looking for. Please try again, or select a download from the list below.",)}
firefox-all-the-pre-alpha-version = {COPY(all_unified, "The pre-alpha version for power users who like to hunt crashes and test new features as they’re coded.",)}
firefox-all-64-bit-installers = {COPY(all_unified, "64-bit installers",)}
firefox-all-choose-a-64-bit-installer = {COPY(all_unified, "Choose a 64-bit installer for computers with 64-bit processors, which allow them to allocate more RAM to individual programs — particularly important for games and other demanding applications.",)}
firefox-all-32-bit-installers = {COPY(all_unified, "32-bit installers",)}
""", all_unified=all_unified) + [
            FTL.Message(
                id=FTL.Identifier("firefox-all-download-the-firefox"),
                value=REPLACE(
                    all_unified,
                    "Download the Firefox Browser in English (US) and more than 90 other languages",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-all-everyone-deserves-access"),
                value=REPLACE(
                    all_unified,
                    "Everyone deserves access to the internet — your language should never be a barrier. That’s why — with the help of dedicated volunteers around the world — we make the Firefox Browser available in more than 90 languages.",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-all-choose-which-firefox"),
                value=REPLACE(
                    all_unified,
                    "Choose which Firefox Browser to download in your language",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-all-firefox-privacy-notice"),
                value=REPLACE(
                    all_unified,
                    "Firefox Privacy Notice",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-all-learn-about-firefox"),
                value=REPLACE(
                    all_unified,
                    "Learn about Firefox browsers",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-all-the-standard-firefox"),
                value=REPLACE(
                    all_unified,
                    "The standard Firefox browser — fast and private. If you’re not sure which Firefox to choose, choose this.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-all-get-a-sneak-peek-at"),
                value=REPLACE(
                    all_unified,
                    "Get a sneak peek at the latest Firefox browser features before they’re released.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-all-test-your-sites-against"),
                value=REPLACE(
                    all_unified,
                    "Test your sites against soon-to-be-released Firefox browser features with powerful, flexible DevTools that are on by default.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-all-count-on-stability-and"),
                value=REPLACE(
                    all_unified,
                    "Count on stability and ease of use with this Firefox browser built for enterprise.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-all-windows-installers-for"),
                value=REPLACE(
                    all_unified,
                    "Windows installers for corporate IT that simplify the configuration, deployment and management of the Firefox Browser.",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-all-choose-a-32-bit-installer"),
                value=REPLACE(
                    all_unified,
                    "Choose a 32-bit installer for computers with 32-bit processors — or for older or less powerful computers. <a href=\"%(url)s\">If you aren’t sure</a> whether to choose a 64-bit or 32-bit installer, we recommend you go with 32-bit.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-all-download-product-for"),
                value=REPLACE(
                    all_unified,
                    "Download %(product_label)s for %(platform)s in %(locale)s",
                    {
                        "%%": "%",
                        "%(product_label)s": VARIABLE_REFERENCE("product_label"),
                        "%(platform)s": VARIABLE_REFERENCE("platform"),
                        "%(locale)s": VARIABLE_REFERENCE("locale"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-all-msi-installers = {COPY(all_unified, "MSI installers",)}
firefox-all-which-version = {COPY(all_unified, "Which version would you like?",)}
firefox-all-select-your-preferred-installer = {COPY(all_unified, "Select your preferred installer",)}
firefox-all-select-your-preferred-language = {COPY(all_unified, "Select your preferred language",)}
firefox-all-learn-about-installers = {COPY(all_unified, "Learn about installers",)}
firefox-all-product-firefox = { -brand-name-firefox }
firefox-all-product-firefox-beta = { -brand-name-firefox-beta }
firefox-all-product-firefox-developer = { -brand-name-firefox-developer-edition }
firefox-all-product-firefox-nightly = { -brand-name-firefox-nightly }
firefox-all-product-firefox-esr = { -brand-name-firefox-extended-support-release }
firefox-all-product-firefox-android = { -brand-name-firefox } { -brand-name-android }
firefox-all-product-firefox-android-beta = { -brand-name-firefox } { -brand-name-android } { -brand-name-beta }
firefox-all-product-firefox-android-nightly = { -brand-name-firefox } { -brand-name-android } { -brand-name-nightly }
""", all_unified=all_unified)
        )
