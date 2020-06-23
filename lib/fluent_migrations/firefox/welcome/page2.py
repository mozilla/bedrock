from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

page2 = "firefox/welcome/page2.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/welcome/page2.html, part {index}."""

    ctx.add_transforms(
        "firefox/welcome/page2.ftl",
        "firefox/welcome/page2.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("welcome-page2-pocket-save-news-videos-stories"),
                value=REPLACE(
                    page2,
                    "Pocket - Save news, videos, stories and more",
                    {
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                    }
                )
            ),
        ] + transforms_from("""
welcome-page2-your-time-online-is-worth = {COPY(page2, "Your time online is worth protecting",)}
""", page2=page2) + [
            FTL.Message(
                id=FTL.Identifier("welcome-page2-discover-and-save-stories"),
                value=REPLACE(
                    page2,
                    "Discover and save stories in Pocket — and come back to them when you’re free.",
                    {
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("welcome-page2-activate-pocket"),
                value=REPLACE(
                    page2,
                    "Activate Pocket",
                    {
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                    }
                )
            ),
        ] + transforms_from("""
welcome-page2-pocket = { -brand-name-pocket }
""", page2=page2) + [
            FTL.Message(
                id=FTL.Identifier("welcome-page2-pocket-is-built-right-into"),
                value=REPLACE(
                    page2,
                    "Pocket is built right into Firefox, so you can easily save stories as you find them, then read them later on any device.",
                    {
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
welcome-page2-save-content-from-everywhere = {COPY(page2, "Save content from everywhere",)}
""", page2=page2) + [
            FTL.Message(
                id=FTL.Identifier("welcome-page2-grab-articles-videos-and-links"),
                value=REPLACE(
                    page2,
                    "Grab articles, videos, and links from any website by clicking the Pocket icon in your browser toolbar.",
                    {
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                    }
                )
            ),
        ] + transforms_from("""
welcome-page2-discover-new-stories = {COPY(page2, "Discover new stories",)}
""", page2=page2) + [
            FTL.Message(
                id=FTL.Identifier("welcome-page2-pocket-shows-recommended-stories"),
                value=REPLACE(
                    page2,
                    "Pocket shows recommended stories every time you open a new tab. Save the ones that interest you.",
                    {
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                    }
                )
            ),
        ] + transforms_from("""
welcome-page2-why-am-i-seeing-this = {COPY(page2, "Why am I seeing this?",)}
""", page2=page2)
        )
