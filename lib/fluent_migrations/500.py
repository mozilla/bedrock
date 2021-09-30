from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

error_page = "mozorg/500.lang"


def migrate(ctx):
    """Migrate bedrock/base/templates/500.html, part {index}."""

    ctx.add_transforms(
        "500.ftl",
        "500.ftl",
        transforms_from(
            """
error-page-error-page-internal-server-error = {COPY(error_page, "500: Internal Server Error",)}
error-page-something-went-wrong = {COPY(error_page, "Something went wrong",)}
error-page-its-probably-just-a-server-error = {COPY(error_page, "It’s probably just a server error and we’re working to fix it.",)}
""",
            error_page=error_page,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("error-page-you-can-also-try-refreshing"),
                value=REPLACE(
                    error_page,
                    "You can also try refreshing this page or go to <a href=%(firefox)s>firefox.com</a> or <a href=%(mozilla)s>mozilla.org</a>",
                    {
                        "%%": "%",
                        "%(firefox)s": VARIABLE_REFERENCE("firefox"),
                        "%(mozilla)s": VARIABLE_REFERENCE("mozilla"),
                    },
                ),
            ),
        ],
    )
