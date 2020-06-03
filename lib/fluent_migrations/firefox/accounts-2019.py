from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

accounts_2019 = "firefox/accounts-2019.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/accounts-2019.html, part {index}."""

    ctx.add_transforms(
        "firefox/accounts.ftl",
        "firefox/accounts.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("firefox-accounts-there-is-a-way-to"),
                value=REPLACE(
                    accounts_2019,
                    "There is a way to protect your privacy. Join Firefox.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-accounts-get-a-firefox-account"),
                value=REPLACE(
                    accounts_2019,
                    "Get a Firefox Account – Keep your data private, safe and synced",
                    {
                        "Firefox Account": TERM_REFERENCE("brand-name-firefox-account"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-accounts-take-your-stand-stay-smart = {COPY(accounts_2019, "Take your stand against an industry that’s selling your data to third parties. Stay smart and safe online with technology that fights for you.",)}
""", accounts_2019=accounts_2019) + [
            FTL.Message(
                id=FTL.Identifier("firefox-accounts-securely-sync-your"),
                value=REPLACE(
                    accounts_2019,
                    "Securely sync your passwords, bookmarks and tabs across all your devices. Get a Firefox Account now – One login – Power and privacy everywhere.",
                    {
                        "Firefox Account": TERM_REFERENCE("brand-name-firefox-account"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-accounts-there-is-a-way-to-protect"),
                value=REPLACE(
                    accounts_2019,
                    "There is a way to protect your privacy. <span>Join Firefox.</span>",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-accounts-take-your-stand-against = {COPY(accounts_2019, "Take your stand against an industry that’s making you the product.",)}
""", accounts_2019=accounts_2019) + [
            FTL.Message(
                id=FTL.Identifier("firefox-accounts-youre-signed-in-to"),
                value=REPLACE(
                    accounts_2019,
                    "You’re signed <br>in to Firefox. <br><span>Now try Firefox Monitor.</span>",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Firefox Monitor": TERM_REFERENCE("brand-name-firefox-monitor"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-accounts-see-if-youve-been = {COPY(accounts_2019, "See if you’ve been involved in an online data breach.",)}
""", accounts_2019=accounts_2019) + [
            FTL.Message(
                id=FTL.Identifier("firefox-accounts-sign-in-to-monitor"),
                value=REPLACE(
                    accounts_2019,
                    "Sign In to Monitor",
                    {
                        "Monitor": TERM_REFERENCE("brand-name-monitor"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-accounts-join-firefox"),
                value=REPLACE(
                    accounts_2019,
                    "Join Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-accounts-enter-your-email-address = {COPY(accounts_2019, "Enter your email address to get started.",)}
firefox-accounts-already-have-an-account = {COPY(accounts_2019, "Already have an account?",)}
firefox-accounts-sign-in = {COPY(accounts_2019, "Sign In",)}
firefox-accounts-meet-our-family-of = {COPY(accounts_2019, "Meet our family of privacy-first products.",)}
""", accounts_2019=accounts_2019) + [
            FTL.Message(
                id=FTL.Identifier("firefox-accounts-firefox-is-technology"),
                value=REPLACE(
                    accounts_2019,
                    "Firefox is technology that fights for you.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-accounts-get-technology-that = {COPY(accounts_2019, "Get technology that fights for you.",)}
firefox-accounts-travel-the-internet = {COPY(accounts_2019, "Travel the internet with protection, on every device.",)}
firefox-accounts-keep-your-passwords = {COPY(accounts_2019, "Keep your passwords protected and portable.",)}
firefox-accounts-get-a-lookout-for = {COPY(accounts_2019, "Get a lookout for data breaches.",)}
firefox-accounts-share-large-files = {COPY(accounts_2019, "Share large files without prying eyes.",)}
firefox-accounts-get-it-all-on-every = {COPY(accounts_2019, "Get it all on every device, without feeling trapped in a single operating system.",)}
firefox-accounts-and-get-it-all-on = {COPY(accounts_2019, "And get it all on every device, without feeling trapped in a single operating system.",)}
firefox-accounts-get-the-respect-you = {COPY(accounts_2019, "Get the respect you deserve.",)}
""", accounts_2019=accounts_2019) + [
            FTL.Message(
                id=FTL.Identifier("firefox-accounts-youll-always-get-the"),
                value=REPLACE(
                    accounts_2019,
                    "You’ll always get the truth from us. Everything we make and do honors our <a href=\"%(promise)s\">Personal Data Promise</a>:",
                    {
                        "%%": "%",
                        "%(promise)s": VARIABLE_REFERENCE("promise"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-accounts-take-less-keep-it = {COPY(accounts_2019, "Take less.<br> Keep it safe.<br> No secrets.",)}
firefox-accounts-get-the-knowledge = {COPY(accounts_2019, "Get the knowledge to keep you safe.",)}
firefox-accounts-learn-everything-you = {COPY(accounts_2019, "Learn everything you need to know (but don’t yet) about staying smart and safe online, from some of the world’s foremost experts.",)}
firefox-accounts-and-be-part-of-protecting = {COPY(accounts_2019, "And be part of protecting the internet for future generations.",)}
""", accounts_2019=accounts_2019) + [
            FTL.Message(
                id=FTL.Identifier("firefox-accounts-help-us-build-a-better"),
                value=REPLACE(
                    accounts_2019,
                    "Help us build a better Firefox for all.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
firefox-accounts-get-into-the-open = {COPY(accounts_2019, "Get into the open source spirit by test-driving upcoming products.",)}
firefox-accounts-help-us-keep-big-tech = {COPY(accounts_2019, "Help us keep Big Tech in check.",)}
firefox-accounts-we-support-communities = {COPY(accounts_2019, "We support communities all over the world standing up for a healthier internet. Add your voice to the fight.",)}
firefox-accounts-firefox-browser = { -brand-name-firefox-browser }
firefox-accounts-firefox-lockwise = { -brand-name-firefox-lockwise }
firefox-accounts-firefox-monitor = { -brand-name-firefox-monitor }
firefox-accounts-firefox-send = { -brand-name-firefox-send }
""", accounts_2019=accounts_2019)
        )
