from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

adblocker = "firefox/adblocker.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/features/adblocker.html, part {index}."""

    ctx.add_transforms(
        "firefox/features/adblocker.ftl",
        "firefox/features/adblocker.ftl",
        transforms_from("""
features-adblocker-how-to-block-annoying = {COPY(adblocker, "How to block annoying ads using an ad blocker",)}
""", adblocker=adblocker) + [
            FTL.Message(
                id=FTL.Identifier("features-adblocker-how-to-stop-seeing-too"),
                value=REPLACE(
                    adblocker,
                    "How to stop seeing too many ads and keep companies from following you around online. An ad blocker guide from the Firefox web browser.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-adblocker-the-ad-blocker-a-secret = {COPY(adblocker, "The ad blocker – a secret weapon against annoying ads.",)}
features-adblocker-so-many-ads-so-little = {COPY(adblocker, "So many ads, so little patience… It’s time to stop the madness.",)}
features-adblocker-the-average-person-sees = {COPY(adblocker, "The average person sees an average of 4,000 ads a day. If you think that’s too many, an ad blocker is your new best friend.",)}
features-adblocker-an-ad-blocker-is-a-piece = {COPY(adblocker, "An ad blocker is a piece of software that can be used to block ads, and they work in two ways. The first way is when an ad blocker blocks the signal from an advertiser’s server, so the ad never shows up on your page. Another way ad blockers work is by blocking out sections of a website that could be ads.",)}
""", adblocker=adblocker) + [
            FTL.Message(
                id=FTL.Identifier("features-adblocker-these-ads-might-be-loud"),
                value=REPLACE(
                    adblocker,
                    "These ads might be loud video ads, ads that follow you around the web, trackers, third-party cookies, and more. To use an ad blocker, you can search for ad blocker add-ons that are available in your browser. <a href=\"%(firefox)s\">Firefox</a>, for example, has <a href=\"%(addons)s\">this list of approved ad blocker add-ons</a>. Click on this list (or ad blockers that are approved for your browser) and see which fits your needs.",
                    {
                        "%%": "%",
                        "%(firefox)s": VARIABLE_REFERENCE("firefox"),
                        "%(addons)s": VARIABLE_REFERENCE("addons"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-adblocker-find-the-right-ad-blocker = {COPY(adblocker, "Find the right ad blocker for you",)}
""", adblocker=adblocker) + [
            FTL.Message(
                id=FTL.Identifier("features-adblocker-theres-adblocker-ultimate"),
                value=REPLACE(
                    adblocker,
                    "There’s <a href=\"%(url)s\">AdBlocker Ultimate</a> that gets rid of every single ad, but buyer beware. Some of your favorite newspapers and magazines rely on advertising. Too many people blocking their ads could put them out of business.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("features-adblocker-popup-ads-are-the-worst"),
                value=REPLACE(
                    adblocker,
                    "Popup ads are the worst. Block them with <a href=\"%(url)s\">Popup Blocker</a> and never deal with another annoying popup again.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("features-adblocker-one-of-the-most-popular"),
                value=REPLACE(
                    adblocker,
                    "One of the most popular ad blockers for Chrome, Safari and Firefox is <a href=\"%(url)s\">AdBlock</a>. Use it to block ads on Facebook, YouTube and Hulu.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "YouTube": TERM_REFERENCE("brand-name-youtube"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Hulu": TERM_REFERENCE("brand-name-hulu"),
                    }
                )
            ),
        ] + transforms_from("""
features-adblocker-create-a-tracker-free = {COPY(adblocker, "Create a tracker-free zone with Content Blocking",)}
""", adblocker=adblocker) + [
            FTL.Message(
                id=FTL.Identifier("features-adblocker-on-firefox-you-can-use"),
                value=REPLACE(
                    adblocker,
                    "On Firefox, you can use <a href=\"%(privacy)s\">Privacy</a> or <a href=\"%(blocking)s\">Content Blocking</a> settings to get even more control over ad trackers that serve you the ads.",
                    {
                        "%%": "%",
                        "%(privacy)s": VARIABLE_REFERENCE("privacy"),
                        "%(blocking)s": VARIABLE_REFERENCE("blocking"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-adblocker-choose-your-level-of-protection = {COPY(adblocker, "Choose your level of protection",)}
""", adblocker=adblocker) + [
            FTL.Message(
                id=FTL.Identifier("features-adblocker-to-start-click-on-the"),
                value=REPLACE(
                    adblocker,
                    "To start, click on the Firefox menu in the top right-hand corner of your screen. It looks like three lines stacked on top of each other. In the drop-down menu, click on Content Blocking. You should see a blue pop-up with different selections.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-adblocker-go-easy-with-standard = {COPY(adblocker, "Go easy with Standard mode",)}
""", adblocker=adblocker) + [
            FTL.Message(
                id=FTL.Identifier("features-adblocker-if-ads-dont-bother-you"),
                value=REPLACE(
                    adblocker,
                    "If ads don’t bother you and you don’t mind being followed by trackers and third-party cookies, then the Standard setting should work for you. To get trackers off your tail in Standard mode, use a <a href=\"%(url)s\">Private Browsing</a> window.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                    }
                )
            ),
        ] + transforms_from("""
features-adblocker-get-tough-with-strict = {COPY(adblocker, "Get tough with Strict mode",)}
""", adblocker=adblocker) + [
            FTL.Message(
                id=FTL.Identifier("features-adblocker-if-seeing-too-many-ads"),
                value=REPLACE(
                    adblocker,
                    "If seeing too many ads ruins your day, then the Strict mode is a better fit. This mode will block known third-party trackers and cookies in all Firefox windows.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-adblocker-do-it-yourself-custom = {COPY(adblocker, "Do-it-yourself Custom mode",)}
features-adblocker-the-custom-setting-gives = {COPY(adblocker, "The Custom setting gives you the ultimate choice. You can decide what you’re blocking, including trackers, cookies and more. If you allow cookies from a website, you’ll automatically be in Custom mode.",)}
features-adblocker-cover-your-trail-block = {COPY(adblocker, "Cover your trail, block trackers",)}
features-adblocker-click-on-the-trackers = {COPY(adblocker, "Click on the Trackers box and you’ll be able to block trackers in two ways. One way to block trackers is to do it when you’re working in a Private Window. Another way to do it is to block trackers in all windows. Keep in mind that if you choose to always block trackers, some pages might not load correctly.",)}
features-adblocker-take-a-bite-out-of-cookies = {COPY(adblocker, "Take a bite out of cookies",)}
""", adblocker=adblocker) + [
            FTL.Message(
                id=FTL.Identifier("features-adblocker-cookies-are-sent-by-websites"),
                value=REPLACE(
                    adblocker,
                    "<a href=\"%(url)s\">Cookies</a> are sent by websites you visit. They live on your computer and monitor what you’ve been doing on a site. When an airline hikes your rates because you’ve looked at plane tickets once that day, that is the handiwork of a cookie.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("features-adblocker-in-firefox-you-can-block"),
                value=REPLACE(
                    adblocker,
                    "In Firefox, you can block all third-party cookies or just those set by trackers. Be aware that blocking all cookies can break some sites.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-adblocker-send-a-do-not-track-signal = {COPY(adblocker, "Send a Do Not Track signal",)}
""", adblocker=adblocker) + [
            FTL.Message(
                id=FTL.Identifier("features-adblocker-if-you-dont-want-your"),
                value=REPLACE(
                    adblocker,
                    "If you don’t want your online behavior used for ads, you can send websites a polite “thanks but no thanks” letter by checking the <a href=\"%(url)s\">Do Not Track</a> option of Firefox. Participation is voluntary, but the websites that participate will stop tracking you immediately.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-adblocker-speed-up-thanks-to-ad = {COPY(adblocker, "Speed up thanks to ad blockers",)}
features-adblocker-in-some-cases-an-ad-blocker = {COPY(adblocker, "In some cases, an ad blocker can help your browser go faster. When an ad is loading, it can slow down a website. At the same time, it takes longer to find what you’re looking for if you’re too busy closing yet another ad.",)}
""", adblocker=adblocker) + [
            FTL.Message(
                id=FTL.Identifier("features-adblocker-if-you-want-to-learn-more"),
                value=REPLACE(
                    adblocker,
                    "If you want to learn more about ad blocking, there are hundreds of ad blocker extensions available for Firefox and other browsers. If want to try out the ad blockers Firefox uses, <a href=\"%(url)s\">click here to download</a> a browser that puts privacy first.",
                    {
                        "%%": "%",
                        "%(url)s": VARIABLE_REFERENCE("url"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
features-adblocker-take-control-of-your-browser = {COPY(adblocker, "Take control of your browser.",)}
""", adblocker=adblocker)
        )
