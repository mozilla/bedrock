from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

index = "firefox/enterprise/index.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/enterprise/index.html, part {index}."""

    ctx.add_transforms(
        "firefox/enterprise.ftl",
        "firefox/enterprise.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-get-firefox-for-your-enterprise-with"),
                value=REPLACE(
                    index,
                    "Get Firefox for your enterprise with ESR and Rapid Release",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "ESR": TERM_REFERENCE("brand-name-esr"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-get-unmatched-data-protection"),
                value=REPLACE(
                    index,
                    "Get unmatched data protection on the release cadence that suits you with Firefox for enterprise. Download ESR and Rapid Release.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "ESR": TERM_REFERENCE("brand-name-esr"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-enterprise"),
                value=REPLACE(
                    index,
                    "Enterprise",
                    {
                        "Enterprise": TERM_REFERENCE("brand-name-enterprise"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-enterprise-overview = {COPY(index, "Overview",)}
firefox-enterprise-downloads = {COPY(index, "Downloads",)}
""",
            index=index,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-get-firefox-for-your-enterprise"),
                value=REPLACE(
                    index,
                    "Get Firefox for your enterprise",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-get-the-firefox-extended-support"),
                value=REPLACE(
                    index,
                    'Get the <a href="%s">Firefox Extended Support Release or Rapid Release</a> browser for comprehensive data security and data protection.',
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("url"),
                        "Firefox Extended Support Release": TERM_REFERENCE("brand-name-firefox-extended-support-release"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-enterprise-unmatched-data-protection = {COPY(index, "Unmatched data protection — on the release cadence that suits you",)}
""",
            index=index,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-the-firefox-browser-is-open"),
                value=REPLACE(
                    index,
                    "The Firefox browser is open source and provides Enhanced Tracking Protection — all part of our longstanding commitment to data protection.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-enterprise-your-data-stays-your-business = {COPY(index, "Your data stays your business",)}
firefox-enterprise-deploy-when-and-how-you-want = {COPY(index, "Deploy when and how you want",)}
""",
            index=index,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-with-install-packages-and"),
                value=REPLACE(
                    index,
                    "With install packages and a wide expansion of group policies and features, deployment is faster and more flexible than ever — and a breeze in Windows and MacOS environments.",
                    {
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "MacOS": TERM_REFERENCE("brand-name-mac"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-enterprise-choose-your-release-cadence = {COPY(index, "Choose your release cadence",)}
firefox-enterprise-get-rapid-releases-to-make = {COPY(index, "Get rapid releases to make sure you get the latest features faster, or go extended to ensure a super stable experience.",)}
""",
            index=index,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-enterprise-downloads"),
                value=REPLACE(
                    index,
                    "Enterprise downloads",
                    {
                        "Enterprise": TERM_REFERENCE("brand-name-enterprise"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-windows-64-bit"),
                value=REPLACE(
                    index,
                    "Windows 64-bit",
                    {
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-enterprise-macos = { -brand-name-mac }
firefox-enterprise-select-your-download = {COPY(index, "Select your download",)}
""",
            index=index,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-firefox-browser"),
                value=REPLACE(
                    index,
                    "Firefox browser",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Firefox browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-firefox-browser-msi-installer"),
                value=REPLACE(
                    index,
                    "Firefox browser - MSI installer",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Firefox browser": TERM_REFERENCE("brand-name-firefox-browser"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-firefox-extended-support-release"),
                value=REPLACE(
                    index,
                    "Firefox Extended Support Release (ESR)",
                    {
                        "Firefox Extended Support Release": TERM_REFERENCE("brand-name-firefox-extended-support-release"),
                        "ESR": TERM_REFERENCE("brand-name-esr"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-firefox-extended-support-release-msi"),
                value=REPLACE(
                    index,
                    "Firefox Extended Support Release (ESR) - MSI installer",
                    {
                        "Firefox Extended Support Release": TERM_REFERENCE("brand-name-firefox-extended-support-release"),
                        "ESR": TERM_REFERENCE("brand-name-esr"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-enterprise-support = {COPY(index, "Support",)}
firefox-enterprise-msi-installers = {COPY(index, "MSI installers",)}
firefox-enterprise-legacy-browser-support = {COPY(index, "Legacy browser support",)}
firefox-enterprise-admx-templates = {COPY(index, "ADMX templates",)}
firefox-enterprise-deployment-guide = {COPY(index, "Deployment guide",)}
firefox-enterprise-policy-documentation = {COPY(index, "Policy documentation",)}
firefox-enterprise-release-notes = {COPY(index, "Release Notes",)}
firefox-enterprise-documentation-and-community = {COPY(index, "Documentation and Community Support",)}
""",
            index=index,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-sample-plist-for-configuration"),
                value=REPLACE(
                    index,
                    'Sample <a href="%s">plist for configuration profile</a>',
                    {
                        "%%": "%",
                        "%s": VARIABLE_REFERENCE("url"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
firefox-enterprise-pkg-installer = {COPY(index, "PKG installer",)}
""",
            index=index,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-windows-32-bit"),
                value=REPLACE(
                    index,
                    "Windows 32-bit",
                    {
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("firefox-enterprise-download-firefox-esr-or-rapid"),
                value=REPLACE(
                    index,
                    'Download Firefox ESR or Rapid Release for<br> <a href="%(firefox_all)s">another language or platform.</a>',
                    {
                        "%%": "%",
                        "%(firefox_all)s": VARIABLE_REFERENCE("firefox_all"),
                        "Firefox ESR": TERM_REFERENCE("brand-name-firefox-esr"),
                    },
                ),
            ),
        ],
    )
