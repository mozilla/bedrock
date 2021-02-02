from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

index = "legal/index.lang"

def migrate(ctx):
    """Migrate bedrock/legal/templates/legal/index.html, part {index}."""

    ctx.add_transforms(
        "mozorg/about/legal.ftl",
        "mozorg/about/legal.ftl",
        transforms_from("""
legal-legal = {COPY(index, "Legal",)}
legal-get-involved = {COPY(index, "Get involved",)}
legal-protect-the-fox = {COPY(index, "Protect the Fox",)}
legal-takedown-requests = {COPY(index, "Takedown requests",)}
legal-back-to-legal = {COPY(index, "Back to Legal",)}
""", index=index) + [
            FTL.Message(
                id=FTL.Identifier("legal-special-thanks-to-all-of-you"),
                value=REPLACE(
                    index,
                    "Special thanks to all of you who help report abuses of Mozilla marks, participate in governance forums, give feedback on our localizations & legal terms, and contribute your skills to the success of the Mozilla project.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
legal-terms = {COPY(index, "Terms",)}
legal-our-websites = {COPY(index, "Our Websites",)}
""", index=index) + [
            FTL.Message(
                id=FTL.Identifier("legal-firefox-services"),
                value=REPLACE(
                    index,
                    "Firefox Services",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("legal-webmaker"),
                value=REPLACE(
                    index,
                    "Webmaker",
                    {
                        "Webmaker": TERM_REFERENCE("brand-name-webmaker"),
                    }
                )
            ),
        ] + transforms_from("""
legal-privacy-trademarks = {COPY(index, "Privacy & trademarks",)}
legal-privacy-notices-and-policy = {COPY(index, "Privacy Notices and Policy",)}
legal-downloadable-software-notices = {COPY(index, "Downloadable software notices",)}
""", index=index) + [
            FTL.Message(
                id=FTL.Identifier("legal-firefox"),
                value=REPLACE(
                    index,
                    "Firefox",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("legal-thunderbird"),
                value=REPLACE(
                    index,
                    "Thunderbird",
                    {
                        "Thunderbird": TERM_REFERENCE("brand-name-thunderbird"),
                    }
                )
            ),
        ] + transforms_from("""
legal-websites-and-communications = {COPY(index, "Websites & Communications Terms of Use",)}
legal-acceptable-use-policy = {COPY(index, "Acceptable Use Policy",)}
""", index=index) + [
            FTL.Message(
                id=FTL.Identifier("legal-firefox-cloud-services"),
                value=REPLACE(
                    index,
                    "Firefox Cloud Services: Terms of Service",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
        )
