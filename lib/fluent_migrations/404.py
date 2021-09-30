from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

not_found = "mozorg/404.lang"


def migrate(ctx):
    """Migrate bedrock/base/templates/404.html, part {index}."""

    ctx.add_transforms(
        "404.ftl",
        "404.ftl",
        transforms_from(
            """
not-found-page-not-found-page-page-not-found = {COPY(not_found, "404: Page Not Found",)}
not-found-page-sorry-we-cant-find-that-page = {COPY(not_found, "Sorry, we can’t find that page",)}
not-found-page-were-all-about-a-healthy-internet = {COPY(not_found, "We’re all about a healthy internet but sometimes broken URLs happen.",)}
not-found-page-go-back = {COPY(not_found, "Go Back",)}
""",
            not_found=not_found,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("not-found-page-learn-about-mozilla-the-non"),
                value=REPLACE(
                    not_found,
                    '<a href="%(about)s">Learn</a> about Mozilla, the non-profit behind Firefox.',
                    {
                        "%%": "%",
                        "%(about)s": VARIABLE_REFERENCE("about"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("not-found-page-explore-the-entire-family-for"),
                value=REPLACE(
                    not_found,
                    "<a href=%(explore)s>Explore</a> the entire family for Firefox products designed to respect your privacy.",
                    {
                        "%%": "%",
                        "%(explore)s": VARIABLE_REFERENCE("explore"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("not-found-page-download-the-firefox-browser"),
                value=REPLACE(
                    not_found,
                    "<a href=%(download)s>Download</a> the Firefox browser for your mobile device or desktop",
                    {
                        "%%": "%",
                        "%(download)s": VARIABLE_REFERENCE("download"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ],
    )
