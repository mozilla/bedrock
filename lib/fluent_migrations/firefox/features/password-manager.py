from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

password_manager = "firefox/features/password-manager.lang"
shared = "firefox/shared.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/features/password-manager.html, part {index}."""

    ctx.add_transforms(
        "firefox/features/password-manager.ftl",
        "firefox/features/password-manager.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("password-manager-firefox-browser"),
                value=REPLACE(
                    password_manager,
                    "Firefox Browser: Fast, Easy Password Manager",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("password-manager-firefox-password"),
                value=REPLACE(
                    password_manager,
                    "Firefox Password Manager saves all your passwords in one place so you can automatically login to sites, or retrieve saved passwords.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
password-manager-password-manager = {COPY(password_manager, "Password Manager achievement unlocked",)}
""", password_manager=password_manager) + [
            FTL.Message(
                id=FTL.Identifier("password-manager-give-up-the-memory"),
                value=REPLACE(
                    password_manager,
                    "Give up the memory game with Firefox Password Manager.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
password-manager-password-hero = {COPY(password_manager, "Password hero",)}
""", password_manager=password_manager) + [
            FTL.Message(
                id=FTL.Identifier("password-manager-forget-the-reset"),
                value=REPLACE(
                    password_manager,
                    "Forget the reset. Firefox Password Manager keeps all your passwords so you can log in automatically, or find saved passwords easily. For super security, give your computer a <a href=\"%(url)s\">master password</a>.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
password-manager-password-ninja = {COPY(password_manager, "Password ninja",)}
""", password_manager=password_manager) + [
            FTL.Message(
                id=FTL.Identifier("password-manager-no-more-try-again"),
                value=REPLACE(
                    password_manager,
                    "No more “try again” while you’re trying to get somewhere. Log in to your Firefox Account on your phone, and your passwords come with you. Your login details will simply appear, just like that.",
                    {
                        "Firefox Account": TERM_REFERENCE("brand-name-firefox-account"),
                    }
                )
            ),
        ] + transforms_from("""
password-manager-password-master = {COPY(password_manager, "Password master",)}
""", password_manager=password_manager) + [
            FTL.Message(
                id=FTL.Identifier("password-manager-earn-your-second"),
                value=REPLACE(
                    password_manager,
                    "Earn your second security black belt with Firefox’s vast array of password manager <a href=\"%(addons)s\">add-ons</a>. Choose an existing favorite or find a next-level one through expert community ratings and reviews.",
                    {
                        "%%": "%",
                        "%(addons)s": VARIABLE_REFERENCE("addons"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
        )
