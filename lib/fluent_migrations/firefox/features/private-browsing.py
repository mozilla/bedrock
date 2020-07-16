from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

private_browsing = "firefox/features/private-browsing.lang"
shared = "firefox/shared.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/features/private-browsing.html, part {index}."""

    ctx.add_transforms(
        "firefox/features/private-browsing.ftl",
        "firefox/features/private-browsing.ftl",
        transforms_from("""
features-private-browsing-private-browser = {COPY(private_browsing, "Private Browser with extra tracking protection",)}
""", private_browsing=private_browsing) + [
            FTL.Message(
                id=FTL.Identifier("features-private-browsing-firefox-protects"),
                value=REPLACE(
                    private_browsing,
                    "Firefox protects your online privacy and blocks trackers that follow you around the web.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("features-private-browsing-firefox-more-protection"),
                value=REPLACE(
                    private_browsing,
                    "Firefox: More protection. Less worry.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("features-private-browsing-were-obsessed-with"),
                value=REPLACE(
                    private_browsing,
                    "We’re obsessed with protecting your privacy. That’s why we’ve made Firefox Private Browsing more powerful than the others.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-private-browsing-browse-without = {COPY(private_browsing, "Browse without a trace",)}
""", private_browsing=private_browsing) + [
            FTL.Message(
                id=FTL.Identifier("features-private-browsing-sharing-is-caring"),
                value=REPLACE(
                    private_browsing,
                    "Sharing is caring, but that should be your call. Firefox Private Browsing automatically erases your online info like passwords, cookies and history from your computer. So that when you close out, you leave no trace.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-private-browsing-catch-those-hidden = {COPY(private_browsing, "Catch those hidden trackers",)}
""", private_browsing=private_browsing) + [
            FTL.Message(
                id=FTL.Identifier("features-private-browsing-some-websites-and"),
                value=REPLACE(
                    private_browsing,
                    "Some websites and ads attach hidden trackers that collect your browsing info long after you’ve left. Only Firefox Private Browsing has tracking protection to block them automatically.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-private-browsing-shake-off-tracking = {COPY(private_browsing, "Shake off tracking weight",)}
""", private_browsing=private_browsing) + [
            FTL.Message(
                id=FTL.Identifier("features-private-browsing-not-only-do-trackers"),
                value=REPLACE(
                    private_browsing,
                    "Not only do trackers collect info, they can weigh down your browsing speeds. Only Firefox Private Browsing blocks ads with hidden trackers, so you can drop the baggage and browse freely.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
        )
