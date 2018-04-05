# Static media bundle definitions.

PIPELINE_CSS = {
    'csrf-failure': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/csrf-failure.less',
        ),
        'output_filename': 'css/csrf-failure-bundle.css',
    },
    'about': {
        'source_filenames': (
            'css/base/mozilla-video-poster.less',
            'css/newsletter/moznewsletter-subscribe.less',
            'css/mozorg/about.less',
        ),
        'output_filename': 'css/about-bundle.css',
    },
    'about-base': {
        'source_filenames': (
            'css/mozorg/about-base.less',
        ),
        'output_filename': 'css/about-base-bundle.css',
    },
    'about-leadership': {
        'source_filenames': (
            'css/newsletter/moznewsletter-subscribe.less',
            'css/mozorg/leadership.scss',
        ),
        'output_filename': 'css/about-leadership-bundle.css',
    },
    'book': {
        'source_filenames': (
            'css/mozorg/book.scss',
        ),
        'output_filename': 'css/book-bundle.css',
    },
    'browser-test': {
        'source_filenames': (
            'css/mozorg/browser-test.scss',
        ),
        'output_filename': 'css/browser-test-bundle.css',
    },
    'credits': {
        'source_filenames': (
            'css/mozorg/credits.scss',
        ),
        'output_filename': 'css/credits-bundle.css',
    },
    'credits-faq': {
        'source_filenames': (
            'css/mozorg/credits-faq.less',
        ),
        'output_filename': 'css/credits-faq-bundle.css',
    },
    'commit-access-policy': {
        'source_filenames': (
            'css/mozorg/commit-access-policy.less',
        ),
        'output_filename': 'css/commit-access-policy-bundle.css',
    },
    'commit-access-requirements': {
        'source_filenames': (
            'css/mozorg/commit-access-requirements.less',
        ),
        'output_filename': 'css/commit-access-requirements.css',
    },
    'css-grid-demo': {
        'source_filenames': (
            'css/mozorg/developer/css-grid-demo.scss',
        ),
        'output_filename': 'css/css-grid-demo-bundle.css',
    },
    'about-forums': {
        'source_filenames': (
            'css/mozorg/about-forums.less',
        ),
        'output_filename': 'css/about-forums-bundle.css',
    },
    'about-lean-data': {
        'source_filenames': (
            'css/mozorg/about-lean-data.less',
        ),
        'output_filename': 'css/about-lean-data-bundle.css',
    },
    'about-transparency': {
        'source_filenames': (
            'css/base/mozilla-accordion.less',
            'css/mozorg/about-transparency.less',
        ),
        'output_filename': 'css/about-transparency-bundle.css',
    },
    'about-patents': {
        'source_filenames': (
            'css/mozorg/about-patents.less',
            'css/base/mozilla-accordion.less',
        ),
        'output_filename': 'css/about-patents-bundle.css',
    },
    'foundation': {
        'source_filenames': (
            'css/newsletter/moznewsletter-subscribe.less',
            'css/foundation/foundation.less',
        ),
        'output_filename': 'css/foundation-bundle.css',
    },
    'grants': {
        'source_filenames': (
            'css/grants/grants.less',
        ),
        'output_filename': 'css/grants-bundle.css',
    },
    'internet-health': {
        'source_filenames': (
            'css/mozorg/internet-health.scss',
        ),
        'output_filename': 'css/mozorg/internet_health-bundle.css',
    },
    'internet-health-hub': {
        'source_filenames': (
            'css/mozorg/internet-health/index.scss',
        ),
        'output_filename': 'css/mozorg/internet-health-hub-bundle.css',
    },
    'health-subpage': {
        'source_filenames': (
            'css/mozorg/internet-health/health-subpage.scss',
        ),
        'output_filename': 'css/mozorg/health-subpage-bundle.css',
    },
    'privacy-day-egg': {
        'source_filenames': (
            'css/mozorg/internet-health/privacy-day-egg.scss',
        ),
        'output_filename': 'css/mozorg/privacy-day-egg-bundle.css',
    },
    'itu': {
        'source_filenames': (
            'css/mozorg/itu.less',
        ),
        'output_filename': 'css/itu-bundle.css',
    },
    'common': {
        'source_filenames': (
            'css/sandstone/sandstone.less',
            'css/base/notification-banner.less',
            'css/tabzilla/tabzilla-static.less',
        ),
        'output_filename': 'css/common-bundle.css',
    },
    'responsive': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/base/global-nav.less',
            'css/base/notification-banner.less',
            'css/tabzilla/tabzilla-static.less',
        ),
        'output_filename': 'css/responsive-bundle.css',
    },
    'pebbles': {
        'source_filenames': (
            'css/pebbles/global.scss',
        ),
        'output_filename': 'css/pebbles-bundle.css',
    },
    'pebbles-basic': {
        'source_filenames': (
            'css/pebbles/basic.scss',
        ),
        'output_filename': 'css/pebbles-basic-bundle.css',
    },
    'oldIE': {
        'source_filenames': (
            'css/sandstone/oldIE.less',
        ),
        'output_filename': 'css/oldIE-bundle.css',
    },
    'oldIE-pebbles': {
        'source_filenames': (
            'css/pebbles/base/oldIE.scss',
        ),
        'output_filename': 'css/oldIE-pebbles-bundle.css',
    },
    'newsletter': {
        'source_filenames': (
            'css/newsletter/newsletter.less',
        ),
        'output_filename': 'css/newsletter-bundle.css',
    },
    'newsletter-mozilla': {
        'source_filenames': (
            'css/newsletter/newsletter-mozilla.scss',
        ),
        'output_filename': 'css/newsletter-mozilla-bundle.css',
    },
    'newsletter-developer': {
        'source_filenames': (
            'css/newsletter/newsletter-developer.scss',
        ),
        'output_filename': 'css/newsletter-developer-bundle.css',
    },
    'newsletter-firefox': {
        'source_filenames': (
            'css/newsletter/newsletter-firefox.scss',
        ),
        'output_filename': 'css/newsletter-firefox-bundle.css',
    },
    'newsletter-opt-out-confirmation': {
        'source_filenames': (
            'css/newsletter/newsletter-opt-out-confirmation.scss',
        ),
        'output_filename': 'css/newsletter-opt-out-confirmation-bundle.css',
    },
    'contact-spaces': {
        'source_filenames': (
            'css/libs/magnific-popup.css',
            'css/mozorg/contact-spaces.scss',
        ),
        'output_filename': 'css/contact-spaces-bundle.css',
    },
    'developer-hub': {
        'source_filenames': (
            'css/base/mozilla-modal.less',
            'css/mozorg/developer/index.scss',
        ),
        'output_filename': 'css/mozorg/developer-hub-bundle.css',
    },
    'firefox_accounts': {
        'source_filenames': (
            'css/base/mozilla-fxa-iframe.scss',
            'css/firefox/accounts.scss',
        ),
        'output_filename': 'css/firefox_accounts-bundle.css',
    },
    'firefox_all': {
        'source_filenames': (
            'css/base/mozilla-share-cta.less',
            'css/base/menu-resp.less',
            'css/newsletter/fxnewsletter-subscribe.less',
            'css/firefox/all.less',
        ),
        'output_filename': 'css/firefox_all-bundle.css',
    },
    'firefox_all_old_ie': {
        'source_filenames': (
            'css/firefox/all-oldIE.less',
        ),
        'output_filename': 'css/firefox_all_old_ie-bundle.css',
    },
    'firefox_unsupported_systems': {
        'source_filenames': (
            'css/base/menu-resp.less',
            'css/firefox/unsupported-systems.less',
        ),
        'output_filename': 'css/firefox_unsupported_systems-bundle.css',
    },
    'firefox_channel': {
        'source_filenames': (
            'css/newsletter/fxnewsletter-subscribe.less',
            'css/firefox/channel.less',
        ),
        'output_filename': 'css/firefox_channel-bundle.css',
    },
    'firefox-features-hub-common': {
        'source_filenames': (
            'css/firefox/features/common.scss',
        ),
        'output_filename': 'css/firefox-features-hub-common-bundle.css',
    },
    'firefox-features-index': {
        'source_filenames': (
            'css/firefox/features/index.scss',
        ),
        'output_filename': 'css/firefox-features-index-bundle.css',
    },
    'firefox-features-hub-detail': {
        'source_filenames': (
            'css/firefox/features/detail.scss',
        ),
        'output_filename': 'css/firefox-features-hub-detail-bundle.css',
    },
    # This bundle is currently used on both /features/sync & /features/send-tabs
    # because they happen to share everything. If/when divergence happens,
    # send-tabs should get it's own .scss file.
    'firefox-features-sync': {
        'source_filenames': (
            'css/firefox/features/sync.scss',
        ),
        'output_filename': 'css/firefox-features-sync-bundle.css',
    },
    'firefox-home': {
        'source_filenames': (
            'css/firefox/home.scss',
        ),
        'output_filename': 'css/firefox-home-bundle.css',
    },
    'firefox_fx38_0_5_firstrun': {
        'source_filenames': (
            'css/firefox/australis/fx38_0_5/firstrun.less',
        ),
        'output_filename': 'css/firefox_fx38_0_5_firstrun-bundle.css',
    },
    'nightly_firstrun': {
        'source_filenames': (
            'css/firefox/nightly_firstrun.less',
        ),
        'output_filename': 'css/nightly_firstrun-bundle.css',
    },
    'nightly_whatsnew': {
        'source_filenames': (
            'css/firefox/whatsnew/whatsnew-nightly.scss',
        ),
        'output_filename': 'css/nightly_whatsnew-bundle.css',
    },
    'firefox_firstrun': {
        'source_filenames': (
            'css/base/notification-banner.less',
            'css/firefox/firstrun/firstrun.less',
            'css/base/mozilla-fxa-iframe.less',
        ),
        'output_filename': 'css/firefox_firstrun-bundle.css',
    },
    'firefox_firstrun_quantum': {
        'source_filenames': (
            'css/firefox/firstrun/firstrun-quantum.scss',
            'css/base/mozilla-fxa-iframe.scss',
        ),
        'output_filename': 'css/firefox_firstrun_quantum-bundle.css',
    },
    'firefox_firstrun_facebook_container': {
        'source_filenames': (
            'css/firefox/firstrun/firstrun-facebook-container.scss',
        ),
        'output_filename': 'css/firefox_firstrun_facebook_container-bundle.css',
    },
    'firefox_feedback': {
        'source_filenames': (
            'css/base/mozilla-share-cta.less',
            'css/firefox/feedback.less',
        ),
        'output_filename': 'css/firefox_feedback-bundle.css',
    },
    'firefox_developer': {
        'source_filenames': (
            'css/firefox/developer/developer.scss',
        ),
        'output_filename': 'css/firefox_developer-bundle.css',
    },
    'firefox_developer_quantum_whatsnew': {
        'source_filenames': (
            'css/firefox/developer/developer.scss',
            'css/firefox/developer/whatsnew.scss',
        ),
        'output_filename': 'css/firefox_developer_quantum_whatsnew-bundle.css',
    },
    'firefox_developer_firstrun': {
        'source_filenames': (
            'css/base/mozilla-modal.less',
            'css/firefox/dev-firstrun.less',
        ),
        'output_filename': 'css/firefox_developer_firstrun-bundle.css',
    },
    'firefox_developer_quantum_firstrun': {
        'source_filenames': (
            'css/firefox/developer/developer.scss',
            'css/firefox/developer/firstrun.scss',
        ),
        'output_filename': 'css/firefox_developer_quantum_firstrun-bundle.css',
    },
    'firefox_enterprise': {
        'source_filenames': (
            'css/firefox/enterprise.scss',
        ),
        'output_filename': 'css/firefox_enterprise-bundle.css',
    },
    'firefox_facebook_container': {
        'source_filenames': (
            'css/firefox/facebook-container.scss',
        ),
        'output_filename': 'css/firefox_facebook_container-bundle.css',
    },
    'firefox_ios_testflight': {
        'source_filenames': (
            'css/firefox/testflight.less',
        ),
        'output_filename': 'css/firefox-ios-testflight-bundle.css',
    },
    'firefox-mobile': {
        'source_filenames': (
            'css/base/send-to-device.less',
            'css/firefox/mobile.scss',
        ),
        'output_filename': 'css/firefox_mobile-bundle.css',
    },
    # favor cache for scene 2 speed over 1 less HTTP request for scene 1
    'firefox_new_common': {
        'source_filenames': (
            'css/firefox/new/common.scss',
        ),
        'output_filename': 'css/firefox_new_common-bundle.css',
    },
    'firefox_new_scene1': {
        'source_filenames': (
            'css/firefox/new/scene1.scss',
        ),
        'output_filename': 'css/firefox_new_scene1-bundle.css',
    },
    'firefox_new_scene2': {
        'source_filenames': (
            'css/firefox/new/scene2.scss',
        ),
        'output_filename': 'css/firefox_new_scene2-bundle.css',
    },
    'firefox_new_wait_face': {
        'source_filenames': (
            'css/firefox/new/wait-face.scss',
        ),
        'output_filename': 'css/firefox_new_wait_face-bundle.css',
    },
    'firefox_new_reggie_watts': {
        'source_filenames': (
            'css/firefox/new/reggie-watts.scss',
        ),
        'output_filename': 'css/firefox_new_reggie_watts-bundle.css',
    },
    'firefox_new_portland': {
        'source_filenames': (
            'css/firefox/new/portland.scss',
        ),
        'output_filename': 'css/firefox_new_portland-bundle.css',
    },
    'firefox_organizations': {
        'source_filenames': (
            'css/firefox/organizations.less',
        ),
        'output_filename': 'css/firefox_organizations-bundle.css',
    },
    'firefox_releases_index': {
        'source_filenames': (
            'css/base/menu-resp.less',
            'css/firefox/releases-index.less',
        ),
        'output_filename': 'css/firefox_releases_index-bundle.css',
    },
    'firefox-switch': {
        'source_filenames': (
            'css/firefox/switch.scss',
        ),
        'output_filename': 'css/firefox-switch-bundle.css',
    },
    'firefox_tour_none': {
        'source_filenames': (
            'css/firefox/australis/australis-page-common.less',
            'css/firefox/sync-animation.less',
            'css/firefox/australis/australis-page-stacked.less',
        ),
        'output_filename': 'css/firefox_tour_none-bundle.css',
    },
    'firefox-update-notification-firstrun-whatsnew': {
        'source_filenames': (
            'css/base/mozilla-modal.less',
            'css/base/notification-modal.less',
        ),
        'output_filename': 'css/firefox-update-notification-firstrun-whatsnew-bundle.css',
    },
    'firefox_whatsnew': {
        'source_filenames': (
            'css/firefox/whatsnew/whatsnew.scss',
        ),
        'output_filename': 'css/firefox_whatsnew-bundle.css',
    },
    'firefox_whatsnew_fxa': {
        'source_filenames': (
            'css/base/mozilla-fxa-iframe.scss',
            'css/firefox/whatsnew/whatsnew-fxa.scss',
        ),
        'output_filename': 'css/firefox_whatsnew_fxa-bundle.css',
    },
    'firefox_whatsnew_zh_tw': {
        'source_filenames': (
            'css/firefox/whatsnew/whatsnew-zh-tw.scss',
        ),
        'output_filename': 'css/firefox_whatsnew_zh_tw-bundle.css',
    },
    'firefox-whatsnew-57': {
        'source_filenames': (
            'css/firefox/whatsnew/whatsnew-57.scss',
        ),
        'output_filename': 'css/firefox-whatsnew-57-bundle.css',
    },
    'firefox-whatsnew-57-letter': {
        'source_filenames': (
            'css/firefox/whatsnew/whatsnew-57-letter.scss',
        ),
        'output_filename': 'css/firefox-whatsnew-57-letter-bundle.css',
    },
    'firefox-whatsnew-rocket': {
        'source_filenames': (
            'css/firefox/whatsnew/whatsnew-rocket.scss',
        ),
        'output_filename': 'css/firefox-whatsnew-rocket-bundle.css',
    },
    'firefox_releasenotes_firefox': {
        'source_filenames': (
            'css/firefox/releasenotes-firefox.less',
        ),
        'output_filename': 'css/firefox_releasenotes_firefox-bundle.css',
    },
    'firefox_releasenotes': {
        'source_filenames': (
            'css/base/menu-resp.less',
            'css/firefox/releasenotes.less',
        ),
        'output_filename': 'css/firefox_releasenotes-bundle.css',
    },
    'firefox_sync_anim': {
        'source_filenames': (
            'css/firefox/sync-animation.less',
        ),
        'output_filename': 'css/firefox_sync_anim-bundle.css',
    },
    'installer_help': {
        'source_filenames': (
            'css/base/menu-resp.less',
            'css/base/mozilla-modal.less',
            'css/firefox/installer-help.less',
        ),
        'output_filename': 'css/installer_help-bundle.css',
    },
    'history-slides': {
        'source_filenames': (
            'css/mozorg/history-slides.less',
        ),
        'output_filename': 'css/history-slides-bundle.css',
    },
    'home': {
        'source_filenames': (
            'css/newsletter/moznewsletter-subscribe.less',
            'css/mozorg/home/home.scss',
        ),
        'output_filename': 'css/home-bundle.css',
    },
    'legal': {
        'source_filenames': (
            'css/legal/legal.less',
            'css/newsletter/moznewsletter-subscribe.less',
        ),
        'output_filename': 'css/legal-bundle.css',
    },
    'legal-eula': {
        'source_filenames': (
            'css/legal/eula.less',
        ),
        'output_filename': 'css/legal-eula-bundle.css',
    },
    'legal_fraud_report': {
        'source_filenames': (
            'css/legal/fraud-report.less',
        ),
        'output_filename': 'css/legal_fraud_report-bundle.css',
    },
    'manifesto': {
        'source_filenames': (
            'css/mozorg/manifesto.scss',
        ),
        'output_filename': 'css/manifesto-bundle.css',
    },
    'mission': {
        'source_filenames': (
            'css/base/mozilla-video-poster.less',
            'css/newsletter/moznewsletter-subscribe.less',
            'css/mozorg/mission.less',
        ),
        'output_filename': 'css/mission-bundle.css',
    },
    'mpl': {
        'source_filenames': (
            'css/mozorg/mpl.less',
        ),
        'output_filename': 'css/mpl-bundle.css',
    },
    'mpl-1-1': {
        'source_filenames': (
            'css/mozorg/mpl-1-1.scss',
        ),
        'output_filename': 'css/mpl-1-1-bundle.css',
    },
    'mpl-1-1-annotated': {
        'source_filenames': (
            'css/mozorg/mpl-1-1-annotated.scss',
        ),
        'output_filename': 'css/mpl-1-1-annotated-bundle.css',
    },
    'mpl-2-0': {
        'source_filenames': (
            'css/mozorg/mpl-2-0.scss',
        ),
        'output_filename': 'css/mpl-2-0-bundle.css',
    },
    'mpl-differences': {
        'source_filenames': (
            'css/mozorg/mpl-differences.scss',
        ),
        'output_filename': 'css/mpl-differences-bundle.css',
    },
    'moss': {
        'source_filenames': (
            'css/mozorg/moss/common.scss',
        ),
        'output_filename': 'css/moss-bundle.css',
    },
    'mozilla_accordion': {
        'source_filenames': (
            'css/base/mozilla-accordion.less',
        ),
        'output_filename': 'css/mozilla_accordion-bundle.css',
    },
    'namespaces': {
        'source_filenames': (
            'css/mozorg/namespaces.scss',
        ),
        'output_filename': 'css/namespaces-bundle.css',
    },
    'partnerships-distribution': {
        'source_filenames': (
            'css/mozorg/partnerships-distribution.scss',
        ),
        'output_filename': 'css/partnerships-distribution-bundle.css',
    },
    'powered-by': {
        'source_filenames': (
            'css/mozorg/powered-by.less',
        ),
        'output_filename': 'css/powered-by-bundle.css',
    },
    'plugincheck': {
        'source_filenames': (
            'css/plugincheck/plugincheck.scss',
        ),
        'output_filename': 'css/plugincheck-bundle.css',
    },
    'press': {
        'source_filenames': (
            'css/press/press.less',
        ),
        'output_filename': 'css/press-bundle.css',
    },
    'privacy_quantum': {
        'source_filenames': (
            'css/privacy/privacy-quantum.scss',
        ),
        'output_filename': 'css/privacy-quantum-bundle.css',
    },
    'privacy': {
        'source_filenames': (
            'css/privacy/privacy.less',
        ),
        'output_filename': 'css/privacy-bundle.css',
    },
    'fb_privacy': {
        'source_filenames': (
            'css/privacy/fb-privacy.less',
        ),
        'output_filename': 'css/fb_privacy-bundle.css',
    },
    'projects_mozilla_based': {
        'source_filenames': (
            'css/mozorg/projects/mozilla-based.less',
        ),
        'output_filename': 'css/projects_mozilla_based-bundle.css',
    },
    'projects-calendar': {
        'source_filenames': (
            'css/mozorg/projects/calendar.less',
        ),
        'output_filename': 'css/projects-calendar-bundle.css',
    },
    'security': {
        'source_filenames': (
            'css/security/security.scss',
        ),
        'output_filename': 'css/security-bundle.css',
    },
    'security-bug-bounty-hall-of-fame': {
        'source_filenames': (
            'css/security/hall-of-fame.scss',
            'css/base/mozilla-accordion.less',
        ),
        'output_filename': 'css/security-bug-bounty-hall-of-fame-bundle.css',
    },
    'smarton': {
        'source_filenames': (
            'css/base/mozilla-share-cta.less',
            'css/teach/smarton.less',
        ),
        'output_filename': 'css/smarton-bundle.css',
    },
    'smarton-ie': {
        'source_filenames': (
            'css/teach/smarton-ie.less',
        ),
        'output_filename': 'css/smarton-ie-bundle.css',
    },
    'styleguide': {
        'source_filenames': (
            'css/styleguide/styleguide.scss',
        ),
        'output_filename': 'css/styleguide-bundle.css',
    },
    'technology': {
        'source_filenames': (
            'css/base/mozilla-modal.less',
            'css/mozorg/technology.scss',
        ),
        'output_filename': 'css/technology-bundle.css',
    },
    'tracking-protection-tour': {
        'source_filenames': (
            'css/firefox/tracking-protection-tour.less',
        ),
        'output_filename': 'css/tracking-protection-tour-bundle.css',
    },
    'contribute-base': {
        'source_filenames': (
            'css/base/mozilla-modal.less',
            'css/mozorg/contribute/contribute-base.less',
        ),
        'output_filename': 'css/contribute-base-bundle.css',
    },
    'contribute-embed': {
        'source_filenames': (
            'css/mozorg/contribute/contribute-embed.less',
        ),
        'output_filename': 'css/contribute-embed-bundle.css',
    },
    'contribute-signup': {
        'source_filenames': (
            'css/mozorg/contribute/signup.less',
        ),
        'output_filename': 'css/contribute-signup-bundle.css',
    },
    'contribute-taskview': {
        'source_filenames': (
            'css/newsletter/moznewsletter-subscribe.less',
            'css/mozorg/contribute/taskview.less',
        ),
        'output_filename': 'css/contribute-taskview-bundle.css',
    },
    'contribute-friends': {
        'source_filenames': (
            'css/mozorg/contribute/friends.less',
        ),
        'output_filename': 'css/contribute-friends-bundle.css',
    },
    'contribute-studentambassadors-landing': {
        'source_filenames': (
            'css/base/social-widgets.less',
            'css/mozorg/contribute/studentambassadors/landing.less',
        ),
        'output_filename': 'css/contribute-studentambassadors-landing-bundle.css',
    },
    'page_not_found': {
        'source_filenames': (
            'css/base/page-not-found.scss',
        ),
        'output_filename': 'css/page_not_found-bundle.css',
    },
    'annual_2011': {
        'source_filenames': (
            'css/foundation/annual2011.less',
        ),
        'output_filename': 'css/annual_2011-bundle.css',
    },
    'annual_2012': {
        'source_filenames': (
            'css/base/mozilla-modal.less',
            'css/foundation/annual2012.less',
        ),
        'output_filename': 'css/annual_2012-bundle.css',
    },
    'annual_2013': {
        'source_filenames': (
            'css/base/mozilla-modal.less',
            'css/foundation/annual2013.less',
        ),
        'output_filename': 'css/annual_2013-bundle.css',
    },
    'annual_2014': {
        'source_filenames': (
            'css/foundation/annual2013.less',
            'css/foundation/annual2014.less',
        ),
        'output_filename': 'css/annual_2014-bundle.css',
    },
    'annual_2015': {
        'source_filenames': (
            'css/foundation/annual2013.less',
            'css/foundation/annual2015.less',
        ),
        'output_filename': 'css/annual_2015-bundle.css',
    },
    'annual_2016': {
        'source_filenames': (
            'css/foundation/annual2016.scss',
        ),
        'output_filename': 'css/annual_2016-bundle.css',
    },
    'thunderbird-features': {
        'source_filenames': (
            'css/base/menu-resp.less',
            'css/thunderbird/features.less',
        ),
        'output_filename': 'css/thunderbird-features-bundle.css',
    },
    'thunderbird-landing': {
        'source_filenames': (
            'css/base/menu-resp.less',
            'css/thunderbird/landing.less',
        ),
        'output_filename': 'css/thunderbird-landing-bundle.css',
    },
    'thunderbird-organizations': {
        'source_filenames': (
            'css/base/menu-resp.less',
            'css/firefox/organizations.less',
        ),
        'output_filename': 'css/thunderbird-organizations-bundle.css',
    },
    'thunderbird-channel': {
        'source_filenames': (
            'css/base/menu-resp.less',
            'css/thunderbird/channel.less',
        ),
        'output_filename': 'css/thunderbird-channel-bundle.css',
    },
    'thunderbird-start': {
        'source_filenames': (
            'css/sandstone/fonts.less',
            'css/thunderbird/start.less',
        ),
        'output_filename': 'css/thunderbird-start-bundle.css',
    },
    'etc-firefox-retention-thank-you-a': {
        'source_filenames': (
            'css/etc/firefox/retention/thank-you.scss',
            'css/etc/firefox/retention/thank-you-a.scss',
        ),
        'output_filename': 'css/etc-firefox-retention-thank-you-a-bundle.css',
    },
    'etc-firefox-retention-thank-you-b': {
        'source_filenames': (
            'css/etc/firefox/retention/thank-you.scss',
            'css/etc/firefox/retention/thank-you-b.scss',
        ),
        'output_filename': 'css/etc-firefox-retention-thank-you-b-bundle.css',
    },
    'etc-firefox-retention-thank-you-referral': {
        'source_filenames': (
            'css/etc/firefox/retention/thank-you.scss',
            'css/etc/firefox/retention/thank-you-referral.scss',
        ),
        'output_filename': 'css/etc-firefox-retention-thank-you-referral-bundle.css',
    },
}

PIPELINE_JS = {
    'site': {
        'source_filenames': (
            'js/base/site.js',  # this is automatically included on every page
            'js/base/dnt-helper.js',
            'js/base/mozilla-cookie-helper.js',
            'js/base/core-datalayer-page-id.js',
        ),
        'output_filename': 'js/site-bundle.js',
    },
    'projects-calendar': {
        'source_filenames': (
            'js/mozorg/calendar.js',
        ),
        'output_filename': 'js/projects-calendar-bundle.js',
    },
    # Served to most pages.
    # nav-main-resp.js isn't used on a handful of pages, but caching a single
    # bundle should offset the extra weight.
    'common': {
        'source_filenames': (
            'js/libs/jquery-3.2.1.min.js',
            'js/libs/spin.min.js',  # used by js/newsletter/form.js
            'js/base/mozilla-utils.js',
            'js/newsletter/form.js',
            'js/base/mozilla-client.js',
            'js/base/mozilla-image-helper.js',
            'js/base/nav-main-resp.js',
            'js/base/class-list-polyfill.js',
            'js/base/mozilla-global-nav.js',
            'js/base/base-page-init.js',
            'js/base/core-datalayer.js',
            'js/base/core-datalayer-init.js',
            # primarily needed by stub attribution script (+ a couple others)
            'js/base/search-params.js',
        ),
        'output_filename': 'js/common-bundle.js',
    },
    'common-ie8': {
        'source_filenames': (
            'js/libs/jquery-1.11.3.min.js',
            'js/ie8/mozilla-utils-ie8.js',
            'js/base/mozilla-client.js',
            'js/ie8/base-page-init-ie8.js',
            'js/base/core-datalayer.js',
            'js/base/core-datalayer-init.js',
            # primarily needed by stub attribution script (+ a couple others)
            'js/base/search-params.js',
        ),
        'output_filename': 'js/common-ie8-bundle.js',
    },
    'contact-spaces': {
        'source_filenames': (
            'js/libs/jquery.magnific-popup.min.js',
            'js/mozorg/contact-spaces.js',
        ),
        'output_filename': 'js/contact-spaces-bundle.js',
    },
    'contribute-base': {
        'source_filenames': (
            'js/mozorg/contribute/contribute-nav.js',
        ),
        'output_filename': 'js/contribute-base.js',
    },
    'contribute-friends': {
        'source_filenames': (
            'js/base/mozilla-svg-image-fallback.js',
            'js/mozorg/contribute/friends.js',
        ),
        'output_filename': 'js/contribute-friends-bundle.js'
    },
    'contribute-landing': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.cycle2.min.js',
            'js/base/mozilla-modal.js',
            'js/mozorg/contribute/contribute-landing.js',
        ),
        'output_filename': 'js/contribute-landing-bundle.js',
    },
    'contribute-signup': {
        'source_filenames': (
            'js/mozorg/contribute/signup.js',
        ),
        'output_filename': 'css/contribute-signup-bundle.js',
    },
    'contribute-stories': {
        'source_filenames': (
            'js/mozorg/contribute/contribute-stories.js',
        ),
        'output_filename': 'js/contribute-stories.js',
    },
    'contribute-taskview': {
        'source_filenames': (
            'js/mozorg/contribute/taskview.js',
        ),
        'output_filename': 'css/contribute-taskview-bundle.js',
    },
    'accordion': {
        'source_filenames': (
            'js/base/mozilla-accordion.js',
            'js/base/mozilla-accordion-gatrack.js',
        ),
        'output_filename': 'js/accordion-bundle.js',
    },
    'about-transparency': {
        'source_filenames': (
            'js/base/mozilla-accordion.js',
            'js/base/mozilla-accordion-gatrack.js',
            'js/mozorg/about-transparency.js',
        ),
        'output_filename': 'js/about-transparency-bundle.js',
    },
    'about-leadership': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/mozorg/about-leadership.js',
        ),
        'output_filename': 'js/about-leadership-bundle.js',
    },
    'css-grid-demo': {
        'source_filenames': (
            'js/base/mozilla-smoothscroll.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/mozorg/developer/css-grid-demo.js',
        ),
        'output_filename': 'js/css-grid-demo-bundle.js',
    },
    'developer-hub': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/hubs/sub-nav.js',
            'js/base/mozilla-modal.js',
            'js/base/mozilla-lazy-load.js',
            'js/mozorg/developer/developer-hub.js',
        ),
        'output_filename': 'js/developer-hub-bundle.js',
    },
    'gtm-snippet': {
        'source_filenames': (
            'js/base/gtm-snippet.js',
        ),
        'output_filename': 'js/gtm-snippet-bundle.js',
    },
    'optimizely-snippet': {
        'source_filenames': (
            'js/base/optimizely-snippet.js',
        ),
        'output_filename': 'js/optimizely-snippet-bundle.js',
    },
    'firefox_accounts': {
        'source_filenames': (
            'js/base/mozilla-fxa-iframe.js',
            'js/base/uitour-lib.js',
            'js/firefox/accounts.js',
        ),
        'output_filename': 'js/firefox_accounts-bundle.js',
    },
    'firefox_all': {
        'source_filenames': (
            'js/base/mozilla-share-cta.js',
            'js/base/mozilla-pager.js',
            'js/firefox/firefox-language-search.js',
        ),
        'output_filename': 'js/firefox_all-bundle.js',
    },
    'firefox_facebook_container_video': {
        'source_filenames': (
            'js/base/mozilla-video-poster.js',
            'js/firefox/facebook-container-video.js',
        ),
        'output_filename': 'js/firefox_facebook_container_video-bundle.js',
    },
    'firefox_facebook_container_funnelcake': {
        'source_filenames': (
            'js/firefox/facebook-container-funnelcake.js',
        ),
        'output_filename': 'js/firefox_facebook_container_funnelcake-bundle.js',
    },
    'firefox-features-hub': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/hubs/sub-nav.js',
        ),
        'output_filename': 'js/firefox-features-hub-bundle.js',
    },
    # This bundle is currently used on both /features/sync & /features/send-tabs
    # because they happen to share everything. If/when divergence happens,
    # send-tabs should get it's own .js files.
    'firefox-features-sync': {
        'source_filenames': (
            'js/base/uitour-lib.js',
            'js/firefox/features/sync.js',
            'js/firefox/features/sync-init.js',
        ),
        'output_filename': 'js/firefox-features-sync-bundle.js',
    },
    'firefox_fx38_0_5_firstrun': {
        'source_filenames': (
            'js/base/uitour-lib.js',
            'js/firefox/australis/fx38_0_5/firstrun.js',
        ),
        'output_filename': 'js/firefox_fx38_0_5_firstrun-bundle.js',
    },
    'firefox_firstrun': {
        'source_filenames': (
            'js/base/mozilla-fxa-iframe.js',
            'js/firefox/firstrun/firstrun.js',
        ),
        'output_filename': 'js/firefox_firstrun-bundle.js',
    },
    'firefox_firstrun_quantum': {
        'source_filenames': (
            'js/base/uitour-lib.js',
            'js/base/mozilla-fxa-iframe.js',
            'js/firefox/firstrun/firstrun_quantum.js',
        ),
        'output_filename': 'js/firefox_firstrun_quantum-bundle.js',
    },
    'firefox_developer': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/hubs/sub-nav.js',
        ),
        'output_filename': 'js/firefox_developer-bundle.js',
    },
    'firefox_developer_firstrun': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/firefox/dev-firstrun.js',
        ),
        'output_filename': 'js/firefox_developer_firstrun-bundle.js',
    },
    'firefox_developer_whatsnew': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/firefox/dev-whatsnew.js',
        ),
        'output_filename': 'js/firefox_developer_whatsnew-bundle.js',
    },
    'firefox-home': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/hubs/sub-nav.js',
            'js/base/mozilla-smoothscroll.js',
            'js/base/mozilla-video-poster.js',
            'js/firefox/home/features-scroller.js',
            'js/firefox/home/main.js',
        ),
        'output_filename': 'js/firefox-home-bundle.js',
    },
    'firefox_new_scene1': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/firefox/new/scene1.js',
        ),
        'output_filename': 'js/firefox_new_scene1-bundle.js',
    },
    'firefox_new_scene2': {
        'source_filenames': (
            'js/firefox/new/scene2.js',
        ),
        'output_filename': 'js/firefox_new_scene2-bundle.js',
    },
    'firefox_new_scene1_wait_face': {
        'source_filenames': (
            'js/firefox/new/wait-face-scene1.js',
        ),
        'output_filename': 'js/firefox_new_scene1_wait_face-bundle.js',
    },
    'firefox_new_scene1_reggie_watts': {
        'source_filenames': (
            'js/firefox/new/reggie-watts-scene1.js',
        ),
        'output_filename': 'js/firefox_new_scene1_reggie_watts-bundle.js',
    },
    'firefox_new_scene1_portland': {
        'source_filenames': (
            'js/firefox/new/portland-scene1.js',
        ),
        'output_filename': 'js/firefox_new_scene1_portland-bundle.js',
    },
    'firefox_new_pixel': {
        'source_filenames': (
            'js/base/mozilla-pixel.js',
            'js/base/mozilla-pixel-init.js',
        ),
        'output_filename': 'js/firefox_new_pixel-bundle.js',
    },
    'firefox_feedback': {
        'source_filenames': (
            'js/base/mozilla-share-cta.js',
        ),
        'output_filename': 'js/firefox_feedback-bundle.js',
    },
    'firefox-mobile': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/base/send-to-device.js',
            'js/base/mozilla-smoothscroll.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/hubs/sub-nav.js',
            'js/firefox/mobile/features-scroller.js',
            'js/firefox/mobile/mobile.js',
        ),
        'output_filename': 'js/firefox_mobile-bundle.js',
    },
    'firefox-switch': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/hubs/sub-nav.js',
        ),
        'output_filename': 'js/firefox-switch-bundle.js',
    },
    'firefox_tour_none': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/base/uitour-lib.js',
            'js/firefox/australis/common.js',
            'js/firefox/australis/no-tour.js',
        ),
        'output_filename': 'js/firefox_tour_none-bundle.js',
    },
    'firefox_whatsnew': {
        'source_filenames': (
            'js/base/send-to-device.js',
            'js/firefox/whatsnew/whatsnew.js',
        ),
        'output_filename': 'js/firefox_whatsnew-bundle.js',
    },
    'firefox_whatsnew_fxa': {
        'source_filenames': (
            'js/base/uitour-lib.js',
            'js/base/mozilla-fxa-iframe.js',
            'js/firefox/whatsnew/whatsnew-fxa.js',
        ),
        'output_filename': 'js/firefox_whatsnew_fxa-bundle.js',
    },
    'firefox-update-notification': {
        'source_filenames': (
            'js/base/mozilla-notification-banner.js',
            'js/base/mozilla-notification-banner-init.js',
        ),
        'output_filename': 'js/firefox-update-notification-bundle.js',
    },
    'firefox-update-notification-firstrun-whatsnew': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/base/mozilla-notification-banner.js',
            'js/base/mozilla-notification-banner-firstrun-whatsnew-init.js',
        ),
        'output_filename': 'js/firefox-update-notification-firstrun-whatsnew-bundle.js',
    },
    'home': {
        'source_filenames': (
            'js/libs/jquery.cycle2.min.js',
            'js/libs/jquery.waypoints.min.js',
            'js/mozorg/home/home.js',
        ),
        'output_filename': 'js/home-bundle.js',
    },
    'history-slides': {
        'source_filenames': (
            'js/libs/jquery.sequence.js',
            'js/mozorg/history-slides.js',
        ),
        'output_filename': 'js/history-slides-bundle.js',
    },
    'installer_help': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/firefox/installer-help.js',
        ),
        'output_filename': 'js/installer_help-bundle.js',
    },
    'internet-health-hub': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/hubs/sub-nav.js',
        ),
        'output_filename': 'js/internet-health-hub-bundle.js',
    },
    'internet-health-subpage': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/hubs/sub-nav.js',
            'js/base/mozilla-smoothscroll.js',
            'js/mozorg/internet-health/health-subpage.js',
        ),
        'output_filename': 'js/internet-health-subpage-bundle.js',
    },
    'privacy-day-egg': {
        'source_filenames': (
            'js/libs/konami-code.js',
            'js/mozorg/internet-health/privacy-day-egg.js',
        ),
        'output_filename': 'js/privacy-day-egg-bundle.js',
    },
    'legal_fraud_report': {
        'source_filenames': (
            'js/libs/jquery.validate.js',
            'js/legal/fraud-report.js',
        ),
        'output_filename': 'js/legal_fraud_report-bundle.js',
    },
    'manifesto': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/base/mozilla-share-cta.js',
            'js/mozorg/manifesto.js',
        ),
        'output_filename': 'js/manifesto-bundle.js',
    },
    'about_video': {
        'source_filenames': (
            'js/base/mozilla-video-poster.js',
            'js/mozorg/about-video.js',
        ),
        'output_filename': 'js/about_video-bundle.js',
    },
    'newsletter-mozilla': {
        'source_filenames': (
            'js/newsletter/mozilla.js',
        ),
        'output_filename': 'js/newsletter-mozilla.js',
    },
    'newsletter-developer': {
        'source_filenames': (
            'js/newsletter/developer.js',
        ),
        'output_filename': 'js/newsletter-developer.js',
    },
    'newsletter-firefox': {
        'source_filenames': (
            'js/newsletter/firefox.js',
        ),
        'output_filename': 'js/newsletter-firefox.js',
    },
    'plugincheck': {
        'source_filenames': (
            'js/plugincheck/plugincheck.js',
        ),
        'output_filename': 'js/plugincheck-bundle.js',
    },
    'press_speaker_request': {
        'source_filenames': (
            'js/libs/jquery.validate.js',
            'js/libs/modernizr.custom.inputtypes.js',
            'js/press/speaker-request.js',
        ),
        'output_filename': 'js/press_speaker_request-bundle.js',
    },
    'privacy_quantum': {
        'source_filenames': (
            'js/privacy/privacy-quantum.js',
        ),
        'output_filename': 'js/privacy-quantum-bundle.js',
    },
    'privacy_quantum_firefox': {
        'source_filenames': (
            'js/base/uitour-lib.js',
            'js/privacy/privacy-quantum.js',
            'js/privacy/privacy-quantum-firefox.js',
        ),
        'output_filename': 'js/privacy-quantum-firefox-bundle.js',
    },
    'privacy': {
        'source_filenames': (
            'js/privacy/privacy.js',
        ),
        'output_filename': 'js/privacy-bundle.js',
    },
    'smarton': {
        'source_filenames': (
            'js/base/mozilla-share-cta.js',
            'js/base/mozilla-smoothscroll.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/libs/circles.min.js',
            'js/teach/smarton.js',
        ),
        'output_filename': 'js/smarton-bundle.js',
    },
    'smarton-landing': {
        'source_filenames': (
            'js/base/mozilla-share-cta.js',
            'js/libs/snap.svg.js',
            'js/teach/smarton-landing.js',
        ),
        'output_filename': 'js/smarton-landing-bundle.js',
    },
    'stub-attribution': {
        'source_filenames': (
            'js/base/stub-attribution.js',
            'js/base/stub-attribution-init.js',
        ),
        'output_filename': 'js/stub-attribution-bundle.js',
    },
    'technology': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/hubs/sub-nav.js',
            'js/base/mozilla-modal.js',
            'js/mozorg/technology.js',
        ),
        'output_filename': 'js/technology-bundle.js',
    },
    'tracking-protection-tour': {
        'source_filenames': (
            'js/libs/jquery-3.2.1.min.js',
            'js/base/uitour-lib.js',
            'js/firefox/tracking-protection-tour.js',
            'js/firefox/tracking-protection-tour-init.js',
        ),
        'output_filename': 'js/tracking-protection-tour-bundle.js',
    },
    'annual_2011': {
        'source_filenames': (
            'js/libs/jquery.hoverIntent.min.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.jcarousel.min.js',
            'js/foundation/annual2011.js',
        ),
        'output_filename': 'js/annual_2011-bundle.js',
    },
    'annual_2012': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/foundation/annual2012.js',
        ),
        'output_filename': 'js/annual_2012-bundle.js',
    },
    'annual_2013': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/foundation/annual2013.js',
        ),
        'output_filename': 'js/annual_2013-bundle.js',
    },
    'releasenotes': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/firefox/releasenotes.js',
        ),
        'output_filename': 'js/releasenotes-bundle.js',
    },
    'thunderbird-all': {
        'source_filenames': (
            'js/base/mozilla-pager.js',
            'js/firefox/firefox-language-search.js',
        ),
        'output_filename': 'js/thunderbird_all-bundle.js',
    },
    'matchmedia': {
        'source_filenames': (
            'js/libs/matchMedia.js',
            'js/libs/matchMedia.addListener.js',
        ),
        'output_filename': 'js/matchmedia-bundle.js',
    },
    'matchmedia_addlistener': {
        'source_filenames': (
            'js/libs/matchMedia.addListener.js',
        ),
        'output_filename': 'js/matchmedia_addlistener-bundle.js',
    },
    'etc-firefox-retention-thank-you': {
        'source_filenames': (
            'js/etc/firefox/retention/confetti.js',
        ),
        'output_filename': 'js/etc-firefox-retention-thank-you-bundle.js',
    }
}
