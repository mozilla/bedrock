from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

safari = "firefox/compare/safari.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/browsers/compare/safari.html, part {index}."""

    ctx.add_transforms(
        "firefox/browsers/compare/safari.ftl",
        "firefox/browsers/compare/safari.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("compare-safari-firefox-vs-safari-which-is"),
                value=REPLACE(
                    safari,
                    "Firefox vs. Safari: Which is the better browser for you?",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-safari-is-the-pre-installed"),
                value=REPLACE(
                    safari,
                    "Safari is the pre-installed browser on Mac and iPhone. Compare Safari to the Firefox Browser to find out which is the better browser for you.",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "iPhone": TERM_REFERENCE("brand-name-iphone"),
                        "Mac": TERM_REFERENCE("brand-name-mac"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-comparing-firefox-browser"),
                value=REPLACE(
                    safari,
                    "Comparing Firefox Browser with Apple Safari",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-if-you-use-a-mac-or-have"),
                value=REPLACE(
                    safari,
                    "If you use a Mac or have an iPhone, chances are you’re familiar with the Safari web browser. The fact that it’s pre-installed as the default browser for Apple product users definitely gives it an early advantage, but Firefox has its own set of useful features that make it an attractive alternative. Here we’ll explore the main differences between our browser and Safari in terms of privacy, utility, and portability between devices.",
                    {
                        "iPhone": TERM_REFERENCE("brand-name-iphone"),
                        "Apple": TERM_REFERENCE("brand-name-apple"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-privacy-has-become-a-white"),
                value=REPLACE(
                    safari,
                    "Privacy has become a white hot topic for tech companies as they realize more and more people are feeling vulnerable to things like data breaches, ad trackers and hackers. But when it comes down to the real tools people use to navigate the actual interwebs, is it all talk or are they actually taking action to keep your data secure?",
                    {
                        "Apple": TERM_REFERENCE("brand-name-apple"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-as-alluded-to-before-apple-fallback"),
                value=REPLACE(
                    safari,
                    "As alluded to before, Apple is one of those companies that recently decided to step up their privacy game. Not long ago, Apple implemented cross-site tracking prevention in Safari, which prevents ads from following you around the internet. Safari also offers a strong password suggestion when you sign up for a new account on any website. And if you’re invested in the iCloud ecosystem, it syncs that password securely with your other devices, so you never actually have to remember it.",
                    {
                        "Apple": TERM_REFERENCE("brand-name-apple"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-like-safari-we-at-firefox"),
                value=REPLACE(
                    safari,
                    "Like Safari, we at Firefox have made a point of focusing on privacy and security. But unlike Safari, we’ve been standing on the privacy soap box for a long time. In fact, Mozilla (our parent company) was one of the first voices in the tech community to sound the alarm for online privacy.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-our-private-browsing-mode"),
                value=REPLACE(
                    safari,
                    "Our Private Browsing mode blocks trackers and erases your passwords, cookies and history every time you close it. But you can also experience our advanced privacy features even in regular browsing mode. With the latest edition of Firefox, enhanced tracking prevention is turned on by default. This prevents things like cross-site trackers from following you as you jump around the web. Also, with Facebook being caught out almost daily for privacy problems, our <a %(attrs)s>Facebook Container</a> extension makes a lot of sense. It makes it harder for Facebook to track you around the web — similar to what Safari does to prevent cross-site tracking — but Firefox actually isolates your Facebook session into a separate container blocking Facebook from tracking what you do on other websites. Why do they need to know what you look up on WebMD anyway?",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                        "Facebook Container": TERM_REFERENCE("brand-name-facebook-container"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-as-far-as-security-goes-firefox"),
                value=REPLACE(
                    safari,
                    "As far as security goes, Firefox is solid there as well. Any time you’re in Firefox, you can right-click in the password field to securely generate a strong password using the Fill Password option. When you save your new password, we will prompt you to save to its built-in password manager, <a %(lockwise)s>Lockwise</a>. We also serve up users and account holders with another free and useful product called <a %(monitor)s>Monitor</a> that automatically alerts you if your data is included in a known data breach.",
                    {
                        "%%": "%",
                        "%(lockwise)s": VARIABLE_REFERENCE("lockwise"),
                        "%(monitor)s": VARIABLE_REFERENCE("monitor"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Lockwise": TERM_REFERENCE("brand-name-lockwise"),
                        "Monitor": TERM_REFERENCE("brand-name-monitor"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-if-you-choose-to-use-safari"),
                value=REPLACE(
                    safari,
                    "If you choose to use Safari, you’re in safe hands as long as you’re using an Apple device. But Safari only works on Apple devices, whereas Firefox works on Windows, Mac, iOS, Android and Linux. So no matter what operating system you choose, Firefox has you covered with our security and privacy protections.",
                    {
                        "Apple": TERM_REFERENCE("brand-name-apple"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                        "Mac": TERM_REFERENCE("brand-name-mac"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-apple-is-widely-known-for"),
                value=REPLACE(
                    safari,
                    "Apple is widely known for its closed ecosystem as it relates to creating software for its products. But inside the App Store, it does offer a section to developers to create plugins and add-ons to make the browser more robust. These extensions are also browsable through the App Store and easily added to Safari.",
                    {
                        "Apple": TERM_REFERENCE("brand-name-apple"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "App Store": TERM_REFERENCE("brand-name-app-store"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-in-addition-to-the-regular"),
                value=REPLACE(
                    safari,
                    "In addition to the regular set of features you’d expect in a browser, such as tabbed browsing and private browsing, Safari has some unexpected features as well. For instance, if a user were to right-click a word anywhere on a page inside Safari, then click Look Up, they’d get a dictionary definition plus entries from the thesaurus, App Store, movies and more. Safari’s Parental Controls are easy to customize, allowing the adults to breathe a little easier when the kids begin to get curious about the internet.",
                    {
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "App Store": TERM_REFERENCE("brand-name-app-store"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-like-safari-firefox-encourages"),
                value=REPLACE(
                    safari,
                    "Like Safari, Firefox encourages its enthusiastic developer community to create <a %(attrs)s>add-ons and extensions</a> to the browser. And since our platform is open-source, there’s a vast selection adding a wealth of functionality.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-also-when-you-sign-up-for-fallback"),
                value=REPLACE(
                    safari,
                    "Also, when you sign up for a Firefox account you get access to some unique services like Screenshots, <a %(pocket)s>Pocket</a> and <a %(send)s>Send</a> that integrate directly into the browser. Screenshots is a feature built right into the Firefox browser, allowing you to copy or download any or all part of a web page. When you save the screenshot, you can also choose which folder you want to find it in, instead of cluttering your desktop. The Pocket for Firefox button lets you save web pages and videos to Pocket in just one click, so you can read a clean, distraction-free version whenever and wherever you want — even offline. With Send, you can share large files with end-to-end encryption and a variety of security controls, such as the ability to set an expiration time for a file link to expire, the number of downloads, and whether to add an optional password for an extra layer of security.",
                    {
                        "%%": "%",
                        "%(pocket)s": VARIABLE_REFERENCE("pocket"),
                        "%(send)s": VARIABLE_REFERENCE("send"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                        "Send": TERM_REFERENCE("brand-name-send"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-firefox-and-safari-both-provide"),
                value=REPLACE(
                    safari,
                    "Firefox and Safari both provide a seamless experience when moving from desktop to mobile browsing or vice versa. For Safari, one of its main strengths is its continuity features. It syncs your bookmarks, tabs, history and more to iCloud so they’re available on all your devices. That means you can open a tab on your iPhone and have it also appear on your Mac laptop with just a click.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "iPhone": TERM_REFERENCE("brand-name-iphone"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-both-browsers-have-a-lot"),
                value=REPLACE(
                    safari,
                    "Both browsers have a lot of crossover features, as well as some unique functions. It’s worth mentioning, if you take a lot of screenshots, you’ll wonder how you ever lived without this handy feature that’s built right into Firefox. But if you’re just looking for a fast, private browser for surfing and shopping, then you may want to give Firefox a try — especially if you’ve been exclusively using Safari because it came preloaded as the default browser on your computer. Eventually, you’ll discover which one is more suited to your needs.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-firefox-also-offers-a-similar"),
                value=REPLACE(
                    safari,
                    "Firefox also offers a similar sync feature when you sign up for a free <a %(attrs)s>Firefox Account</a> that enables users to easily synchronize their bookmarks, browsing history, preferences, passwords, filled forms, add-ons, and the last 25 opened tabs across multiple computers. What sets Firefox apart from Safari is that it is available on any desktop or mobile platform, iOS, Android, Windows or macOS, boosting its portability across any device you may own.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Firefox Account": TERM_REFERENCE("brand-name-firefox-account"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "macOS": TERM_REFERENCE("brand-name-macos"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-the-firefox-app-for-ios-and"),
                value=REPLACE(
                    safari,
                    "The Firefox app for <a %(ios)s>iOS</a> and <a %(android)s>Android</a> is one of the fastest browsers available and also has solid security and anti-tracking features — a huge plus if you’re constantly bouncing between a laptop and mobile devices.",
                    {
                        "%%": "%",
                        "%(ios)s": VARIABLE_REFERENCE("ios"),
                        "%(android)s": VARIABLE_REFERENCE("android"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-since-safari-is-apples-proprietary"),
                value=REPLACE(
                    safari,
                    "Since Safari is Apple’s proprietary web browser, its iCloud syncing works exclusively with Apple products. This can be somewhat limiting if, for example, you’re both an Android user and an iPhone user or if you have a Windows based PC for work but use an iPhone as your personal device.",
                    {
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Apple": TERM_REFERENCE("brand-name-apple"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "iPhone": TERM_REFERENCE("brand-name-iphone"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-safari-does-a-great-job-of"),
                value=REPLACE(
                    safari,
                    "Safari does a great job of making the browsing experience simple, fast, and seamless if you’re an Apple user with multiple Apple products. Like Safari, Firefox is a fast and utilitarian browser, but privacy and cross-platform compatibility are our defining features. Firefox updates each month with new features and functionality. For example, one recent update switched on our <a %(attrs)s>Enhanced Tracking Protection (ETP)</a> by default for new users, which effectively blocks cookies and cross-site trackers.",
                    {
                        "%%": "%",
                        "%(attrs)s": VARIABLE_REFERENCE("attrs"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Apple": TERM_REFERENCE("brand-name-apple"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("compare-safari-in-the-end-it-just-boils"),
                value=REPLACE(
                    safari,
                    "In the end, it just boils down to what you value in your browser. If you’re integrated with the Apple ecosystem, Safari is still a great choice. But if you value having the latest and greatest privacy protections and being able to work across multiple operating systems, we think Firefox is your best bet. Firefox is also a solid option as a secondary browser for those Apple-exclusive users who may want to switch into a different browser for those online moments that call for extra layers of privacy protection.",
                    {
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Apple": TERM_REFERENCE("brand-name-apple"),
                    }
                )
            ),
        ]
    )

