from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

download_button = "firefox/includes/download-button.lang"
download_button = "download_button.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/includes/download-button.html, part {index}."""

    ctx.add_transforms(
        "download_button.ftl",
        "download_button.ftl",
        transforms_from("""
download-button-download-now = {COPY(download_button, "Download now",)}
download-button-free-download = {COPY(download_button, "Free Download",)}
download-button-firefox-beta = { -brand-name-firefox-beta }
download-button-firefox-aurora = { -brand-name-firefox-aurora }
download-button-firefox-developer-edition = <span>{ -brand-name-firefox }</span> { -brand-name-developer-edition }
download-button-firefox-nightly = { -brand-name-firefox-nightly }
download-button-supported-devices = {COPY(download_button, "Supported Devices",)}
download-button-whats-new = {COPY(download_button, "What’s New",)}
download-button-systems-languages = {COPY(download_button, "Systems &amp; Languages",)}
download-button-recommended = {COPY(download_button, "Recommended",)}
""", download_button=download_button) + [
            FTL.Message(
                id=FTL.Identifier("download-button-mozilla-no-longer-provides"),
                value=REPLACE(
                    download_button,
                    "<a href=\"%(url)s\">Mozilla no longer provides security updates for Firefox on Windows XP or Vista</a>, but you can still download the final Windows 32-bit version below.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "XP": TERM_REFERENCE("brand-name-xp"),
                        "Vista": TERM_REFERENCE("brand-name-vista"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-please-follow-these"),
                value=REPLACE(
                    download_button,
                    "Please follow <a href=\"%(url)s\">these instructions</a> to install Firefox.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-your-system-does-not"),
                value=REPLACE(
                    download_button,
                    "Your system doesn't meet the <a href=\"%(url)s\">requirements</a> to run Firefox.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
    )

    ctx.add_transforms(
        "download_button.ftl",
        "download_button.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("download-button-firefox-other-platforms"),
                value=REPLACE(
                    "download_button.lang",
                    "Firefox for Other Platforms & Languages",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-update-your-firefox"),
                value=REPLACE(
                    "download_button.lang",
                    "Update your Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-get-firefox-android"),
                value=REPLACE(
                    "download_button.lang",
                    "Get Firefox for Android",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-get-firefox-ios"),
                value=REPLACE(
                    "download_button.lang",
                    "Get Firefox for iOS",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-google-play"),
                value=REPLACE(
                    "download_button.lang",
                    "Get it on Google Play",
                    {
                        "Google Play": TERM_REFERENCE("brand-name-google-play"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-free-google-play"),
                value=REPLACE(
                    "download_button.lang",
                    "Get it free on Google Play",
                    {
                        "Google Play": TERM_REFERENCE("brand-name-google-play"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-app-store"),
                value=REPLACE(
                    "download_button.lang",
                    "Get it free from the App Store",
                    {
                        "App Store": TERM_REFERENCE("brand-name-app-store"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-download-app-store"),
                value=REPLACE(
                    "download_button.lang",
                    "Download on the App Store",
                    {
                        "App Store": TERM_REFERENCE("brand-name-app-store"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-download-firefox"),
                value=REPLACE(
                    "download_button.lang",
                    "Download Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-your-system-may"),
                value=REPLACE(
                    "download_button.lang",
                    "Your system may not meet the requirements for Firefox, but you can try one of these versions:",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-firefox-beta-android"),
                value=REPLACE(
                    "download_button.lang",
                    "<span>Firefox Beta</span> for Android",
                    {
                        "Firefox Beta": TERM_REFERENCE("brand-name-firefox-beta"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-firefox-aurora-android"),
                value=REPLACE(
                    "download_button.lang",
                    "<span>Firefox Aurora</span> for Android",
                    {
                        "Firefox Aurora": TERM_REFERENCE("brand-name-firefox-aurora"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-firefox-nightly-android"),
                value=REPLACE(
                    "download_button.lang",
                    "<span>Firefox Nightly</span> for Android",
                    {
                        "Firefox Nightly": TERM_REFERENCE("brand-name-firefox-nightly"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-firefox-android"),
                value=REPLACE(
                    "download_button.lang",
                    "<span>Firefox</span> for Android",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-firefox-ios"),
                value=REPLACE(
                    "download_button.lang",
                    "<span>Firefox</span> for iOS",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("download-button-firefox-privacy"),
                value=REPLACE(
                    "download_button.lang",
                    "Firefox Privacy",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
    )
