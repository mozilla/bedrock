from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

nightly_whatsnew = "firefox/nightly_whatsnew.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/nightly_whatsnew.html, part {index}."""

    ctx.add_transforms(
        "firefox/nightly/whatsnew.ftl",
        "firefox/nightly/whatsnew.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("nightly-whatsnew-youve-just-been"),
                value=REPLACE(
                    nightly_whatsnew,
                    "You’ve just been upgraded to Firefox Nightly %(version)s!",
                    {
                        "%%": "%",
                        "%(version)s": VARIABLE_REFERENCE("version"),
                        "Firefox Nightly": TERM_REFERENCE("brand-name-firefox-nightly"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("nightly-whatsnew-your-firefox-nightly"),
                value=REPLACE(
                    nightly_whatsnew,
                    "Your Firefox Nightly has been updated.",
                    {
                        "Firefox Nightly": TERM_REFERENCE("brand-name-firefox-nightly"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
nightly-whatsnew-firefox-nightly = { -brand-name-firefox-nightly }
""",
            nightly_whatsnew=nightly_whatsnew,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("nightly-whatsnew-every-4-to-5-weeks"),
                value=REPLACE(
                    nightly_whatsnew,
                    "Every 4 to 5 weeks, a new major version of Firefox is released and as a result, the Nightly version increases as well.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Nightly": TERM_REFERENCE("brand-name-nightly"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("nightly-whatsnew-every-6-to-8-weeks"),
                value=REPLACE(
                    nightly_whatsnew,
                    "Every 6 to 8 weeks, a new major version of Firefox is released and as a result, the Nightly version increases as well.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Nightly": TERM_REFERENCE("brand-name-nightly"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("nightly-whatsnew-this-is-a-good"),
                value=REPLACE(
                    nightly_whatsnew,
                    "This is a good time to thank you for helping us make Firefox better and to give you some pointers to documentation, communication channels and news sites related to Nightly that may be of interest to you.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Nightly": TERM_REFERENCE("brand-name-nightly"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("nightly-whatsnew-if-you-want-to"),
                value=REPLACE(
                    nightly_whatsnew,
                    'If you want to know what’s happening around Nightly and its community, reading our <a href="%(blog)s">blog</a> and following us on <a href="%(twitter)s">Twitter</a> are good starting points!',
                    {
                        "%%": "%",
                        "%(blog)s": VARIABLE_REFERENCE("blog"),
                        "%(twitter)s": VARIABLE_REFERENCE("twitter"),
                        "Twitter": TERM_REFERENCE("brand-name-twitter"),
                        "Nightly": TERM_REFERENCE("brand-name-nightly"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("nightly-whatsnew-want-to-know-which"),
                value=REPLACE(
                    nightly_whatsnew,
                    'Want to know which platform features you could test on Nightly and can’t see yet on other Firefox channels? Then have a look at the <a href="%(mdn)s">Experimental Features</a> page on <abbr title="Mozilla Developer Network">MDN</abbr>.',
                    {
                        "%%": "%",
                        "%(mdn)s": VARIABLE_REFERENCE("mdn"),
                        "Mozilla Developer Network": TERM_REFERENCE("brand-name-mozilla-developer-network"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Nightly": TERM_REFERENCE("brand-name-nightly"),
                        "MDN": TERM_REFERENCE("brand-name-mdn"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("nightly-whatsnew-do-you-experience"),
                value=REPLACE(
                    nightly_whatsnew,
                    'Do you experience crashes? Unexpected behavior? Web compatibility regressions? We’d love to get them filed in <a href="%(bugzilla)s">Bugzilla</a> to make sure they don’t make it to the final release (extra karma if you add the <em>nightly-community</em> keyword to your bug reports)!',
                    {
                        "%%": "%",
                        "%(bugzilla)s": VARIABLE_REFERENCE("bugzilla"),
                        "Bugzilla": TERM_REFERENCE("brand-name-bugzilla"),
                        "nightly": TERM_REFERENCE("brand-name-nightly"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
nightly-whatsnew-go-community = {COPY(nightly_whatsnew, "Go community!",)}
""",
            nightly_whatsnew=nightly_whatsnew,
        ),
    )
