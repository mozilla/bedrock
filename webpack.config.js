const path = require('path');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const MiniCssExtractPlugin  = require('mini-css-extract-plugin')
const CopyPlugin = require('copy-webpack-plugin')

function resolveBundles(fileList){
  return fileList.map((f) => {
    if (f.match(/^protocol\//)) {
      return `@mozilla-protocol/core/${f}`;
    }
    return path.resolve(__dirname, "media", f);
  });
}

const entry = {
  "about": resolveBundles([
    "css/mozorg/about.scss",
    "js/base/mozilla-lazy-load.js",
    "js/mozorg/about.js",
    "js/newsletter/form-protocol.js",
    "protocol/js/protocol-newsletter.js"
  ]),
  "about-forums": resolveBundles([
    "css/mozorg/about-forums.scss"
  ]),
  "about-leadership": resolveBundles([
    "css/mozorg/leadership.scss",
    "css/newsletter/moznewsletter-subscribe.less",
    "js/base/mozilla-modal.js",
    "js/mozorg/about-leadership.js"
  ]),
  "about-patents": resolveBundles([
    "css/mozorg/about-patents.scss"
  ]),
  "about-transparency": resolveBundles([
    "css/mozorg/about-transparency.scss",
    "js/mozorg/about-transparency.js"
  ]),
  "adblocker": resolveBundles([
    "css/firefox/features/adblocker.scss"
  ]),
  "annual_report": resolveBundles([
    "css/foundation/annual-report.scss"
  ]),
  "annual_report_2011": resolveBundles([
    "css/foundation/annual-report-2011.scss"
  ]),
  "basic-article": resolveBundles([
    "css/protocol/basic-article.scss",
    "js/base/mozilla-article.js",
    "js/newsletter/form-protocol.js",
    "protocol/js/protocol-newsletter.js",
    "protocol/js/protocol-sidemenu.js"
  ]),
  "bestbrowser": resolveBundles([
    "css/firefox/bestbrowser.scss"
  ]),
  "book": resolveBundles([
    "css/mozorg/book.scss"
  ]),
  "browser-history": resolveBundles([
    "css/mozorg/browser-history.scss"
  ]),
  "browser-test": resolveBundles([
    "css/mozorg/browser-test.scss"
  ]),
  "commit-access-requirements": resolveBundles([
    "css/mozorg/commit-access-requirements.scss"
  ]),
  "common": resolveBundles([
    "js/base/base-page-init.js",
    "js/base/class-list-polyfill.js",
    "js/base/core-datalayer-init.js",
    "js/base/core-datalayer.js",
    "js/base/fxa-utm-referral-init.js",
    "js/base/fxa-utm-referral.js",
    "js/base/mozilla-client.js",
    "js/base/mozilla-fxa-sign-in-link.js",
    "js/base/mozilla-run.js",
    "js/base/mozilla-utils.js",
    "js/base/protocol/init-lang-switcher.js",
    "js/base/protocol/init-navigation.js",
    "js/base/search-params.js",
    "js/libs/jquery-3.4.1.min.js",
    "js/libs/spin.min.js",
    "js/newsletter/form.js",
    "protocol/js/protocol-details.js",
    "protocol/js/protocol-footer.js",
    "protocol/js/protocol-lang-switcher.js",
    "protocol/js/protocol-menu.js",
    "protocol/js/protocol-navigation.js",
    "protocol/js/protocol-supports.js",
    "protocol/js/protocol-utils.js"
  ]),
  "common-ie": resolveBundles([
    "js/base/core-datalayer-init.js",
    "js/base/core-datalayer.js",
    "js/base/mozilla-client.js",
    "js/base/search-params.js",
    "js/ie/base-page-init-ie.js",
    "js/ie/mozilla-utils-ie.js",
    "js/libs/jquery-1.11.3.min.js"
  ]),
  "common-protocol": resolveBundles([
    "js/base/base-page-init.js",
    "js/base/class-list-polyfill.js",
    "js/base/core-datalayer-init.js",
    "js/base/core-datalayer.js",
    "js/base/fxa-utm-referral-init.js",
    "js/base/fxa-utm-referral.js",
    "js/base/mozilla-client.js",
    "js/base/mozilla-fxa-sign-in-link.js",
    "js/base/mozilla-run.js",
    "js/base/mozilla-utils.js",
    "js/base/protocol/init-lang-switcher.js",
    "js/base/protocol/init-navigation.js",
    "js/base/search-params.js",
    "js/libs/jquery-3.4.1.min.js",
    "protocol/js/protocol-details.js",
    "protocol/js/protocol-footer.js",
    "protocol/js/protocol-lang-switcher.js",
    "protocol/js/protocol-menu.js",
    "protocol/js/protocol-navigation.js",
    "protocol/js/protocol-supports.js",
    "protocol/js/protocol-utils.js"
  ]),
  "common-protocol-no-jquery": resolveBundles([
    "js/base/base-page-init.js",
    "js/base/class-list-polyfill.js",
    "js/base/core-datalayer-init.js",
    "js/base/core-datalayer.js",
    "js/base/fxa-utm-referral-init.js",
    "js/base/fxa-utm-referral.js",
    "js/base/mozilla-client.js",
    "js/base/mozilla-fxa-sign-in-link.js",
    "js/base/mozilla-run.js",
    "js/base/mozilla-utils.js",
    "js/base/protocol/init-lang-switcher.js",
    "js/base/protocol/init-navigation.js",
    "js/base/search-params.js",
    "protocol/js/protocol-details.js",
    "protocol/js/protocol-footer.js",
    "protocol/js/protocol-lang-switcher.js",
    "protocol/js/protocol-menu.js",
    "protocol/js/protocol-navigation.js",
    "protocol/js/protocol-supports.js",
    "protocol/js/protocol-utils.js"
  ]),
  "contact-spaces": resolveBundles([
    "css/libs/magnific-popup.css",
    "css/mozorg/contact-spaces.scss",
    "js/libs/jquery.magnific-popup.min.js",
    "js/mozorg/contact-spaces.js"
  ]),
  "contribute-base": resolveBundles([
    "css/base/mozilla-modal.less",
    "css/mozorg/contribute/contribute-base.less",
    "js/mozorg/contribute/contribute-nav.js"
  ]),
  "contribute-embed": resolveBundles([
    "css/mozorg/contribute/contribute-embed.less"
  ]),
  "contribute-landing": resolveBundles([
    "js/base/mozilla-modal.js",
    "js/libs/jquery.cycle2.min.js",
    "js/libs/jquery.waypoints.min.js",
    "js/mozorg/contribute/contribute-landing.js"
  ]),
  "contribute-stories": resolveBundles([
    "js/mozorg/contribute/contribute-stories.js"
  ]),
  "convert": resolveBundles([
    "js/exp/convert.js",
    "js/libs/jquery-3.4.1.min.js"
  ]),
  "credits": resolveBundles([
    "css/mozorg/credits.scss"
  ]),
  "csrf-failure": resolveBundles([
    "css/csrf-failure.scss"
  ]),
  "css-grid-demo": resolveBundles([
    "js/base/mozilla-smoothscroll.js",
    "js/libs/jquery.waypoints.min.js",
    "js/libs/jquery.waypoints-sticky.min.js",
    "js/mozorg/developer/css-grid-demo.js"
  ]),
  "developer-hub": resolveBundles([
    "css/base/mozilla-modal.less",
    "css/mozorg/developer/index.scss",
    "js/base/mozilla-lazy-load.js",
    "js/base/mozilla-modal.js",
    "js/hubs/sub-nav.js",
    "js/libs/jquery.waypoints-sticky.min.js",
    "js/libs/jquery.waypoints.min.js",
    "js/mozorg/developer/developer-hub.js"
  ]),
  "etc-firefox-retention-thank-you": resolveBundles([
    "js/etc/firefox/retention/confetti.js"
  ]),
  "etc-firefox-retention-thank-you-a": resolveBundles([
    "css/etc/firefox/retention/thank-you-a.scss",
    "css/etc/firefox/retention/thank-you.scss"
  ]),
  "etc-firefox-retention-thank-you-b": resolveBundles([
    "css/etc/firefox/retention/thank-you-b.scss",
    "css/etc/firefox/retention/thank-you.scss"
  ]),
  "etc-firefox-retention-thank-you-referral": resolveBundles([
    "css/etc/firefox/retention/thank-you-referral.scss",
    "css/etc/firefox/retention/thank-you.scss"
  ]),
  "exp-firefox-home-ie9": resolveBundles([
    "css/exp/firefox/index-ie9.scss"
  ]),
  "exp-firefox-index": resolveBundles([
    "css/base/mozilla-lazy-image.scss",
    "css/exp/firefox/index.scss",
    "js/base/mozilla-lazy-load.js",
    "js/exp/firefox/index.js"
  ]),
  "exp-firefox-new": resolveBundles([
    "css/exp/firefox/new/download.scss"
  ]),
  "exp-lockwise": resolveBundles([
    "css/exp/firefox/lockwise.scss",
    "js/base/uitour-lib.js",
    "js/exp/firefox/lockwise.js"
  ]),
  "exp-opt-out": resolveBundles([
    "css/exp/opt-out.scss"
  ]),
  "exp_firefox_welcome": resolveBundles([
    "css/exp/firefox/welcome.scss"
  ]),
  "exp_firefox_welcome_page": resolveBundles([
    "js/base/mozilla-fxa-product-button-init.js",
    "js/base/mozilla-fxa-product-button.js"
  ]),
  "firefox_whatsnew_71": resolveBundles([
    "css/firefox/whatsnew/whatsnew-71.scss"
  ]),
  "exp_firefox_whatsnew_71": resolveBundles([
    "css/exp/firefox/whatsnew/whatsnew-71.scss"
  ]),
  "firefox-enterprise": resolveBundles([
    "css/firefox/enterprise/landing.scss",
    "js/firefox/enterprise/landing.js"
  ]),
  "firefox-enterprise-signup": resolveBundles([
    "css/firefox/enterprise/signup.scss"
  ]),
  "firefox-enterprise-sla": resolveBundles([
    "css/firefox/enterprise/sla.scss",
    "js/firefox/enterprise/sla.js"
  ]),
  "firefox-features-hub": resolveBundles([
    "js/hubs/sub-nav.js",
    "js/libs/jquery.waypoints-sticky.min.js",
    "js/libs/jquery.waypoints.min.js"
  ]),
  "firefox-features-hub-common": resolveBundles([
    "css/firefox/features/common.scss"
  ]),
  "firefox-features-hub-detail": resolveBundles([
    "css/firefox/features/detail.scss"
  ]),
  "firefox-features-index": resolveBundles([
    "css/firefox/features/index.scss"
  ]),
  "firefox-home-ie9": resolveBundles([
    "css/firefox/home/ie9.scss"
  ]),
  "firefox-master": resolveBundles([
    "css/base/mozilla-lazy-image.scss",
    "css/firefox/home/master.scss",
    "js/base/mozilla-lazy-load.js",
    "js/firefox/home/master.js"
  ]),
  "firefox-mobile": resolveBundles([
    "css/base/send-to-device.less",
    "css/firefox/mobile.scss",
    "js/base/mozilla-modal.js",
    "js/base/mozilla-smoothscroll.js",
    "js/base/send-to-device.js",
    "js/firefox/mobile/features-scroller.js",
    "js/firefox/mobile/mobile.js",
    "js/hubs/sub-nav.js",
    "js/libs/jquery.waypoints-sticky.min.js",
    "js/libs/jquery.waypoints.min.js"
  ]),
  "firefox-mobile-protocol": resolveBundles([
    "css/firefox/mobile-protocol.scss",
    "css/protocol/components/send-to-device.scss",
    "js/base/send-to-device.js",
    "js/firefox/mobile/mobile-protocol.js",
    "js/hubs/sub-nav.js",
    "js/libs/jquery.waypoints-sticky.min.js",
    "js/libs/jquery.waypoints.min.js",
    "js/libs/spin.min.js",
    "protocol/js/protocol-modal.js"
  ]),
  "firefox-privacy-common": resolveBundles([
    "css/firefox/privacy/common.scss"
  ]),
  "firefox-privacy-products": resolveBundles([
    "css/firefox/privacy/products.scss",
    "js/base/mozilla-fxa-form-init.js",
    "js/base/mozilla-fxa-form.js",
    "js/base/uitour-lib.js",
    "js/firefox/privacy/products.js"
  ]),
  "firefox-privacy-promise": resolveBundles([
    "css/firefox/privacy/promise.scss"
  ]),
  "firefox-quantum": resolveBundles([
    "css/base/mozilla-lazy-image.scss",
    "css/firefox/home/quantum.scss",
    "js/base/mozilla-lazy-load.js",
    "js/firefox/home/quantum.js",
    "js/libs/jquery.waypoints.min.js"
  ]),
  "firefox-switch": resolveBundles([
    "css/firefox/switch.scss",
    "js/hubs/sub-nav.js",
    "js/libs/jquery.waypoints-sticky.min.js",
    "js/libs/jquery.waypoints.min.js"
  ]),
  "firefox-update-notification": resolveBundles([
    "js/base/mozilla-notification-banner-init.js",
    "js/base/mozilla-notification-banner.js"
  ]),
  "firefox-update-notification-firstrun-whatsnew": resolveBundles([
    "css/base/mozilla-modal.less",
    "css/base/notification-banner.less",
    "css/base/notification-modal.less",
    "js/base/mozilla-modal.js",
    "js/base/mozilla-notification-banner-firstrun-whatsnew-init.js",
    "js/base/mozilla-notification-banner.js"
  ]),
  "firefox-whatsnew-lite": resolveBundles([
    "css/firefox/whatsnew/whatsnew-lite.scss",
    "css/protocol/components/send-to-device.scss"
  ]),
  "firefox-whatsnew-lite-in": resolveBundles([
    "css/firefox/whatsnew/whatsnew-lite-in.scss"
  ]),
  "firefox_accounts_2019": resolveBundles([
    "css/base/mozilla-fxa-form.scss",
    "css/base/mozilla-fxa-state.scss",
    "css/firefox/accounts-2019.scss",
    "js/base/mozilla-fxa-form.js",
    "js/base/mozilla-fxa-init.js",
    "js/base/mozilla-fxa-product-button.js",
    "js/base/mozilla-fxa.js",
    "js/firefox/accounts-2019.js"
  ]),
  "firefox_all_unified": resolveBundles([
    "css/firefox/all/all-unified.scss",
    "js/firefox/all/all-downloads-unified-init.js",
    "js/firefox/all/all-downloads-unified.js",
    "protocol/js/protocol-modal.js",
    "protocol/js/protocol-sidemenu.js"
  ]),
  "firefox_all_unified_old_ie": resolveBundles([
    "css/firefox/all/all-unified-old-ie.scss"
  ]),
  "firefox_campaign": resolveBundles([
    "css/firefox/campaign/campaign.scss"
  ]),
  "firefox_campaign_berlin": resolveBundles([
    "css/firefox/campaign/berlin.scss"
  ]),
  "firefox_campaign_berlin_aus_gruenden": resolveBundles([
    "css/firefox/campaign/berlin-aus-gruenden.scss",
    "css/firefox/campaign/berlin.scss"
  ]),
  "firefox_campaign_berlin_variation": resolveBundles([
    "css/firefox/campaign/berlin-variation.scss"
  ]),
  "firefox_campaign_better_browser": resolveBundles([
    "css/firefox/campaign/better-browser.scss"
  ]),
  "firefox_campaign_compare": resolveBundles([
    "css/firefox/campaign/compare.scss"
  ]),
  "firefox_campaign_scene1_berlin": resolveBundles([
    "js/firefox/campaign/berlin-scene1.js",
    "js/firefox/new/variation-scene1.js"
  ]),
  "firefox_campaign_scene1_berlin_variation": resolveBundles([
    "js/firefox/campaign/berlin-scene1-variation.js",
    "js/firefox/new/variation-scene1.js"
  ]),
  "firefox_campaign_trailhead": resolveBundles([
    "css/firefox/campaign/download.scss"
  ]),
  "firefox_channel": resolveBundles([
    "css/firefox/channel.less",
    "css/newsletter/fxnewsletter-subscribe.less"
  ]),
  "firefox_concert_series": resolveBundles([
    "css/base/mozilla-fxa-state.scss",
    "css/firefox/concerts.scss",
    "js/firefox/concerts-init.js",
    "js/firefox/concerts.js",
    "js/newsletter/form-protocol.js",
    "protocol/js/protocol-modal.js",
    "protocol/js/protocol-newsletter.js"
  ]),
  "firefox_developer": resolveBundles([
    "css/firefox/developer/developer.scss",
    "js/newsletter/form-protocol.js",
    "protocol/js/protocol-newsletter.js"
  ]),
  "firefox_election": resolveBundles([
    "css/base/mozilla-lazy-image.scss",
    "css/firefox/election.scss",
    "js/base/mozilla-lazy-load.js",
    "js/firefox/election.js",
    "protocol/js/protocol-modal.js"
  ]),
  "firefox_facebook_container": resolveBundles([
    "css/firefox/facebook-container.scss"
  ]),
  "firefox_facebook_container_video": resolveBundles([
    "js/base/mozilla-video-poster.js",
    "js/firefox/facebook-container-video.js"
  ]),
  "firefox_firstrun_quantum": resolveBundles([
    "css/base/mozilla-fxa-form.scss",
    "css/firefox/firstrun/firstrun.scss",
    "js/base/mozilla-fxa-form-init.js",
    "js/base/mozilla-fxa-form.js"
  ]),
  "firefox_ios_testflight": resolveBundles([
    "css/firefox/testflight.less"
  ]),
  "firefox_new_common": resolveBundles([
    "css/firefox/new/common.scss"
  ]),
  "firefox_new_download": resolveBundles([
    "css/firefox/new/trailhead/download.scss",
    "js/firefox/new/trailhead/download.js",
    "protocol/js/protocol-modal.js"
  ]),
  "firefox_new_download_join_modal": resolveBundles([
    "js/firefox/new/trailhead/join-modal.js"
  ]),
  "firefox_new_pixel": resolveBundles([
    "js/base/mozilla-pixel-init.js",
    "js/base/mozilla-pixel.js"
  ]),
  "firefox_new_scene1": resolveBundles([
    "css/base/mozilla-fxa-form.scss",
    "css/firefox/new/scene1.scss",
    "js/base/mozilla-modal.js",
    "js/firefox/new/scene1.js"
  ]),
  "firefox_new_scene1_fxa_modal": resolveBundles([
    "js/base/mozilla-fxa-form-init.js",
    "js/base/mozilla-fxa-form.js",
    "js/firefox/new/scene1_fxa_modal.js"
  ]),
  "firefox_new_scene1_gb_de": resolveBundles([
    "css/firefox/new/scene1.scss",
    "css/firefox/new/scene1_gb_de.scss"
  ]),
  "firefox_new_scene1_variation": resolveBundles([
    "js/firefox/new/variation-scene1.js"
  ]),
  "firefox_new_scene1_yandex": resolveBundles([
    "css/firefox/new/scene1.scss",
    "css/firefox/new/yandex-scene1.scss",
    "js/base/mozilla-modal.js",
    "js/firefox/new/yandex/scene1-init.js",
    "js/firefox/new/yandex/scene1.js"
  ]),
  "firefox_new_scene2": resolveBundles([
    "css/firefox/new/scene2.scss",
    "js/firefox/new/scene2.js"
  ]),
  "firefox_new_scene2_email": resolveBundles([
    "js/firefox/new/scene2-email.js",
    "js/newsletter/form-protocol.js",
    "protocol/js/protocol-modal.js",
    "protocol/js/protocol-newsletter.js"
  ]),
  "firefox_new_thanks": resolveBundles([
    "css/firefox/new/trailhead/thanks.scss",
    "js/firefox/new/scene2.js"
  ]),
  "firefox_recommended": resolveBundles([
    "css/firefox/recommended.scss"
  ]),
  "firefox_releasenotes": resolveBundles([
    "css/firefox/releasenotes.scss"
  ]),
  "firefox_releases_index": resolveBundles([
    "css/firefox/releases-index.scss"
  ]),
  "firefox_system_requirements": resolveBundles([
    "css/firefox/system-requirements.scss"
  ]),
  "firefox_unsupported_systems": resolveBundles([
    "css/firefox/unsupported-systems.scss"
  ]),
  "firefox_welcome": resolveBundles([
    "css/firefox/welcome.scss"
  ]),
  "firefox_welcome_page": resolveBundles([
    "js/base/mozilla-fxa-product-button-init.js",
    "js/base/mozilla-fxa-product-button.js"
  ]),
  "firefox_whatsnew": resolveBundles([
    "css/firefox/whatsnew/whatsnew.scss",
    "css/protocol/components/send-to-device.scss",
    "js/base/send-to-device.js",
    "js/base/uitour-lib.js",
    "js/firefox/whatsnew/up-to-date.js",
    "js/firefox/whatsnew/whatsnew.js",
    "js/libs/spin.min.js"
  ]),
  "firefox_whatsnew_67": resolveBundles([
    "css/firefox/whatsnew/whatsnew-67.scss",
    "js/base/mozilla-fxa-form-init.js",
    "js/base/mozilla-fxa-form.js",
    "js/base/mozilla-fxa-init.js",
    "js/base/mozilla-fxa.js",
    "js/base/uitour-lib.js",
    "js/firefox/whatsnew/whatsnew-67.js",
    "protocol/js/protocol-modal.js"
  ]),
  "firefox_whatsnew_67.0.5": resolveBundles([
    "css/firefox/whatsnew/whatsnew-67.0.5.scss",
    "js/base/mozilla-fxa-form.js",
    "js/base/mozilla-fxa-init.js",
    "js/base/mozilla-fxa-product-button.js",
    "js/base/mozilla-fxa.js",
    "js/base/uitour-lib.js",
    "js/firefox/whatsnew/account-conditional-ctas.js",
    "js/firefox/whatsnew/up-to-date.js"
  ]),
  "firefox_whatsnew_67_newsletter": resolveBundles([
    "js/newsletter/form-protocol.js",
    "protocol/js/protocol-newsletter.js"
  ]),
  "firefox_whatsnew_69": resolveBundles([
    "css/firefox/whatsnew/whatsnew-69.scss",
    "js/base/mozilla-fxa-init.js",
    "js/base/mozilla-fxa-product-button.js",
    "js/base/mozilla-fxa.js",
    "js/base/uitour-lib.js",
    "js/firefox/whatsnew/up-to-date.js",
    "js/firefox/whatsnew/whatsnew-69.js"
  ]),
  "firefox_whatsnew_70": resolveBundles([
    "css/firefox/whatsnew/whatsnew-70.scss"
  ]),
  "firefox_whatsnew_70_experiment_fxaform": resolveBundles([
    "js/base/mozilla-fxa-form-init.js",
    "js/base/mozilla-fxa-form.js",
    "js/base/uitour-lib.js",
    "js/firefox/whatsnew/up-to-date.js",
    "js/firefox/whatsnew/whatsnew-70.js"
  ]),
  "firefox_whatsnew_70_experiment_syncbutton": resolveBundles([
    "js/base/mozilla-fxa-product-button-init.js",
    "js/base/mozilla-fxa-product-button.js",
    "js/base/uitour-lib.js",
    "js/firefox/whatsnew/up-to-date.js",
    "js/firefox/whatsnew/whatsnew-70.js"
  ]),
  "firefox_whatsnew_70_variants": resolveBundles([
    "js/base/mozilla-fxa-init.js",
    "js/base/mozilla-fxa-product-button-init.js",
    "js/base/mozilla-fxa-product-button.js",
    "js/base/mozilla-fxa.js",
    "js/base/uitour-lib.js",
    "js/firefox/whatsnew/up-to-date.js",
    "js/firefox/whatsnew/whatsnew-70.js"
  ]),
  "foundation-feed-icon-guidelines": resolveBundles([
    "css/foundation/feed-icon-guidelines.scss"
  ]),
  "grants": resolveBundles([
    "css/grants/grants.scss"
  ]),
  "gtm-snippet": resolveBundles([
    "js/base/gtm-snippet.js"
  ]),
  "health-subpage": resolveBundles([
    "css/mozorg/internet-health/health-subpage.scss"
  ]),
  "home": resolveBundles([
    "css/mozorg/home/home.scss",
    "css/newsletter/moznewsletter-subscribe.less",
    "js/base/mozilla-lazy-load.js",
    "js/libs/jquery.waypoints.min.js",
    "js/mozorg/home/home.js",
    "js/mozorg/home/youtube.js",
    "js/newsletter/form-protocol.js",
    "protocol/js/protocol-modal.js",
    "protocol/js/protocol-newsletter.js"
  ]),
  "home-2018": resolveBundles([
    "css/mozorg/home/fundraiser.scss",
    "css/mozorg/home/home-2018.scss"
  ]),
  "home-fundraiser": resolveBundles([
    "js/mozorg/home/fundraiser.js"
  ]),
  "incognito-browser": resolveBundles([
    "css/mozorg/incognito-browser.scss"
  ]),
  "installer_help": resolveBundles([
    "css/firefox/installer-help.scss"
  ]),
  "internet-health-hub": resolveBundles([
    "css/mozorg/internet-health/index.scss",
    "js/hubs/sub-nav.js",
    "js/libs/jquery.waypoints-sticky.min.js",
    "js/libs/jquery.waypoints.min.js"
  ]),
  "internet-health-subpage": resolveBundles([
    "js/base/mozilla-smoothscroll.js",
    "js/hubs/sub-nav.js",
    "js/libs/jquery.waypoints-sticky.min.js",
    "js/libs/jquery.waypoints.min.js",
    "js/mozorg/internet-health/health-subpage.js"
  ]),
  "jquery": resolveBundles([
    "js/libs/jquery-3.4.1.min.js"
  ]),
  "lean-data": resolveBundles([
    "css/mozorg/lean-data.scss"
  ]),
  "legal": resolveBundles([
    "css/legal/legal.scss",
    "protocol/js/protocol-newsletter.js"
  ]),
  "locales": resolveBundles([
    "css/mozorg/locales.scss"
  ]),
  "lockwise": resolveBundles([
    "css/firefox/lockwise/lockwise.scss",
    "js/base/uitour-lib.js",
    "js/firefox/lockwise/lockwise.js"
  ]),
  "manifesto": resolveBundles([
    "css/mozorg/manifesto.scss",
    "js/base/mozilla-modal.js",
    "js/base/mozilla-share-cta.js",
    "js/mozorg/manifesto.js"
  ]),
  "mission": resolveBundles([
    "css/mozorg/mission.scss"
  ]),
  "moss": resolveBundles([
    "css/mozorg/moss/common.scss"
  ]),
  "mpl-1-1": resolveBundles([
    "css/mozorg/mpl-1-1.scss"
  ]),
  "mpl-1-1-annotated": resolveBundles([
    "css/mozorg/mpl-1-1-annotated.scss"
  ]),
  "mpl-2-0": resolveBundles([
    "css/mozorg/mpl-2-0.scss"
  ]),
  "mpl-differences": resolveBundles([
    "css/mozorg/mpl-differences.scss"
  ]),
  "namespaces": resolveBundles([
    "css/mozorg/namespaces.scss"
  ]),
  "newsletter": resolveBundles([
    "css/newsletter/newsletter.less"
  ]),
  "newsletter-developer": resolveBundles([
    "css/newsletter/newsletter-developer.scss",
    "js/newsletter/developer.js"
  ]),
  "newsletter-firefox": resolveBundles([
    "css/newsletter/newsletter-firefox.scss",
    "js/newsletter/firefox.js"
  ]),
  "newsletter-mozilla": resolveBundles([
    "css/newsletter/newsletter-mozilla.scss",
    "js/newsletter/mozilla.js"
  ]),
  "newsletter-opt-out-confirmation": resolveBundles([
    "css/newsletter/newsletter-opt-out-confirmation.scss"
  ]),
  "nightly_firstrun": resolveBundles([
    "css/firefox/nightly-firstrun.scss"
  ]),
  "nightly_whatsnew": resolveBundles([
    "css/firefox/whatsnew/whatsnew-nightly.scss"
  ]),
  "oldIE": resolveBundles([
    "css/sandstone/old-ie.scss",
    "css/sandstone/oldIE.less"
  ]),
  "oldIE-pebbles": resolveBundles([
    "css/pebbles/base/oldIE.scss"
  ]),
  "page_not_found": resolveBundles([
    "css/base/page-not-found.scss"
  ]),
  "participation-reporting": resolveBundles([
    "css/mozorg/participation-reporting.scss"
  ]),
  "partnerships-distribution": resolveBundles([
    "css/mozorg/partnerships-distribution.scss"
  ]),
  "pebbles": resolveBundles([
    "css/pebbles/global.scss",
    "css/pebbles/protocol-footer.scss",
    "css/pebbles/protocol-nav.scss"
  ]),
  "pebbles-basic": resolveBundles([
    "css/pebbles/basic.scss"
  ]),
  "plugincheck": resolveBundles([
    "css/plugincheck/plugincheck.scss",
    "js/plugincheck/plugincheck.js"
  ]),
  "press": resolveBundles([
    "css/press/press.scss"
  ]),
  "press_speaker_request": resolveBundles([
    "js/libs/modernizr.custom.inputtypes.js",
    "js/press/speaker-request.js"
  ]),
  "privacy-day-egg": resolveBundles([
    "css/mozorg/internet-health/privacy-day-egg.scss",
    "js/libs/konami-code.js",
    "js/mozorg/internet-health/privacy-day-egg.js"
  ]),
  "privacy_email": resolveBundles([
    "css/privacy/privacy-email.scss"
  ]),
  "privacy_firefox": resolveBundles([
    "js/base/uitour-lib.js",
    "js/privacy/privacy-firefox.js"
  ]),
  "privacy_protocol": resolveBundles([
    "css/privacy/privacy-protocol.scss",
    "js/base/mozilla-article.js",
    "js/privacy/privacy-protocol.js",
    "protocol/js/protocol-sidemenu.js"
  ]),
  "product_pocket": resolveBundles([
    "css/firefox/pocket.scss",
    "js/base/mozilla-fxa-product-button-init.js",
    "js/base/mozilla-fxa-product-button.js",
    "js/base/mozilla-lazy-load.js",
    "js/firefox/pocket.js"
  ]),
  "protocol-core": resolveBundles([
    "css/protocol/protocol.scss"
  ]),
  "protocol-oldIE": resolveBundles([
    "css/protocol/oldIE.scss"
  ]),
  "responsive": resolveBundles([
    "css/base/notification-banner.less",
    "css/sandstone/protocol-footer.scss",
    "css/sandstone/protocol-nav.scss",
    "css/sandstone/sandstone-resp.less",
    "css/tabzilla/tabzilla-static.less"
  ]),
  "safebrowser": resolveBundles([
    "css/firefox/features/safebrowser.scss"
  ]),
  "security": resolveBundles([
    "css/security/security.scss"
  ]),
  "security-bug-bounty-hall-of-fame": resolveBundles([
    "css/security/hall-of-fame.scss"
  ]),
  "site": resolveBundles([
    "js/base/core-datalayer-page-id.js",
    "js/base/dnt-helper.js",
    "js/base/mozilla-cookie-helper.js",
    "js/base/site.js"
  ]),
  "stub-attribution": resolveBundles([
    "js/base/stub-attribution-init.js",
    "js/base/stub-attribution.js"
  ]),
  "stub-attribution-custom": resolveBundles([
    "js/base/stub-attribution-custom.js",
    "js/base/stub-attribution.js"
  ]),
  "stub-attribution-macos": resolveBundles([
    "js/base/stub-attribution-macos-init.js",
    "js/base/stub-attribution-macos.js"
  ]),
  "styleguide": resolveBundles([
    "css/styleguide/styleguide.scss"
  ]),
  "technology": resolveBundles([
    "css/base/mozilla-modal.less",
    "css/mozorg/technology.scss",
    "js/base/mozilla-modal.js",
    "js/hubs/sub-nav.js",
    "js/libs/jquery.waypoints-sticky.min.js",
    "js/libs/jquery.waypoints.min.js",
    "js/mozorg/technology.js"
  ]),
  "update-browser": resolveBundles([
    "css/mozorg/update-browser.scss"
  ]),
  "what-is-a-browser": resolveBundles([
    "css/mozorg/what-is-a-browser.scss"
  ]),
  "whatsnew_lite": resolveBundles([
    "js/base/send-to-device.js",
    "js/base/uitour-lib.js",
    "js/firefox/whatsnew/whatsnew-id.js",
    "js/libs/spin.min.js"
  ]),
  "windows-64-bit": resolveBundles([
    "css/firefox/windows-64-bit.scss"
  ]),
};

module.exports = {
  entry: entry,
  output: {
    'filename': 'js/[name].js',
    'path': path.resolve(__dirname, "assets/"),
    'publicPath': '/media/',
  },

  plugins: [
    new UglifyJSPlugin(),
    new MiniCssExtractPlugin({'filename': 'css/[name].css'}),
  ],

  watchOptions: {
  // this is in milliseconds, causes the rebuild of assets to wait this amount of time to collect changes 
  // before kicking off any recompiling of assets.
    aggregateTimeout: 600, 
    ignored: /node_modules/
  },
  resolve: {
    alias: {
      media: path.resolve(__dirname, "media/"),
    },
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: [/node_modules/, /\.min.js$/, /libs/],
        use: 'babel-loader',
      },
      {
        test: /\.(scss|css)$/,
        exclude: /node_modules/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          "sass-loader"
        ]
      },
      {
        test: /\.less$/,
        exclude: /node_modules/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          {
            'loader': 'less-loader',
            'options': {
              javascriptEnabled: true,
            }
          },
        ]
      },
      {
        test: /\.(ico|jpe?g|png|ttf|eot|svg|woff(2)?)(\?[a-z0-9=&.]+)?$/i,
        loader: 'file-loader',
        options: {
          name: 'img/[path][name].[ext]',
        },
      },
      {
        enforce: 'pre',
        test: /\.js$/,
        exclude: [/node_modules/, /\.min.js$/, /libs/],
        loader: 'eslint-loader',
        options: {
          emitError: true,
          emitWarning: true,
          configFile: ".eslintrc.js",
          failOnError: false, // if this is on builds will fail until lint errors are handled
          cache: true, //caches last eslint issues to make building faster.
          fix: false, // if true it will change files to fix issues it possible.
        }
      },
    ]
  }
}
