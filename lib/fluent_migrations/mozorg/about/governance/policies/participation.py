from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

participation = "mozorg/about/governance/policies/participation.lang"


def migrate(ctx):
    """Migrate bedrock/mozorg/templates/mozorg/about/governance/policies/participation.html, part {index}."""

    ctx.add_transforms(
        "mozorg/about/governance/policies/participation.ftl",
        "mozorg/about/governance/policies/participation.ftl",
        transforms_from(
            """
participation-community-participation = {COPY(participation, "Community Participation Guidelines",)}
""",
            participation=participation,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("participation-mozilla-community"),
                value=REPLACE(
                    participation,
                    "Mozilla Community Participation Guidelines",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
participation-version-31-updated = {COPY(participation, "Version 3.1 – Updated January 16, 2020",)}
""",
            participation=participation,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("participation-the-heart-of-mozilla"),
                value=REPLACE(
                    participation,
                    "The heart of Mozilla is people. We put people first and do our best to recognize, appreciate and respect the diversity of our global contributors. The Mozilla Project welcomes contributions from everyone who shares our goals and wants to contribute in a healthy and constructive manner within our community. As such, we have adopted this code of conduct and require all those who participate to agree and adhere to these Community Participation Guidelines in order to help us create a safe and positive community experience for all.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
participation-these-guidelines-aim = {COPY(participation, "These guidelines aim to support a community where all people should feel safe to participate, introduce new ideas and inspire others, regardless of:",)}
participation-background = {COPY(participation, "Background",)}
participation-family-status = {COPY(participation, "Family status",)}
participation-gender = {COPY(participation, "Gender",)}
participation-gender-identity-or = {COPY(participation, "Gender identity or expression",)}
participation-marital-status = {COPY(participation, "Marital status",)}
participation-sex = {COPY(participation, "Sex",)}
participation-sexual-orientation = {COPY(participation, "Sexual orientation",)}
participation-native-language = {COPY(participation, "Native language",)}
participation-age = {COPY(participation, "Age",)}
participation-ability = {COPY(participation, "Ability",)}
participation-race-andor-ethnicity = {COPY(participation, "Race and/or ethnicity",)}
participation-caste = {COPY(participation, "Caste",)}
participation-national-origin = {COPY(participation, "National origin",)}
participation-socioeconomic-status = {COPY(participation, "Socioeconomic status",)}
participation-religion = {COPY(participation, "Religion",)}
participation-geographic-location = {COPY(participation, "Geographic location",)}
participation-any-other-dimension = {COPY(participation, "Any other dimension of diversity",)}
""",
            participation=participation,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("participation-openness-collaboration"),
                value=REPLACE(
                    participation,
                    "Openness, collaboration and participation are core aspects of our work — from development on Firefox to collaboratively designing curriculum. We gain strength from diversity and actively seek participation from those who enhance it. These guidelines exist to enable diverse individuals and groups to interact and collaborate to mutual advantage. This document outlines both expected and prohibited behavior.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
participation-when-and-how-to-use = {COPY(participation, "When and How to Use These Guidelines",)}
""",
            participation=participation,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("participation-these-guidelines-outline"),
                value=REPLACE(
                    participation,
                    "These guidelines outline our behavior expectations as members of the Mozilla community in all Mozilla activities, both offline and online. Your participation is contingent upon following these guidelines in all Mozilla activities, including but not limited to:",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-working-in-mozilla"),
                value=REPLACE(
                    participation,
                    "Working in Mozilla spaces.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-working-with-other"),
                value=REPLACE(
                    participation,
                    "Working with other Mozillians and other Mozilla community participants virtually or co-located.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-representing-mozilla"),
                value=REPLACE(
                    participation,
                    "Representing Mozilla at public events.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-representing-mozilla-social"),
                value=REPLACE(
                    participation,
                    "Representing Mozilla in social media (official accounts, staff accounts, personal accounts, Facebook pages).",
                    {
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-participating-in-mozilla"),
                value=REPLACE(
                    participation,
                    "Participating in Mozilla offsites and trainings.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-participating-in-mozilla-related"),
                value=REPLACE(
                    participation,
                    "Participating in Mozilla-related forums, mailing lists, wikis, websites, chat channels, bugs, group or person-to-person meetings, and Mozilla-related correspondence.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-these-guidelines-work"),
                value=REPLACE(
                    participation,
                    'These guidelines work in conjunction with our Anti-Harassment/Discrimination Policies<a href="%(note1)s">[1]</a>, which sets out protections for, and obligations of, Mozilla employees. The Anti-Harassment/Discrimination Policy is crafted with specific legal definitions and requirements in mind.',
                    {
                        "%%": "%",
                        "%(note1)s": VARIABLE_REFERENCE("note1"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-while-these-guidelines"),
                value=REPLACE(
                    participation,
                    "While these guidelines / code of conduct are specifically aimed at Mozilla’s work and community, we recognize that it is possible for actions taken outside of Mozilla’s online or inperson spaces to have a deep impact on community health. (For example, in the past, we publicly identified an anonymous posting aimed at a Mozilla employee in a non-Mozilla forum as clear grounds for removal from the Mozilla community.) This is an active topic in the diversity and inclusion realm. We anticipate wide-ranging discussions among our communities about appropriate boundaries.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
participation-expected-behavior = {COPY(participation, "Expected Behavior",)}
participation-the-following-behaviors = {COPY(participation, "The following behaviors are expected of all Mozillians:",)}
participation-be-respectful = {COPY(participation, "Be Respectful",)}
participation-value-each-others = {COPY(participation, "Value each other’s ideas, styles and viewpoints. We may not always agree, but disagreement is no excuse for poor manners. Be open to different possibilities and to being wrong. Be respectful in all interactions and communications, especially when debating the merits of different options. Be aware of your impact and how intense interactions may be affecting people. Be direct, constructive and positive. Take responsibility for your impact and your mistakes – if someone says they have been harmed through your words or actions, listen carefully, apologize sincerely, and correct the behavior going forward.",)}
participation-be-direct-but-professional = {COPY(participation, "Be Direct but Professional",)}
participation-we-are-likely-to-have = {COPY(participation, "We are likely to have some discussions about if and when criticism is respectful and when it’s not. We <em>must</em> be able to speak directly when we disagree and when we think we need to improve. We cannot withhold hard truths. Doing so respectfully is hard, doing so when others don’t seem to be listening is harder, and hearing such comments when one is the recipient can be even harder still. We need to be honest and direct, as well as respectful.",)}
participation-be-inclusive = {COPY(participation, "Be Inclusive",)}
participation-seek-diverse-perspectives = {COPY(participation, "Seek diverse perspectives. Diversity of views and of people on teams powers innovation, even if it is not always comfortable. Encourage all voices. Help new perspectives be heard and listen actively. If you find yourself dominating a discussion, it is especially important to step back and encourage other voices to join in. Be aware of how much time is taken up by dominant members of the group. Provide alternative ways to contribute or participate when possible.",)}
participation-be-inclusive-of-everyone = {COPY(participation, "Be inclusive of everyone in an interaction, respecting and facilitating people’s participation whether they are:",)}
participation-remote-on-video-or = {COPY(participation, "Remote (on video or phone)",)}
participation-not-native-language = {COPY(participation, "Not native language speakers",)}
participation-coming-from-a-different = {COPY(participation, "Coming from a different culture",)}
participation-using-pronouns-other = {COPY(participation, "Using pronouns other than “he” or “she”",)}
participation-living-in-a-different = {COPY(participation, "Living in a different time zone",)}
participation-facing-other-challenges = {COPY(participation, "Facing other challenges to participate",)}
participation-think-about-how-you = {COPY(participation, "Think about how you might facilitate alternative ways to contribute or participate. If you find yourself dominating a discussion, step back. Make way for other voices and listen actively to them.",)}
participation-understand-different = {COPY(participation, "Understand Different Perspectives",)}
participation-our-goal-should-not = {COPY(participation, "Our goal should not be to “win” every disagreement or argument. A more productive goal is to be open to ideas that make our own ideas better. Strive to be an example for inclusive thinking. “Winning” is when different perspectives make our work richer and stronger.",)}
participation-appreciate-and-accommodate = {COPY(participation, "Appreciate and Accommodate Our Similarities and Differences",)}
participation-mozillians-come-from = {COPY(participation, "Mozillians come from many cultures and backgrounds. Cultural differences can encompass everything from official religious observances to personal habits to clothing. Be respectful of people with different cultural practices, attitudes and beliefs. Work to eliminate your own biases, prejudices and discriminatory practices. Think of others’ needs from their point of view. Use preferred titles (including pronouns) and the appropriate tone of voice. Respect people’s right to privacy and confidentiality. Be open to learning from and educating others as well as educating yourself; it is unrealistic to expect Mozillians to know the cultural practices of every ethnic and cultural group, but everyone needs to recognize one’s native culture is only part of positive interactions.",)}
participation-lead-by-example = {COPY(participation, "Lead by Example",)}
""",
            participation=participation,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("participation-by-matching-your-actions"),
                value=REPLACE(
                    participation,
                    'By matching your actions with your words, you become a person others want to follow. Your actions influence others to behave and respond in ways that are valuable and appropriate for our organizational outcomes. Design your community and your work for inclusion. Hold yourself and others accountable for inclusive behaviors. Make decisions based on the highest good for <a href="%(mission)s">Mozilla’s mission</a>.',
                    {
                        "%%": "%",
                        "%(mission)s": VARIABLE_REFERENCE("mission"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
participation-behavior-that-will = {COPY(participation, "Behavior That Will Not Be Tolerated",)}
participation-the-following-behaviors-are = {COPY(participation, "The following behaviors are considered to be unacceptable under these guidelines.",)}
participation-violence-and-threats = {COPY(participation, "Violence and Threats of Violence",)}
participation-violence-and-threats-of = {COPY(participation, "Violence and threats of violence are not acceptable - online or offline. This includes incitement of violence toward any individual, including encouraging a person to commit self-harm. This also includes posting or threatening to post other people’s personally identifying information (“doxxing”) online.",)}
participation-personal-attacks = {COPY(participation, "Personal Attacks",)}
participation-conflicts-will-inevitably = {COPY(participation, "Conflicts will inevitably arise, but frustration should never turn into a personal attack. It is not okay to insult, demean or belittle others. Attacking someone for their opinions, beliefs and ideas is not acceptable. It is important to speak directly when we disagree and when we think we need to improve, but such discussions must be conducted respectfully and professionally, remaining focused on the issue at hand.",)}
participation-derogatory-language = {COPY(participation, "Derogatory Language",)}
participation-hurtful-or-harmful = {COPY(participation, "Hurtful or harmful language related to:",)}
participation-other-attributes = {COPY(participation, "Other attributes",)}
participation-is-not-acceptable = {COPY(participation, "is not acceptable. This includes deliberately referring to someone by a gender that they do not identify with, and/or questioning the legitimacy of an individual’s gender identity. If you’re unsure if a word is derogatory, don’t use it. This also includes repeated subtle and/or indirect discrimination; when asked to stop, stop the behavior in question.",)}
participation-unwelcome-sexual-attention = {COPY(participation, "Unwelcome Sexual Attention or Physical Contact",)}
participation-unwelcome-sexual-attention-or = {COPY(participation, "Unwelcome sexual attention or unwelcome physical contact is not acceptable. This includes sexualized comments, jokes or imagery in interactions, communications or presentation materials, as well as inappropriate touching, groping, or sexual advances. This includes touching a person without permission, including sensitive areas such as their hair, pregnant stomach, mobility device (wheelchair, scooter, etc) or tattoos. This also includes physically blocking or intimidating another person. Physical contact or simulated physical contact (such as emojis like “kiss”) without affirmative consent is not acceptable. This includes sharing or distribution of sexualized images or text.",)}
participation-disruptive-behavior = {COPY(participation, "Disruptive Behavior",)}
participation-sustained-disruption = {COPY(participation, "Sustained disruption of events, forums, or meetings, including talks and presentations, will not be tolerated. This includes:",)}
participation-talking-over-or-heckling = {COPY(participation, "‘Talking over’ or ‘heckling’ speakers.",)}
participation-drinking-alcohol-to = {COPY(participation, "Drinking alcohol to excess or using recreational drugs to excess, or pushing others to do so.",)}
participation-making-derogatory = {COPY(participation, "Making derogatory comments about those who abstain from alcohol or other substances, pushing people to drink, talking about their abstinence or preferences to others, or pressuring them to drink - physically or through jeering.",)}
participation-otherwise-influencing = {COPY(participation, "Otherwise influencing crowd actions that cause hostility in the session.",)}
participation-influencing-unacceptable = {COPY(participation, "Influencing Unacceptable Behavior",)}
participation-we-will-treat-influencing = {COPY(participation, "We will treat influencing or leading such activities the same way we treat the activities themselves, and thus the same consequences apply.",)}
participation-consequences-of-unacceptable = {COPY(participation, "Consequences of Unacceptable Behavior",)}
""",
            participation=participation,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("participation-bad-behavior-from"),
                value=REPLACE(
                    participation,
                    "Bad behavior from any Mozillian, including those with decision-making authority, will not be tolerated. Intentional efforts to exclude people (except as part of a consequence of the guidelines or other official action) from Mozilla activities are not acceptable and will be dealt with appropriately.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
participation-reports-of-harassmentdiscrimination = {COPY(participation, "Reports of harassment/discrimination will be promptly and thoroughly investigated by the people responsible for the safety of the space, event or activity. Appropriate measures will be taken to address the situation.",)}
participation-anyone-asked-to-stop = {COPY(participation, "Anyone asked to stop unacceptable behavior is expected to comply immediately. Violation of these guidelines can result in you being ask to leave an event or online space, either temporarily or for the duration of the event, or being banned from participation in spaces, or future events and activities in perpetuity.",)}
""",
            participation=participation,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("participation-mozilla-staff-are"),
                value=REPLACE(
                    participation,
                    'Mozilla Staff are held accountable, in addition to these guidelines, to Mozilla’s staff Anti-Harassment/Discrimination Policies <a href="%(note1)s">[1]</a>. Mozilla staff in violation of these guidelines may be subject to further consequences, such as disciplinary action, up to and including termination of employment. For contractors or vendors, violation of these guidelines may affect continuation or renewal of contract.',
                    {
                        "%%": "%",
                        "%(note1)s": VARIABLE_REFERENCE("note1"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
participation-in-addition-any-participants = {COPY(participation, "In addition, any participants who abuse the reporting process will be considered to be in violation of these guidelines and subject to the same consequences. False reporting, especially to retaliate or exclude, will not be accepted or tolerated.",)}
participation-reporting = {COPY(participation, "Reporting",)}
""",
            participation=participation,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("participation-if-you-believe-youre"),
                value=REPLACE(
                    participation,
                    'If you believe you’re experiencing unacceptable behavior that will not be tolerated as outlined above, <a href="%(hotline)s">please use our hotline to report</a>. Reports go directly to Mozilla’s Employment Counsel and HR People Partners and are triaged by the Community Participation Guidelines Response Lead.',
                    {
                        "%%": "%",
                        "%(hotline)s": VARIABLE_REFERENCE("hotline"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
participation-after-receiving-a = {COPY(participation, "After receiving a concise description of your situation, they will review and determine next steps. In addition to conducting any investigation, they can provide a range of resources, from a private consultation to other community resources. They will involve other colleagues or outside specialists (such as legal counsel), as needed to appropriately address each situation.",)}
""",
            participation=participation,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("participation-additional-resources"),
                value=REPLACE(
                    participation,
                    'Additional Resources: <a href="%s">How to Report</a>',
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("missing-var"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-questions-cpg-questionsmozillacom"),
                value=REPLACE(
                    participation,
                    'Questions: <a href="%s">cpg-questions@mozilla.com</a>',
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("missing-var"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
participation-please-also-report = {COPY(participation, "Please also report to us if you observe a potentially dangerous situation, someone in distress, or violations of these guidelines, even if the situation is not happening to you.",)}
participation-if-you-feel-you-have = {COPY(participation, "If you feel you have been unfairly accused of violating these guidelines, please follow the same reporting process.",)}
""",
            participation=participation,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("participation-mozilla-spaces"),
                value=REPLACE(
                    participation,
                    "Mozilla Spaces",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-each-physical-or-virtual"),
                value=REPLACE(
                    participation,
                    "Each physical or virtual Mozilla space shall have a designated contact.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-mozilla-events"),
                value=REPLACE(
                    participation,
                    "Mozilla Events",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-all-mozilla-events"),
                value=REPLACE(
                    participation,
                    "All Mozilla events will have designated a specific safety guideline with emergency and anti-abuse contacts at the event as well as online. These contacts will be posted prominently throughout the event, and in print and online materials. Event leaders are requested to speak at the event about the guidelines and to ask participants to review and agree to them when they sign up for the event.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-reports-will-receive"),
                value=REPLACE(
                    participation,
                    'Reports will receive an email notice of receipt. Once an incident has been investigated and a decision has been communicated to the relevant parties, all have the opportunity to appeal this decision by sending an email to <a href="%(mailto_questions)s">cpg-questions@mozilla.com</a>.',
                    {
                        "%%": "%",
                        "%(mailto_questions)s": VARIABLE_REFERENCE("mailto_questions"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
participation-ask-questions = {COPY(participation, "Ask questions",)}
""",
            participation=participation,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("participation-everyone-is-encouraged"),
                value=REPLACE(
                    participation,
                    'Everyone is encouraged to ask questions about these guidelines. If you are organizing an event or activity, reach out for tips building inclusion for your event, activity or space. Your input is welcome and you will always get a response within 24 hours (or on the next weekday, if it is the weekend) if you reach out to <a href="%(mailto_questions)s">cpg-questions@mozilla.com</a>. Please <a href="%(changelog)s">review this change log</a> for updates to this document.',
                    {
                        "%%": "%",
                        "%(mailto_questions)s": VARIABLE_REFERENCE("mailto_questions"),
                        "%(changelog)s": VARIABLE_REFERENCE("changelog"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
participation-license-and-attribution = {COPY(participation, "License and attribution",)}
""",
            participation=participation,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("participation-this-set-of-guidelines"),
                value=REPLACE(
                    participation,
                    'This set of guidelines is distributed under a <a href="%(license)s" rel="license">Creative Commons Attribution-ShareAlike license</a>.',
                    {
                        "%%": "%",
                        "%(license)s": VARIABLE_REFERENCE("license"),
                        "Creative Commons": TERM_REFERENCE("brand-name-creative-commons"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-these-guidelines-have"),
                value=REPLACE(
                    participation,
                    'These guidelines have been adapted with modifications from Mozilla’s original Community Participation Guidelines, the <a href="%(ubuntu_coc)s">Ubuntu Code of Conduct</a>, Mozilla’s <a href="%(viewsource_coc)s">View Source Conference Code of Conduct</a>, and the <a href="%(rustlang_coc)s">Rust Language Code of Conduct</a>, which are based on Stumptown Syndicate’s <a href="%(citizen_coc)s">Citizen Code of Conduct</a>. Additional text from the <a href="%(lgbtqtech_coc)s">LGBTQ in Technology Code of Conduct</a> and the <a href="%(wiscon_coc)s">WisCon code of conduct</a>. This document and all associated processes are only possible with the hard work of many, many Mozillians.',
                    {
                        "%%": "%",
                        "%(ubuntu_coc)s": VARIABLE_REFERENCE("ubuntu_coc"),
                        "%(viewsource_coc)s": VARIABLE_REFERENCE("viewsource_coc"),
                        "%(rustlang_coc)s": VARIABLE_REFERENCE("rustlang_coc"),
                        "%(citizen_coc)s": VARIABLE_REFERENCE("citizen_coc"),
                        "%(lgbtqtech_coc)s": VARIABLE_REFERENCE("lgbtqtech_coc"),
                        "%(wiscon_coc)s": VARIABLE_REFERENCE("wiscon_coc"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Rust": TERM_REFERENCE("brand-name-rust"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
participation-modifications-to-these = {COPY(participation, "Modifications to these guidelines",)}
""",
            participation=participation,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("participation-mozilla-may-amend"),
                value=REPLACE(
                    participation,
                    "Mozilla may amend the guidelines from time to time and may also vary the procedures it sets out where appropriate in a particular case. Your agreement to comply with the guidelines will be deemed agreement to any changes to it. This policy does not form part of any Mozilla employee’s contract of employment or otherwise have contractual effect.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("participation-1-the-anti-harassment"),
                value=REPLACE(
                    participation,
                    '[1] The anti-harassment policy is accessible to paid staff <a href="%s">here</a>.',
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("missing-var"),
                    },
                ),
            ),
        ],
    )
