from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

opera = "firefox/compare/opera.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/browsers/compare/opera.html, part {index}."""

    ctx.add_transforms(
        "firefox/browsers/compare/opera.ftl",
        "firefox/browsers/compare/opera.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("compare-opera-firefox-vs-opera-which-is"),
                value=REPLACE(
                    opera,
                    "Firefox vs. Opera: Which is the better browser for you?",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-compare-opera-to-the-firefox"),
                value=REPLACE(
                    opera,
                    "Compare Opera to the Firefox Browser to find out which is the best browser for you.",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-comparing-firefox-browser"),
                value=REPLACE(
                    opera,
                    "Comparing Firefox Browser with Opera",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-the-firefox-browser-and-opera"),
                value=REPLACE(
                    opera,
                    "The Firefox Browser and Opera are two of the earliest browsers on the scene still releasing frequent updates. While Opera has not reached the same level of user adoption as Firefox or Google Chrome, it’s maintained a relatively stable and loyal base over a sustained period of time. In this review, we’ll compare the Opera browser with our Firefox browser in terms of security and privacy, utility, and portability to help you choose which browser might be the best fit for you.",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-operas-privacy-policy-lacks-fallback"),
                value=REPLACE(
                    opera,
                    "Opera’s privacy policy lacks some specificity in its explanation of which types of information it collects and how, in certain sections, it says they collect names of account holders, IP addresses and search terms. What seems confusing and troubling is the section about International data transfers; when, how often and why they need to transfer your data internationally is not explained.",
                    {
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-firefoxs-privacy-policy-is"),
                value=REPLACE(
                    opera,
                    "Firefox’s <a %(attrs)s>privacy policy</a> is very transparent in describing what personal information we collect with the only end goal being to give you greater control over the information you share online.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-as-far-as-actual-privacy-protections"),
                value=REPLACE(
                    opera,
                    "As far as actual privacy protections in the Opera browser, it does offer a robust Private mode that allows you to surf the web without the browser tracking your activity. Also in normal browsing mode, you can also turn off some data collection features by digging into the settings to enable the ad blocker and adjust other security features.",
                    {
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-with-the-latest-version-of"),
                value=REPLACE(
                    opera,
                    "With the latest version of Firefox, <a %(attrs)s>Enhanced Tracking Protection</a> is turned on by default in normal browsing mode, so you don’t have to mess around with the settings just to protect yourself from trackers. With Enhanced Tracking Protection, Firefox actively blocks thousands of third-party trackers that try to follow you around the web. You are provided with a personalized protection report that shows how often Firefox blocked third-party cookies, social media trackers, fingerprinting tools and cryptominers as you browse the web.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-we-make-firefox-for-people"),
                value=REPLACE(
                    opera,
                    "We make Firefox for people like you, who care deeply about personal privacy and security. That's why we collect so little info about users and are transparent about how we use that info. It's hard to know how Opera is operating from a privacy perspective. While there are robust privacy features, how they themselves collect and share your data is murky. Firefox remains consistent in what we say and what we do in protecting your privacy.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-theres-no-debate-that-opera"),
                value=REPLACE(
                    opera,
                    "There’s no debate that Opera is a feature-packed browser with a clean user interface and strong customization options. Because Opera is built on Chromium, it can take advantage of most of Google Chrome’s vast extension library. Firefox also features a large <a %(attrs)s>extension library to browse</a>, but not quite as large as Chrome’s.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                        "Chromium": TERM_REFERENCE("brand-name-chromium"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-like-firefox-opera-delivers"),
                value=REPLACE(
                    opera,
                    "Like Firefox, Opera delivers a scrolling tab experience, which means that when you open more tabs than will fit on screen, it scrolls them off screen instead of just continuously shrinking them down. Also both Firefox and Opera have a screenshot tool that lets you capture a snapshot of your screen or part of the page. However, the Opera tool doesn’t give you the ability to create one huge capture of the whole webpage, only the visible portion.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-opera-provides-a-lot-of-hidden"),
                value=REPLACE(
                    opera,
                    "Opera provides a lot of hidden utility within its simple and manageable interface. For example there’s built-in support for messaging apps, like Facebook Messenger. There’s also a news reader that aggregates articles from your choice of sites and news outlets. The parallel feature to this on Firefox is called <a %(attrs)s>Pocket</a>. Pocket is a free service for Firefox account holders that makes it easy to find and save interesting articles and videos from all around the web. In addition, it recommends a variety of articles that expand your knowledge base curated by real, thoughtful humans.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-in-terms-of-head-to-head-utility"),
                value=REPLACE(
                    opera,
                    "In terms of head to head utility, Opera and Firefox are close competitors. Opera may have an advantage in one aspect with its compatibility with and access to Chrome’s huge extension library. But one significant factor to consider is the fact that Opera, because it’s built on Chromium, is a processor-hungry browser with its RAM consumption comparable to Chrome, which is known for its high CPU usage.",
                    {
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Chromium": TERM_REFERENCE("brand-name-chromium"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-both-firefox-and-opera-are"),
                value=REPLACE(
                    opera,
                    "Both Firefox and Opera are compatible across every platform including Windows, Mac, Linux, Android and iOS. Firefox account holders can easily sync their bookmarks, passwords, open tabs, and browsing history across all their signed into devices. The same is true for Opera users with an account. However, many sites, especially old sites that haven’t been updated in years, block the latest version of Opera entirely. So if visiting places like your Ex’s old blog is important, take heed, you may not be able to access some of the dustier corners of the internet if you use Opera.",
                    {
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "Mac": TERM_REFERENCE("brand-name-mac"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-in-addition-to-the-regular"),
                value=REPLACE(
                    opera,
                    "In addition to the regular mobile app, Opera has two other mobile versions of its browser: Touch and Mini. Touch is light on features but it’s designed to use on the go with only one hand. The Mini version aims at lowering data usage and increased speeds on slow connections by downgrading images and stripping away content.",
                    {
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-we-also-offer-an-additional"),
                value=REPLACE(
                    opera,
                    "We also offer an additional, albeit experimental version of our Firefox mobile app, <a %(attrs)s>Firefox Preview</a>, which focuses on speed and security.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-most-major-browsers-these"),
                value=REPLACE(
                    opera,
                    "Most major browsers these days, with the exception of Safari, work seamlessly across platforms and browsers. Opera and Firefox are no exception with both browsers providing excellent portability across every device.",
                    {
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-opera-overall-opera-is-a-solid-browser"),
                value=REPLACE(
                    opera,
                    "Overall, Opera is a solid browser, with a clean interface and a lot of useful features available. There are, however, some serious privacy concerns as well as an issue with it using a lot of processing power. Although Opera has some really terrific ease of use features, we still believe Firefox remains a superior browser based on performance and with a transparent user-privacy stance and strict privacy protections.",
                    {
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
    ),

