from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

edge = "firefox/compare/edge.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/browsers/compare/edge.html, part {index}."""

    ctx.add_transforms(
        "firefox/browsers/compare/edge.ftl",
        "firefox/browsers/compare/edge.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("compare-edge-firefox-vs-microsoft-edge-which"),
                value=REPLACE(
                    edge,
                    "Firefox vs. Microsoft Edge: Which is the better browser for you?",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-compare-microsoft-edge-to-the"),
                value=REPLACE(
                    edge,
                    "Compare Microsoft Edge to the Firefox Browser to find out which is the better browser for you.",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-comparing-firefox-browser-with"),
                value=REPLACE(
                    edge,
                    "Comparing Firefox Browser with Microsoft Edge",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-with-windows-10-microsoft-introduced"),
                value=REPLACE(
                    edge,
                    "With Windows 10, Microsoft introduced its Edge browser to compete with Firefox and Chrome making it the default browser pre-installed on millions of PCs sold. Even so, users were slow to adopt it and Microsoft eventually announced plans to relaunch Edge as a Chromium-based browser (Chromium of course being Google’s Open Source browser project).",
                    {
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Chromium": TERM_REFERENCE("brand-name-chromium"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-here-well-compare-our-firefox"),
                value=REPLACE(
                    edge,
                    "Here we’ll compare our Firefox Browser to the Chromium-based Microsoft Edge in terms of privacy, utility, and portability, to help you have a better understanding of which browser better suits your needs and preferences.",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Chromium": TERM_REFERENCE("brand-name-chromium"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-edge-is-integrated-into-the"),
                value=REPLACE(
                    edge,
                    "Edge is integrated into the Windows 10 platform and runs in a sandbox environment, meaning it isolates programs and prevents malicious programs from spying on your computer. It has a built-in SmartScreen that scans the reputation of sites you visit and blocks suspicious sites. To enhance privacy, Edge allows you to use biometrics or a PIN with Windows Hello instead of passwords for online authentication.",
                    {
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-at-firefox-our-privacy-fallback"),
                value=REPLACE(
                    edge,
                    "At Firefox, our <a %(attrs)s>privacy policy</a> is transparent and in plain language. We actually put a lot of work into making sure it was straightforward and easy to read. We pride ourselves in protecting our users security and privacy. With Enhanced Tracking Protection now on by default, we block 2000+ trackers automatically. Trackers are those little pieces of code that try to piece together what you're doing across multiple internet sites to build a composite and detailed picture of who you are, compromising your privacy all just to target better ads.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-your-privacy-protections-shows"),
                value=REPLACE(
                    edge,
                    "Your <a %(attrs)s>Privacy Protections</a> shows you the trackers and cookies that pages have attempted to leave, and how many Firefox has blocked for you.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-in-firefox-private-browsing"),
                value=REPLACE(
                    edge,
                    "In Firefox, Private Browsing mode automatically erases your browsing information like passwords, cookies, and history, leaving no trace after you close out the session. Edge on the other hand, actually records browsing history in their private mode (called “InPrivate”) and it’s a relatively easy task for someone to reconstruct your full browsing history, regardless of whether your browsing was done in regular or InPrivate mode.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-both-browsers-are-relatively"),
                value=REPLACE(
                    edge,
                    "Both browsers are relatively equal in terms of data encryption. However, if online privacy and transparency are important to you, then Firefox is clearly a better choice here.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-firefox-is-a-fast-and-open-fallback"),
                value=REPLACE(
                    edge,
                    "Firefox is a fast and open source browser, which means users can customize their browsing experience in every way possible. Firefox also allows the casual user several different ways to customize the UI with applying different themes and toolbar configurations. Since our browser has always been open source we have a large following of devoted developers who have created an extensive library of add-ons and browser extensions.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-since-edge-has-moved-to-the"),
                value=REPLACE(
                    edge,
                    "Since Edge has moved to the processor intensive Chromium platform, you can expect it to run a little slower, especially if you have multiple programs running at once. However, with Chromium platform comes a massive library of extensions as well as a decent level of UI customization that Edge did not have before it’s move to Chromium.",
                    {
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Chromium": TERM_REFERENCE("brand-name-chromium"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-edge-has-some-nice-ui-features"),
                value=REPLACE(
                    edge,
                    "Edge has some nice UI features, like their tab previews which can make it easy to find the right open tabs if you’ve got a lot of them open. Another helpful tab-related feature lets you set aside any active tabs that you aren’t using but don’t want to close down.",
                    {
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-firefox-features-a-scrolling"),
                value=REPLACE(
                    edge,
                    "Firefox features a scrolling tab interface, which keeps tab information viewable and scrolls them horizontally instead of shrinking them down to just favicon size. Also whenever you open a new tab, our <a %(attrs)s>Pocket feature</a> suggests relevant articles and content for you. Plus with Pocket, you can also save articles, videos, and other content with one click, for reading at a later time.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-firefox-and-edge-both-offer-fallback"),
                value=REPLACE(
                    edge,
                    "Firefox and Edge both offer excellent reading modes. With Firefox you just tap on the small icon in the search bar and the browser strips down all unnecessary elements and presents you a clean looking article. In Edge you just tap on the small book icon and browser to get a clean easy-to-read UI.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-firefox-also-includes-lots"),
                value=REPLACE(
                    edge,
                    "Firefox also includes lots of handy built-in features by default like <a %(attrs)s>Enhanced Tracking Protection</a>, a built-in screenshot tool, large file sending and more.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-out-of-the-gate-firefox-has"),
                value=REPLACE(
                    edge,
                    "Out of the gate, Firefox has more features and integrations built into the browser and readily available on download. And while both browsers have a tremendous number of add-ons and extensions available, Edge’s compatibility with Google’s Chromium platform gives it the advantage in terms of sheer numbers.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                        "Chromium": TERM_REFERENCE("brand-name-chromium"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-with-internet-explorer-fallback"),
                value=REPLACE(
                    edge,
                    "With Internet Explorer, Microsoft learned from its lack of availability across platforms and made Edge available for macOS and Android. The software is now readily available on iOS, Android, Windows and Mac.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "macOS": TERM_REFERENCE("brand-name-mac"),
                        "Mac": TERM_REFERENCE("brand-name-mac"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-firefox-has-been-available"),
                value=REPLACE(
                    edge,
                    "Firefox has been available on iOS, Android, Windows, macOS and Linux for years. And as you would expect with any modern browser, Firefox lets you log in with a <a %(attrs)s>free account</a> and sync data such as passwords, browsing history, bookmarks, and open tabs between your computer, tablet and phone. It also allows you to sync across platforms as well.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "macOS": TERM_REFERENCE("brand-name-mac"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-edge-also-allows-you-to-fallback"),
                value=REPLACE(
                    edge,
                    "Edge also allows you to connect your associated Microsoft account and sign in to sync your favorites, history, passwords, and more between your computer and iOS or Android devices, although some Android tablets are not currently supported.",
                    {
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-aside-from-sucking-up-a-lot"),
                value=REPLACE(
                    edge,
                    "Aside from sucking up a lot of computing power, Edge running on Chromium has answered a lot of users’ needs for functionality and features. But there’s still a lot to account for in terms of the browser’s privacy protections. It’s our assessment that Firefox is still a better choice for most people to use in their daily lives, based not only on functionality but more importantly on our transparency in how we collect user data, what exactly we collect, and what we do with it. Because our parent company is <a %(attrs)s>Mozilla</a>, a non-profit organization dedicated to internet privacy and freedom, we simply have a different set of priorities when it comes to users’ data.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Chromium": TERM_REFERENCE("brand-name-chromium"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-edge-the-bottom-line-is-that-while"),
                value=REPLACE(
                    edge,
                    "The bottom line is that while we suggest using Firefox, the best browser for you ultimately will be the one that fits your individual needs with extension support, browsing tools customization, speed, privacy and security.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
    )
