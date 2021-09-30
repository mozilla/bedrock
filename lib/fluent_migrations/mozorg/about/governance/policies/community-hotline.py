from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

community_hotline = "mozorg/about/governance/policies/community-hotline.lang"


def migrate(ctx):
    """Migrate bedrock/mozorg/templates/mozorg/about/governance/policies/community-hotline.html, part {index}."""

    ctx.add_transforms(
        "mozorg/about/governance/policies/community-hotline.ftl",
        "mozorg/about/governance/policies/community-hotline.ftl",
        transforms_from(
            """
community-hotline-community-participation = {COPY(community_hotline, "Community Participation Guidelines - How to Report",)}
community-hotline-community-participation = {COPY(community_hotline, "Community Participation Guidelines Hotline",)}
""",
            community_hotline=community_hotline,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("community-hotline-the-heart-of-mozilla"),
                value=REPLACE(
                    community_hotline,
                    "The heart of Mozilla is people. We put people first and do our best to recognize, appreciate and respect the diversity of our global contributors. The Mozilla Project welcomes contributions from everyone who shares our goals and wants to contribute in a healthy and constructive manner within our community.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("community-hotline-to-report-violations"),
                value=REPLACE(
                    community_hotline,
                    'To report violations of the Community Participation Guidelines <strong>in Mozilla’s communities</strong>, please click the “Report” button below. For more information on how to take and give a report, please read “<a href="%(howto)s">How to Report</a>”.',
                    {
                        "%%": "%",
                        "%(howto)s": VARIABLE_REFERENCE("howto"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
community-hotline-report = {COPY(community_hotline, "Report",)}
""",
            community_hotline=community_hotline,
        ),
    )
