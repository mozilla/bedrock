from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

fast = "firefox/features/fast.lang"
shared = "firefox/shared.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/features/fast.html, part {index}."""

    ctx.add_transforms(
        "firefox/features/fast.ftl",
        "firefox/features/fast.ftl",
        transforms_from("""
features-fast-get-more-done-browse-faster = {COPY(fast, "Get more done. Browse faster and lighter with multiple tabs",)}
features-fast-our-new-powerful-multi-process = {COPY(fast, "Our new, powerful multi-process platform handles all your tabs without slowing down your computer.",)}
""", fast=fast) + [
            FTL.Message(
                id=FTL.Identifier("features-fast-firefox-is-now-faster-and-leaner"),
                value=REPLACE(
                    fast,
                    "Firefox is now faster and leaner",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-fast-weve-been-working-out-so-you = {COPY(fast, "We’ve been working out, so you can get more done.",)}
features-fast-use-less-memory = {COPY(fast, "Use less memory",)}
""", fast=fast) + [
            FTL.Message(
                id=FTL.Identifier("features-fast-no-one-likes-a-computer-hog"),
                value=REPLACE(
                    fast,
                    "No one likes a computer hog! Firefox is a lean, mean (actually we’re pretty nice) browsing machine. Since we use less RAM than Chrome, your other programs can keep running at top speed.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
        ] + transforms_from("""
features-fast-get-all-the-tabs-without-lags = {COPY(fast, "Get all the tabs without lags",)}
""", fast=fast) + [
            FTL.Message(
                id=FTL.Identifier("features-fast-multi-tasking-with-multiple"),
                value=REPLACE(
                    fast,
                    "Multi-tasking with multiple tabs just got easier. Firefox is now a multi-process browser, which means that your tabs stay fresh and won’t take forever to reload. With 86% less hang time, switch quickly between tabs even as you open more.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-fast-level-up-browser-gameplay = {COPY(fast, "Level-up browser gameplay",)}
""", fast=fast) + [
            FTL.Message(
                id=FTL.Identifier("features-fast-we-led-the-tech-to-run-3d-games"),
                value=REPLACE(
                    fast,
                    "We led the tech to run 3D games at near-native speeds, and now Firefox is bringing better performance to online gaming. Our powerful browser reduces lags, speeds up ping times and optimizes overall gameplay through faster, leaner browsing.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
        )
