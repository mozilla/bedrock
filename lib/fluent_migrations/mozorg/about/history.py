from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

history = "mozorg/about/history.lang"
history_details = "mozorg/about/history-details.lang"
about = "mozorg/about.lang"


def migrate(ctx):
    """Migrate bedrock/mozorg/templates/mozorg/about/history.html, part {index}."""

    ctx.add_transforms(
        "mozorg/about/history.ftl",
        "mozorg/about/history.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("history-history-of-the-mozilla-project"),
                value=REPLACE(
                    history_details,
                    "History of the Mozilla Project",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-the-mozilla-project-was"),
                value=REPLACE(
                    history_details,
                    'The Mozilla project was <a href="%(coderush)s">created in 1998</a> with the <a href="%(sourcerelease)s">release of the Netscape browser suite source code</a>.',
                    {
                        "%%": "%",
                        "%(coderush)s": VARIABLE_REFERENCE("coderush"),
                        "%(sourcerelease)s": VARIABLE_REFERENCE("sourcerelease"),
                        "Netscape": TERM_REFERENCE("brand-name-netscape"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
history-it-was-intended-to-harness = {COPY(history_details, "It was intended to harness the creative power of thousands of programmers on the Internet and fuel unprecedented levels of innovation in the browser market.",)}
""",
            history_details=history_details,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("history-within-the-first-year-new"),
                value=REPLACE(
                    history_details,
                    'Within the <a href="%(firstyear)s">first year</a>, new community members from around the world had already contributed new functionality, enhanced existing features and became engaged in the management and planning of the project itself.',
                    {
                        "%%": "%",
                        "%(firstyear)s": VARIABLE_REFERENCE("firstyear"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-by-creating-an-open-community"),
                value=REPLACE(
                    history_details,
                    'By creating an open community, the Mozilla project had become <a href="%(stevecase)s">larger than any one company</a>.',
                    {
                        "%%": "%",
                        "%(stevecase)s": VARIABLE_REFERENCE("stevecase"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-community-members-got-involved"),
                value=REPLACE(
                    history_details,
                    'Community members got involved and expanded the scope of the project’s <a href="%(mission)s">original mission</a> — instead of just working on Netscape’s next browser, people started creating <a href="%(browsers)s">a variety of browsers</a>, <a href="%(bugzilla)s">development tools</a> and a range of other <a href="%(projects)s">projects</a>.',
                    {
                        "%%": "%",
                        "%(mission)s": VARIABLE_REFERENCE("mission"),
                        "%(browsers)s": VARIABLE_REFERENCE("browsers"),
                        "%(bugzilla)s": VARIABLE_REFERENCE("bugzilla"),
                        "%(projects)s": VARIABLE_REFERENCE("projects"),
                        "Netscape": TERM_REFERENCE("brand-name-netscape"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-people-contributed-to-mozilla"),
                value=REPLACE(
                    history_details,
                    "People contributed to Mozilla in different ways, but everyone was passionate about creating free software that would enable people to have a choice in how they experienced the Internet.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-after-several-years-of-development"),
                value=REPLACE(
                    history_details,
                    'After several years of development, <a href="%(mozilla1)s">Mozilla 1.0</a>, the first major version, was released in 2002. This version featured many improvements to the browser, email client and other applications included in the suite, but not many people were using it.',
                    {
                        "%%": "%",
                        "%(mozilla1)s": VARIABLE_REFERENCE("mozilla1"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-by-2002-well-over-90"),
                value=REPLACE(
                    history_details,
                    'By 2002, <a href="%(over90)s">well over 90%% of Internet users</a> were browsing with Internet Explorer.',
                    {
                        "%%": FTL.TextElement("%"),
                        "%(over90)s": VARIABLE_REFERENCE("over90"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-not-many-people-noticed"),
                value=REPLACE(
                    history_details,
                    'Not many people noticed at the time, but the first version of Phoenix (later renamed to Firefox) was also released by Mozilla community members that year with the goal of providing the <a href="%(charter)s">best possible browsing experience</a> to the widest possible set of people.',
                    {
                        "%%": "%",
                        "%(charter)s": VARIABLE_REFERENCE("charter"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-in-2003-the-mozilla-project"),
                value=REPLACE(
                    history_details,
                    'In 2003, the Mozilla project created the Mozilla Foundation, an <a href="%(foundation)s">independent non-profit organization</a> supported by individual donors and a variety of companies.',
                    {
                        "%%": "%",
                        "%(foundation)s": VARIABLE_REFERENCE("foundation"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Mozilla Foundation": TERM_REFERENCE("brand-name-mozilla-foundation"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-the-new-mozilla-foundation"),
                value=REPLACE(
                    history_details,
                    'The new Mozilla Foundation continued the role of managing the daily operations of the project and also officially took on the role of promoting <a href="%(manifesto)s">openness, innovation and opportunity</a> on the Internet.',
                    {
                        "%%": "%",
                        "%(manifesto)s": VARIABLE_REFERENCE("manifesto"),
                        "Mozilla Foundation": TERM_REFERENCE("brand-name-mozilla-foundation"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-it-did-this-by-continuing"),
                value=REPLACE(
                    history_details,
                    'It did this by continuing to release software, such as Firefox and Thunderbird, and expanding to new areas, such as providing <a href="%(grants)s">grants</a> to support accessibility improvements on the Web.',
                    {
                        "%%": "%",
                        "%(grants)s": VARIABLE_REFERENCE("grants"),
                        "Thunderbird": TERM_REFERENCE("brand-name-thunderbird"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-firefox-10-was-released"),
                value=REPLACE(
                    history_details,
                    '<a href="%(firefox1)s">Firefox 1.0</a> was released in 2004 and became a big success — in less than a year, it was downloaded <a href="%(millions)s">over 100 million times</a>.',
                    {
                        "%%": "%",
                        "%(firefox1)s": VARIABLE_REFERENCE("firefox1"),
                        "%(millions)s": VARIABLE_REFERENCE("millions"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-new-versions-of-firefox"),
                value=REPLACE(
                    history_details,
                    "New versions of Firefox have come out regularly since then and keep setting new records. The popularity of Firefox has helped bring choice back to users.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-the-renewed-competition"),
                value=REPLACE(
                    history_details,
                    'The renewed competition has <a href="%(innovation)s">accelerated innovation</a> and improved the Internet for everyone.',
                    {
                        "%%": "%",
                        "%(innovation)s": VARIABLE_REFERENCE("innovation"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-in-2013-we-launched-firefox"),
                value=REPLACE(
                    history_details,
                    'In 2013, we launched <a href="%(firefoxos)s">Firefox OS</a> to unleash the full power of the Web on smartphones and once again offer control and choice to a new generation of people coming online.',
                    {
                        "%%": "%",
                        "%(firefoxos)s": VARIABLE_REFERENCE("firefoxos"),
                        "Firefox OS": TERM_REFERENCE("brand-name-firefox-os"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-mozilla-also-celebrated"),
                value=REPLACE(
                    history_details,
                    "Mozilla also celebrated its 15th anniversary in 2013.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
history-the-community-has-shown = {COPY(history_details, "The community has shown that commercial companies can benefit by collaborating in open source projects and that great end user products can be produced as open source software.",)}
""",
            history_details=history_details,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("history-more-people-than-ever-before"),
                value=REPLACE(
                    history_details,
                    'More people than ever before are using the Internet and are experiencing it <a href="%(all)s">in their own language</a>.',
                    {
                        "%%": "%",
                        "%(all)s": VARIABLE_REFERENCE("all"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-a-sustainable-organization"),
                value=REPLACE(
                    history_details,
                    'A sustainable organization has been created that uses market mechanisms to support a public benefit mission and this model has been reused by others to create open, transparent and collaborative organizations in a <a href="%(range)s">broad range</a> <a href="%(areas)s">of areas</a>.',
                    {
                        "%%": "%",
                        "%(range)s": VARIABLE_REFERENCE("range"),
                        "%(areas)s": VARIABLE_REFERENCE("areas"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
history-the-future-is-full-of-challenges = {COPY(history_details, "The future is full of challenges and opportunities equal to those of our past.",)}
history-theres-no-guarantee-that = {COPY(history_details, "There’s no guarantee that the Internet will remain open or enjoyable or safe.",)}
""",
            history_details=history_details,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("history-mozilla-will-continue-to"),
                value=REPLACE(
                    history_details,
                    "Mozilla will continue to provide an opportunity for people to make their voices heard and to shape their own online lives.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
history-of-course-were-not-alone = {COPY(history_details, "Of course, we’re not alone in doing this.",)}
""",
            history_details=history_details,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("history-the-mozilla-community-together"),
                value=REPLACE(
                    history_details,
                    "The Mozilla community, together with other open source projects and other public benefit organizations, exists only because of the people who are engaged in making our common goals a reality.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-if-you-want-to-join-us-in"),
                value=REPLACE(
                    history_details,
                    'If you want to join us in our mission, please <a href="%(contribute)s">get involved</a>.',
                    {
                        "%%": "%",
                        "%(contribute)s": VARIABLE_REFERENCE("contribute"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-for-more-information-about"),
                value=REPLACE(
                    history_details,
                    "For more information about Mozilla’s history, see the following:",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-mozilla-bookmarks"),
                value=REPLACE(
                    history_details,
                    "Mozilla Bookmarks",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-timeline-of-mozilla-project"),
                value=REPLACE(
                    history_details,
                    "Timeline of Mozilla Project",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-mozilla-digital-memory-bank"),
                value=REPLACE(
                    history_details,
                    "Mozilla Digital Memory Bank",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("history-the-history-of-firefox-and"),
                value=REPLACE(
                    history_details,
                    '<a href="%(link)s">The History of Firefox and Mozilla Posters</a> (available in English and Japanese)',
                    {
                        "%%": "%",
                        "%(link)s": VARIABLE_REFERENCE("link"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ],
    )
