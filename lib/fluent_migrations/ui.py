from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

main = "main.lang"


def migrate(ctx):
    """Migrate common UI strings from main.lang, part {index}."""

    ctx.add_transforms(
        "ui.ftl",
        "ui.ftl",
        transforms_from(
            """
ui-back-to-home-page = {COPY(main, "Back to home page",)}
ui-return-to-top = {COPY(main, "Return to top",)}
ui-close = {COPY(main, "Close",)}
ui-previous = {COPY(main, "Previous",)}
ui-next = {COPY(main, "Next",)}
ui-watch-the-video = {COPY(main, "Watch the video",)}
ui-replay = {COPY(main, "Replay",)}
ui-share = {COPY(main, "Share",)}
ui-menu = {COPY(main, "Menu",)}
ui-please-turn-on-javascript = {COPY(main, "Please turn on JavaScript to display this page correctly.",)}
ui-show-more = {COPY(main, "Show More",)}
ui-show-less = {COPY(main, "Show Less",)}
ui-show-all = {COPY(main, "Show All",)}
ui-hide-all = {COPY(main, "Hide All",)}
ui-learn-more = {COPY(main, "Learn more",)}
""",
            main=main,
        ),
    )
