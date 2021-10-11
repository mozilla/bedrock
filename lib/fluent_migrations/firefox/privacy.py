from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

privacy_hub = "firefox/privacy-hub.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/privacy/base.html, part {index}."""

    ctx.add_transforms(
        "firefox/privacy-hub.ftl",
        "firefox/privacy-hub.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-firefox-privacy-promise"),
                value=REPLACE(
                    privacy_hub,
                    "Firefox Privacy Promise",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-firefox-takes-less-data-keeps"),
                value=REPLACE(
                    privacy_hub,
                    "Firefox takes less data, keeps it safe, and with no secrets.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-firefox-products-are-designed"),
                value=REPLACE(
                    privacy_hub,
                    "Firefox products are designed to protect your <strong>privacy</strong>",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-privacy-privacy = {COPY(privacy_hub, "Privacy",)}
firefox-privacy-our-promise = {COPY(privacy_hub, "Our Promise",)}
firefox-privacy-our-products = {COPY(privacy_hub, "Our Products",)}
firefox-privacy-hub-you-should-be-able-to-decide = {COPY(privacy_hub, "You should be able to decide who sees your personal info. Not just among your friends, but with every advertiser and company on the internet — including us.",)}
firefox-privacy-hub-thats-why-everything-we-make = {COPY(privacy_hub, "That’s why everything we make and do honors our Personal Data Promise",)}
firefox-privacy-hub-take-less = {COPY(privacy_hub, "Take Less",)}
firefox-privacy-hub-we-make-a-point-of-knowing = {COPY(privacy_hub, "We make a point of knowing less about you",)}
firefox-privacy-hub-all-tech-companies-collect = {COPY(privacy_hub, "All tech companies collect data to improve their products. But it doesn’t need to include so much of your personal info. The only data we want is the data that serves you in the end. We ask ourselves: do we actually need this? What do we need it for? And when can we delete it?",)}
firefox-privacy-hub-keep-it-safe = {COPY(privacy_hub, "Keep it safe",)}
firefox-privacy-hub-we-do-the-hard-work-to-protect = {COPY(privacy_hub, "We do the hard work to protect your personal info",)}
firefox-privacy-hub-data-security-is-complicated = {COPY(privacy_hub, "Data security is complicated — or at least it should be. Which is why we take the extra steps to classify the data we have, maintain rules for how we store and protect each type, and never stop iterating on our processes. We prioritize your privacy. We invest in it. We’re committed to it. We even teach other companies how to do it.",)}
firefox-privacy-hub-no-secrets = {COPY(privacy_hub, "No secrets",)}
firefox-privacy-hub-youll-always-know-where-you = {COPY(privacy_hub, "You’ll always know where you stand with us",)}
""",
            privacy_hub=privacy_hub,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-theres-no-hidden-agenda-here"),
                value=REPLACE(
                    privacy_hub,
                    'There’s no hidden agenda here. Our business doesn’t depend on secretly abusing your trust. Our <a href="%(privacy)s">Privacy Notice</a> is actually readable. Anyone in the world can attend our <a href="%(meetings)s">weekly company meetings</a>. If you want to dig into every datapoint we collect, our code is open. And so are we.',
                    {
                        "%%": "%",
                        "%(privacy)s": VARIABLE_REFERENCE("privacy"),
                        "%(meetings)s": VARIABLE_REFERENCE("meetings"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-why-trust-firefox"),
                value=REPLACE(
                    privacy_hub,
                    "Why trust Firefox?",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-because-we-put-people-first"),
                value=REPLACE(
                    privacy_hub,
                    'Because we put people first. In fact, we’re backed by a <a href="%(foundation)s">non-profit</a>. From day one, it’s been our mission to protect the internet and everyone on it',
                    {
                        "%%": "%",
                        "%(foundation)s": VARIABLE_REFERENCE("foundation"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-privacy-hub-learn-more-about-our-mission = {COPY(privacy_hub, "Learn more about our mission",)}
firefox-privacy-hub-your-privacy-by-the-product = {COPY(privacy_hub, "Your privacy, by the product",)}
""",
            privacy_hub=privacy_hub,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-firefox-products-work-differently"),
                value=REPLACE(
                    privacy_hub,
                    "Firefox products work differently — because they’re designed to protect your privacy first.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-privacy-hub-learn-about-our-products = {COPY(privacy_hub, "Learn about our products",)}
""",
            privacy_hub=privacy_hub,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-firefox-privacy-by-the"),
                value=REPLACE(
                    privacy_hub,
                    "Firefox privacy, by the product",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-firefox-protects-your-privacy"),
                value=REPLACE(
                    privacy_hub,
                    "Firefox protects your privacy in every product.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-firefox-protects-your-privacy-strong"),
                value=REPLACE(
                    privacy_hub,
                    "Firefox <strong>protects</strong> your privacy in every product",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-privacy-hub-firefox-browser = { -brand-name-firefox-browser }
firefox-privacy-hub-2000-trackers-blocked-automatically = {COPY(privacy_hub, "2,000+ trackers blocked — automatically",)}
""",
            privacy_hub=privacy_hub,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-tracking-has-become-an"),
                value=REPLACE(
                    privacy_hub,
                    "Tracking has become an epidemic online: companies follow every move, click and purchase, collecting data to predict and influence what you’ll do next. We think that’s a gross invasion of your privacy. That’s why Firefox mobile and desktop browsers have Enhanced Tracking Protection on by default.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-if-you-want-to-see-what"),
                value=REPLACE(
                    privacy_hub,
                    "If you want to see what Firefox is blocking for you, visit this page on your Firefox desktop browser.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-see-what-firefox-has-blocked"),
                value=REPLACE(
                    privacy_hub,
                    "See what Firefox has blocked for you",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-privacy-hub-get-enhanced-tracking-protection = {COPY(privacy_hub, "Get Enhanced Tracking Protection",)}
""",
            privacy_hub=privacy_hub,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-download-the-firefox-browser"),
                value=REPLACE(
                    privacy_hub,
                    "Download the Firefox browser",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-update-your-firefox-browser"),
                value=REPLACE(
                    privacy_hub,
                    "Update your Firefox browser",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-privacy-hub-invisible-to-the-top-trackers = {COPY(privacy_hub, "Invisible to the top trackers",)}
firefox-privacy-hub-meet-four-of-the-most-common = {COPY(privacy_hub, "Meet four of the most common categories of trackers — who won’t meet you.",)}
firefox-privacy-hub-always-in-your-control = {COPY(privacy_hub, "Always in your control",)}
firefox-privacy-hub-want-to-customize-what = {COPY(privacy_hub, "Want to customize what gets blocked? Your settings are only one click away.",)}
firefox-privacy-hub-protection-beyond-tracking = {COPY(privacy_hub, "Protection beyond tracking",)}
""",
            privacy_hub=privacy_hub,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-if-you-have-a-firefox-account"),
                value=REPLACE(
                    privacy_hub,
                    "If you have a Firefox account, you can also see how we’re helping you protect your personal info and passwords.",
                    {
                        "Firefox account": TERM_REFERENCE("brand-name-firefox-account"),
                        "Firefox Account": TERM_REFERENCE("brand-name-firefox-account"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-more-than-s-trackers-blocked"),
                value=REPLACE(
                    privacy_hub,
                    "More than %s trackers blocked each day for Firefox users worldwide",
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("trackers"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-privacy-hub-firefox-monitor = { -brand-name-firefox-monitor }
""",
            privacy_hub=privacy_hub,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-when-you-enter-your-email"),
                value=REPLACE(
                    privacy_hub,
                    "When you enter your email address in Firefox Monitor, we forget it immediately after we’ve checked for a match in known data breaches — unless you authorize us to continue monitoring new breaches for your personal information.",
                    {
                        "Firefox Monitor": TERM_REFERENCE("brand-name-firefox-monitor"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-privacy-hub-check-for-breaches = {COPY(privacy_hub, "Check for breaches",)}
firefox-privacy-hub-firefox-lockwise = { -brand-name-firefox-lockwise }
""",
            privacy_hub=privacy_hub,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-the-passwords-and-credentials"),
                value=REPLACE(
                    privacy_hub,
                    "The passwords and credentials you save in Firefox Lockwise are encrypted on all your devices, so not even we can see them.",
                    {
                        "Firefox Lockwise": TERM_REFERENCE("brand-name-firefox-lockwise"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-learn-more-about-lockwise"),
                value=REPLACE(
                    privacy_hub,
                    "Learn more about Lockwise",
                    {
                        "Lockwise": TERM_REFERENCE("brand-name-lockwise"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-privacy-hub-firefox-send = { -brand-name-firefox-send }
""",
            privacy_hub=privacy_hub,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-we-cant-see-the-names-or"),
                value=REPLACE(
                    privacy_hub,
                    "We can’t see the names or content of the large files you share through Firefox Send because they’re encrypted end-to-end — you choose who sees what you send, and you can even set an expiration date and password.",
                    {
                        "Firefox Send": TERM_REFERENCE("brand-name-firefox-send"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-privacy-hub-send-a-file = {COPY(privacy_hub, "Send a file",)}
firefox-privacy-hub-pocket = { -brand-name-pocket }
""",
            privacy_hub=privacy_hub,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-pocket-recommends-high"),
                value=REPLACE(
                    privacy_hub,
                    "Pocket recommends high-quality, human-curated articles without collecting your browsing history or sharing your personal information with advertisers.",
                    {
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-get-pocket"),
                value=REPLACE(
                    privacy_hub,
                    "Get Pocket",
                    {
                        "Pocket": TERM_REFERENCE("brand-name-pocket"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-your-firefox-account"),
                value=REPLACE(
                    privacy_hub,
                    "Your Firefox account",
                    {
                        "Firefox account": TERM_REFERENCE("brand-name-firefox-account"),
                        "Firefox Account": TERM_REFERENCE("brand-name-firefox-account"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-all-the-information-synced"),
                value=REPLACE(
                    privacy_hub,
                    "All the information synced through your Firefox account — from browser history to passwords — is encrypted. And your account password is the only key.",
                    {
                        "Firefox account": TERM_REFERENCE("brand-name-firefox-account"),
                        "Firefox Account": TERM_REFERENCE("brand-name-firefox-account"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-take-your-privacy-and-bookmarks"),
                value=REPLACE(
                    privacy_hub,
                    "Take your privacy and bookmarks everywhere with a Firefox account.",
                    {
                        "Firefox account": TERM_REFERENCE("brand-name-firefox-account"),
                        "Firefox Account": TERM_REFERENCE("brand-name-firefox-account"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-already-have-an-account"),
                value=REPLACE(
                    privacy_hub,
                    'Already have an account? <a %(sign_in)s class="%(class_name)s">Sign In</a> or <a href="%(learn_more)s">learn more</a> about joining Firefox.',
                    {
                        "%%": "%",
                        "%(sign_in)s": VARIABLE_REFERENCE("sign_in"),
                        "%(class_name)s": VARIABLE_REFERENCE("class_name"),
                        "%(learn_more)s": VARIABLE_REFERENCE("learn_more"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-privacy-hub-read-the-privacy-notice-for"),
                value=REPLACE(
                    privacy_hub,
                    'Read the <a href="%s">Privacy Notice</a> for our products',
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("url"),
                    },
                ),
            ),
        ],
    )
