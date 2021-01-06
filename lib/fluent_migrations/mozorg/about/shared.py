from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

main = "main.lang"

def migrate(ctx):
    """Migrate bedrock/mozorg/templates/mozorg/about/manifesto.html, part {index}."""

    ctx.add_transforms(
        "mozorg/about/shared.ftl",
        "mozorg/about/shared.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("about-shared-about-mozilla"),
                value=REPLACE(
                    main,
                    "About Mozilla",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
about-shared-mission = {COPY(main, "Mission",)}
about-shared-history = {COPY(main, "History",)}
about-shared-leadership = {COPY(main, "Leadership",)}
about-shared-governance = {COPY(main, "Governance",)}
about-shared-forums = {COPY(main, "Forums",)}
about-shared-patents = {COPY(main, "Patents",)}
about-shared-our-products = {COPY(main, "Our Products",)}
about-shared-software-innovations = {COPY(main, "Software and other innovations designed to advance our mission.",)}
about-shared-get-involved = {COPY(main, "Get Involved",)}
about-shared-volunteer = {COPY(main, "Become a volunteer contributor in a number of different areas.",)}
""", main=main)
    )
