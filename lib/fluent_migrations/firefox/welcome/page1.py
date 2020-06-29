from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

page1 = "firefox/welcome/page1.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/welcome/page1.html, part {index}."""

    ctx.add_transforms(
        "firefox/welcome/page1.ftl",
        "firefox/welcome/page1.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("welcome-page1-more-than-a-browser-firefox"),
                value=REPLACE(
                    page1,
                    "More than a browser - Firefox Monitor is your lookout for hackers",
                    {
                        "Firefox Monitor": TERM_REFERENCE("brand-name-firefox-monitor"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("welcome-page1-take-the-next-step-to-protect"),
                value=REPLACE(
                    page1,
                    "Take the next step to protect your privacy online with the Firefox family of products.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("welcome-page1-stay-ahead-of-hackers-check"),
                value=REPLACE(
                    page1,
                    "Stay ahead of hackers. Check for data breaches with Firefox Monitor.",
                    {
                        "Firefox Monitor": TERM_REFERENCE("brand-name-firefox-monitor"),
                    }
                )
            ),
        ] + transforms_from("""
welcome-page1-youre-on-track-to-stay-protected = {COPY(page1, "You’re on track to stay protected",)}
welcome-page1-youve-got-the-web-browser = {COPY(page1, "You’ve got the web browser that protects your privacy — now it’s time to get a lookout for hackers.",)}
welcome-page1-check-your-breach-report = {COPY(page1, "Check Your Breach Report",)}
welcome-page1-firefox-monitor = { -brand-name-firefox-monitor }
""", page1=page1) + [
            FTL.Message(
                id=FTL.Identifier("welcome-page1-firefox-monitor-shows-you"),
                value=REPLACE(
                    page1,
                    "Firefox Monitor shows you if your information has been leaked in a known data breach, and alerts you in case it happens in the future.",
                    {
                        "Firefox Monitor": TERM_REFERENCE("brand-name-firefox-monitor"),
                    }
                )
            ),
        ] + transforms_from("""
welcome-page1-stay-ahead-of-hackers = {COPY(page1, "Stay ahead of hackers",)}
""", page1=page1) + [
            FTL.Message(
                id=FTL.Identifier("welcome-page1-find-ways-to-protect-your"),
                value=REPLACE(
                    page1,
                    "Find ways to protect your info with <a href=\"%(security_tips)s\">Monitor Security Tips</a>.",
                    {
                        "%%": "%",
                        "%(security_tips)s": VARIABLE_REFERENCE("security_tips"),
                        "Monitor": TERM_REFERENCE("brand-name-monitor"),
                    }
                )
            ),
        ] + transforms_from("""
welcome-page1-stay-in-the-know = {COPY(page1, "Stay in the know",)}
""", page1=page1) + [
            FTL.Message(
                id=FTL.Identifier("welcome-page1-were-you-one-of-many"),
                value=REPLACE(
                    page1,
                    "Were you one of 100,985,047 invited to the <a href=\"%(evite_breach)s\">Evite data breach “party”</a>?",
                    {
                        "%%": "%",
                        "%(evite_breach)s": VARIABLE_REFERENCE("evite_breach"),
                    }
                )
            ),
        ] + transforms_from("""
welcome-page1-why-am-i-seeing-this = {COPY(page1, "Why am I seeing this?",)}
""", page1=page1)
        )
