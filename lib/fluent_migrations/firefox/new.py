from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

trailhead = "firefox/new/trailhead.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/new/trailhead/base.html, part {index}."""

    ctx.add_transforms(
        "firefox/new/download.ftl",
        "firefox/new/download.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("firefox-new-download-firefox"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "Download Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-download-mozilla-firefox"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "Download Mozilla Firefox, a free Web browser. Firefox is created by a global non-profit dedicated to putting individuals in control online. Get Firefox for Windows, macOS, Linux, Android and iOS today!",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "macOS": TERM_REFERENCE("brand-name-mac"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-download-the-fastest-firefox"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "Download the fastest Firefox ever",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-faster-page-loading-less-memory"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "Faster page loading, less memory usage and packed with features, the new Firefox is here.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-automatic-privacy-is-here"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "Automatic privacy is here. Download Firefox to block over 2000 trackers.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-get-the-latest-firefox"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "Get the latest Firefox browser.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-firefox-shows-you-how-many"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "Firefox shows you how many data-collecting trackers are blocked with <strong>Enhanced Tracking Protection</strong>.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-firefox-lockwise-makes-secure"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "<strong>Firefox Lockwise</strong> makes the passwords you save in Firefox secure and available on all your devices.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Firefox Lockwise": TERM_REFERENCE("brand-name-firefox-lockwise"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-firefox-monitor-alerts"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "<strong>Firefox Monitor</strong> alerts you if we know your information is a part of another company’s data breach.",
                    {
                        "Firefox Monitor": TERM_REFERENCE("brand-name-firefox-monitor"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-join-firefox"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "Join Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-firefox-lockwise-makes"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "<strong>Firefox Lockwise</strong> makes the passwords you save in Firefox available on all your devices.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Firefox Lockwise": TERM_REFERENCE("brand-name-firefox-lockwise"),

                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-download-firefox-for-windows"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "Download Firefox <br>for Windows",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-download-firefox-for-macos"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "Download Firefox <br>for macOS",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "macOS": TERM_REFERENCE("brand-name-mac"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-download-firefox-for-linux"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "Download Firefox <br>for Linux",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-youve-already-got-the-browser"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "You’ve already got the browser. Now get even more from Firefox.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-watch-for-hackers-with"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "Watch for hackers with Firefox Monitor, protect passwords with Firefox Lockwise, and more.",
                    {
                        "Firefox Monitor": TERM_REFERENCE("brand-name-firefox-monitor"),
                        "Firefox Lockwise": TERM_REFERENCE("brand-name-firefox-lockwise"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-get-more-from-firefox"),
                value=REPLACE(
                    "firefox/new/trailhead.lang",
                    "Get More From Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
    )

    ctx.add_transforms(
        "firefox/new/download.ftl",
        "firefox/new/download.ftl",
        transforms_from("""
firefox-new-free-web-browser = {COPY(trailhead, "Free Web Browser",)}
firefox-new-and-start-getting-the-respect = {COPY(trailhead, "And start getting the respect you deserve with our family of privacy-first products.",)}
firefox-new-advanced-install-options = {COPY(trailhead, "Advanced install options & other platforms",)}
firefox-new-download-in-another-language = {COPY(trailhead, "Download in another language",)}
firefox-new-fix-a-problem = {COPY(trailhead, "Fix a problem",)}
firefox-new-need-help = {COPY(trailhead, "Need help?",)}
firefox-new-see-whats-being-blocked = {COPY(trailhead, "See what’s being blocked",)}
firefox-new-make-your-passwords-portable = {COPY(trailhead, "Make your passwords portable",)}
firefox-new-watch-for-data-breaches = {COPY(trailhead, "Watch for data breaches",)}
firefox-new-connect-to-a-whole-family = {COPY(trailhead, "Connect to a whole family of respectful products, plus all the knowledge you need to protect yourself online.",)}
firefox-new-passwords-made-portable = {COPY(trailhead, "Passwords made portable",)}
firefox-new-protect-your-privacy = {COPY(trailhead, "Protect your privacy",)}
firefox-new-private-browsing-clears = {COPY(trailhead, "<strong>Private Browsing</strong> clears your history to keep it secret from anyone who uses your computer.",)}
firefox-new-advanced-install-options-heading = {COPY(trailhead, "Advanced Install Options & Other Platforms",)}
firefox-new-just-download-the-browser = {COPY(trailhead, "Just Download The Browser",)}
""", trailhead=trailhead)
        )

    ctx.add_transforms(
        "firefox/new/download.ftl",
        "firefox/new/download.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("firefox-new-youre-using-an-insecure-outdated"),
                value=REPLACE(
                    trailhead,
                    "You’re using an insecure, outdated operating system <a href=\"%(url)s\">no longer supported by Firefox</a>.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-your-firefox-new-should-begin"),
                value=REPLACE(
                    trailhead,
                    "Your download should begin automatically. Didn’t work? <a id=\"%(id)s\" href=\"%(fallback_url)s\">Try downloading again</a>.",
                    {
                        "%%": "%",
                        "%(id)s": VARIABLE_REFERENCE("id"),
                        "%(fallback_url)s": VARIABLE_REFERENCE("fallback_url"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-new-firefox-is-more-than-a-browser"),
                value=REPLACE(
                    trailhead,
                    "Firefox is more than a browser.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-new-its-privacy-and-peace-of = {COPY(trailhead, "It’s <strong>privacy and peace of mind</strong> on mobile, too.",)}
firefox-new-its-a-family-of-products = {COPY(trailhead, "It’s a <strong>family of products</strong> that treat your personal data with respect.",)}
firefox-new-its-everything-you-need-to = {COPY(trailhead, "It’s everything you need to know about <strong>staying safe online</strong>.",)}
firefox-new-its-a-community-that-believes = {COPY(trailhead, "It’s <strong>a community</strong> that believes tech can do better.",)}
""", trailhead=trailhead)
        )
