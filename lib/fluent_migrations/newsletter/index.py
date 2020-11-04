from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

newsletters = "mozorg/newsletters.lang"

def migrate(ctx):
    """Migrate bedrock/newsletter/templates/newsletter/index.html, part {index}."""

    ctx.add_transforms(
        "mozorg/newsletters.ftl",
        "mozorg/newsletters.ftl",
        transforms_from("""
newsletters-newsletter-subscriptions = {COPY(newsletters, "Newsletter Subscriptions",)}
""", newsletters=newsletters)
        )

    ctx.add_transforms(
        "mozorg/newsletters.ftl",
        "mozorg/newsletters.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("newsletters-mozilla-newsletter"),
                value=REPLACE(
                    newsletters,
                    "Mozilla Newsletter",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
newsletters-read-all-about-it-in-our-newsletter = {COPY(newsletters, "Read all about it in our <span>newsletter</span>",)}
""", newsletters=newsletters) + [
            FTL.Message(
                id=FTL.Identifier("newsletters-subscribe-to-updates-and-keep"),
                value=REPLACE(
                    newsletters,
                    "Subscribe to updates and keep current with Mozilla news. It’s the perfect way for us to keep in touch!",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ]
        )

    ctx.add_transforms(
        "mozorg/newsletters.ftl",
        "mozorg/newsletters.ftl",
        transforms_from("""
newsletters-newsletter-confirm = {COPY(newsletters, "Newsletter confirm",)}
newsletters-thanks-for-subscribing = {COPY(newsletters, "Thanks for Subscribing!",)}
newsletters-your-newsletter-subscription = {COPY(newsletters, "Your newsletter subscription has been confirmed.",)}
newsletters-please-be-sure-to-add-our = {COPY(newsletters, "Please be sure to add our sending address: mozilla@e.mozilla.org to your address book to ensure we always reach your inbox.",)}
newsletters-the-supplied-link-has-expired = {COPY(newsletters, "The supplied link has expired. You will receive a new one in the next newsletter.",)}
newsletters-something-is-amiss-with = {COPY(newsletters, "Something is amiss with our system, sorry! Please try again later.",)}
""", newsletters=newsletters)
        )

    ctx.add_transforms(
        "mozorg/newsletters.ftl",
        "mozorg/newsletters.ftl",
        transforms_from("""
newsletters-youre-awesome = {COPY(newsletters, "You’re awesome!",)}
newsletters-and-were-not-just-saying = {COPY(newsletters, "And we’re not just saying that because you trusted us with your email address.",)}
newsletters-please-be-sure-to-add-mozillaemozillaorg = {COPY(newsletters, "Please be sure to add mozilla@e.mozilla.org to your address book to ensure we always reach your inbox.",)}
""", newsletters=newsletters) + [
            FTL.Message(
                id=FTL.Identifier("newsletters-mozilla-touches-on-a-variety"),
                value=REPLACE(
                    newsletters,
                    "Mozilla touches on a variety of important issues.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
newsletters-open-your-inbox-and-your = {COPY(newsletters, "Open your inbox (and your heart) even more — take a look at other topics we cover.",)}
newsletters-manage-your-email-preferences = {COPY(newsletters, "Manage your Email Preferences",)}
newsletters-this-page-is-in-maintenance = {COPY(newsletters, "This page is in maintenance mode and is temporarily unavailable.",)}
newsletters-to-update-your-email-preferences = {COPY(newsletters, "To update your email preferences, please check back in a little while. Thanks!",)}
""", newsletters=newsletters) + [
            FTL.Message(
                id=FTL.Identifier("newsletters-we-love-sharing-updates"),
                value=REPLACE(
                    newsletters,
                    "We love sharing updates about all the awesome things happening at Mozilla.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
newsletters-set-your-preferences-below = {COPY(newsletters, "Set your preferences below to make sure you always receive the news you want.",)}
newsletters-your-email-address = {COPY(newsletters, "Your email address:",)}
newsletters-country-or-region = {COPY(newsletters, "Country or region:",)}
newsletters-country = {COPY(newsletters, "Country:",)}
newsletters-language = {COPY(newsletters, "Language:",)}
newsletters-not-all-subscriptions-are = {COPY(newsletters, "Not all subscriptions are supported in all the languages listed. Almost all are offered in English, German and French.",)}
newsletters-format = {COPY(newsletters, "Format:",)}
newsletters-text-subscribers-will-receive = {COPY(newsletters, "Text subscribers will receive an email twice a year to confirm continuation of the subscription. Those emails may include HTML.",)}
""", newsletters=newsletters) + [
            FTL.Message(
                id=FTL.Identifier("newsletters-many-of-our-communications"),
                value=REPLACE(
                    newsletters,
                    "Many of our communications are related to an account you’ve signed up for, such as Firefox Accounts, MDN Web Docs, or Add-on Developer. To manage one of your accounts or see a list of all the accounts visit our <a href=\"%s\">account management support page</a>.",
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("url"),
                        "Firefox Accounts": TERM_REFERENCE("brand-name-firefox-accounts"),
                        "MDN Web Docs": TERM_REFERENCE("brand-name-mdn-web-docs"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-to-get-access-to-the-whole"),
                value=REPLACE(
                    newsletters,
                    "To get access to the whole world of Firefox products, knowledge and services in one account, join us! Learn more about the benefits <a href=\"%s\">here</a>.",
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("url"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-there-are-many-ways-to"),
                value=REPLACE(
                    newsletters,
                    "There are many ways to engage with Mozilla and Firefox. If you didn’t find what you were looking for here, check out our <a href=\"%s\">community pages</a>.",
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("url"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-is-not-a-valid-newsletter"),
                value=REPLACE(
                    newsletters,
                    "%s is not a valid newsletter",
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("newsletter"),
                    }
                )
            ),

        ] + transforms_from("""
newsletters-subscribe = {COPY(newsletters, "Subscribe",)}
newsletters-remove-me-from-all-the = {COPY(newsletters, "Remove me from all the subscriptions on this page",)}
newsletters-save-preferences = {COPY(newsletters, "Save Preferences",)}
""", newsletters=newsletters)
        )

    ctx.add_transforms(
        "mozorg/newsletters.ftl",
        "mozorg/newsletters.ftl",
        transforms_from("""
newsletters-newsletter-email-recovery = {COPY(newsletters, "Newsletter email recovery",)}
newsletters-manage-your-newsletter = {COPY(newsletters, "Manage your <span>Newsletter Subscriptions</span>",)}
newsletters-enter-your-email-address = {COPY(newsletters, "Enter your email address and we’ll send you a link to your email preference center.",)}
newsletters-send-me-a-link = {COPY(newsletters, "Send me a link",)}
""", newsletters=newsletters)
        )

    ctx.add_transforms(
        "mozorg/newsletters.ftl",
        "mozorg/newsletters.ftl",
        transforms_from("""
newsletters-youve-been-unsubscribed = {COPY(newsletters, "You’ve been unsubscribed.",)}
newsletters-were-sorry-to-see-you-go = {COPY(newsletters, "We’re sorry to see you go.",)}
newsletters-would-you-mind-telling-us = {COPY(newsletters, "Would you mind telling us why you’re leaving?",)}
newsletters-other = {COPY(newsletters, "Other…",)}
newsletters-submit = {COPY(newsletters, "Submit",)}
newsletters-thanks-for-telling-us-why = {COPY(newsletters, "Thanks for telling us why you’re leaving.",)}
""", newsletters=newsletters) + [
            FTL.Message(
                id=FTL.Identifier("newsletters-while-here-why-not-check"),
                value=REPLACE(
                    newsletters,
                    "While here, why not check out some more Firefox awesomeness.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
newsletters-get-up-and-go = {COPY(newsletters, "Get up and go",)}
newsletters-its-your-web-anywhere-you = {COPY(newsletters, "It’s your Web anywhere you go.",)}
""", newsletters=newsletters) + [
            FTL.Message(
                id=FTL.Identifier("newsletters-get-firefox-for-mobile"),
                value=REPLACE(
                    newsletters,
                    "Get Firefox for mobile!",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
newsletters-added-extras = {COPY(newsletters, "Added extras",)}
""", newsletters=newsletters) + [
            FTL.Message(
                id=FTL.Identifier("newsletters-make-firefox-do-more-with"),
                value=REPLACE(
                    newsletters,
                    "Make Firefox do more with add-ons.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
newsletters-find-out-how = {COPY(newsletters, "Find out how!",)}
newsletters-about-us = {COPY(newsletters, "About us",)}
""", newsletters=newsletters) + [
            FTL.Message(
                id=FTL.Identifier("newsletters-whats-mozilla-all-about"),
                value=REPLACE(
                    newsletters,
                    "What’s Mozilla all about?",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
newsletters-were-glad-you-asked = {COPY(newsletters, "We’re glad you asked!",)}
""", newsletters=newsletters)
        )

    ctx.add_transforms(
        "mozorg/newsletters.ftl",
        "mozorg/newsletters.ftl",
        transforms_from("""
newsletters-love-the-web-so-do-we = {COPY(newsletters, "Love the web? So do we!",)}
""", newsletters=newsletters) + [
            FTL.Message(
                id=FTL.Identifier("newsletters-unlock-the-world-of-web"),
                value=REPLACE(
                    newsletters,
                    "Unlock the world of web development with our weekly Mozilla Developer Newsletter. Each edition brings you coding techniques and best practices, MDN updates, info about emerging technologies, developer tools tips, and more.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "MDN": TERM_REFERENCE("brand-name-mdn"),
                    }
                )
            ),
        ] + transforms_from("""
newsletters-join-thousands-of-developers = {COPY(newsletters, "Join thousands of developers like you who are learning the best of web development.",)}
""", newsletters=newsletters)
        )

    ctx.add_transforms(
        "mozorg/newsletters.ftl",
        "mozorg/newsletters.ftl",
        transforms_from("""
newsletters-put-more-fox-in-your-inbox = {COPY(newsletters, "Put more fox in your inbox.",)}
""", newsletters=newsletters) + [
            FTL.Message(
                id=FTL.Identifier("newsletters-see-where-the-web-can-take"),
                value=REPLACE(
                    newsletters,
                    "See where the Web can take you with monthly Firefox tips, tricks and Internet intel.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
        )

    ctx.add_transforms(
        "mozorg/newsletters.ftl",
        "mozorg/newsletters.ftl",
        transforms_from("""
newsletters-we-are-sorry-but-there = {COPY(newsletters, "We are sorry, but there was a problem with our system. Please try again later!",)}
newsletters-thanks-for-updating-your = {COPY(newsletters, "Thanks for updating your email preferences.",)}
newsletters-the-supplied-link-has-expired-long = {COPY(newsletters, "The supplied link has expired or is not valid. You will receive a new one in the next newsletter, or below you can request an email with the link.",)}
newsletters-success-an-email-has-been-sent = {COPY(newsletters, "Success! An email has been sent to you with your preference center link. Thanks!",)}
newsletters-this-is-not-a-valid-email = {COPY(newsletters, "This is not a valid email address. Please check the spelling.",)}
newsletters-about-standards = {COPY(newsletters, "About Standards",)}
newsletters-addon-development = {COPY(newsletters, "Addon Development",)}
newsletters-a-developers-guide = {COPY(newsletters, "A developer's guide to highlights of Web platform innovations, best practices, new documentation and more.",)}
newsletters-developer-newsletter = {COPY(newsletters, "Developer Newsletter",)}
newsletters-drumbeat-newsgroup = {COPY(newsletters, "Drumbeat Newsgroup",)}
newsletters-dont-miss-the-latest = {COPY(newsletters, "Don’t miss the latest announcements about our desktop browser.",)}
newsletters-periodic-email-updates = {COPY(newsletters, "Periodic email updates about our annual international film competition.",)}
newsletters-get-involved = {COPY(newsletters, "Get Involved",)}
newsletters-internet-health-report = {COPY(newsletters, "Internet Health Report",)}
newsletters-keep-up-with-our-annual = {COPY(newsletters, "Keep up with our annual compilation of research and stories on the issues of privacy &amp; security, openness, digital inclusion, decentralization, and web literacy.",)}
newsletters-get-all-the-knowledge = {COPY(newsletters, "Get all the knowledge you need to stay safer and smarter online.",)}
newsletters-knowledge-is-power = {COPY(newsletters, "Knowledge is Power",)}
newsletters-about-labs = {COPY(newsletters, "About Labs",)}
newsletters-maker-party = {COPY(newsletters, "Maker Party",)}
newsletters-desktop = {COPY(newsletters, "Desktop",)}
newsletters-regular-updates-to-keep = {COPY(newsletters, "Regular updates to keep you informed and active in our fight for a better internet.",)}
newsletters-special-accouncements-and-messages = {COPY(newsletters, "Special announcements and messages from the team dedicated to keeping the Web free and open.",)}
newsletters-updates-from-our-global = {COPY(newsletters, "Updates from our global community, helping people learn the most important skills of our age: the ability to read, write and participate in the digital world.",)}
newsletters-email-updates-from-vouched = {COPY(newsletters, "Email updates for vouched Mozillians on mozillians.org.",)}
newsletters-mozillians = {COPY(newsletters, "Mozillians",)}
newsletters-were-building-the-technology = {COPY(newsletters, "We're building the technology of the future. Come explore with us.",)}
newsletters-news-and-information = {COPY(newsletters, "News and information related to the health of the web.",)}
newsletters-shapre-of-the-web = {COPY(newsletters, "Shape of the Web",)}
newsletters-former-university-program = {COPY(newsletters, "Former University program from 2008-2011, now retired and relaunched as the Firefox Student Ambassadors program.")}
newsletters-student-reps = {COPY(newsletters, "Student Reps",)}
newsletters-add-your-voice = {COPY(newsletters, "Add your voice to petitions, events and initiatives that fight for the future of the web.",)}
newsletters-take-action = {COPY(newsletters, "Take Action for the Internet",)}
newsletters-new-product-testing = {COPY(newsletters, "New Product Testing",)}
newsletters-you-send-too-many-emails = {COPY(newsletters, "You send too many emails.",)}
newsletters-your-content-wasnt-relevant = {COPY(newsletters, "Your content wasn't relevant to me.",)}
newsletters-your-email-design = {COPY(newsletters, "Your email design was too hard to read.",)}
newsletters-i-didnt-sign-up = {COPY(newsletters, "I didn't sign up for this.",)}
""", newsletters=newsletters) + [
            FTL.Message(
                id=FTL.Identifier("newsletters-this-email-address-is-not"),
                value=REPLACE(
                    newsletters,
                    "This email address is not in our system. Please double check your address or <a href=\"%s\">subscribe to our newsletters.</a>",
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("url"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-join-mozillians-all-around"),
                value=REPLACE(
                    newsletters,
                    "Join Mozillians all around the world and learn about impactful opportunities to support Mozilla’s mission.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-mozilla-community"),
                value=REPLACE(
                    newsletters,
                    "Mozilla Community",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-a-monthly-newsletter-affiliates"),
                value=REPLACE(
                    newsletters,
                    "A monthly newsletter to keep you up to date with the Firefox Affiliates program.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-firefox-affiliates"),
                value=REPLACE(
                    newsletters,
                    "Firefox Affiliates",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-a-monthly-newsletter-ambassadors"),
                value=REPLACE(
                    newsletters,
                    "A monthly newsletter on how to get involved with Mozilla on your campus.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-firefox-student-ambassadors"),
                value=REPLACE(
                    newsletters,
                    "Firefox Student Ambassadors",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-aurora"),
                value=REPLACE(
                    newsletters,
                    "Aurora",
                    {
                        "Aurora": TERM_REFERENCE("brand-name-aurora"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-read-about-the-latest-features"),
                value=REPLACE(
                    newsletters,
                    "Read about the latest features for Firefox desktop and mobile before the final release.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-beta-news"),
                value=REPLACE(
                    newsletters,
                    "Beta News",
                    {
                        "Beta": TERM_REFERENCE("brand-name-beta"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-download-firefox-for-android"),
                value=REPLACE(
                    newsletters,
                    "Download Firefox for Android",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-get-firefox-for-android"),
                value=REPLACE(
                    newsletters,
                    "Get Firefox for Android",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-download-firefox-for-ios"),
                value=REPLACE(
                    newsletters,
                    "Download Firefox for iOS",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-download-firefox-for-mobile"),
                value=REPLACE(
                    newsletters,
                    "Download Firefox for Mobile",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-get-the-most-firefox-account"),
                value=REPLACE(
                    newsletters,
                    "Get the most out of your Firefox Account.",
                    {
                        "Firefox Account": TERM_REFERENCE("brand-name-firefox-account"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-firefox-accounts-tips"),
                value=REPLACE(
                    newsletters,
                    "Firefox Accounts Tips",
                    {
                        "Firefox Accounts": TERM_REFERENCE("brand-name-firefox-accounts"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-firefox-for-desktop"),
                value=REPLACE(
                    newsletters,
                    "Firefox for desktop",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-firefox-flicks"),
                value=REPLACE(
                    newsletters,
                    "Firefox Flicks",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-be-the-first-to-know"),
                value=REPLACE(
                    newsletters,
                    "Be the first to know when Firefox is available for iOS devices.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-firefox-ios"),
                value=REPLACE(
                    newsletters,
                    "Firefox iOS",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-dont-miss-important-news"),
                value=REPLACE(
                    newsletters,
                    "Don’t miss important news and updates about your Firefox OS device.",
                    {
                        "Firefox OS": TERM_REFERENCE("brand-name-firefox-os"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-firefox-os-smartphone-owner"),
                value=REPLACE(
                    newsletters,
                    "Firefox OS smartphone owner?",
                    {
                        "Firefox OS": TERM_REFERENCE("brand-name-firefox-os"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-a-monthly-newsletter-and-special"),
                value=REPLACE(
                    newsletters,
                    "A monthly newsletter and special announcements on how to get the most from your Firefox OS device, including the latest features and coolest Firefox Marketplace apps.",
                    {
                        "Firefox OS": TERM_REFERENCE("brand-name-firefox-os"),
                        "Firefox Marketplace": TERM_REFERENCE("brand-name-firefox-marketplace"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-firefox-os-and-you"),
                value=REPLACE(
                    newsletters,
                    "Firefox OS + You",
                    {
                        "Firefox OS": TERM_REFERENCE("brand-name-firefox-os"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-get-a-weekly-tip"),
                value=REPLACE(
                    newsletters,
                    "Get a weekly tip on how to super-charge your Firefox experience.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-firefox-weekly-tips"),
                value=REPLACE(
                    newsletters,
                    "Firefox Weekly Tips",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-join-mozilla"),
                value=REPLACE(
                    newsletters,
                    "Join Mozilla",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-mozillas-largest-celebration"),
                value=REPLACE(
                    newsletters,
                    "Mozilla's largest celebration of making and learning on the web.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-discover-the-latest"),
                value=REPLACE(
                    newsletters,
                    "Discover the latest, coolest HTML5 apps on Firefox OS.",
                    {
                        "Firefox OS": TERM_REFERENCE("brand-name-firefox-os"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-firefox-os"),
                value=REPLACE(
                    newsletters,
                    "Firefox OS",
                    {
                        "Firefox OS": TERM_REFERENCE("brand-name-firefox-os"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-android"),
                value=REPLACE(
                    newsletters,
                    "Android",
                    {
                        "Android": TERM_REFERENCE("brand-name-android"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-keep-up-with-releases"),
                value=REPLACE(
                    newsletters,
                    "Keep up with releases and news about Firefox for Android.",
                    {
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-firefox-for-android"),
                value=REPLACE(
                    newsletters,
                    "Firefox for Android",
                    {
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-get-how-tos"),
                value=REPLACE(
                    newsletters,
                    "Get how-tos, advice and news to make your Firefox experience work best for you.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-firefox-news"),
                value=REPLACE(
                    newsletters,
                    "Firefox News",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-special-announcements-about-mozilla"),
                value=REPLACE(
                    newsletters,
                    "Special announcements about Mozilla's annual, hands-on festival dedicated to forging the future of the open Web.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-mozilla-festival"),
                value=REPLACE(
                    newsletters,
                    "Mozilla Festival",
                    {
                        "Mozilla Festival": TERM_REFERENCE("brand-name-mozilla-festival"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-mozilla-news"),
                value=REPLACE(
                    newsletters,
                    "Mozilla News",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-mozilla"),
                value=REPLACE(
                    newsletters,
                    "Mozilla",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-mozilla-learning-network"),
                value=REPLACE(
                    newsletters,
                    "Mozilla Learning Network",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-mozilla-labs"),
                value=REPLACE(
                    newsletters,
                    "Mozilla Labs",
                    {
                        "Mozilla Labs": TERM_REFERENCE("brand-name-mozilla-labs"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-firefox-os-news"),
                value=REPLACE(
                    newsletters,
                    "Firefox OS news, tips, launch information and where to buy.",
                    {
                        "Firefox OS": TERM_REFERENCE("brand-name-firefox-os"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-help-us-make-a-better"),
                value=REPLACE(
                    newsletters,
                    "Help us make a better Firefox for you by test-driving our latest products and features.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-special-announcements-helping-you"),
                value=REPLACE(
                    newsletters,
                    "Special announcements helping you get the most out of Webmaker.",
                    {
                        "Webmaker": TERM_REFERENCE("brand-name-webmaker"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-webmaker"),
                value=REPLACE(
                    newsletters,
                    "Webmaker",
                    {
                        "Webmaker": TERM_REFERENCE("brand-name-webmaker"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("newsletters-im-keeping-in-touch"),
                value=REPLACE(
                    newsletters,
                    "I'm keeping in touch with Mozilla on Facebook and Twitter instead.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Facebook": TERM_REFERENCE("brand-name-facebook"),
                        "Twitter": TERM_REFERENCE("brand-name-twitter"),
                    }
                )
            ),

        ]
        )

    ctx.add_transforms(
        "mozorg/newsletters.ftl",
        "mozorg/newsletters.ftl",
        transforms_from("""
newsletters-sign-up-read-up-stay-informed = {COPY(newsletters, "Sign up, read up,<br> stay informed.",)}
newsletters-sign-up-read-up-make-a-difference = {COPY(newsletters, "Sign up. Read up.<br> Make a difference.",)}
newsletters-get-smart-on-the-issues = {COPY(newsletters, "Get smart on the issues affecting your life online.",)}
""", newsletters=newsletters) + [
            FTL.Message(
                id=FTL.Identifier("newsletters-get-the-mozilla-newsletter"),
                value=REPLACE(
                    newsletters,
                    "Get the Mozilla newsletter to stay informed about issues challenging the health of the Internet and to discover how you can get involved.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ]
        )
