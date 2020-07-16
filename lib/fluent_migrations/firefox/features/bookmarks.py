from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

bookmarks = "firefox/features/bookmarks.lang"
shared = "firefox/shared.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/features/bookmarks.html, part {index}."""

    ctx.add_transforms(
        "firefox/features/bookmarks.ftl",
        "firefox/features/bookmarks.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("features-bookmarks-firefox-browser-better"),
                value=REPLACE(
                    bookmarks,
                    "Firefox Browser: Better bookmarks everywhere you go",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    }
                )
            ),
        ] + transforms_from("""
features-bookmarks-easily-organize-your-bookmarks = {COPY(bookmarks, "Easily organize your bookmarks into folder and access them across all your devices, from desktop to mobile.",)}
features-bookmarks-better-bookmarks = {COPY(bookmarks, "Better bookmarks",)}
""", bookmarks=bookmarks) + [
            FTL.Message(
                id=FTL.Identifier("features-bookmarks-dont-agonize-lovers-of"),
                value=REPLACE(
                    bookmarks,
                    "Don’t agonize, lovers of bookmarking. Organize with Firefox.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-bookmarks-file-that-bookmark = {COPY(bookmarks, "File that bookmark",)}
features-bookmarks-get-your-faves-all-sorted = {COPY(bookmarks, "Get your faves all sorted with the bookmark star icon, which lets you add custom names and folders quickly. Then dial in your bookmarks toolbar to make sure you never lose sight of the links you love.",)}
features-bookmarks-fly-with-that-bookmark = {COPY(bookmarks, "Fly with that bookmark",)}
""", bookmarks=bookmarks) + [
            FTL.Message(
                id=FTL.Identifier("features-bookmarks-take-your-favorites-on"),
                value=REPLACE(
                    bookmarks,
                    "Take your favorites on the fly. Use Firefox Sync to access your bookmarks across all your devices, from desktop to mobile. Or try <a href=\"%(url)s\">Pocket</a> to save any online article, or page and come back to later – even without internet.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                        "Firefox Sync": TERM_REFERENCE("brand-name-firefox-sync"),
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                    }
                )
            ),
        ] + transforms_from("""
features-bookmarks-futz-with-that-bookmark = {COPY(bookmarks, "Futz with that bookmark",)}
""", bookmarks=bookmarks) + [
            FTL.Message(
                id=FTL.Identifier("features-bookmarks-practice-your-exactitude"),
                value=REPLACE(
                    bookmarks,
                    "Practice your exactitude with every bookmark manager <a href=\"%(url)s\">add-on</a> you can think of, from full page snapshots to quick-switch sidebars to locked-down-tight private bookmarks.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                    }
                )
            ),
        ]
        )
