# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

### URL: https://www-dev.allizom.org/products/vpn/

vpn-shared-product-name = { -brand-name-mozilla-vpn }
vpn-shared-subscribe-link = Get { -brand-name-mozilla-vpn }
vpn-shared-waitlist-link = Join the Waitlist
vpn-shared-sign-in-link = Already a subscriber?

# Outdated string
vpn-shared-available-countries-v4 = We currently offer { -brand-name-mozilla-vpn } in Austria, Belgium, Canada, France, Germany, Ireland, Italy, Malaysia, the Netherlands, New Zealand, Singapore, Spain, Switzerland, the UK, and the US.

vpn-shared-available-countries-v5 = We currently offer { -brand-name-mozilla-vpn } in Austria, Belgium, Canada, Finland, France, Germany, Ireland, Italy, Malaysia, the Netherlands, New Zealand, Singapore, Spain, Sweden, Switzerland, the UK, and the US.

# This is a standalone string that is typically displayed underneath a "Get Mozilla VPN" button.
vpn-shared-money-back-guarantee = 30-day money-back guarantee

# This string will be followed by a lockup of press logos for publications that have featured Mozilla VPN.
vpn-shared-featured-in = Featured in

vpn-shared-features-encrypt = Device-level encryption

# Variables:
#   $servers (number) - number of available servers
#   $countries (number) - number of available countries
vpn-shared-features-servers = { $servers }+ servers in { $countries }+ countries

vpn-shared-features-bandwidth = No bandwidth restrictions
vpn-shared-features-activity = No logging of your network activity
vpn-shared-features-activity-logs = No online activity logs now or ever

# Variables:
#   $countries (number) - number of available countries
vpn-shared-features-access-countries = Access to servers in { $countries }+ countries

# Variables:
#   $devices (number) - maximum number of connected devices
vpn-shared-features-devices = Option to connect up to { $devices } devices

# Variables:
#   $devices (number) - number of available devices
vpn-shared-features-protection = Protection for up to { $devices } devices

# Variables:
#   $servers (number) - number of available servers
#   $countries (number) - number of available countries
vpn-shared-features-server-countries = Connect to more than { $servers } servers in over { $countries } countries

# Variables:
#   $countries (number) - number of available countries
vpn-shared-countries-coming-soon = Available in { $countries } countries now. More regions coming soon

# Variables:
#   $url (number) - link to https://mullvad.net/servers/
#   $attrs (string) - specific attributes added to external links
vpn-shared-features-full-list-servers = See our full list of <a href="{ $url }" { $attrs }>servers</a>.

# Variables:
#   $countries (number) - number of available countries
vpn-shared-features-strong-servers = Strong servers in { $countries }+ countries

# Variables:
#   $devices (number) - number of available devices
vpn-shared-features-connect = Connect up to { $devices } devices

# This string is displayed as an item in a list of features.
vpn-shared-features-guarantee = 30-day money-back guarantee

vpn-shared-refund-policy = Refund Policy
vpn-shared-privacy-notice = Privacy Notice
vpn-shared-terms-conditions = Terms and Conditions
vpn-shared-wireguard-copyright = { -brand-name-wireguard } is a registered trademark of Jason A. Donenfeld

## Pricing options. Some offers may be only shown in select countries (e.g. German and France).

vpn-shared-pricing-variable-heading-v2 = Choose a subscription plan that works for you

# Outdated string
vpn-shared-pricing-variable-heading = Choose a plan that works for you

vpn-shared-pricing-variable-sub-heading = All of our plans include:
vpn-shared-pricing-recommended-offer = Recommended
vpn-shared-pricing-plan-6-month = 6 Month
vpn-shared-pricing-plan-12-month = 12 Month
vpn-shared-pricing-plan-monthly = Monthly

# Variables:
#   $amount (string) - a string containing the monthly subscription price together with the appropriate currency symbol e.g. 'US$4.99' or '6,99 €'.
vpn-shared-pricing-monthly = { $amount }<span>/month</span>

# Outdated string
vpn-shared-pricing-get-6-month = Get 6 month plan

# Outdated string
vpn-shared-pricing-get-12-month = Get 12 month plan

vpn-shared-pricing-get-6-month-v2 = Get 6-month plan
vpn-shared-pricing-get-12-month-v2 = Get 12-month plan
vpn-shared-pricing-get-monthly = Get monthly plan

# Variables:
#   $percent (number) - percentage saved with chosen subscription plan e.g. '40'
vpn-shared-pricing-save-percent = Save { $percent }%

# Variables:
#   $percent (string) - percentage saved with chosen subscription plan e.g. '40'.
# Asterisk indicates a footnote for the following string
vpn-shared-save-percent-on = Save { $percent }% on { -brand-name-mozilla-vpn }*
# this is used as a footnote for the previous string and should include the asterisk OR matching character for both strings.
vpn-shared-when-you-subscribe = *when you subscribe to a 12-month plan

# Variables:
#   $amount (string) - a string containing the total annual subscription price together with the appropriate currency symbol e.g. '35,94 €'
vpn-shared-pricing-total = { $amount } total

# Platform subpage shared strings

vpn-shared-platform-cta-headline = Let’s get started
vpn-shared-platform-cta-button = See pricing & availability

vpn-shared-platform-privacy-promise = Your privacy is our promise

vpn-shared-platform-trust-partner-headline = About our trusted partner
# Variables:
#   $policy (url) - link to https://mullvad.net/help/no-logging-data-policy/
#   $wireguard (url) - link to https://mullvad.net/help/why-wireguard/
vpn-shared-platform-trust-partner-copy = The { -brand-name-mozilla-vpn } runs on a global network of servers powered by <a href="{ $policy }">{ -brand-name-mullvad }</a> using the <a href="{ $wireguard }">{ -brand-name-wireguard }</a>® protocol. { -brand-name-mullvad } puts your privacy first and does not keep logs of any kind.

vpn-shared-platform-what-youll-get = What you’ll get with { -brand-name-mozilla-vpn }:

# Subnav strings
vpn-subnav-title = { -brand-name-mozilla-vpn }
vpn-subnav-whats-a-vpn = What’s a VPN?
vpn-subnav-faqs = FAQs
vpn-subnav-get-help = Get Help
vpn-subnav-platform-android = { -brand-name-android }
vpn-subnav-platform-desktop = Desktop
vpn-subnav-platform-ios = { -brand-name-ios }
vpn-subnav-platform-linux = { -brand-name-linux }
vpn-subnav-platform-mac = { -brand-name-mac-short }
vpn-subnav-platform-mobile = Mobile
vpn-subnav-platform-windows = { -brand-name-windows }
vpn-subnav-whats-an-ip-address = What’s an IP address?
vpn-subnav-when-to-use-a-vpn = When to use a VPN
vpn-subnav-vpn-vs-proxy = VPN vs Proxy
vpn-subnav-subscribe = Subscribe to { -brand-name-mozilla-vpn }

## VPN Affiliate cookie notice

# Variables:
#   $attrs (string) - link to https://www.mozilla.org/en-US/privacy/websites/ with additional attributes.
vpn-shared-affiliate-notification-message = We use cookies to understand which affiliate partner led you to { -brand-name-mozilla-vpn }. We do not share personally identifying information with our partners. Read our <a { $attrs }>Privacy Policy</a>.

vpn-shared-affiliate-notification-reject = Reject
vpn-shared-affiliate-notification-ok = OK

##
