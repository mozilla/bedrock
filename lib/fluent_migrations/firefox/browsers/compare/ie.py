from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

ie = "firefox/compare/ie.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/browsers/compare/ie.html, part {index}."""

    ctx.add_transforms(
        "firefox/browsers/compare/ie.ftl",
        "firefox/browsers/compare/ie.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("compare-ie-firefox-vs-internet-explorer"),
                value=REPLACE(
                    ie,
                    "Firefox vs. Internet Explorer: Which is the better browser for you?",
                    {
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-compare-internet-explorer-to"),
                value=REPLACE(
                    ie,
                    "Compare Internet Explorer to the Firefox Browser to find out which is the better browser for you.",
                    {
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-comparing-firefox-browser-with"),
                value=REPLACE(
                    ie,
                    "Comparing Firefox Browser with Microsoft Internet Explorer",
                    {
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-while-microsofts-internet-explorer"),
                value=REPLACE(
                    ie,
                    "While Microsoft’s Internet Explorer still comes pre-installed on most Windows-based PCs, clearly Microsoft would prefer you to use their Edge browser, which is set as the default when you purchase.",
                    {
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-microsoft-discontinued-its-internet"),
                value=REPLACE(
                    ie,
                    "Microsoft discontinued its Internet Explorer brand several years ago, in favor of its updated Edge browser for Windows 10. However, slow adoption for Edge created room for Internet Explorer to live on, mainly for business compatibility reasons.",
                    {
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-here-well-compare-our-firefox"),
                value=REPLACE(
                    ie,
                    "Here we’ll compare our Firefox Browser with Internet Explorer in terms of security, utility, and portability. We’ll help you understand the differences between how a modern browser like Firefox that adheres to web standards compares with the browser you may be using for business purposes or out of old habits that die hard.",
                    {
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-if-you-havent-moved-on-from-using"),
                value=REPLACE(
                    ie,
                    "If you haven’t moved on from using Internet Explorer, the security risk factor alone should be enough to convince you. <a %(attrs)s>Microsoft’s own security chief has warned</a> millions of people who continue to use Internet Explorer as their main web browser that they are placing themselves in “peril.”",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-microsoft-is-no-longer-supporting"),
                value=REPLACE(
                    ie,
                    "Microsoft is no longer supporting new development for Internet Explorer, which means security concerns are rampant. Microsoft openly acknowledges the fact that vulnerabilities exist within basically every version of Internet Explorer.",
                    {
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-so-whats-the-solution-if-your-fallback"),
                value=REPLACE(
                    ie,
                    "So what’s the solution if your company is running outdated apps that only work on Internet Explorer? Our best advice for you personally is, don’t mix business with pleasure. The simple thing to do is download and use a more secure browser like Firefox. Then, if you need to do things like check your personal email or shop online, you can just switch over to the more secure browser. The bottom line is, if Microsoft is warning people not to use Internet Explorer, don’t use it. Your online privacy and security are not worth risking because you (or your company) have a hard time breaking an old habit. We make Firefox with security and privacy features like <a %(lockwise)s>Lockwise</a>, our password manager, private browsing and lots of other add-ons that help us make the web safer for you. Also, our <a %(privacy)s>Privacy Policy</a> is straightforward: we tell you what we know about you, and why we collect that information. All of these things obviously go beyond what Internet Explorer offers, and even what other modern browsers like Google Chrome and Microsoft Edge offer.",
                    {
                        "%%": "%",
                        "%(lockwise)s": VARIABLE_REFERENCE("lockwise"),
                        "%(privacy)s": VARIABLE_REFERENCE("privacy"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Lockwise": TERM_REFERENCE("brand-name-lockwise"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-alarmingly-4-to-5-of-all-desktop-fallback"),
                value=REPLACE(
                    ie,
                    "Alarmingly, 4 to 5% of all desktop web traffic comes through Internet Explorer. That might not seem like a lot, but in reality it means millions of people are being served a poor internet experience with slow loading and rendering times, pages that won’t display properly — all on top of the security issues already discussed.",
                    {
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-really-the-only-reasons-to-use"),
                value=REPLACE(
                    ie,
                    "Really the only reasons to use Internet Explorer are for developers to test what their sites look like on an older browser or if a company has business-critical apps that only work with the Internet Explorer browser.",
                    {
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-on-the-other-end-of-the-spectrum-fallback"),
                value=REPLACE(
                    ie,
                    "On the other end of the spectrum, Firefox is one of the most frequently updated browsers, and comes loaded with lots of useful and interesting features, like <a %(pocket)s>Pocket</a> that suggests interesting content every time you open a new tab. Our unified search and web address bar, or <em>Awesome Bar</em> as we call it, also gives you suggestions based on your existing bookmarks and tags, history, open tabs and popular searches. And with a free Firefox account you also get access to all your settings and <a %(products)s>our other Firefox products</a> on any device simply by signing in. Plus the peace of mind of knowing your browser is proactively working to protect your personal data.",
                    {
                        "%%": "%",
                        "%(pocket)s": VARIABLE_REFERENCE("pocket"),
                        "%(products)s": VARIABLE_REFERENCE("products"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-as-microsoft-has-made-the-move"),
                value=REPLACE(
                    ie,
                    "As Microsoft has made the move to sunset the Internet Explorer browser, it no longer supports any version for iOS, and has never been available for Android. Which means unless you’re running a Windows-based laptop or desktop, you won’t have access to your bookmarks, browsing history, saved passwords, and other information that modern browsers sync across devices.",
                    {
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-firefox-works-on-any-platform"),
                value=REPLACE(
                    ie,
                    "Firefox works on any platform, including Windows, macOS, Linux, Android and iOS. Which also means you can sync all your information across platforms. So if you’re browsing on a Windows-based laptop, you can pick up where you left off when you move to browsing on your iPhone or Android device. This convenience should come standard with any modern web browser, and is sorely lacking with Internet Explorer.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "macOS": TERM_REFERENCE("brand-name-mac"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                        "iPhone": TERM_REFERENCE("brand-name-iphone"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-there-was-a-time-not-so-long"),
                value=REPLACE(
                    ie,
                    "There was a time not so long ago where Internet Explorer was the most popular and widely used browser in the world. Times have changed and so has technology, but unfortunately Internet Explorer has pretty much stayed the same. Microsoft itself openly implores users to stop using Internet Explorer and instead switch to their newer Chromium-based Edge browser.",
                    {
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Chromium": TERM_REFERENCE("brand-name-chromium"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-ie-our-opinion-is-just-to-go-with"),
                value=REPLACE(
                    ie,
                    "Our opinion is just to go with a trusted, private browser with a track record of delivering a great experience across devices. In a head-to-head comparison, it’s really no contest at all. Firefox is hands down the winner across all assessment categories. If you do find yourself at Nana’s house firing up Internet Explorer, maybe you want to do Nana a favor and <a %(attrs)s>download Firefox</a> for her.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                    }
                )
            ),
        ]
    )

