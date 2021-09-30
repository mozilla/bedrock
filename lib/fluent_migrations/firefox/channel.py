from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

index = "firefox/channel/index.lang"
main = "main.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/channel/base.html, part {index}."""

    ctx.add_transforms(
        "firefox/channel.ftl",
        "firefox/channel.ftl",
        transforms_from(
            """
firefox-channel-desktop = {COPY(index, "Desktop",)}
""",
            index=index,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-channel-android"),
                value=REPLACE(
                    index,
                    "Android",
                    {
                        "Android": TERM_REFERENCE("brand-name-android"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-ios"),
                value=REPLACE(
                    index,
                    "iOS",
                    {
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-channel-take-a-browse-on-the-wild-side = {COPY(index, "Take a browse on the wild side.",)}
""",
            index=index,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-channel-be-among-the-first-to-explore"),
                value=REPLACE(
                    index,
                    "Be among the first to explore future releases of Firefox for desktop, Android and iOS.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-channel-see-something-that-isnt-working = {COPY(index, "See something that isn’t working? Let us know.",)}
firefox-channel-file-a-bug-now = {COPY(index, "File a bug now",)}
firefox-channel-tips-for-filing-a-bug = {COPY(index, "Tips for filing a bug",)}
""",
            index=index,
        ),
    )

    ctx.add_transforms(
        "firefox/channel.ftl",
        "firefox/channel.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("firefox-channel-try-new-features-in-a-pre"),
                value=REPLACE(
                    index,
                    "Try New Features in a Pre-Release Android Browser | Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-download-and-test-future"),
                value=REPLACE(
                    index,
                    "Download and test future releases of Firefox for desktop, Android and iOS.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-experience-cutting-edge-android-updated"),
                value=REPLACE(
                    index,
                    "Experience cutting-edge features in a pre-release browser for Android: Firefox Beta and Firefox Nightly. Install now!",
                    {
                        "Firefox Nightly": TERM_REFERENCE("brand-name-firefox-nightly"),
                        "Firefox Beta": TERM_REFERENCE("brand-name-firefox-beta"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-experience-cutting-edge-android"),
                value=REPLACE(
                    index,
                    "Experience cutting-edge features in a pre-release browser for Android: Firefox Beta, Firefox Aurora and Firefox Nightly. Install now!",
                    {
                        "Firefox Nightly": TERM_REFERENCE("brand-name-firefox-nightly"),
                        "Firefox Aurora": TERM_REFERENCE("brand-name-firefox-aurora"),
                        "Firefox Beta": TERM_REFERENCE("brand-name-firefox-beta"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-download-and-test-the-latest-android"),
                value=REPLACE(
                    index,
                    "Download and test the latest Firefox for Android features with Aurora, Beta and Nightly builds.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Nightly": TERM_REFERENCE("brand-name-nightly"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "Beta": TERM_REFERENCE("brand-name-beta"),
                        "Aurora": TERM_REFERENCE("brand-name-aurora"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-try-the-latest-android-features"),
                value=REPLACE(
                    index,
                    "Try the latest Android features, before they get released to the rest of the world.",
                    {
                        "Android": TERM_REFERENCE("brand-name-android"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-channel-all-languages-and-platforms = {COPY(index, "All Languages and Platforms",)}
firefox-channel-all-languages-and-builds = {COPY(index, "All Languages and Builds",)}
""",
            index=index,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-channel-beta-is-an-unstable-testing"),
                value=REPLACE(
                    index,
                    'Beta is an unstable testing and development platform. By default, Beta sends data to Mozilla — and sometimes our partners — to help us handle problems and try ideas. <a href="%(link)s">Learn what is shared</a>.',
                    {
                        "%%": "%",
                        "%(link)s": VARIABLE_REFERENCE("link"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Beta": TERM_REFERENCE("brand-name-beta"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-firefox-beta-automatically"),
                value=REPLACE(
                    index,
                    "Firefox Beta automatically sends feedback to Mozilla.",
                    {
                        "Firefox Beta": TERM_REFERENCE("brand-name-firefox-beta"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-give-us-feedback-to-help"),
                value=REPLACE(
                    index,
                    '<a rel="external" href="%(feedback)s">Give us feedback</a> to help us put the final tweaks on performance and functionality in a stable environment.',
                    {
                        "%%": "%",
                        "%(feedback)s": VARIABLE_REFERENCE("feedback"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-check-out-new-android-features"),
                value=REPLACE(
                    index,
                    "Check out new Android features in their earliest stages. Enjoy at your own risk.",
                    {
                        "Android": TERM_REFERENCE("brand-name-android"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-nightly-blog"),
                value=REPLACE(
                    index,
                    "Nightly Blog",
                    {
                        "Nightly": TERM_REFERENCE("brand-name-nightly"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-nightly-is-an-unstable-testing"),
                value=REPLACE(
                    index,
                    'Nightly is an unstable testing and development platform. By default, Nightly sends data to Mozilla — and sometimes our partners — to help us handle problems and try ideas. <a href="%(link)s">Learn what is shared</a>.',
                    {
                        "%%": "%",
                        "%(link)s": VARIABLE_REFERENCE("link"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Nightly": TERM_REFERENCE("brand-name-nightly"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-firefox-nightly-automatically"),
                value=REPLACE(
                    index,
                    "Firefox Nightly automatically sends feedback to Mozilla.",
                    {
                        "Firefox Nightly": TERM_REFERENCE("brand-name-firefox-nightly"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ],
    )

    ctx.add_transforms(
        "firefox/channel.ftl",
        "firefox/channel.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("firefox-channel-try-new-browser-features"),
                value=REPLACE(
                    index,
                    "Try New Browser Features in Pre-Release Versions | Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-experience-cutting-edge-desktop"),
                value=REPLACE(
                    index,
                    "Experience cutting-edge browser features in pre-release versions: Firefox Developer Edition, Firefox Beta and Firefox Nightly. Download now!",
                    {
                        "Firefox Developer Edition": TERM_REFERENCE("brand-name-firefox-developer-edition"),
                        "Firefox Nightly": TERM_REFERENCE("brand-name-firefox-nightly"),
                        "Firefox Beta": TERM_REFERENCE("brand-name-firefox-beta"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-download-and-test-the-latest-desktop"),
                value=REPLACE(
                    index,
                    "Download and test the latest Firefox for desktop features with Developer Edition, Beta and Nightly builds.",
                    {
                        "Developer Edition": TERM_REFERENCE("brand-name-developer-edition"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Nightly": TERM_REFERENCE("brand-name-nightly"),
                        "Beta": TERM_REFERENCE("brand-name-beta"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-channel-beta = { -brand-name-beta }
firefox-channel-test-about-to-be-released = {COPY(index, "Test about-to-be-released features in the most stable pre-release build.",)}
firefox-channel-release-notes = {COPY(main, "Release Notes")}
firefox-channel-developer-edition = { -brand-name-developer-edition }
firefox-channel-build-test-scale-and-more = {COPY(index, "Build, test, scale and more with the only browser built just for developers.",)}
""",
            index=index,
            main=main,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-channel-developer-edition-is-an"),
                value=REPLACE(
                    index,
                    'Developer Edition is an unstable testing and development platform. By default, Developer Edition sends data to Mozilla — and sometimes our partners — to help us handle problems and try ideas. <a href="%(link)s">Learn what is shared</a>.',
                    {
                        "%%": "%",
                        "%(link)s": VARIABLE_REFERENCE("link"),
                        "Developer Edition": TERM_REFERENCE("brand-name-developer-edition"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-firefox-developer-edition"),
                value=REPLACE(
                    index,
                    "Firefox Developer Edition automatically sends feedback to Mozilla.",
                    {
                        "Firefox Developer Edition": TERM_REFERENCE("brand-name-firefox-developer-edition"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-channel-nightly = { -brand-name-nightly }
""",
            index=index,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-channel-get-a-sneak-peek-at-our"),
                value=REPLACE(
                    index,
                    "Get a sneak peek at our next generation web browser, and help us make it the best browser it can be: try Firefox Nightly.",
                    {
                        "Firefox Nightly": TERM_REFERENCE("brand-name-firefox-nightly"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-channel-test-brand-new-features = {COPY(index, "Test brand new features daily (or… nightly). Enjoy at your own risk.",)}
""",
            index=index,
        ),
    )

    ctx.add_transforms(
        "firefox/channel.ftl",
        "firefox/channel.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("firefox-channel-try-new-features-in-a-pre-release"),
                value=REPLACE(
                    index,
                    "Try New Features in a Pre-Release iOS Browser | Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-experience-cutting-edge-features-ios"),
                value=REPLACE(
                    index,
                    "Experience cutting-edge features in a pre-release browser for iOS via Apple’s TestFlight program. Install now!",
                    {
                        "Apple": TERM_REFERENCE("brand-name-apple"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "TestFlight": TERM_REFERENCE("brand-name-test-flight"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-channel-test-beta-versions-of-firefox-ios-long"),
                value=REPLACE(
                    index,
                    "Test beta versions of Firefox for iOS via Apple’s TestFlight program and help make our mobile browser for iPhone, iPad and iPod touch even better.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "iPhone": TERM_REFERENCE("brand-name-iphone"),
                        "Apple": TERM_REFERENCE("brand-name-apple"),
                        "iPad": TERM_REFERENCE("brand-name-ipad"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "TestFlight": TERM_REFERENCE("brand-name-test-flight"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-channel-test-flight = { -brand-name-test-flight }
""",
            index=index,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-channel-test-beta-versions-of-firefox-ios"),
                value=REPLACE(
                    index,
                    "Test beta versions of Firefox for iOS via Apple’s TestFlight program.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Apple": TERM_REFERENCE("brand-name-apple"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "TestFlight": TERM_REFERENCE("brand-name-test-flight"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-channel-sign-up-now = {COPY(index, "Sign up now",)}
""",
            index=index,
        ),
    )
