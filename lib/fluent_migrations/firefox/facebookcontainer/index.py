from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

index = "firefox/facebookcontainer/index.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/facebookcontainer/index.html, part {index}."""

    ctx.add_transforms(
        "firefox/facebook_container.ftl",
        "firefox/facebook_container.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("facebook-container-facebook-container-for-firefox"),
                value=REPLACE(
                    index,
                    "Facebook Container for Firefox | Prevent Facebook from seeing what websites you visit.",
                    {
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                        "Facebook Container": TERM_REFERENCE("brand-name-facebook-container"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("facebook-container-millions-of-people-around"),
                value=REPLACE(
                    index,
                    "Millions of people around the world trust Firefox Web browsers on Android, iOS and desktop computers. Fast. Private. Download now!",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("facebook-container-facebook-well-contained-keep"),
                value=REPLACE(
                    index,
                    "Facebook. Well contained. Keep the rest of your life to yourself.",
                    {
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("facebook-container-get-the-facebook-container"),
                value=REPLACE(
                    index,
                    "Get the Facebook Container Extension",
                    {
                        "Facebook Container": TERM_REFERENCE("brand-name-facebook-container"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("facebook-container-download-firefox-and-get-the"),
                value=REPLACE(
                    index,
                    "Download Firefox and get the Facebook Container Extension",
                    {
                        "Facebook Container": TERM_REFERENCE("brand-name-facebook-container"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("facebook-container-the-facebook-container-extension"),
                value=REPLACE(
                    index,
                    "The Facebook Container Extension is not available on mobile devices.",
                    {
                        "Facebook Container": TERM_REFERENCE("brand-name-facebook-container"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("facebook-container-try-firefox-focus-the-privacy"),
                value=REPLACE(
                    index,
                    "Try <strong>Firefox Focus</strong>, the privacy browser for Android and iOS.",
                    {
                        "Firefox Focus": TERM_REFERENCE("brand-name-firefox-focus"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
facebook-container-opt-out-on-your-terms = {COPY(index, "Opt out on your terms",)}
""",
            index=index,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("facebook-container-facebook-can-track-almost"),
                value=REPLACE(
                    index,
                    'Facebook can track almost all your web activity and tie it to your Facebook identity. If that’s too much for you, the <a href="%(fbcontainer)s">Facebook Container extension</a> isolates your identity into a separate container tab, making it harder for Facebook to track you on the web outside of Facebook.',
                    {
                        "%%": "%",
                        "%(fbcontainer)s": VARIABLE_REFERENCE("fbcontainer"),
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                        "Facebook Container": TERM_REFERENCE("brand-name-facebook-container"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
facebook-container-install-and-contain = {COPY(index, "Install and contain",)}
""",
            index=index,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("facebook-container-installing-the-extension-is"),
                value=REPLACE(
                    index,
                    'Installing the <a href="%(fbcontainer)s">extension</a> is easy and, once activated, will open Facebook in a blue tab each time you use it. Use and enjoy Facebook normally. Facebook will still be able to send you advertising and recommendations on their site, but it will be much harder for Facebook to use your activity collected <strong>off Facebook</strong> to send you ads and other targeted messages.',
                    {
                        "%%": "%",
                        "%(fbcontainer)s": VARIABLE_REFERENCE("fbcontainer"),
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("facebook-container-about-firefox-and-mozilla"),
                value=REPLACE(
                    index,
                    "About Firefox and Mozilla",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("facebook-container-were-backed-by-mozilla-the"),
                value=REPLACE(
                    index,
                    'We’re backed by <a href="%(mozilla)s">Mozilla</a>, the not-for-profit organization that puts people over profit to give everyone more power online. We created this extension because we believe that you should have easy-to-use tools that help you manage your privacy and security.',
                    {
                        "%%": "%",
                        "%(mozilla)s": VARIABLE_REFERENCE("mozilla"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("facebook-container-browse-freely-with-firefox"),
                value=REPLACE(
                    index,
                    "Browse freely with Firefox today.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ],
    )
