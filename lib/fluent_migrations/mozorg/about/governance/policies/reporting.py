from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

reporting = "mozorg/about/governance/policies/reporting.lang"


def migrate(ctx):
    """Migrate bedrock/mozorg/templates/mozorg/about/governance/policies/reporting.html, part {index}."""

    ctx.add_transforms(
        "mozorg/about/governance/policies/reporting.ftl",
        "mozorg/about/governance/policies/reporting.ftl",
        transforms_from("""
reporting-community-participation = {COPY(reporting, "Community Participation Guidelines - How to Report",)}
reporting-how-to-report-violations = {COPY(reporting, "How to Report Violations of the Community Participation Guidelines",)}
""", reporting=reporting) + [
            FTL.Message(
                id=FTL.Identifier("reporting-this-document-provides"),
                value=REPLACE(
                    reporting,
                    "This document provides high-level information, for understanding and reporting violations of Mozilla's Community Participation Guidelines.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("reporting-from-the-community-participation"),
                value=REPLACE(
                    reporting,
                    "From the <a href=\"%(cpg)s\">Community Participation Guidelines</a>:",
                    {
                        "%%": "%",
                        "%(cpg)s": VARIABLE_REFERENCE("cpg"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("reporting-the-heart-of-mozilla-is"),
                value=REPLACE(
                    reporting,
                    "The heart of Mozilla is people. We put people first and do our best to recognize, appreciate and respect the diversity of our global contributors. The Mozilla Project welcomes contributions from everyone who shares our goals and wants to contribute in a healthy and constructive manner within our community. As such, we have adopted this code of conduct and require all those who participate to agree and adhere to these Community Participation Guidelines in order to help us create a safe and positive community experience for all.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("reporting-this-document-is-intended"),
                value=REPLACE(
                    reporting,
                    "This document is intended as an interface to existing documents, processes and people responsible for ensuring Mozilla’s communities are healthy, and inclusive for all.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
reporting-when-to-report = {COPY(reporting, "When To Report",)}
""", reporting=reporting) + [
            FTL.Message(
                id=FTL.Identifier("reporting-please-report-all-incidents"),
                value=REPLACE(
                    reporting,
                    "Please report all incidents where someone has engaged in behavior that is potentially illegal or makes you or someone else feel unsafe, unwelcome or uncomfortable <a href=\"%(cpg)s\">as further explained in the CPG</a>.",
                    {
                        "%%": "%",
                        "%(cpg)s": VARIABLE_REFERENCE("cpg"),
                    }
                )
            ),
        ] + transforms_from("""
reporting-how-to-give-a-report = {COPY(reporting, "How to Give a Report",)}
reporting-if-you-believe-someone = {COPY(reporting, "If you believe someone is in physical danger call your local emergency number.",)}
""", reporting=reporting) + [
            FTL.Message(
                id=FTL.Identifier("reporting-if-you-have-a-report-by"),
                value=REPLACE(
                    reporting,
                    "If you have a report <strong>by <em>and</em> about</strong> a contributor (for example, the report is made <strong>by</strong> one contributor <strong>about</strong> another contributor), then you should make your report at the <a href=\"%(community_hotline)s\">Community Participation Guidelines hotline</a>.",
                    {
                        "%%": "%",
                        "%(community_hotline)s": VARIABLE_REFERENCE("community_hotline"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("reporting-if-you-have-a-report-involving"),
                value=REPLACE(
                    reporting,
                    "If you have a report <strong>involving an employee, contractor, or vendor</strong> (for example, the report is made <strong>by</strong> an employee or is <strong>about</strong> an employee) then you should report at the <a href=\"%(employee_hotline)s\">Mozilla Employee hotline</a>.",
                    {
                        "%%": "%",
                        "%(employee_hotline)s": VARIABLE_REFERENCE("employee_hotline"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
reporting-put-another-way = {COPY(reporting, "Put another way…",)}
reporting-by = {COPY(reporting, "By",)}
reporting-employee = {COPY(reporting, "Employee",)}
reporting-contributor = {COPY(reporting, "Contributor",)}
reporting-about = {COPY(reporting, "About",)}
reporting-employee-hotline = {COPY(reporting, "Employee Hotline",)}
reporting-community-hotline = {COPY(reporting, "Community Hotline",)}
reporting-contractor = {COPY(reporting, "Contractor",)}
reporting-vendor = {COPY(reporting, "Vendor",)}
reporting-if-someone-reports-to = {COPY(reporting, "If someone reports to you…",)}
reporting-do-not-question-or-judge = {COPY(reporting, "Do not question, or judge their experience.",)}
reporting-do-not-invite-them-to = {COPY(reporting, "Do not invite them to withdraw the incident report.",)}
reporting-do-not-promise-any-particular = {COPY(reporting, "Do not promise any particular response.",)}
""", reporting=reporting) + [
            FTL.Message(
                id=FTL.Identifier("reporting-do-let-them-know-that"),
                value=REPLACE(
                    reporting,
                    "<strong>Do</strong> let them know that for Mozilla’s policy to be impactful, reports should go through the hotline. If they do not feel comfortable filing the report themselves, you may do so.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
reporting-no-matter-who-files-the = {COPY(reporting, "No matter who files the report, the information below is important to capture.",)}
reporting-names-of-the-people-involved = {COPY(reporting, "Names of the people involved (or if names are unknown, use descriptions and any identifiable info such as appearance, role, handle, project/community affiliation).",)}
reporting-description-of-incident = {COPY(reporting, "Description of incident, including memorable dates (or event) and locations.",)}
""", reporting=reporting) + [
            FTL.Message(
                id=FTL.Identifier("reporting-if-the-reporter-wants"),
                value=REPLACE(
                    reporting,
                    "If the reporter wants to make an anonymous report, please inform them that this contact information we may not be able to update the initial reporter if appropriate. Some laws prohibit anonymous reporting and that you may be required to provide their name if you are a Mozilla Manager or Community Leader.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
reporting-relationship-of-reportervictim = {COPY(reporting, "Relationship of reporter/victim.",)}
""", reporting=reporting) + [
            FTL.Message(
                id=FTL.Identifier("reporting-mozilla-managers-and-community"),
                value=REPLACE(
                    reporting,
                    "Mozilla Managers and Community leaders",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("reporting-if-a-mozilla-manager-or"),
                value=REPLACE(
                    reporting,
                    "If a Mozilla Manager or Community leaders is informed about potential <a href=\"%(cpg)s\">CPG</a> violations they are expected to immediately report the incident through the applicable hotline, even if the initial reporter will also file a report. Mozilla Managers and Community leaders are not permitted to investigate complaints on their own.",
                    {
                        "%%": "%",
                        "%(cpg)s": VARIABLE_REFERENCE("cpg"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("reporting-do-not-impose-your-own"),
                value=REPLACE(
                    reporting,
                    "Do not impose your own judgement on how the reporter should react. Focus on listening.",
                    {
                        "Focus": TERM_REFERENCE("brand-name-focus"),
                    }
                )
            ),
        ] + transforms_from("""
reporting-what-happens-after-the = {COPY(reporting, "What happens after the Report is filed",)}
reporting-investigation = {COPY(reporting, "Investigation",)}
reporting-reports-are-handled-discretely = {COPY(reporting, "Reports are handled discretely and privately, and will only be shared with the people who can investigate, respond, and advise. As part of this investigation, it may be necessary for some information to be disclosed to others, for example to key stakeholders administering communities or events, witnesses, and the wrongdoer.",)}
reporting-correspondence = {COPY(reporting, "Correspondence",)}
reporting-all-reports-are-reviewed = {COPY(reporting, "All reports are reviewed and responded to based on the nature of the report and we try to provide reasonably timed updates as part of open investigations.",)}
reporting-redress = {COPY(reporting, "Redress",)}
""", reporting=reporting) + [
            FTL.Message(
                id=FTL.Identifier("reporting-when-an-investigation"),
                value=REPLACE(
                    reporting,
                    "When an investigation is complete, to the extent the wrongdoer is subject to Mozilla’s control, appropriate measures will be taken to address the situation.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
reporting-no-retaliation = {COPY(reporting, "No Retaliation",)}
""", reporting=reporting) + [
            FTL.Message(
                id=FTL.Identifier("reporting-mozilla-does-not-tolerate"),
                value=REPLACE(
                    reporting,
                    "Mozilla does not tolerate retaliation against Mozillians who report concerns under the CPG in good faith. Acts of retaliation should be reported in the same process as described above.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
reporting-license = {COPY(reporting, "License",)}
""", reporting=reporting) + [
            FTL.Message(
                id=FTL.Identifier("reporting-this-document-includes"),
                value=REPLACE(
                    reporting,
                    "This document includes content forked from the <a href=\"%(pycon)s\">PyCon Code of Conduct Revision 2f4d980</a> which is licensed under a Creative Commons Attribution 3.0 Unported License.",
                    {
                        "%%": "%",
                        "%(pycon)s": VARIABLE_REFERENCE("pycon"),
                        "Creative Commons": TERM_REFERENCE("brand-name-creative-commons"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("reporting-this-document-is-licensed"),
                value=REPLACE(
                    reporting,
                    "This document is licensed under a <a href=\"%(license)s\">Creative Commons Attribution 3.0 Unported License</a>.",
                    {
                        "%%": "%",
                        "%(license)s": VARIABLE_REFERENCE("license"),
                        "Creative Commons": TERM_REFERENCE("brand-name-creative-commons"),
                    }
                )
            ),
        ]
    )
