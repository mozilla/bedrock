from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

nightly_firstrun = "firefox/nightly_firstrun.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/nightly_firstrun.html, part {index}."""

    ctx.add_transforms(
        "firefox/nightly/firstrun.ftl",
        "firefox/nightly/firstrun.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("nightly-firstrun-firefox-nightly"),
                value=REPLACE(
                    nightly_firstrun,
                    "Firefox Nightly First Run Page",
                    {
                        "Firefox Nightly": TERM_REFERENCE("brand-name-firefox-nightly"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("nightly-firstrun-thank-you-for-using"),
                value=REPLACE(
                    nightly_firstrun,
                    "Thank you for using Firefox Nightly",
                    {
                        "Firefox Nightly": TERM_REFERENCE("brand-name-firefox-nightly"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("nightly-firstrun-choose-an-area"),
                value=REPLACE(
                    nightly_firstrun,
                    "Choose an area to get involved below and help make Firefox better for users everywhere",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
nightly-firstrun-test = {COPY(nightly_firstrun, "Test",)}
nightly-firstrun-find-and-file-bugs = {COPY(nightly_firstrun, "Find and file bugs and generally make sure things work as they should.",)}
nightly-firstrun-start-testing = {COPY(nightly_firstrun, "Start testing",)}
nightly-firstrun-code = {COPY(nightly_firstrun, "Code",)}
""",
            nightly_firstrun=nightly_firstrun,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("nightly-firstrun-file-bugs-and-work"),
                value=REPLACE(
                    nightly_firstrun,
                    "File bugs and work on the building blocks of the Firefox browser.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
nightly-firstrun-start-coding = {COPY(nightly_firstrun, "Start coding",)}
nightly-firstrun-localize = {COPY(nightly_firstrun, "Localize",)}
""",
            nightly_firstrun=nightly_firstrun,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("nightly-firstrun-make-firefox-available"),
                value=REPLACE(
                    nightly_firstrun,
                    "Make Firefox available (and better) in more languages around the world.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
nightly-firstrun-contribute-link = {COPY(nightly_firstrun, "https://wiki.mozilla.org/L10n:Contribute",)}
nightly-firstrun-start-localizing = {COPY(nightly_firstrun, "Start localizing",)}
""",
            nightly_firstrun=nightly_firstrun,
        ),
    )
