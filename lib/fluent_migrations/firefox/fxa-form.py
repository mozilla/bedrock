from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

main = "main.lang"


def migrate(ctx):
    """Migrate bedrock/base/templates/macros.html, part {index}."""

    ctx.add_transforms(
        "fxa_form.ftl",
        "fxa_form.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("fxa-form-enter-your-email"),
                value=REPLACE(
                    "main.lang",
                    "<strong>Enter your email</strong> to access Firefox Accounts.",
                    {
                        "Firefox Accounts": TERM_REFERENCE("brand-name-firefox-accounts"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("fxa-form-by-proceeding"),
                value=REPLACE(
                    "main.lang",
                    'By proceeding, you agree to the <a href="%(url1)s">Terms of Service</a> and <a href="%(url2)s">Privacy Notice</a>.',
                    {
                        "%%": "%",
                        "%(url1)s": VARIABLE_REFERENCE("url1"),
                        "%(url2)s": VARIABLE_REFERENCE("url2"),
                    },
                ),
            ),
        ],
    )

    ctx.add_transforms(
        "fxa_form.ftl",
        "fxa_form.ftl",
        transforms_from(
            """
fxa-form-email-address = {COPY(main, "Email address",)}
fxa-form-continue = {COPY(main, "Continue",)}
fxa-form-create-account = {COPY(main, "Create account",)}
fxa-form-get-the-app = {COPY(main, "Get the app",)}
""",
            main=main,
        ),
    )
