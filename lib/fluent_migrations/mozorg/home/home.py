from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

home = "mozorg/home/home.lang"
index_quantum = "mozorg/home/index-quantum.lang"


def migrate(ctx):
    """Migrate bedrock/mozorg/templates/mozorg/home/home.html, part {index}."""

    ctx.add_transforms(
        "mozorg/home.ftl",
        "mozorg/home.ftl",
        transforms_from(
            """
home-internet-for-people-not-profit = {COPY(index_quantum, "Internet for people, not profit",)}
""",
            index_quantum=index_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("home-did-you-know-mozilla-the-maker"),
                value=REPLACE(
                    index_quantum,
                    "Did you know? Mozilla — the maker of Firefox — fights to keep the Internet a global public resource, open and accessible to all.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
home-fast-for-good = {COPY(index_quantum, "Fast for good.",)}
""",
            index_quantum=index_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("home-with-2x-the-speed-built-in"),
                value=REPLACE(
                    index_quantum,
                    "With 2x the speed, built-in privacy protection and Mozilla behind it, the new Firefox is the better way to browse.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
home-we-make-the-internet-safer = {COPY(index_quantum, "We make the internet safer, healthier and faster for good.",)}
""",
            index_quantum=index_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("home-mozilla-is-the-not-for-profit"),
                value=REPLACE(
                    index_quantum,
                    "Mozilla is the not-for-profit behind Firefox, the original alternative browser. We create products and policy to keep the internet in service of people, not profit.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
home-our-impact = {COPY(index_quantum, "Our impact",)}
""",
            index_quantum=index_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("home-when-you-use-firefox-you-help"),
                value=REPLACE(
                    index_quantum,
                    "When you use Firefox, you help Mozilla fight misinformation online, teach digital skills and make the comments section more human. Check out what helps create a healthier internet.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
home-working-to-keep-the-internet = {COPY(index_quantum, "Working to keep the Internet healthy, open and accessible to all, we teach web literacy, provide tools and advocate on behalf of every individual who values the Internet as a global public resource.",)}
home-working-at-the-grassroots-and = {COPY(index_quantum, "Working at the grassroots and policy levels, we teach web literacy, provide tools and advocate on behalf of every individual who values an internet built on fairness, inclusion and respect.",)}
""",
            index_quantum=index_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("home-mozilla-information-trust-initiative"),
                value=REPLACE(
                    index_quantum,
                    "Mozilla Information Trust Initiative",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
home-empowering-women-online = {COPY(index_quantum, "Empowering Women Online",)}
home-the-coral-project = {COPY(index_quantum, "The Coral Project",)}
home-read-our-internet-health-report = {COPY(index_quantum, "Read our Internet Health Report",)}
home-our-innovations = {COPY(index_quantum, "Our innovations",)}
home-using-the-web-as-the-platform = {COPY(index_quantum, "Using the web as the platform, we build open, innovative technologies that allow developers to work free of closed, corporate ecosystems and create faster, safer web experiences for us all.",)}
home-virtual-reality-platform = {COPY(index_quantum, "Virtual Reality Platform",)}
""",
            index_quantum=index_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("home-common-voice"),
                value=REPLACE(
                    index_quantum,
                    "Common Voice",
                    {
                        "Common Voice": TERM_REFERENCE("brand-name-common-voice"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
home-extensions = {COPY(index_quantum, "Extensions",)}
""",
            index_quantum=index_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("home-personalize-firefox-with-your"),
                value=REPLACE(
                    index_quantum,
                    "Personalize Firefox with your favorite extras like password managers, ad blockers and more.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
home-careers = {COPY(index_quantum, "Careers",)}
""",
            index_quantum=index_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("home-learn-about-the-benefits-of"),
                value=REPLACE(
                    index_quantum,
                    "Learn about the benefits of working at Mozilla and view open positions around the world.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
home-need-help = {COPY(index_quantum, "Need help?",)}
""",
            index_quantum=index_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("home-get-answers-to-your-questions"),
                value=REPLACE(
                    index_quantum,
                    "Get answers to your questions about Firefox and all Mozilla products from our support team.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ],
    )
