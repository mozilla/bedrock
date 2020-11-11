from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

base_download = "firefox/new/protocol/base_download.lang"
quantum = "firefox/new/quantum.lang"
main = "main.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/new/protocol/base_download.html, part {index}."""

    ctx.add_transforms(
        "firefox/new/platform.ftl",
        "firefox/new/platform.ftl",
        transforms_from("""
new-platform-free-web-browser = {COPY(quantum, "Free Web Browser",)}
""", quantum=quantum) + [
            FTL.Message(
                id=FTL.Identifier("new-platform-download-firefox"),
                value=REPLACE(
                    quantum,
                    "Download Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-download-the-fastest"),
                value=REPLACE(
                    quantum,
                    "Download the fastest Firefox ever",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-faster-page-loading"),
                value=REPLACE(
                    quantum,
                    "Faster page loading, less memory usage and packed with features, the new Firefox is here.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-the-new-firefox"),
                value=REPLACE(
                    quantum,
                    "The new <strong>Firefox</strong>",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
new-platform-2x-faster = {COPY(quantum, "2x Faster",)}
""", quantum=quantum) + [
            FTL.Message(
                id=FTL.Identifier("new-platform-the-best-firefox-ever"),
                value=REPLACE(
                    quantum,
                    "The best Firefox ever",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
new-platform-lightweight = {COPY(quantum, "Lightweight",)}
""", quantum=quantum) + [
            FTL.Message(
                id=FTL.Identifier("new-platform-uses-30-less-memory"),
                value=REPLACE(
                    quantum,
                    "Uses 30% less memory than Chrome",
                    {
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
        ] + transforms_from("""
new-platform-powerfully-private = {COPY(quantum, "Powerfully private",)}
new-platform-truly-private-browsing = {COPY(quantum, "Truly Private Browsing with Tracking Protection",)}
new-platform-advanced-install-options = {COPY(quantum, "Advanced install options & other platforms",)}
new-platform-download-in-another = {COPY(quantum, "Download in another language",)}
new-platform-fix-a-problem = {COPY(quantum, "Fix a problem",)}
new-platform-need-help = {COPY(main, "Need help?",)}
""", quantum=quantum, main=main)
        )

    ctx.add_transforms(
        "firefox/new/platform.ftl",
        "firefox/new/platform.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("new-platform-download-mozilla-firefox-title"),
                value=REPLACE(
                    quantum,
                    "Download Mozilla Firefox, a free Web browser. Firefox is created by a global non-profit dedicated to putting individuals in control online. Get Firefox for Windows, macOS, Linux, Android and iOS today!",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                        "macOS": TERM_REFERENCE("brand-name-mac"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    }
                )
            ),
        ]
    )

    ctx.add_transforms(
        "firefox/new/platform.ftl",
        "firefox/new/platform.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("new-platform-download-mozilla-linux"),
                value=REPLACE(
                    quantum,
                    "Download Mozilla Firefox for Linux",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-download-mozilla-desc-linux"),
                value=REPLACE(
                    quantum,
                    "Download Mozilla Firefox for Linux, a free Web browser. Firefox is created by a global non-profit dedicated to putting individuals in control online. Get Firefox for Linux today!",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-download-the-fastest-linux"),
                value=REPLACE(
                    quantum,
                    "Download the fastest Firefox for Linux ever",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-faster-page-loading-linux"),
                value=REPLACE(
                    quantum,
                    "Faster page loading, less memory usage and packed with features, the new Firefox for Linux is here.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-firefox-for-linux"),
                value=REPLACE(
                    quantum,
                    "Firefox for Linux",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                    }
                )
            ),
        ] + transforms_from("""
new-platform-own-your-online-life = {COPY(quantum, "Own your online life.",)}
new-platform-privacy-more-than = {COPY(quantum, "Privacy - more than a policy",)}
""", quantum=quantum) + [
            FTL.Message(
                id=FTL.Identifier("new-platform-your-life-your-business"),
                value=REPLACE(
                    quantum,
                    "Your life, your business. Firefox blocks third-party tracking cookies on Linux.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-speed-meet-security"),
                value=REPLACE(
                    quantum,
                    "Speed, meet security. Firefox is two times faster with 30% less memory than Chrome.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
        ] + transforms_from("""
new-platform-open-source = {COPY(quantum, "Open source",)}
""", quantum=quantum) + [
            FTL.Message(
                id=FTL.Identifier("new-platform-look-under-the-hood"),
                value=REPLACE(
                    quantum,
                    "Look under the hood. Like Linux, Firefox features are open source.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                    }
                )
            ),
        ]
    )

    ctx.add_transforms(
        "firefox/new/platform.ftl",
        "firefox/new/platform.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("new-platform-download-mozilla-firefox-mac"),
                value=REPLACE(
                    quantum,
                    "Download Mozilla Firefox for Mac",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Mac": TERM_REFERENCE("brand-name-mac-short"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-download-mozilla-firefox-desc-mac"),
                value=REPLACE(
                    quantum,
                    "Download Mozilla Firefox for Mac, a free Web browser. Firefox is created by a global non-profit dedicated to putting individuals in control online. Get Firefox for Mac today!",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Mac": TERM_REFERENCE("brand-name-mac-short"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-download-the-fastest-mac"),
                value=REPLACE(
                    quantum,
                    "Download the fastest Firefox for Mac ever",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Mac": TERM_REFERENCE("brand-name-mac-short"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-faster-page-loading-mac"),
                value=REPLACE(
                    quantum,
                    "Faster page loading, less memory usage and packed with features, the new Firefox for Mac is here.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Mac": TERM_REFERENCE("brand-name-mac-short"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-firefox-respects-your"),
                value=REPLACE(
                    quantum,
                    "Firefox respects <span>your privacy on Mac.</span>",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Mac": TERM_REFERENCE("brand-name-mac-short"),
                    }
                )
            ),
        ] + transforms_from("""
new-platform-privacy-comes-first = {COPY(quantum, "Privacy comes first",)}
""", quantum=quantum) + [
            FTL.Message(
                id=FTL.Identifier("new-platform-firefox-doesnt-spy"),
                value=REPLACE(
                    quantum,
                    "Firefox doesn’t spy on searches. We stop third-party tracking cookies and give you full control.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-get-speed-and-security"),
                value=REPLACE(
                    quantum,
                    "Get speed and security. Firefox is fast on Mac because we don’t track your moves.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Mac": TERM_REFERENCE("brand-name-mac-short"),
                    }
                )
            ),
        ] + transforms_from("""
new-platform-block-trackers = {COPY(quantum, "Block trackers",)}
new-platform-be-the-master-of-your = {COPY(quantum, "Be the master of your domain with strict content blocking. Cut off all cookies and trackers.",)}
""", quantum=quantum)
        )

    ctx.add_transforms(
        "firefox/new/platform.ftl",
        "firefox/new/platform.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("new-platform-download-mozilla-windows"),
                value=REPLACE(
                    quantum,
                    "Download Mozilla Firefox for Windows",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-download-mozilla-desc-windows"),
                value=REPLACE(
                    quantum,
                    "Download Mozilla Firefox for Windows, a free Web browser. Firefox is created by a global non-profit dedicated to putting individuals in control online. Get Firefox for Windows today!",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-download-the-fastest-windows"),
                value=REPLACE(
                    quantum,
                    "Download the fastest Firefox for Windows ever",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-faster-page-loading-windows"),
                value=REPLACE(
                    quantum,
                    "Faster page loading, less memory usage and packed with features, the new Firefox for Windows is here.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-firefox-fights"),
                value=REPLACE(
                    quantum,
                    "Firefox fights for you <span>on Windows.</span>",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("new-platform-firefox-moves-fast"),
                value=REPLACE(
                    quantum,
                    "Firefox moves fast and treats your data with care - no ad tracking and no slowdown.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
new-platform-common-sense-privacy = {COPY(quantum, "Common sense privacy",)}
""", quantum=quantum) + [
            FTL.Message(
                id=FTL.Identifier("new-platform-live-your-life"),
                value=REPLACE(
                    quantum,
                    "Live your life, Firefox isn’t watching. Choose what to share and when to share it.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
new-platform-seamless-setup = {COPY(quantum, "Seamless setup",)}
""", quantum=quantum) + [
            FTL.Message(
                id=FTL.Identifier("new-platform-easy-migration"),
                value=REPLACE(
                    quantum,
                    "Easy migration of preferences and bookmarks when you download Firefox for Windows.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    }
                )
            ),
        ]
        )
