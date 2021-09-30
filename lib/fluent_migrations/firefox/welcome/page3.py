from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

page3 = "firefox/welcome/page3.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/welcome/page3.html, part {index}."""

    ctx.add_transforms(
        "firefox/welcome/page3.ftl",
        "firefox/welcome/page3.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("welcome-page3-get-the-free-account-that"),
                value=REPLACE(
                    page3,
                    "Get the free account that protects your privacy. Join Firefox.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page3-no-account-required-but-you = {COPY(page3, "No account required. But you might want one.",)}
""",
            page3=page3,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("welcome-page3-the-firefox-browser-collects"),
                value=REPLACE(
                    page3,
                    "The Firefox browser collects so little data about you, we don’t even require your email address. But when you use it to create a Firefox account, we can protect your privacy across more of your online life.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Firefox account": TERM_REFERENCE("brand-name-firefox-account"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page3-firefox-monitor = { -brand-name-firefox-monitor }
welcome-page3-have-at-least-one-company = {COPY(page3, "Have at least one company looking out for your data, instead of leaking it.",)}
welcome-page3-firefox-lockwise = { -brand-name-firefox-lockwise }
welcome-page3-never-forget-reset-or-travel = {COPY(page3, "Never forget, reset or travel without your passwords again.",)}
welcome-page3-facebook-container = { -brand-name-facebook-container }
""",
            page3=page3,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("welcome-page3-get-a-container-to-keep-facebook"),
                value=REPLACE(
                    page3,
                    "Get a container to keep Facebook out of your business.",
                    {
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
welcome-page3-pocket = { -brand-name-pocket }
welcome-page3-trade-clickbait-and-fake-news = {COPY(page3, "Trade clickbait and fake news for quality content.",)}
welcome-page3-firefox-send = { -brand-name-firefox-send }
welcome-page3-send-huge-files-to-anyone = {COPY(page3, "Send huge files to anyone you want, with self-destructing links.",)}
welcome-page3-why-am-i-seeing-this = {COPY(page3, "Why am I seeing this?",)}
""",
            page3=page3,
        ),
    )
