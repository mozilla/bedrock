# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

### URL: https://www-dev.allizom.org/products/relay/waitlist/[vpn|phone].html

waitlist-bundle-name = { -brand-name-relay } + { -brand-name-vpn } bundle
waitlist-phone-name = { -brand-name-relay } phone masking
## old variables
waitlist-heading-2 = Join the { -brand-name-relay-premium } waitlist
waitlist-heading-phone = Join the { -brand-name-relay } phone masking waitlist
waitlist-heading-bundle = Join the waitlist for the { -brand-name-relay } + { -brand-name-vpn } bundle
waitlist-lead-2 = We’ll let you know when { -brand-name-relay-premium } is available in your area.
waitlist-lead-phone = We’ll let you know when phone masking is available in your area.
waitlist-lead-bundle = We’ll let you know when you can get { -brand-name-relay-premium } and { -brand-name-mozilla-vpn } at a discount in your area.
waitlist-control-required = Required
waitlist-control-email-label = What is your email address?
# Please only translate `yourname`; example.com is an actual example domain that is safe to use.
waitlist-control-email-placeholder = yourname@example.com
waitlist-control-country-label-2 = What country or region do you live in?
waitlist-control-locale-label = Select your preferred language.
waitlist-submit-label-2 = Join the waitlist
# Variables:
#   $url (url) - https://www.mozilla.org/en-US/privacy/subscription-services/
waitlist-privacy-policy-agree-2 = By clicking “{ waitlist-submit-label-2 }”, you agree to our <a href="{ $url }">Privacy Policy</a>.
waitlist-privacy-policy-use = Your information will only be used to notify you about { -brand-name-firefox-relay-premium } availability.
waitlist-privacy-policy-use-phone = Your information will only be used to notify you when phone masking is available in your area.
waitlist-privacy-policy-use-bundle = Your information will only be used to notify you about { -brand-name-relay } + { -brand-name-vpn } bundle availability.
waitlist-subscribe-success-title = Thanks! You're on the list
# Variables:
#   $product (string) one of the following three options:
#      - { -brand-name-firefox-firefox-relay-premium }
#      - { waitlist-bundle-name }
#      - { waitlist-phone-name }
waitlist-subscribe-success-desc = Once { $product } becomes available for your region, we’ll email you.
waitlist-subscribe-please-enter-a-valid = Please enter a valid email address
waitlist-subscribe-please-select-country = Please select a country or region
waitlist-subscribe-please-select-language = Please select a language
waitlist-subscribe-error-unknown = There was an error adding you to the waitlist. Please try again.
