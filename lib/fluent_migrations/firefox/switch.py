from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

switch = "firefox/switch.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/switch.html, part {index}."""

    ctx.add_transforms(
        "firefox/switch.ftl",
        "firefox/switch.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("switch-switch-from-chrome"),
                value=REPLACE(
                    "firefox/switch.lang",
                    "Switch from Chrome to Firefox in just a few minutes",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox"), "Chrome": TERM_REFERENCE("brand-name-chrome")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("switch-switching-to-firefox-is-fast"),
                value=REPLACE(
                    "firefox/switch.lang",
                    "Switching to Firefox is fast, easy and risk-free, because Firefox imports your bookmarks, autofills, passwords and preferences from Chrome.",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox"), "Chrome": TERM_REFERENCE("brand-name-chrome")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("switch-switching-to-firefox-page-description"),
                value=REPLACE(
                    "firefox/switch.lang",
                    "Switching to Firefox is fast, easy and risk-free. Firefox imports your bookmarks, autofills, passwords and preferences from Chrome.",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox"), "Chrome": TERM_REFERENCE("brand-name-chrome")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("switch-select-what-to-take"),
                value=REPLACE("firefox/switch.lang", "Select what to take from Chrome.", {"Chrome": TERM_REFERENCE("brand-name-chrome")}),
            ),
            FTL.Message(
                id=FTL.Identifier("switch-let-firefox-do-the-rest"),
                value=REPLACE("firefox/switch.lang", "Let Firefox do the rest.", {"Firefox": TERM_REFERENCE("brand-name-firefox")}),
            ),
            FTL.Message(
                id=FTL.Identifier("switch-use-firefox-and-still-chrome"),
                value=REPLACE(
                    "firefox/switch.lang",
                    "You can use Firefox and still have Chrome. Chrome won’t change on your machine one bit.",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox"), "Chrome": TERM_REFERENCE("brand-name-chrome")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("switch-share-with-your-friends"),
                value=REPLACE(
                    "firefox/switch.lang", "Share with your friends how to switch to Firefox", {"Firefox": TERM_REFERENCE("brand-name-firefox")}
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("switch-firefox-makes-switching-fast-tweet"),
                value=REPLACE(
                    "firefox/switch.lang",
                    "🔥 Firefox makes switching from Chrome really fast. Try it out!",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox"), "Chrome": TERM_REFERENCE("brand-name-chrome")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("switch-switch-to-firefox"),
                value=REPLACE("firefox/switch.lang", "Switch to Firefox", {"Firefox": TERM_REFERENCE("brand-name-firefox")}),
            ),
            FTL.Message(
                id=FTL.Identifier("switch-firefox-makes-switching-fast-email"),
                value=REPLACE(
                    "firefox/switch.lang",
                    "Firefox makes switching from Chrome really fast. I like it a lot, and you should try it.",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox"), "Chrome": TERM_REFERENCE("brand-name-chrome")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("switch-still-not-convinced"),
                value=REPLACE(
                    "firefox/switch.lang", "Still not convinced that switching to Firefox is easy?", {"Firefox": TERM_REFERENCE("brand-name-firefox")}
                ),
            ),
        ],
    )

    ctx.add_transforms(
        "firefox/switch.ftl",
        "firefox/switch.ftl",
        transforms_from(
            """
switch-enjoy-the-web-faster = {COPY(switch, "Enjoy the web faster, all set up for you.",)}
switch-download-and-switch = {COPY(switch, "Download and switch",)}
switch-share-to-facebook = {COPY(switch, "Share to Facebook",)}
switch-send-a-tweet = {COPY(switch, "Send a tweet",)}
switch-hey = {COPY(switch, "Hey,",)}
switch-check-it-out = {COPY(switch, "Check it out and let me know what you think:",)}
switch-send-an-email = {COPY(switch, "Send an email",)}
""",
            switch=switch,
        ),
    )
