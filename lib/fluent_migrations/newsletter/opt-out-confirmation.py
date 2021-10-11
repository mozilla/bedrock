from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

opt_out_confirmation = "newsletter/opt-out-confirmation.lang"


def migrate(ctx):
    """Migrate bedrock/newsletter/templates/newsletter/opt-out-confirmation.html, part {index}."""

    ctx.add_transforms(
        "newsletter/opt-out-confirmation.ftl",
        "newsletter/opt-out-confirmation.ftl",
        transforms_from(
            """
opt-out-confirmation-cool-we-hear = {COPY(opt_out_confirmation, "Cool. We hear you.",)}
opt-out-confirmation-youre-now-opted = {COPY(opt_out_confirmation, "You’re now opted out of a series of emails about setting up your account.",)}
opt-out-confirmation-youll-continue = {COPY(opt_out_confirmation, "You’ll continue to receive other emails you’re subscribed to, along with occasional important updates about your account. To manage all your subscriptions, enter your email below — we need to make sure we’re talking to the right person.",)}
opt-out-confirmation-your-email = {COPY(opt_out_confirmation, "Your email address:",)}
opt-out-confirmation-yournameexamplecom = {COPY(opt_out_confirmation, "yourname@example.com",)}
opt-out-confirmation-manage-preferences = {COPY(opt_out_confirmation, "Manage Preferences",)}
opt-out-confirmation-prefer-to-get = {COPY(opt_out_confirmation, "Prefer to get information another way?",)}
opt-out-confirmation-check-out-our = {COPY(opt_out_confirmation, "Check out our blogs",)}
opt-out-confirmation-get-help = {COPY(opt_out_confirmation, "Get help",)}
""",
            opt_out_confirmation=opt_out_confirmation,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("opt-out-confirmation-subscribe-to"),
                value=REPLACE(
                    opt_out_confirmation,
                    "Subscribe to occasional newsletter updates from Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ],
    )
