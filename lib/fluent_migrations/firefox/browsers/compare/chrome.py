from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

chrome = "firefox/compare/chrome.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/browsers/compare/chrome.html, part {index}."""

    ctx.add_transforms(
        "firefox/browsers/compare/chrome.ftl",
        "firefox/browsers/compare/chrome.ftl",
        transforms_from("""
compare-chrome-we-compare-mozilla-firefox = {COPY(chrome, "We compare Mozilla Firefox with Google Chrome in terms of privacy, utility and portability",)}
""", chrome=chrome) + [
            FTL.Message(
                id=FTL.Identifier("compare-chrome-at-firefox-we-have-a-huge"),
                value=REPLACE(
                    chrome,
                    "At Firefox, we have a huge number of dedicated users who appreciate our steadfast dedication to online privacy. For example, the latest version of Firefox includes a feature called Enhanced Tracking Protection (ETP) which is turned on by default for all users worldwide. ETP blocks over 2,000 trackers, including social trackers from companies like Facebook, Twitter, and LinkedIn. It also has an integrated feature called <a %(attrs)s>Firefox Monitor</a> that automatically notifies you if your password has been breached or needs to be updated. In addition to these protections, Firefox's Private Browsing mode automatically deletes your browsing information such as history and cookies, leaving no trace after you finish your session.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                        "Twitter": TERM_REFERENCE("brand-name-twitter"),
                        "Firefox Monitor": TERM_REFERENCE("brand-name-firefox-monitor"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-weve-also-recently-restated"),
                value=REPLACE(
                    chrome,
                    "We’ve also recently restated our commitment to privacy and transparency regarding user data in our most recent <a %(attrs)s>Privacy Notice</a> that states, “At Mozilla, we believe that privacy is fundamental to a healthy internet.”",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                    }
                )
            ),
        ] + transforms_from("""
compare-chrome-google-chrome-is-by-all-accounts = {COPY(chrome, "Google Chrome is by all accounts a secure browser, with features like Google Safe Browsing, which helps protect users by displaying an impossible-to-miss warning when they attempt to navigate to dangerous sites or download dangerous files.",)}
compare-chrome-ultimately-its-up-to-you = {COPY(chrome, "Ultimately, it’s up to you to decide whether or not or where to draw the line with sharing things like your search history and shopping history. But if you’re anything like most people, you’ve probably searched for some things on the internet that you would rather keep private.",)}
""", chrome=chrome)
        )
    ctx.add_transforms(
        "firefox/browsers/compare/chrome.ftl",
        "firefox/browsers/compare/chrome.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("compare-chrome-firefox-vs-chrome-which-is"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                    "Firefox vs. Chrome: Which is better?",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-comparing-firefox-browser"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "Comparing Firefox Browser with Google Chrome",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-fast-forward-to-today-the"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                    "Fast-forward to today, the competitive landscape for browsers has changed with many people beginning to question just what is happening to their online data such as browsing history, passwords, and other sensitive information. A lot has changed since 2008 when Chrome came onto the scene. At Firefox, we’ve been heads down, working to redesign our interface and provide users with an ever growing number of privacy and performance enhancements as well as plenty of handy browser tools.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-and-so-here-we-are-the-browser"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "And so here we are, the browser-wars are escalating once again and it’s time to reevaluate and compare Firefox Browser vs Google Chrome.",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-in-2008-google-introduced"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "In 2008, Google introduced Chrome, and its impact as an innovation in browser technology was immediate. It was faster for loading sites, took up minimal screen space and offered an undeniably simple user interface.",
                    {
                        "Google": TERM_REFERENCE("brand-name-google"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-in-fact-both-chrome-and-firefox"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "In fact, both Chrome and Firefox have rigorous security in place. Both include a thing called “sandboxing” which separates the processes of the browser so something like a harmful website doesn’t infect other parts of your laptop or other device.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-while-chrome-proves-to-be"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "While Chrome proves to be a safe web browser, its privacy record is questionable. Google actually collects a disturbingly large amount of data from its users including location, search history and site visits. Google makes its case for data collection saying it’s doing it to improve its services – like helping you find a sweater or a coffee shop like the one you previously bought or visited. However, others might disagree, making the point that Google is actually gathering an unprecedented amount of data for its own marketing purposes. They tout that they’re keeping your information private from hackers, but that’s beside the point. Google itself runs the world’s largest advertising network, thanks in large part to data they harvest from their users.",
                    {
                        "Google": TERM_REFERENCE("brand-name-google"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-in-terms-of-features-both"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "In terms of features, both Firefox and Chrome offer a large library of extensions and plug-ins, with Chrome’s catalog vastly outnumbering any other browser while nicely integrating with other Google services, like Gmail and Google Docs.",
                    {
                        "Google": TERM_REFERENCE("brand-name-google"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-firefox-also-has-a-sync-feature"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "Firefox also has a sync feature to see your open and recent tabs, browsing history, and bookmarks across all your devices.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-while-chrome-gets-the-nod"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "While Chrome gets the nod with add-ons and extensions, Firefox has a nicely curated set of built-in features, such as the incredibly handy screen capture tool, and reading mode feature which strips away everything from the page except the text from the article you’re reading.",
                    {
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-although-not-as-extensive"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "Although not as extensive as Chrome’s add-on library, Firefox, as open-source software with a huge number of active contributors, also features an incredible number of useful extensions.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-if-having-tons-of-open-tabs"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "If having tons of open tabs is your thing, then it really comes down to your UI preference. Firefox features a horizontal scroll on all your open tabs rather than shrinking them smaller and smaller with each new one. Google Chrome prefers to shrink them down so just the favicon is visible. The only problem with this is when you have multiple tabs open from the same website, so you see the same favicon across your tabs.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-almost-needless-to-say-versions"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "Almost needless to say, versions of both Firefox and Chrome are available for the most popular desktop and mobile operating systems (Windows, macOS, Linux, Android, iOS).",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "macOS": TERM_REFERENCE("brand-name-mac"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-both-chrome-and-firefox-also"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "Both Chrome and Firefox also allow you to sync things like passwords, bookmarks, and open tabs across all your devices. If you have a Firefox account, you can manually send an open tab on your desktop to your mobile device or vice versa. With Chrome, it’s done automatically if you’ve chosen that setting in your preferences. Not having to manually send the tab from one device to the other is convenient when you want to do something like continue reading an article you didn’t finish earlier. But there could be times where automatic syncing might not be ideal if there’s a chance multiple users are browsing while signed in to your Google account.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-we-think-its-fair-to-say"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "We think it’s fair to say Firefox and Chrome are really neck and neck in terms of portability and utility, with Chrome having a slight edge in utility because of its huge library of extensions and add-on features. But in terms of Privacy, Firefox wins the day with our commitment to preserving our users’ online data and providing free baked-in services like password managers that also alert you if there happens to be a data breach involving your credentials.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-as-for-customization-our"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "As for customization, our fans will tell you one of the things they love most about our browser is its ability to allow you to move and arrange a majority of the UI elements to best suit your needs. Chrome allows you to hide certain UI elements but there’s not much allowance, if any, for moving things around based on your preferences. However, it should be noted that both Chrome and Firefox make it pretty easy to change your browser’s appearance and theme.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-chrome-for-practical-purposes-theres"),
                value=REPLACE(
                    "firefox/compare/chrome.lang",
                     "For practical purposes, there’s obviously really nothing preventing you from using both browsers—Firefox for those moments in life when privacy really matters, and Chrome if you’re still invested in the Google ecosystem. Yet with the growing number of incursions into our personal data, Firefox may prove to be the right choice in the long run for those of us who value protecting our personal privacy online.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                    }
                )
            ),
        ]
    )

