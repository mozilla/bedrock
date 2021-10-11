from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

navigation = "navigation.lang"
main = "main.lang"


def migrate(ctx):
    """Migrate bedrock/base/templates/includes/protocol/navigation/navigation.html, part {index}."""

    ctx.add_transforms(
        "navigation.ftl",
        "navigation.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("navigation-download-firefox"),
                value=REPLACE("navigation.lang", "Download Firefox", {"Firefox": TERM_REFERENCE("brand-name-firefox")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-get-a-firefox-account"),
                value=REPLACE("navigation.lang", "Get a Firefox Account", {"Firefox Account": TERM_REFERENCE("brand-name-firefox-account")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-firefox-browser-for-desktop"),
                value=REPLACE("navigation.lang", "Firefox Browser for Desktop", {"Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-get-the-browser-that-respects"),
                value=REPLACE(
                    "navigation.lang",
                    "Get the browser that respects your privacy automatically. On Windows, macOS or Linux.",
                    {
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "macOS": TERM_REFERENCE("brand-name-mac"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-firefox-browser-for-mobile"),
                value=REPLACE("navigation.lang", "Firefox Browser for Mobile", {"Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-take-speed-privacy-and"),
                value=REPLACE(
                    "navigation.lang",
                    "Take speed, privacy and peace of mind with you. On Android and iOS.",
                    {"Android": TERM_REFERENCE("brand-name-android"), "iOS": TERM_REFERENCE("brand-name-ios")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-download-for-ios"),
                value=REPLACE("navigation.lang", "Download for iOS", {"iOS": TERM_REFERENCE("brand-name-ios")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-download-for-android"),
                value=REPLACE("navigation.lang", "Download for Android", {"Android": TERM_REFERENCE("brand-name-android")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-ios-support"),
                value=REPLACE("navigation.lang", "iOS Support", {"iOS": TERM_REFERENCE("brand-name-ios")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-android-support"),
                value=REPLACE("navigation.lang", "Android Support", {"Android": TERM_REFERENCE("brand-name-android")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-firefox-browser-for-enterprise"),
                value=REPLACE("navigation.lang", "Firefox Browser for Enterprise", {"Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-strap-on-your-goggles"),
                value=REPLACE(
                    "navigation.lang",
                    "Strap on your goggles and step into the immersive web with Firefox Browser for VR.",
                    {"Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-firefox-for-fire-tv"),
                value=REPLACE(
                    "navigation.lang",
                    "Firefox for Fire TV",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox"), "Fire TV": TERM_REFERENCE("brand-name-fire-tv")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-watch-videos-and-browse"),
                value=REPLACE(
                    "navigation.lang",
                    "Watch videos and browse the internet on your Amazon Fire TV.",
                    {"Amazon": TERM_REFERENCE("brand-name-amazon"), "Fire TV": TERM_REFERENCE("brand-name-fire-tv")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-firefox-browsers-put"),
                value=REPLACE(
                    "navigation.lang", "Firefox browsers put your privacy first — and always have.", {"Firefox": TERM_REFERENCE("brand-name-firefox")}
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-take-the-passwords-youve"),
                value=REPLACE(
                    "navigation.lang",
                    "Take the passwords you’ve saved in Firefox with you everywhere.",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-firefox-is-a-whole-family"),
                value=REPLACE(
                    "navigation.lang",
                    "Firefox is a whole family of products designed to keep you safer and smarter online.",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-join-firefox"),
                value=REPLACE("navigation.lang", "Join Firefox", {"Firefox": TERM_REFERENCE("brand-name-firefox")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-access-all-of-firefox"),
                value=REPLACE(
                    "navigation.lang",
                    "Access all of Firefox with a single login — and get more from every product when you do.",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-meet-the-firefox-family"),
                value=REPLACE("navigation.lang", "Meet the Firefox Family", {"Firefox": TERM_REFERENCE("brand-name-firefox")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-firefox-blog"),
                value=REPLACE("navigation.lang", "Firefox Blog", {"Firefox": TERM_REFERENCE("brand-name-firefox")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-read-about-new-firefox"),
                value=REPLACE(
                    "navigation.lang",
                    "Read about new Firefox features, and get tips for staying safer online.",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-the-non-profit-behind"),
                value=REPLACE(
                    "navigation.lang",
                    "The non-profit behind Firefox is fighting for a healthy internet for all.",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-learn-how-firefox-treats"),
                value=REPLACE(
                    "navigation.lang", "Learn how Firefox treats your data with respect.", {"Firefox": TERM_REFERENCE("brand-name-firefox")}
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-mozilla-careers"),
                value=REPLACE("navigation.lang", "Mozilla Careers", {"Mozilla": TERM_REFERENCE("brand-name-mozilla")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-approach-your-career"),
                value=REPLACE(
                    "navigation.lang",
                    "Approach your career with a sense of purpose. Find worthy work at Mozilla.",
                    {"Mozilla": TERM_REFERENCE("brand-name-mozilla")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-close-firefox-menu"),
                value=REPLACE("navigation.lang", "Close Firefox menu", {"Firefox": TERM_REFERENCE("brand-name-firefox")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-get-the-browser-that-gives"),
                value=REPLACE(
                    "navigation.lang",
                    "Get the browser that gives more power to you on Windows, macOS or Linux.",
                    {
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "macOS": TERM_REFERENCE("brand-name-mac"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-take-firefox-and-firefox"),
                value=REPLACE(
                    "navigation.lang",
                    "Take Firefox and Firefox Focus with you. For Android and iOS.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Firefox Focus": TERM_REFERENCE("brand-name-firefox-focus"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-get-firefox"),
                value=REPLACE("navigation.lang", "Get Firefox", {"Firefox": TERM_REFERENCE("brand-name-firefox")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-get-firefox-focus"),
                value=REPLACE("navigation.lang", "Get Firefox Focus", {"Firefox Focus": TERM_REFERENCE("brand-name-firefox-focus")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-android-extensions"),
                value=REPLACE("navigation.lang", "Android Extensions", {"Android": TERM_REFERENCE("brand-name-android")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-your-firefox-account"),
                value=REPLACE("navigation.lang", "Your Firefox Account", {"Firefox Account": TERM_REFERENCE("brand-name-firefox-account")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-make-the-most-of-your"),
                value=REPLACE(
                    "navigation.lang",
                    "Make the most of your Firefox experience, across every device.",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-learn-how-to-customize"),
                value=REPLACE("navigation.lang", "Learn how to customize the way Firefox works.", {"Firefox": TERM_REFERENCE("brand-name-firefox")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-experience-augmented"),
                value=REPLACE(
                    "navigation.lang", "Experience augmented and virtual reality with Firefox.", {"Firefox": TERM_REFERENCE("brand-name-firefox")}
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-meet-people-in-experimental"),
                value=REPLACE(
                    "navigation.lang",
                    "Meet people in experimental Mixed Reality chatrooms with Firefox.",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-mozilla-webvr"),
                value=REPLACE("navigation.lang", "Mozilla WebVR", {"Mozilla": TERM_REFERENCE("brand-name-mozilla")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-mozilla-brings-firefox"),
                value=REPLACE(
                    "navigation.lang",
                    "Mozilla brings Firefox to augmented and virtual reality.",
                    {"Mozilla": TERM_REFERENCE("brand-name-mozilla"), "Firefox": TERM_REFERENCE("brand-name-firefox")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-firefox-built-just-for"),
                value=REPLACE("navigation.lang", "Firefox, built just for developers.", {"Firefox": TERM_REFERENCE("brand-name-firefox")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-preview-the-latest-build"),
                value=REPLACE(
                    "navigation.lang",
                    "Preview the latest build of Firefox and help us make it the best.",
                    {"Firefox": TERM_REFERENCE("brand-name-firefox")},
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-firefox-playground"),
                value=REPLACE("navigation.lang", "Firefox Playground", {"Firefox": TERM_REFERENCE("brand-name-firefox")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-mozilla-open-source-support"),
                value=REPLACE("navigation.lang", "Mozilla Open Source Support (MOSS)", {"Mozilla": TERM_REFERENCE("brand-name-mozilla")}),
            ),
            FTL.Message(
                id=FTL.Identifier("navigation-mozilla-manifesto"),
                value=REPLACE("navigation.lang", "Mozilla Manifesto", {"Mozilla": TERM_REFERENCE("brand-name-mozilla")}),
            ),
        ],
    )

    ctx.add_transforms(
        "navigation.ftl",
        "navigation.ftl",
        transforms_from(
            """
navigation-menu = {COPY(navigation, "Menu",)}
navigation-check-out-the-benefits = {COPY(navigation, "Check out the Benefits",)}
navigation-browsers = {COPY(navigation, "Browsers",)}
navigation-close-browsers-menu = {COPY(navigation, "Close Browsers menu",)}
navigation-download = {COPY(navigation, "Download",)}
navigation-extensions = {COPY(navigation, "Extensions",)}
navigation-support = {COPY(navigation, "Support",)}
navigation-privacy = {COPY(navigation, "Privacy",)}
navigation-get-unmatched-data-protection = {COPY(navigation, "Get unmatched data protection on the release cadence that suits your organization.",)}
navigation-made-with-respect = {COPY(navigation, "Made with respect",)}
navigation-close-products-menu = {COPY(navigation, "Close Products menu",)}
navigation-see-if-your-personal = {COPY(navigation, "See if your personal info has been leaked online, and sign up for future breach alerts.",)}
navigation-check-for-breaches = {COPY(navigation, "Check for Breaches",)}
navigation-see-breaches = {COPY(navigation, "See Breaches",)}
navigation-security-tips = {COPY(navigation, "Security Tips",)}
navigation-share-large-files-safely = {COPY(navigation, "Share large files safely, with links that ‘self-destruct’.",)}
navigation-save-quality-content = {COPY(navigation, "Save quality content from anywhere. Fuel your mind everywhere.",)}
navigation-sign-up = {COPY(navigation, "Sign Up",)}
navigation-connected-and-protected = {COPY(navigation, "Connected and protected",)}
navigation-join = {COPY(navigation, "Join",)}
navigation-close-join-menu = {COPY(navigation, "Close Join menu",)}
navigation-sign-in = {COPY(navigation, "Sign In",)}
navigation-benefits = {COPY(navigation, "Benefits",)}
navigation-protect-your-life-online = {COPY(navigation, "Protect your life online with a whole family of privacy-first products.",)}
navigation-about = {COPY(navigation, "About",)}
navigation-close-about-menu = {COPY(navigation, "Close About menu",)}
navigation-meet-the-technology-company = {COPY(navigation, "Meet the technology company that puts people before profit.",)}
navigation-new-features = {COPY(navigation, "New Features",)}
navigation-save-content-absorb-knowledge = {COPY(navigation, "Save content. Absorb knowledge.",)}
navigation-same-speed-and-safety = {COPY(navigation, "Same speed and safety you trust, designed just for business.",)}
navigation-add-ons = {COPY(navigation, "Add-ons",)}
navigation-projects = {COPY(navigation, "Projects",)}
navigation-close-projects-menu = {COPY(navigation, "Close Projects menu",)}
navigation-donate-your-voice-to = {COPY(navigation, "Donate your voice to help make voice recognition open to everyone.",)}
navigation-web-of-things-iot = {COPY(navigation, "Web of Things (IoT)",)}
navigation-make-devices-connected = {COPY(navigation, "Make devices connected to the internet safe, secure and interoperable.",)}
navigation-developers = {COPY(navigation, "Developers",)}
navigation-close-developers-menu = {COPY(navigation, "Close Developers menu",)}
navigation-test-soon-to-be-released = {COPY(navigation, "Test soon-to-be-released features in our most stable pre-release build.",)}
navigation-developer-innovations = {COPY(navigation, "Developer Innovations",)}
navigation-projects-that-help-keep = {COPY(navigation, "Projects that help keep the internet open and accessible for all.",)}
navigation-mixed-reality = {COPY(navigation, "Mixed Reality",)}
navigation-resources = {COPY(navigation, "Resources",)}
navigation-resources-for-developers = {COPY(navigation, "Resources for developers, by developers.",)}
navigation-developer-blog = {COPY(navigation, "Developer Blog",)}
navigation-build-test-scale-and = {COPY(navigation, "Build, test, scale and more with the only browser built just for developers.",)}
navigation-leadership = {COPY(navigation, "Leadership",)}
navigation-mission = {COPY(navigation, "Mission",)}
navigation-press-center = {COPY(navigation, "Press Center",)}
navigation-contact = {COPY(navigation, "Contact",)}
navigation-careers = {COPY(navigation, "Careers",)}
navigation-work-for-a-mission-driven = {COPY(navigation, "Work for a mission-driven organization that builds purpose-driven products.",)}
navigation-get-involved = {COPY(navigation, "Get involved",)}
navigation-join-the-fight-for-a = {COPY(navigation, "Join the fight for a healthy internet.",)}
navigation-events = {COPY(navigation, "Events",)}
navigation-donate = {COPY(navigation, "Donate",)}
navigation-your-right-to-security = {COPY(navigation, "Your right to security and privacy on the internet is fundamental – never optional.",)}

navigation-release-notes = {COPY(main, "Release Notes",)}
navigation-features = {COPY(main, "Features",)}
navigation-products = {COPY(main, "Products",)}

navigation-mozilla = { -brand-name-mozilla }
navigation-mozilla-foundation = { -brand-name-mozilla-foundation }
navigation-mozilla-corporation = { -brand-name-mozilla-corporation }
navigation-firefox-developer-edition = { -brand-name-firefox-developer-edition }
navigation-firefox-beta = { -brand-name-firefox-beta }
navigation-firefox-nightly = { -brand-name-firefox-nightly }
navigation-firefox-reality = { -brand-name-firefox-reality }
navigation-firefox-lockwise = { -brand-name-firefox-lockwise }
navigation-firefox-monitor = { -brand-name-firefox-monitor }
navigation-firefox-send = { -brand-name-firefox-send }
navigation-pocket = { -brand-name-pocket }
navigation-common-voice = { -brand-name-common-voice }
navigation-hubs = { -brand-name-hubs }
navigation-rust = { -brand-name-rust }
navigation-web-assembly = { -brand-name-web-assembly }
navigation-mdn-web-docs = { -brand-name-mdn-web-docs }
""",
            navigation=navigation,
            main=main,
        ),
    )
