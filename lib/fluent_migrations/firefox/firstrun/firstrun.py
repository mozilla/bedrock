from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

firstrun = "firefox/firstrun/firstrun.lang"
quantum = "firefox/new/quantum.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/firstrun/firstrun.html, part {index}."""

    ctx.add_transforms(
        "firefox/firstrun.ftl",
        "firefox/firstrun.ftl",
        transforms_from(
            """
firstrun-firefox-browser = { -brand-name-firefox-browser }
""",
            quantum=quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firstrun-welcome-to-firefox"),
                value=REPLACE(
                    quantum,
                    "Welcome to Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firstrun-take-firefox-with-you"),
                value=REPLACE(
                    quantum,
                    "Take Firefox with You",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firstrun-already-using-firefox"),
                value=REPLACE(
                    quantum,
                    "Already using Firefox?",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firstrun-get-your-bookmarks-history = {COPY(quantum, "Get your bookmarks, history, passwords and other settings on all your devices.",)}
""",
            quantum=quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firstrun-sign-in-to-your-account"),
                value=REPLACE(
                    quantum,
                    "Sign in to your account and we’ll sync the bookmarks, passwords and other great things you’ve saved to Firefox on other devices.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firstrun-already-have-an-account = {COPY(quantum, "Already have an account?",)}
firstrun-sign-in = {COPY(quantum, "Sign In",)}
""",
            quantum=quantum,
        ),
    )
