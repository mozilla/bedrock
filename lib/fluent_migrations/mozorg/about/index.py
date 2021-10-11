from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

about = "mozorg/about.lang"
about_2019 = "mozorg/about-2019.lang"


def migrate(ctx):
    """Migrate bedrock/mozorg/templates/mozorg/about.html, part {index}."""

    ctx.add_transforms(
        "mozorg/about.ftl",
        "mozorg/about.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("about-learn-about-mozilla"),
                value=REPLACE(
                    about_2019,
                    "Learn About Mozilla",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("about-mozilla-makes-browsers-apps-desc"),
                value=REPLACE(
                    about_2019,
                    "Mozilla makes browsers, apps, code and tools that put people before profit. Our mission: Keep the internet open and accessible to all.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("about-mozilla-makes-browsers-apps"),
                value=REPLACE(
                    about_2019,
                    "Mozilla makes browsers, apps, code and tools that put people before profit.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
about-our-mission-keep-the-internet = {COPY(about_2019, "Our mission: Keep the internet open and accessible to all.",)}
about-read-our-mission = {COPY(about_2019, "Read Our Mission",)}
about-our-mission-in-action = {COPY(about_2019, "Our Mission in Action",)}
about-pioneers-of-the-open-web = {COPY(about_2019, "Pioneers of The Open Web",)}
about-our-leadership-has-been-at = {COPY(about_2019, "Our leadership has been at the forefront of building a healthier internet since Day 1. What began as an alternative to corporate domination has grown into a global force for good online.",)}
""",
            about_2019=about_2019,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("about-firefox-fast-for-good"),
                value=REPLACE(
                    about_2019,
                    "Firefox: Fast for Good",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("about-when-you-use-the-new-firefox"),
                value=REPLACE(
                    about_2019,
                    "When you use the new Firefox, you get a blazing fast experience while supporting Mozilla’s mission to keep the internet healthy, weird and welcoming to all.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
about-walking-our-privacy-talk = {COPY(about_2019, "Walking Our Privacy Talk",)}
""",
            about_2019=about_2019,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("about-when-the-facebook-breach-was"),
                value=REPLACE(
                    about_2019,
                    "When the Facebook breach was revealed, Mozilla had an immediate response – and a Firefox product to support user privacy.",
                    {
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
about-talking-internet-issues-irl = {COPY(about_2019, "Talking Internet Issues IRL",)}
""",
            about_2019=about_2019,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("about-in-mozillas-irl-podcast-host"),
                value=REPLACE(
                    about_2019,
                    "In Mozilla’s IRL podcast, host Manoush Zomorodi shares real stories of life online and real talk about the future of the Web.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
about-corporation-foundation-not = {COPY(about_2019, "Corporation. Foundation. Not-for-profit.",)}
""",
            about_2019=about_2019,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("about-learn-about-the-mozilla-foundation"),
                value=REPLACE(
                    about_2019,
                    "Learn about the Mozilla Foundation",
                    {
                        "Mozilla Foundation": TERM_REFERENCE("brand-name-mozilla-foundation"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("about-mozilla-puts-people-over-profit"),
                value=REPLACE(
                    about_2019,
                    "Mozilla puts people over profit in everything we say, build and do. In fact, there’s a non-profit Foundation at the heart of our enterprise.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("about-the-mozilla-manifesto"),
                value=REPLACE(
                    about_2019,
                    "The Mozilla Manifesto",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
about-the-principles-we-wrote-in = {COPY(about_2019, "The principles we wrote in 1998 still guide us today. And in 2018, we created an addendum to emphasize inclusion, privacy and safety for everyone online.",)}
about-read-the-manifesto = {COPY(about_2019, "Read The Manifesto",)}
about-a-global-view = {COPY(about_2019, "A Global View",)}
""",
            about_2019=about_2019,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("about-with-offices-all-over-the"),
                value=REPLACE(
                    about_2019,
                    'With <a href="%(url)s">offices all over the world</a>, we consider the internet from multiple cultures and contexts.',
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
about-san-francisco = {COPY(about_2019, "San Francisco",)}
about-2000-non-employee-guests-welcomed = {COPY(about_2019, "<strong>2000</strong> non-employee guests welcomed each year",)}
about-berlin = {COPY(about_2019, "Berlin",)}
about-500-annual-attendees-to-the = {COPY(about_2019, "<strong>500</strong> annual attendees to the Berlin speaker series",)}
about-toronto = {COPY(about_2019, "Toronto",)}
about-800-bottles-of-cold-brew-coffee = {COPY(about_2019, "<strong>800</strong> bottles of cold brew coffee consumed yearly.",)}
""",
            about_2019=about_2019,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("about-work-at-mozilla"),
                value=REPLACE(
                    about_2019,
                    "Work at Mozilla",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
about-join-a-mission-driven-organization = {COPY(about_2019, "Join a mission-driven organization that builds purpose-driven products.",)}
""",
            about_2019=about_2019,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("about-mozilla-careers"),
                value=REPLACE(
                    about_2019,
                    "Mozilla Careers",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
about-how-you-can-help = {COPY(about_2019, "How You Can Help",)}
about-your-voice-your-code-your = {COPY(about_2019, "Your voice. Your code. Your support. There are so many ways to join the fight for a healthy internet.",)}
about-get-involved = {COPY(about_2019, "Get Involved",)}
""",
            about_2019=about_2019,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("about-get-the-mozilla-newsletter"),
                value=REPLACE(
                    about_2019,
                    "Get The Mozilla Newsletter",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
about-stay-informed-about-the-issues = {COPY(about_2019, "Stay informed about the issues affecting the internet, and learn how you can get involved in protecting the world’s newest public resource.",)}
about-subscribe = {COPY(about_2019, "Subscribe",)}
""",
            about_2019=about_2019,
        ),
    )
