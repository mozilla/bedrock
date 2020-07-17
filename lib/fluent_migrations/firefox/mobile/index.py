from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

index = "firefox/mobile/index.lang"
mobile_2019 = "firefox/mobile-2019.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/mobile/index.html, part {index}."""

    ctx.add_transforms(
        "firefox/mobile.ftl",
        "firefox/mobile.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("firefox-mobile-download-the-firefox-browser"),
                value=REPLACE(
                    mobile_2019,
                    "Download the Firefox Browser on your Mobile for iOS and Android",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-mobile-firefox-browser-for-mobile"),
                value=REPLACE(
                    mobile_2019,
                    "Firefox Browser for Mobile blocks over 2000 trackers by default, giving you the privacy you deserve and the speed you need in a private mobile browser.",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-mobile-firefox = { -brand-name-firefox }
firefox-mobile-firefox-browser = { -brand-name-firefox-browser }
firefox-mobile-get-the-mobile-browser-built = {COPY(mobile_2019, "Get the mobile browser built for you, not advertisers",)}
""", mobile_2019=mobile_2019) + [
            FTL.Message(
                id=FTL.Identifier("firefox-mobile-check-out-firefox-again-its"),
                value=REPLACE(
                    mobile_2019,
                    "Check out Firefox again. It’s fast, private and on your side. For iOS and Android.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-mobile-get-automatic-privacy-on-mobile = {COPY(mobile_2019, "Get automatic privacy on mobile",)}
firefox-mobile-super-fast-private-by-default = {COPY(mobile_2019, "Super fast. Private by default. Blocks 2000+ online trackers.",)}
""", mobile_2019=mobile_2019) + [
            FTL.Message(
                id=FTL.Identifier("firefox-mobile-get-firefox-mobile"),
                value=REPLACE(
                    mobile_2019,
                    "Get Firefox Mobile",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-mobile-block-online-trackers-and = {COPY(mobile_2019, "Block online trackers and invasive ads",)}
firefox-mobile-privacy-protection-by-default = {COPY(mobile_2019, "Privacy protection by default",)}
""", mobile_2019=mobile_2019) + [
            FTL.Message(
                id=FTL.Identifier("firefox-mobile-leave-no-trace-with-private"),
                value=REPLACE(
                    mobile_2019,
                    "Leave no trace with <a href=\"%s\">Private Browsing mode</a>. When you close out, your history and cookies are deleted.",
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("url"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-mobile-stop-companies-from-following = {COPY(mobile_2019, "Stop companies from following you",)}
""", mobile_2019=mobile_2019) + [
            FTL.Message(
                id=FTL.Identifier("firefox-mobile-stay-off-their-radar-with"),
                value=REPLACE(
                    mobile_2019,
                    "Stay off their radar with <a href=\"%s\">Firefox Tracking Protection</a>",
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("url"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-mobile-discover-products-that-keep = {COPY(mobile_2019, "Discover products that keep you safe",)}
firefox-mobile-sync-your-history-passwords = {COPY(mobile_2019, "Sync your history, passwords, and bookmarks. Send tabs across all of your devices.",)}
""", mobile_2019=mobile_2019) + [
            FTL.Message(
                id=FTL.Identifier("firefox-mobile-android-only"),
                value=REPLACE(
                    mobile_2019,
                    "Android only",
                    {
                        "Android": TERM_REFERENCE("brand-name-android"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-mobile-make-android-your-own"),
                value=REPLACE(
                    mobile_2019,
                    "Make Android your own",
                    {
                        "Android": TERM_REFERENCE("brand-name-android"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-mobile-customize-your-firefox-mobile"),
                value=REPLACE(
                    mobile_2019,
                    "Customize your Firefox mobile browser with <a href=\"%s\">extensions</a> to block ads, manage passwords, stop Facebook from tracking you and more.",
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("url"),
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-mobile-find-it-fast-with-a-smart = {COPY(mobile_2019, "Find it fast with a smart search bar",)}
""", mobile_2019=mobile_2019) + [
            FTL.Message(
                id=FTL.Identifier("firefox-mobile-firefox-anticipates-your-needs"),
                value=REPLACE(
                    mobile_2019,
                    "Firefox anticipates your needs with smart search suggestions and quick access to the sites you visit most.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-mobile-the-privacy-you-deserve-the = {COPY(mobile_2019, "The privacy you deserve. The speed you need.",)}
""", mobile_2019=mobile_2019) + [
            FTL.Message(
                id=FTL.Identifier("firefox-mobile-get-firefox-for-mobile"),
                value=REPLACE(
                    mobile_2019,
                    "Get Firefox for mobile",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-mobile-send-a-download-link-to-your = {COPY(mobile_2019, "Send a download link to your phone.",)}
firefox-mobile-scan-the-qr-code-to-get-started = {COPY(mobile_2019, "Scan the QR code to get started",)}
""", mobile_2019=mobile_2019)
        )
