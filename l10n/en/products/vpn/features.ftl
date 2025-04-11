# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

### URL: https://www-dev.allizom.org/products/vpn/features/

vpn-features-mozilla-vpn = { -brand-name-mozilla-vpn }

# HTML page title
# Line break for visual format only
vpn-features-features-that-protect = Features that protect <br> your life online

vpn-features-convenient = Convenient

# Variables
#   $servers (number) - number of VPN servers
#   $countries (number) - number of available countries
vpn-features-more-than = { $servers ->
    [one] More than { $servers } server in { $countries }+ countries
   *[other] More than { $servers } servers in { $countries }+ countries
}
vpn-features-see-our-list = See our list of servers.

# Variables:
#   $devices (number) - number of devices users can connect to VPN
vpn-features-connect-up-to = { $devices ->
    [one] Connect up to { $devices } device
   *[other] Connect up to { $devices } devices
}
vpn-features-supported-platforms = Supported on Windows, macOS, Android, iOS and Linux operating systems.
vpn-features-no-bandwidth = No bandwidth restrictions or throttling
vpn-features-including-no-data = Including no data cap or speed limit.
vpn-features-fast-network = Fast network speeds even while gaming

# Variables
#   $wireguard (url) - link to https://mullvad.net/help/why-wireguard/
vpn-features-mozilla-vpn-uses-wireguard = { -brand-name-mozilla-vpn } uses <a { $wireguard }>Wireguard</a>™, one of the most performant VPN protocols.

vpn-features-secure = Secure
vpn-features-block-ads = Block advertisers from targeting you
vpn-features-automatically-block-ads = { -brand-name-mozilla-vpn } helps you automatically block ads and ad trackers from seeing your online activity.
vpn-features-encrypt-your-internet = Encrypt all your internet traffic
vpn-features-vpn-protects-all-apps = { -brand-name-mozilla-vpn } protects all of the apps on your device, not just your browser.
vpn-features-stronger-malware = Stronger malware protection
vpn-features-vpn-prevents-downloading-malware = { -brand-name-mozilla-vpn } prevents you from downloading malware from known unsafe sources.
vpn-features-super-private-mode = Super-private mode: route traffic through two locations

# Variables
#   $feature (url) - link to https://support.mozilla.org/kb/multi-hop-encrypt-your-data-twice-enhanced-security
vpn-features-multi-hop-feature = Our <a { $feature }>multi-hop feature</a> gives you an extra security boost.
vpn-features-support-for-custom-dns = Support for custom DNS

# Variables
#   $dns (url) - link to https://support.mozilla.org/kb/how-do-i-change-my-dns-settings
vpn-features-keep-traffic-protected = With { -brand-name-mozilla-vpn }, you can keep your traffic protected and still route your DNS queries wherever you prefer. <a { $dns }>Learn more about custom DNS support</a>.

vpn-features-flexible = Flexible
vpn-features-webste-specific-vpn = Website-specific VPN settings, seamlessly integrated into { -brand-name-firefox }
vpn-features-with-the-mozilla-vpn-extention = With the { -brand-name-mozilla-vpn } Extension for { -brand-name-firefox } (Windows only), you can fine-tune your VPN experience on a per-website basis. Exclude individual websites from VPN protection or set preferred server locations for specific sites, giving you a more flexible and personalized experience.
vpn-features-personalized-server = Personalized server location recommendations
vpn-features-well-suggest-which-servers = We’ll suggest which servers near you will ensure the fastest, most reliable internet connection.
vpn-features-personalize-which-apps = Personalize which apps get VPN protection
vpn-features-easily-exclude-apps = Easily exclude apps from VPN protection — no need to disconnect your device from { -brand-name-mozilla-vpn }. Available in Windows, Android and Linux devices.

vpn-features-trustworthy = Trustworthy
vpn-features-money-back = 30-day money-back guarantee
vpn-features-plus-customer-support = Plus 24/7 customer support.
vpn-features-we-never-log = We never log, track or share your network data

# Variables
#   $privacy (url) - link to https://www.mozilla.org/privacy/subscription-services/
vpn-features-simply-put-we-dont = Simply put, we don’t collect your personal browsing information. Here’s our <a { $privacy }>easy-to-read privacy policy</a>.

vpn-features-built-transparently = Built transparently in open source

# Variables
#   $github (url) - link to https://github.com/mozilla-mobile/mozilla-vpn-client
vpn-features-made-with-open-source-code = { -brand-name-mozilla-vpn } is made with open-source code, meaning that all the code is publicly accessible. See our <a { $github }>GitHub repository</a>.

vpn-features-reviewed-by-third = Reviewed by third-party security experts

# Variables
#   $report (url) - link to https://blog.mozilla.org/mozilla/news/mozilla-vpn-completes-independent-security-audit-by-cure53
vpn-features-weve-been-audited = We’ve been audited by Cure53, a leading cybersecurity auditing firm. <a { $report }>See the report here</a>.
vpn-features-people-over-profits = People over profits

# Variables
#   $mofo (url) - link to https://foundation.mozilla.org/
vpn-features-were-backed-by-mofo = We’re backed by the <a { $mofo }>{ -brand-name-mozilla-foundation }</a>, a non-profit fighting to keep the web open and healthy for all people.
