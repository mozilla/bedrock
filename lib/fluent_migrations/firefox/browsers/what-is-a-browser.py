from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

what_is_a_browser = "firefox/browsers/what-is-a-browser.lang"
what_is_a_browser = "mozorg/what-is-a-browser.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/browsers/what-is-a-browser.html, part {index}."""

    ctx.add_transforms(
        "firefox/browsers/history/what-is-a-browser.ftl",
        "firefox/browsers/history/what-is-a-browser.ftl",
        transforms_from(
            """
what-is-a-browser-what-is-a-web = {COPY(what_is_a_browser, "What is a web browser?",)}
what-is-a-browser-a-web-browser = {COPY(what_is_a_browser, "A web browser takes you anywhere on the internet, letting you see text, images and video from anywhere in the world.",)}
what-is-a-browser-the-web-is-a-vast = {COPY(what_is_a_browser, "The web is a vast and powerful tool. Over the course of a few decades the internet has changed the way we work, the way we play and the way we interact with one another. Depending on how it’s used, it bridges nations, drives commerce, nurtures relationships, drives the innovation engine of the future and is responsible for more memes than we know what to do with.",)}
""",
            what_is_a_browser=what_is_a_browser,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("what-is-a-browser-its-important"),
                value=REPLACE(
                    what_is_a_browser,
                    'It’s important that everyone has access to the web, but it’s also vital that we all <a href="%(tools)s">understand the tools</a> we use to access it. We use web browsers like Mozilla Firefox, Google Chrome, Microsoft Edge and Apple Safari every day, but do we understand what they are and how they work?',
                    {
                        "%%": "%",
                        "%(tools)s": VARIABLE_REFERENCE("tools"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Apple": TERM_REFERENCE("brand-name-apple"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
what-is-a-browser-in-a-short-period-long = {COPY(what_is_a_browser, "In a short period of time we’ve gone from being amazed by the ability to send an email to someone around the world, to a change in how we think of information. It’s not a question of how much you know anymore, but simply a question of what browser or app can get you to that information fastest.",)}
what-is-a-browser-in-a-short-period = {COPY(what_is_a_browser, "In a short period of time we’ve gone from being amazed by the ability to send an email to someone around the world, to a change in how we think about information.",)}
what-is-a-browser-how-does-a-web = {COPY(what_is_a_browser, "How does a web browser work?",)}
what-is-a-browser-a-web-browser-long = {COPY(what_is_a_browser, "A web browser takes you anywhere on the internet. It retrieves information from other parts of the web and displays it on your desktop or mobile device. The information is transferred using the Hypertext Transfer Protocol, which defines how text, images and video are transmitted on the web. This information needs to be shared and displayed in a consistent format so that people using any browser, anywhere in the world can see the information.",)}
""",
            what_is_a_browser=what_is_a_browser,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("what-is-a-browser-sadly-not-all"),
                value=REPLACE(
                    what_is_a_browser,
                    'Sadly, not all browser makers choose to interpret the format in the same way. For users, this means that a website can look and function differently. Creating consistency between browsers, so that any user can enjoy the internet, regardless of the browser they choose, is called <a href="%(standards)s">web standards</a>.',
                    {
                        "%%": "%",
                        "%(standards)s": VARIABLE_REFERENCE("standards"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("what-is-a-browser-when-the-web-browser"),
                value=REPLACE(
                    what_is_a_browser,
                    'When the web browser fetches data from an internet connected server and it then uses a piece of software called a rendering engine to translate that data into text and images. This data is written in <a href="%(html)s">Hypertext Markup Language</a> (HTML) and web browsers read this code to create what we see, hear and experience on the internet.',
                    {
                        "%%": "%",
                        "%(html)s": VARIABLE_REFERENCE("html"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("what-is-a-browser-hyperlinks-allow"),
                value=REPLACE(
                    what_is_a_browser,
                    '<a href="%(hyperlink)s">Hyperlinks</a> allow users to follow a path to other pages or sites on the web. Every webpage, image and video has its own unique <a href="%(url)s">Uniform Resource Locator</a> (URL), which is also known as a web address. When a browser visits a server for data, the web address tells the browser where to look for each item that is described in the html, which then tells the browser where it goes on the web page.',
                    {
                        "%%": "%",
                        "%(hyperlink)s": VARIABLE_REFERENCE("hyperlink"),
                        "%(url)s": VARIABLE_REFERENCE("url"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
what-is-a-browser-cookies-not-the = {COPY(what_is_a_browser, "Cookies (not the yummy kind)",)}
""",
            what_is_a_browser=what_is_a_browser,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("what-is-a-browser-websites-save"),
                value=REPLACE(
                    what_is_a_browser,
                    'Websites save information about you in files called <a href="%(cookies)s">cookies</a>. They are saved on your computer for the next time you visit that site. Upon your return, the website code will read that file to see that it’s you. For example, when you go to a website and the page remembers your username and password – that’s made possible by a cookie.',
                    {
                        "%%": "%",
                        "%(cookies)s": VARIABLE_REFERENCE("cookies"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
what-is-a-browser-there-are-also = {COPY(what_is_a_browser, "There are also cookies that remember more detailed information about you. Perhaps your interests, your web browsing patterns, etc. This means that a site can provide you more targeted content – often in the form of ads. There are types of cookies, called <em>third-party</em> cookies, that come from sites you’re not even visiting at the time and can track you from site to site to gather information about you, which is sometimes sold to other companies. Sometimes you can block these kinds of cookies, though not all browsers allow you to.",)}
what-is-a-browser-when-you-go-to = {COPY(what_is_a_browser, "When you go to a website and the page remembers your username and password – that’s made possible by a cookie.",)}
what-is-a-browser-understanding = {COPY(what_is_a_browser, "Understanding privacy",)}
""",
            what_is_a_browser=what_is_a_browser,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("what-is-a-browser-nearly-all-major"),
                value=REPLACE(
                    what_is_a_browser,
                    "Nearly all major browsers have a private browsing setting. These exist to hide the browsing history from other users on the same computer. Many people think that private browsing or incognito mode will hide both their identity and browsing history from internet service providers, governments and advertisers. They don’t. These settings just clear the history on your system, which is helpful if you’re dealing with sensitive personal information on a shared or public computer. Firefox goes beyond that.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("what-is-a-browser-firefox-helps"),
                value=REPLACE(
                    what_is_a_browser,
                    "Firefox helps you be more private online by letting you block trackers from following you around the web.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
what-is-a-browser-making-your-web = {COPY(what_is_a_browser, "Making your web browser work for you",)}
what-is-a-browser-most-major-web = {COPY(what_is_a_browser, "Most major web browsers let users modify their experience through extensions or add-ons. Extensions are bits of software that you can add to your browser to customize it or add functionality. Extensions can do all kinds of fun and practical things like enabling new features, foreign language dictionaries, or visual appearances and themes.",)}
""",
            what_is_a_browser=what_is_a_browser,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("what-is-a-browser-all-browser-makers"),
                value=REPLACE(
                    what_is_a_browser,
                    "All browser makers develop their products to display images and video as quickly and smoothly as possible making it easy for you to make the most of the web. They all work hard to make sure users have a browser that is fast, powerful and easy to use. Where they differ is why. It’s important to choose the right browser for you. Mozilla builds Firefox to ensure that users have control over their online lives and to ensure that the internet is a global, public resource, accessible to all.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ],
    )
