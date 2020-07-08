from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

memory = "firefox/features/memory.lang"
shared = "firefox/shared.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/features/memory.html, part {index}."""

    ctx.add_transforms(
        "firefox/features/memory.ftl",
        "firefox/features/memory.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("features-memory-firefox-browser-use-less"),
                value=REPLACE(
                    memory,
                    "Firefox Browser: Use less memory, get more speed",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("features-memory-is-your-computer-slow-your"),
                value=REPLACE(
                    memory,
                    "Is your computer slow? Your browser might be using too much memory. Switch to Firefox today for more speed.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("features-memory-less-memory-usage-than-chrome"),
                value=REPLACE(
                    memory,
                    "Less memory usage than Chrome",
                    {
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("features-memory-if-your-web-browser-uses"),
                value=REPLACE(
                    memory,
                    "If your web browser uses too much memory, switch to Firefox.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-memory-speed-up-your-computer = {COPY(memory, "Speed up your computer",)}
""", memory=memory) + [
            FTL.Message(
                id=FTL.Identifier("features-memory-every-computer-program-you"),
                value=REPLACE(
                    memory,
                    "Every computer program you run takes up some memory. When too much is used, your system can slooooowww down. Firefox aims for a balance — using enough memory to let you browse smoothly and leaving plenty of memory to keep your computer responsive.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-memory-stop-running-out-of-memory = {COPY(memory, "Stop running out of memory",)}
""", memory=memory) + [
            FTL.Message(
                id=FTL.Identifier("features-memory-chrome-uses-up-to-177x-more"),
                value=REPLACE(
                    memory,
                    "<a href=\"%(url)s\">Chrome uses up to 1.77x more memory than Firefox</a>. If your computer is already low on memory, this can cause a significant slowdown. Using Firefox’s latest version with multi-process can result in more available memory to run your favorite programs.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
        ] + transforms_from("""
features-memory-browse-faster-privately = {COPY(memory, "Browse faster, privately",)}
""", memory=memory) + [
            FTL.Message(
                id=FTL.Identifier("features-memory-explore-the-web-faster-with"),
                value=REPLACE(
                    memory,
                    "Explore the web faster with <a href=\"%(url)s\">Firefox Private Browsing</a>. Only Firefox’s private mode includes tracking protection which blocks ads with trackers from loading on pages. Decluttering sites means web pages can load faster.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
        )
