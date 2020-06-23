from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

compare = "firefox/compare.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/browsers/compare/index.html, part {index}."""

    ctx.add_transforms(
        "firefox/browsers/compare/index.ftl",
        "firefox/browsers/compare/index.ftl",
        transforms_from("""
compare-index-six-of-the-best-browsers-fallback = {COPY(compare, "Six of the best browsers in direct comparison",)}
compare-index-privacy-utility-portability = {COPY(compare, "Privacy. Utility. Portability.",)}
compare-index-a-great-internet-browser-should = {COPY(compare, "A great internet browser should have the functionality you need, portability across devices, and the privacy you deserve.",)}
compare-index-which-browser-is-best-at-keeping = {COPY(compare, "Which browser is best at keeping things confidential?",)}
compare-index-its-not-unreasonable-to-expect = {COPY(compare, "It’s not unreasonable to expect a high level of data protection and privacy from the products we regularly use to get online. At a minimum, a browser should offer some version of “private browsing mode” that automatically deletes your history and search history so other users on the same computer can’t access it. In this area, all six of the browsers compared here score points.",)}
compare-index-what-you-do-online-literally = {COPY(compare, "What you do online literally shouldn’t be anyone else’s business.",)}
compare-index-what-has-your-browser-done = {COPY(compare, "What has your browser done for you lately?",)}
compare-index-how-well-does-your-browser = {COPY(compare, "How well does your browser work across your devices?",)}
compare-index-almost-all-of-the-browsers = {COPY(compare, "Almost all of the browsers compared here allow synchronization between desktop and mobile devices. You’ll need an account to do it, which you can use to log into the browser on all devices and synchronize things like passwords, browsing history, bookmarks and settings.",)}
compare-index-conclusion = {COPY(compare, "Conclusion:",)}
compare-index-and-the-winner-is = {COPY(compare, "And the winner is…",)}
""", compare=compare)
        )
    ctx.add_transforms(
        "firefox/browsers/compare/index.ftl",
        "firefox/browsers/compare/index.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("compare-index-using-a-browser-that-blocks"),
                value=REPLACE(
                    "firefox/compare.lang",
                    "Using a browser that blocks third-party trackers isn’t just important for privacy — it usually means it runs much faster, too. Most trackers are just scripts that run in the background on a number of websites. You can’t see them, but you can feel them slowing down your browser. As of version 67 of Firefox, fingerprinting and cryptominers are also blocked. If you’re not familiar with cryptominers, here’s an example of how they can affect you: maybe you’ve experienced your computer suddenly running hotter or the battery depleting faster than normal. That’s often the byproduct of cryptominers creeping around on your device.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-index-another-browser-feature-fallback"),
                value=REPLACE(
                    "firefox/compare.lang",
                    "Another browser feature that should be a given is the ability to prevent websites and companies from tracking your browsing and shopping data — even in normal browsing mode. But that’s actually not the case: in fact, the only browsers that block third party tracking cookies by default are Firefox and Safari.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-index-in-addition-to-privacy-protection-fallback"),
                value=REPLACE(
                    "firefox/compare.lang",
                    "In addition to privacy protection, which largely takes place in the background of the browser, another key ingredient to a well-made browser is the actual user interface and functionality. Almost all six browsers are equal when it comes to tab browsing, bookmark management, auto-completion, proofreading and extensions. Firefox, Edge and Opera also offer a quick screenshot function that proves to be quite handy and is definitely something you notice is missing when you switch over to a browser without it.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-index-find-out-how-firefox-fallback"),
                value=REPLACE(
                    "firefox/compare.lang",
                    "Find out how Firefox, Chrome, Edge, Safari, Opera and Internet Explorer differ in terms of privacy, utility and portability.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-index-looking-for-a-better-fallback"),
                value=REPLACE(
                    "firefox/compare.lang",
                    "Looking for a better browser? We’ll compare Firefox with Chrome, Edge, Safari, Opera and Internet Explorer to help you make your decision.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-index-so-is-your-browser-the-fallback"),
                value=REPLACE(
                    "firefox/compare.lang",
                    "So is your browser the best one for what you do online? The right browser can make a big difference in how you experience the web. So, without further ado, let’s compare Google Chrome, Firefox, Safari, Opera, Microsoft Internet Explorer and Edge — and see which best suits your needs.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-index-since-your-browser-is-your"),
                value=REPLACE(
                    "firefox/compare.lang",
                    "Since your browser is your gateway to the internet, speed, security, privacy and utility are paramount. In recent years, Google Chrome has been the browser of choice for many. But at a time when online ads seem to follow us everywhere and data breaches are a fixture of news headlines, a lot of people are starting to demand more privacy and respect from their browser.",
                    {
                        "Google": TERM_REFERENCE("brand-name-google"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-index-the-first-thing-to-point-fallback"),
                value=REPLACE(
                    "firefox/compare.lang",
                    "The first thing to point out about portability is that not all browsers run on all operating systems. While Firefox, Chrome and Opera work on all major systems and are easy to install, Internet Explorer, Edge and Safari only work on Microsoft and Apple’s own systems. The mobile version of Safari is pre-installed on Apple’s mobile devices, and most Android devices come with a pre-installed browser modified by the manufacturer for the device. Firefox, Chrome, Edge and Opera can easily be installed and even used side by side.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-index-browsers-have-come-a-long"),
                value=REPLACE(
                    "firefox/compare.lang",
                    "Browsers have come a long way since Chrome was introduced and took over the market share. Most of the modern browsers have closed the gap on portability and functionality, and in some areas, like speed and privacy, have actually surpassed Chrome. Still, determining which browser is right for you will always depend on your individual needs and what you value most as you navigate online.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-index-firefox-is-backed-by-the-not"),
                value=REPLACE(
                    "firefox/compare.lang",
                    "Firefox is backed by the not-for-profit Mozilla.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-index-firefox-puts-your-privacy"),
                value=REPLACE(
                    "firefox/compare.lang",
                    "Firefox puts your privacy first — in everything we make and do. We believe you have the right to decide how and with whom you share your personal information. Firefox collects as little data as possible and never sells it. The little data we do collect is only used to make products and features better. No secrets. But a lot of transparency and real privacy.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-index-based-on-the-criteria-we-outlined"),
                value=REPLACE(
                    "firefox/compare.lang",
                    "Based on the criteria we outlined — privacy, utility, and portability — there’s really only one browser that meets the mark, and that’s Firefox. The real area of difference isn’t in functionality, it’s privacy. Firefox is the most private browser that doesn’t lock you into an ecosystem. Use it on any operating system, on all your devices, and feel secure when you do.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
    )
