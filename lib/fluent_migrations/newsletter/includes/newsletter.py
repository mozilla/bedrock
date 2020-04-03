from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

main = "main.lang"

def migrate(ctx):
    """Migrate bedrock/newsletter/templates/newsletter/includes/form-protocol.html, part {index}."""

    ctx.add_transforms(
        "newsletter_form.ftl",
        "newsletter_form.ftl",
        transforms_from("""
newsletter-form-your-email-here = {COPY(main, "YOUR EMAIL HERE",)}
newsletter-form-format = {COPY(main, "Format",)}
newsletter-form-html = {COPY(main, "HTML",)}
newsletter-form-text = {COPY(main, "Text",)}
""", main=main) + [
            FTL.Message(
                id=FTL.Identifier("newsletter-form-get-firefox-news"),
                value=REPLACE(
                    main,
                    "Get Firefox news",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletter-form-im-okay-with-mozilla"),
                value=REPLACE(
                    main,
                    "I’m okay with Mozilla handling my info as explained in <a href=\"%s\">this Privacy Notice</a>",
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("url"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletter-form-we-will-only-send"),
                value=REPLACE(
                    main,
                    "We will only send you Mozilla-related information.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletter-form-if-you-havent-previously"),
                value=REPLACE(
                    main,
                    "If you haven’t previously confirmed a subscription to a Mozilla-related newsletter you may have to do so. Please check your inbox or your spam filter for an email from us.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
newsletter-form-available-languages = {COPY(main, "Available Languages",)}
newsletter-form-select-country = {COPY(main, "Select country",)}
newsletter-form-sign-me-up = {COPY(main, "Sign me up",)}
newsletter-form-sign-up-now = {COPY(main, "Sign Up Now",)}
newsletter-form-thanks = {COPY(main, "Thanks!",)}
""", main=main)
        )
