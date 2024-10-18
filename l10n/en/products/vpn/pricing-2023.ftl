# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

### URL: https://www-dev.allizom.org/products/vpn/pricing/

vpn-pricing-page-title = Pricing - { -brand-name-mozilla-vpn }
vpn-pricing-mozilla-vpn = { -brand-name-mozilla-vpn }

# HTML page title
vpn-pricing-one-subscription = One subscription for all your devices

# Pricing section
vpn-pricing-included-in-subscription = Included in subscription:

# Variables:
#   $devices (number) - number of devices users can connect to VPN
vpn-pricing-connect-up-to = { $devices ->
    [one] Connect up to { $devices } device
   *[other] Connect up to { $devices } devices
}

# Variables:
#   $devices (number) - number of devices users can connect to VPN
vpn-pricing-connect-up-to-platforms = { $devices ->
    [one] Connect up to { $devices } Android, iOS, Windows, macOS or Linux device
   *[other] Connect up to { $devices } Android, iOS, Windows, macOS or Linux devices
}

# Variables:
#   $servers (number) - number of VPN servers
#   $countries (number) - number of available countries
vpn-pricing-access = { $servers ->
    [one] Access { $servers } server in { $countries }+ countries
   *[other] Access { $servers } servers in { $countries }+ countries
}
vpn-pricing-money-back = 30-day money-back guarantee (for first-time customers only)
vpn-pricing-annual = Annual
vpn-pricing-monthly = Monthly
vpn-pricing-get-annual-subscription = Get annual subscription
vpn-pricing-get-monthly-subscription = Get monthly subscription
vpn-pricing-vpn-not-available = { -brand-name-mozilla-vpn } is not yet available in your country

# FAQs is short for Frequently Asked Questions
vpn-pricing-faqs = FAQs
vpn-pricing-refund-policy = What is { -brand-name-mozilla-vpn }’s refund policy?
vpn-pricing-the-first-time-you = The first time you subscribe to { -brand-name-mozilla-vpn } through { -brand-name-mozilla }’s website, if you cancel your account within the first 30 days, you may request a refund and { -brand-name-mozilla } will refund your first subscription term.
vpn-pricing-if-you-purchased = If you purchased your subscription through in-app purchase from the Apple App Store or the Google Play Store, your payment is subject to the terms and conditions of the store. You must direct any billing and refund inquiries for such purchases to Apple or Google, as appropriate.

vpn-pricing-what-information = What information does { -brand-name-mozilla-vpn } keep?

# Variables
#   $principles (url) - link to https://www.mozilla.org/privacy/principles/
#   $notice (url) - link to https://www.mozilla.org/privacy/subscription-services/
vpn-pricing-we-adhere-strictly = We adhere strictly to { -brand-name-mozilla }’s <a { $principles }>Data Privacy Principles</a>. We only collect data required to keep { -brand-name-mozilla-vpn } operational and improve the product over time. We also track campaign and referral data on our mobile app to help { -brand-name-mozilla } understand the effectiveness of our marketing campaigns. Read more in our <a { $notice }>Privacy Notice</a>.

vpn-pricing-how-do-i-manage = How do I manage my subscription and change my plan?

# Variables
# $manage (url) - link to subscription management page
vpn-pricing-if-already-subscribed = If you’re already subscribed to { -brand-name-mozilla-vpn }, you can change your plan or <a { $manage }>manage your subscription</a> anytime.

## Mobile only subscription copy

vpn-pricing-scan-qrcode-to-download = To download the app, scan the QR Code with your mobile device or tablet
vpn-pricing-scan-qrcode-to-download-android = To download the app, scan the QR Code with your Android device or tablet
vpn-pricing-sign-up-on-your-mobile-device = Sign up for a { -brand-name-mozilla-vpn } subscription on your mobile device
vpn-pricing-sign-up-on-your-android-device = Sign up for a { -brand-name-mozilla-vpn } subscription on your Android device
vpn-pricing-download-the-app = Download the app
