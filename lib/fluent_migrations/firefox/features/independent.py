from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

independent = "firefox/features/independent.lang"
shared = "firefox/shared.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/features/independent.html, part {index}."""

    ctx.add_transforms(
        "firefox/features/independent.ftl",
        "firefox/features/independent.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("features-independent-firefox-a-different"),
                value=REPLACE(
                    independent,
                    "Firefox, a different browser for different times. Browse free.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-independent-browse-the-internet = {COPY(independent, "Browse the Internet as it was meant to be… free, safe and accessible to all. Declare your online independence.",)}
""", independent=independent) + [
            FTL.Message(
                id=FTL.Identifier("features-independent-firefox-rebel-with-a"),
                value=REPLACE(
                    independent,
                    "Firefox: Rebel with a cause",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("features-independent-firefox-is-independent"),
                value=REPLACE(
                    independent,
                    "Firefox is independent and a part of the non-profit Mozilla, which fights for your online rights, keeps corporate powers in check and makes the Internet accessible to everyone, everywhere.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-independent-no-strings-attached = {COPY(independent, "No strings attached",)}
""", independent=independent) + [
            FTL.Message(
                id=FTL.Identifier("features-independent-firefox-is-built-by"),
                value=REPLACE(
                    independent,
                    "Firefox is built by a non-profit. That means we can do things that others can’t, like build new products and features without a hidden agenda. We champion your right to privacy with tools like Private Browsing with Tracking Protection.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("features-independent-firefox-is-built-by-old"),
                value=REPLACE(
                    independent,
                    "Firefox is built by a non-profit. That means we can do things that others can’t, like build new products and features without a hidden agenda. We champion your right to privacy with tools like Private Browsing with Tracking Protection, which go beyond what Google Chrome and Microsoft Edge offer.",
                    {
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                    }
                )
            ),
        ] + transforms_from("""
features-independent-what-you-see-is-what = {COPY(independent, "What you see is what you get",)}
features-independent-we-believe-the-internet = {COPY(independent, "We believe the Internet is for people, not profit. Unlike other companies, we don’t sell access to your data. <em>You’re</em> in control over who sees your search and browsing history. Choice — that’s what a healthy Internet is all about!",)}
features-independent-a-browser-on-a-mission = {COPY(independent, "A browser on a mission",)}
""", independent=independent) + [
            FTL.Message(
                id=FTL.Identifier("features-independent-in-addition-to-fighting"),
                value=REPLACE(
                    independent,
                    "In addition to fighting for your online rights, we also keep corporate powers in check, while working with allies all around the globe to nurture healthy Internet practices. So when you choose Firefox, we’re choosing you, too.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("features-independent-firefox-is-a-browser"),
                value=REPLACE(
                    independent,
                    "Firefox is a browser with a conscience. As part of the technology non-profit Mozilla, we fight for your online rights, keep corporate powers in check and help educate developing countries on healthy Internet practices. So when you choose Firefox, we’re choosing you, too.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
        )
