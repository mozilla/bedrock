from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

page7 = "firefox/welcome/page7.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/welcome/page7.html, part {index}."""

    ctx.add_transforms(
        "firefox/welcome/page7.ftl",
        "firefox/welcome/page7.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("page7-make-it-harder-for-facebook"),
                value=REPLACE(
                    page7,
                    "Make it harder for Facebook to track you",
                    {
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("page7-its-okay-to-like-facebook"),
                value=REPLACE(
                    page7,
                    "It’s okay to like Facebook",
                    {
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("page7-if-you-still-kinda-like-facebook"),
                value=REPLACE(
                    page7,
                    "If you still kinda like Facebook but don’t trust them, then try the Facebook Container extension by Firefox and make it harder for them to track you around the web.",
                    {
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Facebook Container": TERM_REFERENCE("brand-name-facebook-container"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("page7-get-facebook-container"),
                value=REPLACE(
                    page7,
                    "Get Facebook Container",
                    {
                        "Facebook Container": TERM_REFERENCE("brand-name-facebook-container"),
                    }
                )
            ),
        ] + transforms_from("""
page7-do-it-for-the-gram = {COPY(page7, "Do it for the ’Gram",)}
""", page7=page7) + [
            FTL.Message(
                id=FTL.Identifier("page7-facebook-container-also-works"),
                value=REPLACE(
                    page7,
                    "Facebook Container also works on other Facebook owned sites like Instagram, Facebook Messenger and Workplace.",
                    {
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                        "Facebook Container": TERM_REFERENCE("brand-name-facebook-container"),
                        "Facebook Messenger": TERM_REFERENCE("brand-name-facebook-messenger"),
                        "Instagram": TERM_REFERENCE("brand-name-instagram"),
                        "Workplace": TERM_REFERENCE("brand-name-workplace"),
                    }
                )
            ),
        ] + transforms_from("""
page7-make-them-unfollow-you = {COPY(page7, "Make them unfollow you",)}
page7-that-sneaky-little-button = {COPY(page7, "That sneaky little button",)}
""", page7=page7) + [
            FTL.Message(
                id=FTL.Identifier("page7-those-innocent-looking-f-buttons"),
                value=REPLACE(
                    page7,
                    "Those innocent-looking F buttons from Facebook track your web activity, even if you don’t have an account. Facebook Container blocks them.",
                    {
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                        "Facebook Container": TERM_REFERENCE("brand-name-facebook-container"),
                    }
                )
            ),
        ] + transforms_from("""
page7-stay-ahead-of-hackers = {COPY(page7, "Stay ahead of hackers",)}
""", page7=page7) + [
            FTL.Message(
                id=FTL.Identifier("page7-firefox-monitor-lets-you-find"),
                value=REPLACE(
                    page7,
                    "Firefox Monitor lets you find out what hackers might already know about you and helps you stay a step ahead of them. (And it’s free.)",
                    {
                        "Firefox Monitor": TERM_REFERENCE("brand-name-firefox-monitor"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("page7-get-firefox-monitor"),
                value=REPLACE(
                    page7,
                    "Get Firefox Monitor",
                    {
                        "Firefox Monitor": TERM_REFERENCE("brand-name-firefox-monitor"),
                    }
                )
            ),
        ] + transforms_from("""
page7-why-am-i-seeing-this = {COPY(page7, "Why am I seeing this?",)}
""", page7=page7)
        )
