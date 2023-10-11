# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

### URL: https://www-dev.allizom.org/products/monitor/breaches/

-brand-HIBP = Have I Been Pwned

# HTML all breaches page title
monitor-breaches-page-title = { -brand-name-mozilla-monitor } — All Data Breaches

# HTML detail breach page title
# Variables:
#   $breach_title (string) - the title of the breach
monitor-breach-page-title = { -brand-name-mozilla-monitor } — { $breach_title }

# HTML page description
monitor-breaches-page-desc = Browse the complete list of known breaches detected by { -brand-name-mozilla-monitor }, then find out if your information was exposed.

monitor-breaches-hero-heading = All breaches detected by { -brand-name-mozilla-monitor }
monitor-breaches-hero-tagline = We monitor all known data breaches to find out if your personal information was compromised. Here’s a complete list of all of the breaches that have been reported since 2007.

breach-added-label = Breach added
breach-exposed-data = Exposed data

# Breach categories
website-breach = Website Breach
sensitive-breach = Sensitive Website Breach
data-aggregator-breach = Data Aggregator Breach
unverified-breach = Unverified Breach
spam-list-breach = Spam List Breach

website-breach-plural = Website Breaches
sensitive-breach-plural = Sensitive Breaches
data-aggregator-breach-plural = Data Aggregator Breaches
unverified-breach-plural = Unverified Breaches
spam-list-breach-plural = Spam List Breaches

# This is a section headline on the breach detail page that appears above
# a short summary about the breach.
breach-overview-title = Overview

# This is a standardized breach overview blurb that appears on all breach detail pages.
# $breachTitle is the name of the breached company or website.
# $breachDate and $addedDate are calendar dates.
breach-overview-new = On { $breachDate }, { $breachTitle } was breached. Once the breach was discovered and verified, it was added to our database on { $addedDate }.

delayed-reporting-headline = Why did it take so long to report this breach?
delayed-reporting-copy = It can sometimes take months or years for credentials exposed
  in a data breach to appear on the dark web. Breaches get added to our database as
  soon as they have been discovered and verified.

what-data = What data was compromised:

find-out-if = Find out if you were involved in this breach
find-out-if-description = We’ll help you quickly see if your email address was exposed in this breach, and understand what to do next.

# Breach data provided by Have I Been Pwned.
# Variables:
#   $hibp_link_attr (String) - anchor tag attributes, including URL, to Have I Been Pwned
hibp-attribution = Breach data provided by <a { $hibp_link_attr }>{ -brand-name-hibp }</a>

breach-detail-cta-signup = Check for breaches

# Section headline
rec-section-headline = What to do for this breach
rec-section-subhead = We recommend you take these steps to keep your personal info safe and protect your digital identity.

# Section headline
rec-section-headline-no-pw = What to do to protect your personal info
rec-section-subhead-no-pw = Though passwords weren’t exposed in this breach, there are still steps you can take to better protect your personal info.
