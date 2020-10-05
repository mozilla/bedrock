from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

principles = "privacy/principles.lang"

def migrate(ctx):
    """Migrate bedrock/privacy/templates/privacy/principles.html, part {index}."""

    ctx.add_transforms(
        "privacy/principles.ftl",
        "privacy/principles.ftl",
        transforms_from("""
privacy-principles-data-privacy-principles = {COPY(principles, "Data Privacy Principles",)}
""", principles=principles) + [
            FTL.Message(
                id=FTL.Identifier("privacy-principles-mozilla-is-an-open-source"),
                value=REPLACE(
                    principles,
                    "Mozilla is an open source project with a mission to improve your Internet experience. This is a driving force behind our privacy practices.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-principles-the-following-five-principles"),
                value=REPLACE(
                    principles,
                    "The following five principles stem from the <a href=\"%(link)s\">Mozilla Manifesto</a> and inform how we:",
                    {
                        "%%": "%",
                        "%(link)s": VARIABLE_REFERENCE("link"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
privacy-principles-develop-our-products = {COPY(principles, "develop our products and services",)}
privacy-principles-manage-user-data-we-collect = {COPY(principles, "manage user data we collect",)}
privacy-principles-select-and-interact-with = {COPY(principles, "select and interact with partners",)}
privacy-principles-shape-our-public-policy = {COPY(principles, "shape our public policy and advocacy work",)}
privacy-principles-no-surprises = {COPY(principles, "No surprises",)}
privacy-principles-use-and-share-information = {COPY(principles, "Use and share information in a way that is transparent and benefits the user.",)}
privacy-principles-user-control = {COPY(principles, "User control",)}
privacy-principles-develop-products-and = {COPY(principles, "Develop products and advocate for best practices that put users in control of their data and online experiences.",)}
privacy-principles-limited-data = {COPY(principles, "Limited data",)}
privacy-principles-collect-what-we-need = {COPY(principles, "Collect what we need, de-identify where we can and delete when no longer necessary.",)}
privacy-principles-sensible-settings = {COPY(principles, "Sensible settings",)}
privacy-principles-design-for-a-thoughtful = {COPY(principles, "Design for a thoughtful balance of safety and user experience.",)}
privacy-principles-defense-in-depth = {COPY(principles, "Defense in depth",)}
privacy-principles-maintain-multi-layered = {COPY(principles, "Maintain multi-layered security controls and practices, many of which are publicly verifiable.",)}
""", principles=principles)
        )
