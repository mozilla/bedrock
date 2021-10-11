from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

faq = "privacy/faq.lang"


def migrate(ctx):
    """Migrate bedrock/privacy/templates/privacy/faq.html, part {index}."""

    ctx.add_transforms(
        "privacy/faq.ftl",
        "privacy/faq.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("privacy-faq-mozillas-data-privacy-faq"),
                value=REPLACE(
                    faq,
                    "Mozilla’s Data Privacy FAQ",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-faq-at-mozilla-we-respect-and-protect-desc"),
                value=REPLACE(
                    faq,
                    "At Mozilla we respect and protect your personal information.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
privacy-faq-we-stand-for-people-over-profit = {COPY(faq, "We Stand for People Over Profit.",)}
""",
            faq=faq,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("privacy-faq-it-can-be-tricky-for-people"),
                value=REPLACE(
                    faq,
                    "It can be tricky for people to know what to expect of any software or services they use today. The technology that powers our lives is complex and people don’t have the time to dig into the details. That is still true for Firefox, where we find that people have many different ideas of what is happening under the hood in their browser.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-faq-at-mozilla-we-respect-and-protect"),
                value=REPLACE(
                    faq,
                    "At Mozilla, we respect and protect your personal information:",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-faq-we-follow-a-set-of-data-privacy"),
                value=REPLACE(
                    faq,
                    'We follow a set of <a href="%(link)s">Data Privacy Principles</a> that shape our approach to privacy in the Firefox desktop and mobile browsers.',
                    {
                        "%%": "%",
                        "%(link)s": VARIABLE_REFERENCE("link"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
privacy-faq-we-only-collect-the-data-we = {COPY(faq, "We only collect the data we need to make the best products.",)}
privacy-faq-we-put-people-in-control-of = {COPY(faq, "We put people in control of their data and online experiences.",)}
""",
            faq=faq,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("privacy-faq-we-adhere-to-no-surprises-principle"),
                value=REPLACE(
                    faq,
                    "We adhere to “no surprises” principle, meaning we work hard to ensure people’s understanding of Firefox matches reality.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-faq-the-following-questions-and"),
                value=REPLACE(
                    faq,
                    "The following questions and answers should help you understand what to expect from Mozilla and Firefox:",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-faq-i-use-firefox-for-almost-everything"),
                value=REPLACE(
                    faq,
                    "I use Firefox for almost everything on the Web. You folks at Mozilla must know a ton of stuff about me, right?",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-faq-firefox-the-web-browser-that"),
                value=REPLACE(
                    faq,
                    "Firefox, the web browser that runs on your device or computer, is your gateway to the internet. Your browser will manage a lot of information about the websites you visit, but that information stays on your device. Mozilla, the company that makes Firefox, doesn’t collect it (unless you ask us to).",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
privacy-faq-really-you-dont-collect-my-browsing = {COPY(faq, "Really, you don’t collect my browsing history?",)}
""",
            faq=faq,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("privacy-faq-mozilla-doesnt-know-as-much"),
                value=REPLACE(
                    faq,
                    'Mozilla doesn’t know as much as you’d expect about how people browse the web. As a browser maker, that’s actually a big challenge for us. That is why we’ve built opt-in tools, such as <a href="%(link)s">Firefox Pioneer</a>, which allows interested users to give us insight into their web browsing. If you sync your browsing history across Firefox installations, we don’t know what that history is - because it’s encrypted by your device.',
                    {
                        "%%": "%",
                        "%(link)s": VARIABLE_REFERENCE("link"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
privacy-faq-it-seems-like-every-company = {COPY(faq, "It seems like every company on the web is buying and selling my data. You’re probably no different.",)}
""",
            faq=faq,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("privacy-faq-mozilla-doesnt-sell-data-about"),
                value=REPLACE(
                    faq,
                    "Mozilla doesn’t sell data about you, and we don’t buy data about you.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
privacy-faq-wait-so-how-do-you-make-money = {COPY(faq, "Wait, so how do you make money?",)}
""",
            faq=faq,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("privacy-faq-mozilla-is-not-your-average"),
                value=REPLACE(
                    faq,
                    'Mozilla is not your average organization. Founded as a community open source project in 1998, Mozilla is a mission-driven organization working towards a more healthy internet. The majority of Mozilla Corporation’s revenue is from royalties earned through Firefox web browser search partnerships and distribution deals around the world. You can learn more about how we make money in our <a href="%(link)s">annual financial report</a>.',
                    {
                        "%%": "%",
                        "%(link)s": VARIABLE_REFERENCE("link"),
                        "Mozilla Corporation": TERM_REFERENCE("brand-name-mozilla-corporation"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
privacy-faq-okay-those-first-few-were-softballs = {COPY(faq, "Okay, those first few were softballs. What data do you collect?",)}
""",
            faq=faq,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("privacy-faq-mozilla-does-collect-a-limited"),
                value=REPLACE(
                    faq,
                    'Mozilla does collect a limited set of data by default from Firefox that helps us to understand how people use the browser. That data is tied to a random identifier, rather than your name or email address. You can read more about that on our <a href="%(privacy)s">privacy notice</a> and you can read the <a href="%(data)s">full documentation for that data collection</a>.',
                    {
                        "%%": "%",
                        "%(privacy)s": VARIABLE_REFERENCE("privacy"),
                        "%(data)s": VARIABLE_REFERENCE("data"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
privacy-faq-we-make-our-documentation-public = {COPY(faq, "We make our documentation public so that anyone can verify what we say is true, tell us if we need to improve, and have confidence that we aren’t hiding anything.",)}
privacy-faq-that-documentation-is-gobbledygook = {COPY(faq, "That documentation is gobbledygook to me! Can you give it to me in plain English?",)}
""",
            faq=faq,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("privacy-faq-there-are-two-categories-of"),
                value=REPLACE(
                    faq,
                    "There are two categories of data that we collect by default in our release version of Firefox.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-faq-the-first-is-what-we-call-technical"),
                value=REPLACE(
                    faq,
                    'The first is what we call "technical data." This is data about the browser itself, such as the operating system it is running on and information about errors or crashes.',
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-faq-the-second-is-what-we-call-interaction"),
                value=REPLACE(
                    faq,
                    'The second is what we call "interaction data." This is data about an individual\'s engagement with Firefox, such as the number of tabs that were open, the status of user preferences, or number of times certain browser features were used, such as screenshots or containers. For example, we collect this data in terms of the back button, that arrow in the upper left corner of your browser that lets you navigate back to a previous webpage in a way that shows us someone used the back button, but doesn’t tell what specific webpages are accessed.',
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-faq-do-you-collect-more-data-in"),
                value=REPLACE(
                    faq,
                    "Do you collect more data in pre-release versions of Firefox?",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-faq-sort-of-in-addition-to-the-data"),
                value=REPLACE(
                    faq,
                    "Sort-of. In addition to the data described above, we receive crash and error reports by default in pre-release version of Firefox.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-faq-we-may-also-collect-additional"),
                value=REPLACE(
                    faq,
                    'We may also collect additional data in pre-release for one of our <a href="%(link)s">studies</a>. For example, some studies require what we call “web activity data” data, which may include URLs and other information about certain websites. This helps us answer specific questions to improve Firefox, for example, how to better integrate popular websites in specific locales.',
                    {
                        "%%": "%",
                        "%(link)s": VARIABLE_REFERENCE("link"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("privacy-faq-mozillas-pre-release-versions"),
                value=REPLACE(
                    faq,
                    "Mozilla’s pre-release versions of Firefox are development platforms, frequently updated with experimental features. We collect more data in pre-release than what we do after release in order to understand how these experimental features are working. You can opt out of having this data collected in preferences.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
privacy-faq-but-why-do-you-collect-any-data = {COPY(faq, "But why do you collect any data at all?",)}
privacy-faq-if-we-dont-know-how-the-browser = {COPY(faq, "If we don’t know how the browser is performing or which features people use, we can’t make it better and deliver the great product you want. We’ve invested in building data collection and analysis tools that allow us to make smart decisions about our product while respecting people's privacy.",)}
privacy-faq-data-collection-still-bugs-me = {COPY(faq, "Data collection still bugs me. Can I turn it off?",)}
""",
            faq=faq,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("privacy-faq-yes-user-control-is-one-of-our"),
                value=REPLACE(
                    faq,
                    'Yes. User control is one of our data privacy principles. We put that into practice in Firefox on our <a href="%(settings)s">privacy settings page</a>, which serves as a one-stop shop for anyone looking to take control of their privacy in Firefox. You can <a href="%(data)s">turn off data collection</a> there.',
                    {
                        "%%": "%",
                        "%(settings)s": VARIABLE_REFERENCE("settings"),
                        "%(data)s": VARIABLE_REFERENCE("data"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
privacy-faq-what-about-my-account-data = {COPY(faq, "What about my account data?",)}
privacy-faq-we-are-big-believers-of-data = {COPY(faq, "We are big believers of data minimization and not asking for things we don't need.",)}
""",
            faq=faq,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("privacy-faq-you-dont-need-an-account-to"),
                value=REPLACE(
                    faq,
                    "You don't need an account to use Firefox. <a href=\"%(accounts)s\">Accounts</a> are required to sync data across devices, but we only ask you for an email address. We don't want to know things like your name, address, birthday and phone number.",
                    {
                        "%%": "%",
                        "%(accounts)s": VARIABLE_REFERENCE("accounts"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
privacy-faq-you-use-digital-advertising = {COPY(faq, "You use digital advertising as part of your marketing mix. Do you buy people's data to better target your online ads?",)}
privacy-faq-no-we-do-not-buy-peoples-data = {COPY(faq, "No, we do not buy people's data to target advertising.",)}
privacy-faq-we-do-ask-our-advertising-partners = {COPY(faq, "We do ask our advertising partners to use only first party data that websites and publishers know about all users, such as the browser you are using and the device you are on.",)}
privacy-faq-well-it-seems-like-you-really = {COPY(faq, "Well, it seems like you really have my back on this privacy stuff.",)}
privacy-faq-yes-we-do = {COPY(faq, "Yes, we do.",)}
""",
            faq=faq,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("privacy-faq-find-out-more-about-how-mozilla"),
                value=REPLACE(
                    faq,
                    "Find out more about how Mozilla protects the internet.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ],
    )
