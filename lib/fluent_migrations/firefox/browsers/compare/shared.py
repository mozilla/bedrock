from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

shared = "firefox/compare/shared.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/browsers/compare/index.html, part {index}."""

    ctx.add_transforms(
        "firefox/browsers/compare/shared.ftl",
        "firefox/browsers/compare/shared.ftl",
        transforms_from("""
compare-shared-yes = {COPY(shared, "Yes",)}
compare-shared-no = {COPY(shared, "No",)}
compare-shared-private-browsing-mode = {COPY(shared, "Private Browsing mode",)}
compare-shared-blocks-third-party-tracking = {COPY(shared, "Blocks third-party tracking cookies",)}
compare-shared-blocks-cryptomining-scripts = {COPY(shared, "Blocks cryptomining scripts",)}
compare-shared-blocks-social-trackers = {COPY(shared, "Blocks social trackers",)}
compare-shared-autoplay-blocking = {COPY(shared, "Autoplay blocking",)}
compare-shared-tab-browsing = {COPY(shared, "Tab browsing",)}
compare-shared-bookmark-manager = {COPY(shared, "Bookmark manager",)}
compare-shared-automatically-fills-out-forms = {COPY(shared, "Automatically fills out forms",)}
compare-shared-search-engine-options = {COPY(shared, "Search engine options",)}
compare-shared-text-to-speech = {COPY(shared, "Text to speech",)}
compare-shared-reader-mode = {COPY(shared, "Reader mode",)}
compare-shared-spell-checking = {COPY(shared, "Spell checking",)}
compare-shared-web-extensionsadd-ons = {COPY(shared, "Web extensions/Add-ons",)}
compare-shared-in-browser-screenshot-tool = {COPY(shared, "In-browser screenshot tool",)}
compare-shared-os-availability = {COPY(shared, "OS availability",)}
compare-shared-mobile-os-availability = {COPY(shared, "Mobile OS availability",)}
compare-shared-syncs-with-mobile = {COPY(shared, "Syncs with mobile",)}
compare-shared-password-management = {COPY(shared, "Password management",)}
compare-shared-master-password = {COPY(shared, "Master Password",)}
compare-shared-security-and-privacy = {COPY(shared, "Security and Privacy",)}
compare-shared-utility = {COPY(shared, "Utility",)}
compare-shared-portability = {COPY(shared, "Portability",)}
compare-shared-security-and-privacy-strong = {COPY(shared, "Security and <strong>Privacy</strong>",)}
compare-shared-utility-strong = {COPY(shared, "<strong>Utility</strong>",)}
compare-shared-portability-strong = {COPY(shared, "<strong>Portability</strong>",)}
compare-shared-overall-assessment = {COPY(shared, "Overall Assessment",)}
compare-shared-the-comparisons-made-here = {COPY(shared, "The comparisons made here were done so across browser release versions as follows:",)}
compare-shared-brand-name-firefox = { -brand-name-firefox }
compare-shared-brand-name-chrome = { -brand-name-chrome }
compare-shared-brand-name-edge = { -brand-name-edge }
compare-shared-brand-name-ie = { -brand-name-ie }
compare-shared-brand-name-opera = { -brand-name-opera }
compare-shared-brand-name-safari = { -brand-name-safari }
compare-shared-brand-name-brave = { -brand-name-brave }
compare-shared-compare-browsers = {COPY(shared, "Compare Browsers",)}
""", shared=shared)
        )

