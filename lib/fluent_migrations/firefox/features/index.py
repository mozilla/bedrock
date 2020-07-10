from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

index = "firefox/features/index.lang"
shared = "firefox/shared.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/features/index.html, part {index}."""

    ctx.add_transforms(
        "firefox/features/index.ftl",
        "firefox/features/index.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("features-index-protect-your-privacy-and-browse"),
                value=REPLACE(
                    index,
                    "Protect your privacy and browse faster with Firefox features",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("features-index-youre-in-control-with-firefoxs"),
                value=REPLACE(
                    index,
                    "You’re in control with Firefox’s easy-to-use features that protect your privacy and browsing speeds.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("features-index-explore-the-features-of-the"),
                value=REPLACE(
                    index,
                    "Explore the features of the all new Firefox browser",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("features-index-firefox-features"),
                value=REPLACE(
                    index,
                    "Firefox features",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-index-your-favorite-add-ons-and = {COPY(index, "Your favorite add-ons and extensions",)}
features-index-customize-your-browser = {COPY(index, "Customize your browser",)}
features-index-sync-between-devices = {COPY(index, "Sync between devices",)}
features-index-tabs-that-travel = {COPY(index, "Tabs that travel",)}
features-index-better-bookmarks = {COPY(index, "Better bookmarks",)}
features-index-more-powerful-private-browsing = {COPY(index, "More powerful Private Browsing",)}
features-index-ad-tracker-blocking = {COPY(index, "Ad tracker blocking",)}
features-index-password-manager = {COPY(index, "Password Manager",)}
features-index-balanced-memory-usage = {COPY(index, "Balanced memory usage",)}
features-index-browse-faster = {COPY(index, "Browse faster",)}
""", index=index) + [
            FTL.Message(
                id=FTL.Identifier("features-index-firefox-product-benefits"),
                value=REPLACE(
                    index,
                    "Firefox Product Benefits",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-index-open-source = {COPY(index, "Open source",)}
features-index-were-always-transparent = {COPY(index, "We’re always transparent.",)}
features-index-see-what-makes-us-different = {COPY(index, "See what makes us different",)}
""", index=index) + [
            FTL.Message(
                id=FTL.Identifier("features-index-by-non-profit-mozilla"),
                value=REPLACE(
                    index,
                    "By non-profit, Mozilla",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
features-index-protecting-the-health-of-the = {COPY(index, "Protecting the health of the internet.",)}
""", index=index) + [
            FTL.Message(
                id=FTL.Identifier("features-index-read-mozillas-mission"),
                value=REPLACE(
                    index,
                    "Read Mozilla’s mission",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
features-index-protect-your-rights = {COPY(index, "Protect your rights",)}
features-index-we-help-keep-corporate-powers = {COPY(index, "We help keep corporate powers in check.",)}
features-index-choose-independence = {COPY(index, "Choose independence",)}
features-index-limited-data-collection = {COPY(index, "Limited data collection",)}
features-index-opted-in-to-privacy-so-you = {COPY(index, "Opted-in to privacy, so you can browse freely.",)}
features-index-read-our-privacy-policy = {COPY(index, "Read our privacy policy",)}
features-index-more-private = {COPY(index, "More private",)}
features-index-we-dont-sell-access-to-your = {COPY(index, "We don’t sell access to your online data. Period.",)}
""", index=index) + [
            FTL.Message(
                id=FTL.Identifier("features-index-get-firefox-for-privacy"),
                value=REPLACE(
                    index,
                    "Get Firefox for privacy",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
        )
