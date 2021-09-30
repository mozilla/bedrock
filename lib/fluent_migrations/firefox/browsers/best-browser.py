from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

best_browser = "firefox/browsers/best-browser.lang"
best_browser = "firefox/best-browser.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/browsers/best-browser.html, part {index}."""

    ctx.add_transforms(
        "firefox/browsers/best-browser.ftl",
        "firefox/browsers/best-browser.ftl",
        transforms_from(
            """
best-browser-find-your-best-browser = {COPY(best_browser, "Find your best browser for speed, privacy and security.",)}
best-browser-so-many-browser-options = {COPY(best_browser, "So many browser options, but there’s only one that works best for your needs. The best browser for you should offer both speed and privacy protection.",)}
best-browser-privacy-speed-and-security = {COPY(best_browser, "Privacy, speed, and security.",)}
best-browser-how-to-choose-the-best = {COPY(best_browser, "How to choose the best browser for you.",)}
best-browser-the-internet-has-become = {COPY(best_browser, "The internet has become as essential as electricity and running water, so choosing the best browser for you is more important than ever. The internet is a second office, a teacher and sometimes a medical advisor, even if your actual doctor would prefer you didn’t look up your symptoms online.",)}
""",
            best_browser=best_browser,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("best-browser-in-the-mid-nineties"),
                value=REPLACE(
                    best_browser,
                    "In the mid-nineties, Netscape, Internet Explorer and AOL dominated the landscape. It was a simpler time when the sweet melody of dial-up internet rang across the land. You learned the meaning of patience waiting for web pages to load. Back then, all that mattered was browser speed.",
                    {
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Netscape": TERM_REFERENCE("brand-name-netscape"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
best-browser-today-is-a-different = {COPY(best_browser, "Today is a different story. Ads, privacy hacks, security breaches, and fake news might have you looking at other qualities in a browser. How does the browser protect your privacy? Does it allow trackers to follow you across the web? Does it built to multitask and handle many computer and internet operations at once?",)}
best-browser-when-you-use-a-browser = {COPY(best_browser, "When you use a browser for everything, it needs to be fast. But for the same reason, it needs to be private. A browser has access to everything you do online, so it can put you at real risk if it doesn’t have strong privacy features.",)}
""",
            best_browser=best_browser,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("best-browser-marshall-erwin-senior"),
                value=REPLACE(
                    best_browser,
                    "Marshall Erwin, Senior Director of Trust and Security at Mozilla",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
best-browser-if-youre-wondering = {COPY(best_browser, "If you’re wondering what it means to have a private or fast browser, here’s a breakdown of three things a browser should have.",)}
best-browser-a-browser-built-for = {COPY(best_browser, "A browser built for speed.",)}
best-browser-a-browser-is-still = {COPY(best_browser, "A browser is still a tool, so it makes sense that you’ll want to pick the best one for the job. If you’re a human who needs to work to survive, you’ll need a fast internet browser. One thing to keep in mind is a browser that runs third-party trackers is more likely to be slower than a browser that doesn’t. Third-party trackers are cookies, and while you can’t see them, they are running in the background of the site, taking up precious time. The more third-party trackers a browser blocks, the faster it can run.",)}
""",
            best_browser=best_browser,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("best-browser-this-is-one-of-the"),
                value=REPLACE(
                    best_browser,
                    "This is one of the many reasons to choose the Firefox browser: Firefox blocks third-party trackers by default. We have other reasons and we’ll get into those later.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
best-browser-a-browser-that-puts = {COPY(best_browser, "A browser that puts safety first.",)}
best-browser-remember-the-last-massive = {COPY(best_browser, "Remember the last massive data breach? If not, it’s probably because it happens so often. Companies hold on to customer data, like their personal or financial information, and hackers steal it. If you’re making safety a priority, then a secure internet browser is the best browser for you.",)}
best-browser-there-are-a-few-ways = {COPY(best_browser, "There are a few ways a browser can help its users stay secure. A browser that is up to date with the latest security tech can help protect your computer and websites from unwanted visitors, such as malware or computer viruses.",)}
""",
            best_browser=best_browser,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("best-browser-the-second-is-not-storing"),
                value=REPLACE(
                    best_browser,
                    'The second is not storing too much user data. Hackers can’t steal what’s not there, which is why Firefox keeps a minimum amount of information about its users. <a href="%(data)s">Firefox knows</a> if you use the browser and your general location <a href="%(privacy)s">but not the name of your childhood pet or your favorite color.</a>',
                    {
                        "%%": "%",
                        "%(data)s": VARIABLE_REFERENCE("data"),
                        "%(privacy)s": VARIABLE_REFERENCE("privacy"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
best-browser-last-but-not-least = {COPY(best_browser, "Last but not least, a safe browser should offer tools to help you keep an eye on your accounts. Think of alerts that go straight to your email if any of your accounts get breached or icons that tell you whether a website is encrypted, (i.e., if it’s a good idea to enter your credit number on a shopping site).",)}
""",
            best_browser=best_browser,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("best-browser-firefox-is-offering"),
                value=REPLACE(
                    best_browser,
                    'Firefox is offering something new to keep you safe: <a href="%(monitor)s">Firefox Monitor</a>. It’s a free service that will alert you if there are any public hacks on your accounts and let you know if your accounts got hacked in the past. Another neat feature is the Green Lock. It looks like a small green icon at the top left side of the browser window. If you’re on Firefox and see the green lock, it means the website is encrypted and secure. If the lock is grey, you might want to think twice about entering any sensitive information.',
                    {
                        "%%": "%",
                        "%(monitor)s": VARIABLE_REFERENCE("monitor"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Firefox Monitor": TERM_REFERENCE("brand-name-firefox-monitor"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
best-browser-we-visit-hundreds-or = {COPY(best_browser, "We visit hundreds or even thousands of websites each day, and you can’t expect users to make security and privacy decisions for each of these sites. That is why a browser that gives you more control is so important - because it offers real, meaningful protection.",)}
best-browser-a-browser-that-minds = {COPY(best_browser, "A browser that minds its business.",)}
best-browser-privacy-on-the-web = {COPY(best_browser, "Privacy on the web is a hot button issue. If privacy is number one on your list of priorities, you want to look for a browser that takes that seriously. When choosing the best private browser for you, look at the tracking policy and how a browser handles your data. These seem like technical questions, but they’re the reason some browsers are more private than others.",)}
best-browser-trackers-are-all-those = {COPY(best_browser, "Trackers are all those annoying “cookies” messages you get on airline sites. These third-party trackers know where you click and can be used to analyze your behavior. A private browser should give users the option to turn off third-party trackers, but ideally, turn them off by default.",)}
best-browser-another-way-to-stop = {COPY(best_browser, "Another way to stop trackers from tracking is using private mode to browse. Any browser that claims to be private should offer browsing in private mode.",)}
""",
            best_browser=best_browser,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("best-browser-one-easy-way-to-check"),
                value=REPLACE(
                    best_browser,
                    'One easy way to check is to visit a browser’s content setting page and privacy policy. The privacy webpage should outline if your data is shared and why. It’s why the <a href="%(privacy)s">Firefox privacy notice</a> is easy to read and easy to find.',
                    {
                        "%%": "%",
                        "%(privacy)s": VARIABLE_REFERENCE("privacy"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
best-browser-choosing-the-best-browser = {COPY(best_browser, "Choosing the best browser for you is a lot like choosing a home. You want to explore your options, do some research and make a decision based on what’s important to you.",)}
""",
            best_browser=best_browser,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("best-browser-at-firefox-weve-worked"),
                value=REPLACE(
                    best_browser,
                    'At <a href="%(firefox)s">Firefox</a>, we’ve worked hard to build a browser that is twice as fast as before and gives users more control over their online life.',
                    {
                        "%%": "%",
                        "%(firefox)s": VARIABLE_REFERENCE("firefox"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
best-browser-take-control-of-your = {COPY(best_browser, "Take control of your browser.",)}
""",
            best_browser=best_browser,
        ),
    )
