from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

lockwise = "firefox/products/lockwise.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/lockwise/lockwise.html, part {index}."""

    ctx.add_transforms(
        "firefox/products/lockwise.ftl",
        "firefox/products/lockwise.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("lockwise-firefox-lockwise-password"),
                value=REPLACE(
                    lockwise,
                    "Firefox Lockwise — password manager — take your passwords everywhere",
                    {
                        "Firefox Lockwise": TERM_REFERENCE("brand-name-firefox-lockwise"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("lockwise-firefox-lockwise-lets-you"),
                value=REPLACE(
                    lockwise,
                    "Firefox Lockwise lets you securely access the passwords you’ve saved in Firefox from anywhere — even outside of the browser. Features 256-bit encryption and Face/Touch ID.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Firefox Lockwise": TERM_REFERENCE("brand-name-firefox-lockwise"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
lockwise-firefox-lockwise = { -brand-name-firefox-lockwise }
lockwise-take-your-passwords-everywhere = {COPY(lockwise, "Take your passwords everywhere",)}
""",
            lockwise=lockwise,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("lockwise-securely-access-the-passwords"),
                value=REPLACE(
                    lockwise,
                    "Securely access the passwords you’ve saved in Firefox from anywhere — even outside of the browser.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("lockwise-try-lockwise-now"),
                value=REPLACE(
                    lockwise,
                    "Try Lockwise now",
                    {
                        "Lockwise": TERM_REFERENCE("brand-name-lockwise"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("lockwise-install-for-firefox"),
                value=REPLACE(
                    lockwise,
                    "Install for Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("lockwise-open-in-firefox"),
                value=REPLACE(
                    lockwise,
                    "Open in Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("lockwise-only-in-the-firefox-browser"),
                value=REPLACE(
                    lockwise,
                    "Only in the Firefox Browser",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
lockwise-256-bit-encryption-protects = {COPY(lockwise, "256-bit encryption protects you while syncing",)}
lockwise-get-to-your-passwords-securely = {COPY(lockwise, "Get to your passwords securely with Face or Touch ID",)}
lockwise-your-privacy-comes-first = {COPY(lockwise, "Your privacy comes first.",)}
lockwise-we-keep-your-data-safe = {COPY(lockwise, "We keep your data safe, never sold.",)}
lockwise-support = {COPY(lockwise, "Support",)}
lockwise-your-privacy = {COPY(lockwise, "Your Privacy",)}
lockwise-github = { -brand-name-github }
""",
            lockwise=lockwise,
        ),
    )
