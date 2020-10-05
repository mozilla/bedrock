from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

index = "privacy/index.lang"

def migrate(ctx):
    """Migrate bedrock/privacy/templates/privacy/index.html, part {index}."""

    ctx.add_transforms(
        "privacy/index.ftl",
        "privacy/index.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("privacy-index-mozilla-privacy"),
                value=REPLACE(
                    index,
                    "Mozilla Privacy",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-index-contact-mozilla"),
                value=REPLACE(
                    index,
                    "Contact Mozilla",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
privacy-index-if-you-want-to-make-a-correction = {COPY(index, "If you want to make a correction to your information, or you have any questions about our privacy policies, please get in touch with:",)}
""", index=index) + [
            FTL.Message(
                id=FTL.Identifier("privacy-index-see-here-for-data-subject"),
                value=REPLACE(
                    index,
                    "<a href=\"%(dsar)s\">See here for Data Subject Access Requests.</a>",
                    {
                        "%%": "%",
                        "%(dsar)s": VARIABLE_REFERENCE("dsar"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-index-for-product-support-requests"),
                value=REPLACE(
                    index,
                    "For product support requests, please <a href=\"%(sumo)s\">visit our forums</a>.",
                    {
                        "%%": "%",
                        "%(sumo)s": VARIABLE_REFERENCE("sumo"),
                    }
                )
            ),
        ] + transforms_from("""
privacy-index-data-privacy-principles = {COPY(index, "Data Privacy Principles",)}
""", index=index) + [
            FTL.Message(
                id=FTL.Identifier("privacy-index-mozillas-data-privacy-principles"),
                value=REPLACE(
                    index,
                    "Mozilla's <a href=\"%(principles)s\">Data Privacy Principles</a> inspire our practices that respect and protect people who use the Internet. Learn how these principles shape Firefox and all of our products in this <a href=\"%(faq)s\">FAQ</a>.",
                    {
                        "%%": "%",
                        "%(principles)s": VARIABLE_REFERENCE("principles"),
                        "%(faq)s": VARIABLE_REFERENCE("faq"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-index-mozillas-data-privacy-principles"),
                value=REPLACE(
                    index,
                    "Mozilla's Data Privacy Principles inspire our practices that respect and protect people who use the Internet. Learn how these principles shape Firefox and all of our products in this <a href=\"%(faq)s\">FAQ</a>.",
                    {
                        "%%": "%",
                        "%(faq)s": VARIABLE_REFERENCE("faq"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
privacy-index-transparency-report = {COPY(index, "Transparency Report",)}
""", index=index) + [
            FTL.Message(
                id=FTL.Identifier("privacy-index-as-an-open-source-project"),
                value=REPLACE(
                    index,
                    "As an open source project, transparency and openness are an essential part of Mozilla’s founding principles. Our codebases are open and auditable. Our development work is open. Our bi-annual <a href=\"%(report)s\">Transparency Report</a> also demonstrates our commitment to these principles.",
                    {
                        "%%": "%",
                        "%(report)s": VARIABLE_REFERENCE("report"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-index-to-review-and-comment-on-proposed"),
                value=REPLACE(
                    index,
                    "To review and comment on proposed changes to our privacy policies, <a href=\"%(group)s\"> subscribe to Mozilla’s governance group</a>.",
                    {
                        "%%": "%",
                        "%(group)s": VARIABLE_REFERENCE("group"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-index-to-review-and-comment-on-proposed"),
                value=REPLACE(
                    index,
                    "To review and comment on proposed changes to our privacy policies <a href=\"%(group)s\"> subscribe to Mozilla’s Governance Group</a>.",
                    {
                        "%%": "%",
                        "%(group)s": VARIABLE_REFERENCE("group"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-index-read-more-about-our-ongoing"),
                value=REPLACE(
                    index,
                    "Read more about our ongoing privacy and security public policy work on <a href=\"%(blog)s\">Mozilla's Open Policy and Advocacy Blog</a>.",
                    {
                        "%%": "%",
                        "%(blog)s": VARIABLE_REFERENCE("blog"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-index-mozilla-websites-communications"),
                value=REPLACE(
                    index,
                    "Mozilla Websites, Communications &amp; Cookies",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-index-firefox-fire-tv"),
                value=REPLACE(
                    index,
                    "Firefox for Fire TV",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Fire TV": TERM_REFERENCE("brand-name-fire-tv"),
                    }
                )
            ),
        ] + transforms_from("""
privacy-index-outdated-policies = {COPY(index, "Outdated Policies",)}
""", index=index)
        )
