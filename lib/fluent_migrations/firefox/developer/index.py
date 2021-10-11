from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

index = "firefox/developer/index.lang"
developer_quantum = "firefox/products/developer-quantum.lang"
shared = "firefox/shared.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/developer/index.html, part {index}."""

    ctx.add_transforms(
        "firefox/developer.ftl",
        "firefox/developer.ftl",
        transforms_from(
            """
firefox-developer-page-title = { -brand-name-firefox-developer-edition }
""",
            developer_quantum=developer_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-developer-firefox-developer-edition-desc"),
                value=REPLACE(
                    developer_quantum,
                    "Firefox Developer Edition is the blazing fast browser that offers cutting edge developer tools and latest features like CSS Grid support and framework debugging",
                    {
                        "Firefox Developer Edition": TERM_REFERENCE("brand-name-firefox-developer-edition"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-developer-firefox-browser = { -brand-name-firefox-browser } { -brand-name-developer-edition }
firefox-developer-welcome-to-your-new-favorite = {COPY(developer_quantum, "Welcome to your new favorite browser. Get the latest features, fast performance, and the development tools you need to build for the open web.",)}
firefox-developer-speak-up = {COPY(developer_quantum, "Speak up",)}
firefox-developer-feedback-makes-us = {COPY(developer_quantum, "Feedback makes us better. Tell us how we can improve the browser and Developer tools.",)}
firefox-developer-join-the-convo = {COPY(developer_quantum, "Join the conversation",)}
firefox-developer-get-involved = {COPY(developer_quantum, "Get involved",)}
firefox-developer-help-build-the-last = {COPY(developer_quantum, "Help build the last independent browser. Write code, fix bugs, make add-ons, and more.",)}
firefox-developer-start-now = {COPY(developer_quantum, "Start now",)}
firefox-developer-design-code-test = {COPY(developer_quantum, "Design. Code. Test. Refine.",)}
""",
            developer_quantum=developer_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-developer-build-and-perfect"),
                value=REPLACE(
                    developer_quantum,
                    "Build and Perfect your sites<br> with Firefox DevTools",
                    {
                        "Firefox DevTools": TERM_REFERENCE("brand-name-firefox-devtools"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-developer-inspector = {COPY(developer_quantum, "Inspector",)}
firefox-developer-inspect-and-refine = {COPY(developer_quantum, "Inspect and refine code to build pixel-perfect layouts.",)}
firefox-developer-learn-about-page-inspector = {COPY(developer_quantum, "Learn more about Page Inspector",)}
firefox-developer-console = {COPY(developer_quantum, "Console",)}
firefox-developer-track-css = {COPY(developer_quantum, "Track CSS, JavaScript, security and network issues.",)}
firefox-developer-learn-about-web-console = {COPY(developer_quantum, "Learn more about Web Console",)}
firefox-developer-debugger = {COPY(developer_quantum, "Debugger",)}
firefox-developer-powerful-javascript = {COPY(developer_quantum, "Powerful JavaScript debugger with support for your framework.",)}
firefox-developer-learn-more-about-debugger = {COPY(developer_quantum, "Learn more about JavaScript Debugger",)}
firefox-developer-network = {COPY(developer_quantum, "Network",)}
firefox-developer-monitor-network-requests = {COPY(developer_quantum, "Monitor network requests that can slow or block your site.",)}
firefox-developer-learn-more-about-newtork-monitor = {COPY(developer_quantum, "Learn more about Network Monitor",)}
firefox-developer-storage-panel = {COPY(developer_quantum, "Storage panel",)}
firefox-developer-add-modify-remove = {COPY(developer_quantum, "Add, modify and remove cache, cookies, databases and session data.",)}
firefox-developer-learn-more-about-storage = {COPY(developer_quantum, "Learn more about Storage Panel",)}
firefox-developer-responsive-design-mode = {COPY(developer_quantum, "Responsive Design Mode",)}
firefox-developer-test-sites-emulated = {COPY(developer_quantum, "Test sites on emulated devices in your browser.",)}
firefox-developer-learn-more-about-responsive = {COPY(developer_quantum, "Learn more about Responsive Design View",)}
firefox-developer-visual-editing = {COPY(developer_quantum, "Visual Editing",)}
firefox-developer-fine-tuning-animations = {COPY(developer_quantum, "Fine-tune animations, alignment and padding.",)}
firefox-developer-learn-more-about-visual-editing = {COPY(developer_quantum, "Learn more about Visual Editing",)}
firefox-developer-performance = {COPY(developer_quantum, "Performance",)}
firefox-developer-unblock-bottlenecks = {COPY(developer_quantum, "Unblock bottlenecks, streamline processes, optimize assets.",)}
firefox-developer-learn-more-about-performance = {COPY(developer_quantum, "Learn more about Performance Tools",)}
firefox-developer-memory = {COPY(developer_quantum, "Memory",)}
firefox-developer-find-memory-leaks = {COPY(developer_quantum, "Find memory leaks and make your application zippy.",)}
firefox-developer-learn-more-about-memory = {COPY(developer_quantum, "Learn more about Memory Tools",)}
firefox-developer-style-editor = {COPY(developer_quantum, "Style Editor",)}
firefox-developer-edit-and-manage = {COPY(developer_quantum, "Edit and manage all your CSS stylesheets in your browser.",)}
firefox-developer-learn-more-about-style = {COPY(developer_quantum, "Learn more about Style Editor",)}
firefox-developer-made-for-developers = {COPY(developer_quantum, "The browser made for developers",)}
firefox-developer-all-the-latest = {COPY(developer_quantum, "All the latest developer tools in beta, plus <strong>experimental features</strong> like the Multi-line Console Editor and WebSocket Inspector.",)}
""",
            developer_quantum=developer_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-developer-welcome-to-firefox-browser"),
                value=REPLACE(
                    developer_quantum,
                    "Welcome to Firefox Browser Developer Edition",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                        "Developer Edition": TERM_REFERENCE("brand-name-developer-edition"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-developer-congrats-you-now-have"),
                value=REPLACE(
                    developer_quantum,
                    "Congrats. You now have Firefox Browser Developer Edition.",
                    {
                        "Firefox Browser": TERM_REFERENCE("brand-name-firefox-browser"),
                        "Developer Edition": TERM_REFERENCE("brand-name-developer-edition"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-developer-a-separate-profile"),
                value=REPLACE(
                    developer_quantum,
                    "A <strong>separate profile and path</strong> so you can easily run it alongside Release or Beta Firefox.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-developer-preferences-tailored = {COPY(developer_quantum, "Preferences <strong>tailored for web developers</strong>: Browser and remote debugging are enabled by default, as are the dark theme and developer toolbar button.",)}
firefox-developer-new-tools = {COPY(developer_quantum, "New Tools",)}
firefox-developer-inactive-css = {COPY(developer_quantum, "Inactive CSS",)}
""",
            developer_quantum=developer_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-developer-firefox-devtools-now-grays-out"),
                value=REPLACE(
                    developer_quantum,
                    "Firefox DevTools now grays out CSS declarations that don’t have an effect on the page. When you hover over the info icon, you’ll see a useful message about why the CSS is not being applied, including a hint about how to fix the problem.",
                    {
                        "Firefox DevTools": TERM_REFERENCE("brand-name-firefox-devtools"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-developer-firefox-devtools"),
                value=REPLACE(
                    developer_quantum,
                    "Firefox DevTools",
                    {
                        "Firefox DevTools": TERM_REFERENCE("brand-name-firefox-devtools"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-developer-the-new-firefox-devtools"),
                value=REPLACE(
                    developer_quantum,
                    "The new Firefox DevTools are powerful, flexible, and best of all, hackable. This includes a best-in-class JavaScript debugger, which can target multiple browsers and is built in React and Redux.",
                    {
                        "Firefox DevTools": TERM_REFERENCE("brand-name-firefox-devtools"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-developer-master-css-grid = {COPY(developer_quantum, "Master CSS Grid",)}
firefox-developer-next-gen-css-engine = {COPY(developer_quantum, "Next-Gen CSS Engine",)}
firefox-developer-a-next-generation = {COPY(developer_quantum, "A Next-Generation CSS Engine",)}
firefox-developer-master-innovative-features = {COPY(developer_quantum, "Innovative Features",)}
firefox-developer-want-to-be-on-the-cutting-edge = {COPY(developer_quantum, "Want to be on the cutting-edge?",)}
""",
            developer_quantum=developer_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-developer-firefox-nightly-receives"),
                value=REPLACE(
                    developer_quantum,
                    "Firefox Nightly receives daily updates and allows you to access features months before they go mainstream.",
                    {
                        "Firefox Nightly": TERM_REFERENCE("brand-name-firefox-nightly"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-developer-firefox-quantum-includes"),
                value=REPLACE(
                    developer_quantum,
                    "Firefox Quantum includes a new CSS engine, written in Rust, that has state-of-the-art innovations and is blazingly fast.",
                    {
                        "Firefox Quantum": TERM_REFERENCE("brand-name-firefox-quantum"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-developer-firefox-is-the-only-browser"),
                value=REPLACE(
                    developer_quantum,
                    "Firefox is the only browser with tools built specifically for building and designing with CSS Grid. These tools allow you to visualize the grid, display associated area names, preview transformations on the grid and much more.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-developer-convenient-features = {COPY(developer_quantum, "Convenient Features",)}
firefox-developer-faster-performance = {COPY(developer_quantum, "Faster Performance",)}
firefox-developer-shapes-editor = {COPY(developer_quantum, "Shapes Editor",)}
""",
            developer_quantum=developer_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-developer-firefox-devtools-has-a-brand-new-v2"),
                value=REPLACE(
                    developer_quantum,
                    "Firefox DevTools has a brand new shape path editor that takes the guesswork out of fine-tuning your shape-outside and clip-path shapes by allowing you to very easily fine-tune your adjustments with a visual editor.",
                    {
                        "Firefox DevTools": TERM_REFERENCE("brand-name-firefox-devtools"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-developer-firefox-devtools-has-a-brand-new"),
                value=REPLACE(
                    developer_quantum,
                    "Firefox DevTools has a brand new shape path editor that takes the guesswork out of fine-tuning your shadow-outside and clip-path shapes by allowing you to very easily fine-tune your adjustments with a visual editor.",
                    {
                        "Firefox DevTools": TERM_REFERENCE("brand-name-firefox-devtools"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-developer-faster-innovation = {COPY(developer_quantum, "Faster Information",)}
firefox-developer-fonts-panel = {COPY(developer_quantum, "Fonts Panel",)}
""",
            developer_quantum=developer_quantum,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-developer-the-new-fonts-panel"),
                value=REPLACE(
                    developer_quantum,
                    "The new fonts panel in Firefox DevTools gives developers quick access to all of the information they need about the fonts being used in an element. It also includes valuable information such as the font source, weight, style and more.",
                    {
                        "Firefox DevTools": TERM_REFERENCE("brand-name-firefox-devtools"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-developer-firefox-developer-edition-sends"),
                value=REPLACE(
                    developer_quantum,
                    "Firefox Developer Edition automatically sends feedback to Mozilla.",
                    {
                        "Firefox Developer Edition": TERM_REFERENCE("brand-name-firefox-developer-edition"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-developer-download-the-firefox-browser"),
                value=REPLACE(
                    developer_quantum,
                    "Download the Firefox browser made for developers",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ],
    )

    ctx.add_transforms(
        "firefox/developer.ftl",
        "firefox/developer.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("firefox-developer-welcome-to-the-all-new"),
                value=REPLACE(
                    developer_quantum,
                    "Welcome to the all-new Firefox Quantum: Developer Edition",
                    {
                        "Developer Edition": TERM_REFERENCE("brand-name-developer-edition"),
                        "Firefox Quantum": TERM_REFERENCE("brand-name-firefox-quantum"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-developer-firefox-has-been-rebuilt"),
                value=REPLACE(
                    developer_quantum,
                    "Firefox has been rebuilt from the ground-up to be faster, sleeker, and more powerful than ever.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ],
    )

    ctx.add_transforms(
        "firefox/developer.ftl",
        "firefox/developer.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("firefox-developer-congrats-you-now-have-firefox"),
                value=REPLACE(
                    developer_quantum,
                    "Congrats. You now have Firefox Quantum: Developer Edition.",
                    {
                        "Developer Edition": TERM_REFERENCE("brand-name-developer-edition"),
                        "Firefox Quantum": TERM_REFERENCE("brand-name-firefox-quantum"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-developer-this-isnt-just-an-update"),
                value=REPLACE(
                    developer_quantum,
                    "This isn’t just an update. This is Firefox Quantum: A brand new Firefox that has been rebuilt from the ground-up to be faster, sleeker, and more powerful than ever.",
                    {
                        "Firefox Quantum": TERM_REFERENCE("brand-name-firefox-quantum"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ],
    )
