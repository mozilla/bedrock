# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

### URL: https://www-dev.allizom.org/products/relay/


## FAQ Page

faq-headline = Frequently Asked Questions
# String used to display the attachment limit, e.g. 10 MB
# Variables:
#  $size (number): maximum size for attachments
#  $unit (string): unit of measurement (e.g. MB for Megabyte)
email-size-limit = { $size } { $unit }
faq-question-what-is-question-2 = What is a { -brand-name-relay } email mask?
faq-question-what-is-answer-2 = Email masks are masked, or private, email addresses that forward messages to your true email address. These masks allow you to share an address with third parties which will mask your true email address and forward messages to it.
faq-question-missing-emails-question-2 = I’m not getting messages from my email masks
faq-question-missing-emails-answer-a-2 = There are a few reasons you might not be receiving emails forwarded through your masks. These reasons include:
faq-question-missing-emails-answer-reason-spam = Messages are going into spam
faq-question-missing-emails-answer-reason-blocked-2 = Your email provider is blocking your email masks
faq-question-missing-emails-answer-reason-size = The email forwarded has an attachment larger than { email-size-limit }
faq-question-missing-emails-answer-reason-not-accepted-2 = The site doesn’t accept email masks
faq-question-missing-emails-answer-reason-turned-off-2 = The mask might have forwarding turned off
faq-question-missing-emails-answer-reason-delay = { -brand-name-relay } might be taking longer than usual to forward your messages
#   $url (url) - link to the support site
#   $attrs (string) - specific attributes added to external links
faq-question-missing-emails-answer-b-html = If you’re a { -brand-name-relay-premium } user struggling with any of these issues, please <a href="{ $url }" { $attrs }>contact our support team</a>.
#   $url (url) - link to the support site
#   $attrs (string) - specific attributes added to external links
faq-question-missing-emails-answer-support-site-html = If you’re struggling with any of these issues, please <a href="{ $url }" { $attrs }>visit our support site</a>.
faq-question-use-cases-question-2 = When should I use { -brand-name-relay } email masks?
faq-question-use-cases-answer-part1-2 = You can use { -brand-name-relay } email masks most places you’d use your regular email address. We recommend using them when signing up for marketing/informational emails where you may want to control whether or not you receive emails in the future.
faq-question-use-cases-answer-part2-2 = We don’t recommend using masks when you need your identity verified or for very important emails or those where you must receive attachments. For example, you’d want to share your true email address with your bank, your doctor, and your lawyer, as well as when receiving concert or flight boarding passes.
faq-question-2-question-2 = Why won’t a site accept my { -brand-name-relay } email mask?
# Variables:
#   $url (url) - https://addons.mozilla.org/firefox/addon/private-relay/
#   $attrs (string) - specific attributes added to external links
faq-question-2-answer-v4 =
    Some sites may not accept an email address that includes a subdomain (@subdomain.mozmail.com) and others have stopped accepting all addresses except those from Gmail, Hotmail, or Yahoo accounts.
faq-question-1-question = What about spam?
faq-question-1-answer-a-2 = While { -brand-name-relay } does not filter for spam, our email partner Amazon SES does block spam and malware. If { -brand-name-relay } forwards messages you don’t want, you can update your { -brand-name-relay } settings to block messages from the mask forwarding them.
# Variables:
#   $url (url) - https://addons.mozilla.org/firefox/addon/private-relay/
#   $attrs (string) - specific attributes added to external links
faq-question-1-answer-b-2-html = If you see a broader problem of unwanted email from all of your masks, please <a href="{ $url }" { $attrs }>report this to us</a> so we can consider adjusting the SES spam thresholds for this service. If you report these as spam, your email provider will see { -brand-name-relay } as the source of spam, not the original sender.
faq-question-availability-question = Where is { -brand-name-relay } available?
faq-question-availability-answer = Free { -brand-name-relay } is available in most countries. { -brand-name-relay-premium } is available in the United States, Germany, United Kingdom, Canada, Singapore, Malaysia, New Zealand, France, Belgium, Austria, Spain, Italy, Switzerland, Netherlands, and Ireland.
faq-question-availability-answer-v2 = Free { -brand-name-relay } is available in most countries. { -brand-name-relay-premium } is available in the United States, Germany, United Kingdom, Canada, Singapore, Malaysia, New Zealand, Finland, France, Belgium, Austria, Spain, Italy, Sweden, Switzerland, the Netherlands, and Ireland.
faq-question-availability-answer-v3 = Free { -brand-name-relay } is available in most countries. { -brand-name-relay-premium } is available in Austria, Belgium, Canada, Cyprus, Estonia, Finland, France, Germany, Greece, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malaysia, Malta, Netherlands, New Zealand, Portugal, Singapore, Slovakia, Slovenia, Spain, Sweden, Switzerland, United Kingdom, and the United States.
faq-question-landing-page-availability = Free { -brand-name-relay } is available in most countries. { -brand-name-relay-premium } email masking is available in the United States, Germany, United Kingdom, Canada, Singapore, Malaysia, New Zealand, France, Belgium, Austria, Spain, Italy, Switzerland, Netherlands, and Ireland. { -brand-name-relay-premium } phone masking is only available in the US and Canada.
faq-question-4-question-2 = Can I reply to messages using my { -brand-name-relay } email mask?
faq-question-4-answer-v4 = { -brand-name-relay-premium } users can reply to a forwarded email within 3 months of receiving the email. If you add a CC or BCC when you reply back to an email, your original email address will be exposed to the recipient and those copied on the email. If you do not want your original email address exposed, do not add CCs or BCCs when replying.
faq-question-subdomain-characters-question = What characters can I use to create a subdomain?
faq-question-subdomain-characters-answer-v2 = You can only use lower-case English letters, numbers, and hyphens to create a subdomain.
faq-question-browser-support-question = Can I use { -brand-name-relay } on other browsers or my mobile device?
faq-question-browser-support-answer-2 = Yes, you can generate { -brand-name-relay } masks on other browsers or mobile devices simply by logging in to your { -brand-name-relay } dashboard.
faq-question-longevity-question = What happens if Mozilla shuts down the { -brand-name-firefox-relay } service?
faq-question-longevity-answer-2 = We will give you advance notice that you need to change the email address of any accounts that are using { -brand-name-relay } email masks.
faq-question-mozmail-question-2 = Why did my email masks start to use the domain “mozmail.com?”
faq-question-mozmail-answer-2 = We made the switch from “relay.firefox.com” to “mozmail.com” in order to make it possible to get a custom email subdomain, such as mask@yourdomain.mozmail.com. Custom email subdomains, available to { -brand-name-relay-premium } subscribers, allow you to generate easier-to-remember email masks.
faq-question-attachments-question = Will { -brand-name-firefox-relay } forward emails with attachments?
faq-question-attachments-answer-v2 = We now support attachment forwarding. However, there is a { email-size-limit } limit for email forwarding using { -brand-name-relay }. Any emails larger than { email-size-limit } will not be forwarded.
faq-question-unsubscribe-domain-question-2 = What happens to my custom subdomain if I unsubscribe from { -brand-name-relay-premium }?
faq-question-unsubscribe-domain-answer-2 = If you downgrade from { -brand-name-relay-premium }, you’ll still receive emails forwarded through your custom email masks, but you’ll no longer be able to create new masks using that subdomain. If you have more than five masks in total, you will not be able to create any more. You’ll also lose the ability to reply to forwarded messages. You can resubscribe to { -brand-name-relay-premium } and regain access to these features.
faq-question-8-question = What data does { -brand-name-firefox-relay } collect?
# Variables:
#   $url (url) - https://www.mozilla.org/privacy/firefox-relay/
#   $attrs (string) - specific attributes added to external links
faq-question-8-answer-2-html = You can learn more about the data { -brand-name-firefox-relay } collects by taking a look at our <a href="{ $url }" { $attrs }>Privacy Notice</a>. You’re also able to optionally share data about the labels and site you use for your email masks so we can provide you that service and improve it for you.
faq-question-8-answer-3-html = { -brand-name-firefox-relay } collects the websites where you’ve used your email masks, and labels your masks with those websites so you can easily identify them. You can opt out of this on your Settings page, under Privacy. But please note, turning that setting off means you won’t be able to see where you’ve used each mask, and your account names will no longer sync between devices. You can learn more about the data { -brand-name-firefox-relay } collects in our <a href="{ $url }" { $attrs }>Privacy Notice</a>.
faq-question-email-storage-question = Does { -brand-name-relay } store my emails?
faq-question-email-storage-answer = Under the rare circumstance in which the service is down, we may temporarily store your emails until we are able to send them. We will never store your emails for longer than three days.
faq-question-acceptable-use-question = What are the acceptable uses of { -brand-name-relay }?
#   $url (url) - link to Mozilla's Acceptable Use Policy, i.e. https://www.mozilla.org/about/legal/acceptable-use/
#   $attrs (string) - specific attributes added to external links
faq-question-acceptable-use-answer-a-html = { -brand-name-firefox-relay } has the same <a href="{ $url }" { $attrs }>conditions of use as all { -brand-name-mozilla } products</a>. We have a zero-tolerance policy when it comes to using { -brand-name-relay } for malicious purposes like spam, resulting in the termination of a user’s account. We take measures to prevent users from violating our conditions by:
faq-question-acceptable-use-answer-measure-account = Requiring a { -brand-name-firefox-account(capitalization: "uppercase") } with a verified email address
faq-question-acceptable-use-answer-measure-unlimited-payment-2 = Requiring payment for a user to create more than five masks
faq-question-acceptable-use-answer-measure-rate-limit-2 = Rate-limiting the number of masks that can be generated in one day
#   $url (url) - link to the Terms of Service, i.e. https://www.mozilla.org/about/legal/terms/firefox-relay/
#   $attrs (string) - specific attributes added to external links
faq-question-acceptable-use-answer-b-html = Please review our <a href="{ $url }" { $attrs }>Terms of Service</a> for more information.
faq-question-promotional-email-blocking-question = What is promotional email blocking?
faq-question-promotional-email-blocking-answer = { -brand-name-relay-premium } subscribers can enable promotional email blocking. This feature will forward you important emails, such as receipts, password resets and confirmations while still blocking marketing messages. There is a slight risk that an important message could still be blocked, so we recommend that you not use this feature for very important places like your bank. If an email is blocked, it cannot be recovered.
faq-question-detect-promotional-question = How does { -brand-name-relay } detect if an email is Promotional or not?
faq-question-detect-promotional-answer = Many emails are sent with “header” metadata to indicate that they are from list-based automated tools. { -brand-name-firefox-relay } detects this header data so it can block these emails.
faq-question-disable-trackerremoval-question = Can I stop removing email trackers?
faq-question-disable-trackerremoval-answer = Yes. If you’re having trouble with emails looking broken or would like to stop removing trackers, you can disable the feature in settings.
faq-question-bulk-trackerremoval-question = Can I remove trackers only on some of my email masks?
faq-question-bulk-trackerremoval-answer = You can only turn tracker removal on at an account level — it either removes trackers from all of your emails, or none of them.
faq-question-trackerremoval-breakage-question = Why do my emails look broken?
# Deprecated
faq-question-trackerremoval-breakage-answer = Sometimes removing trackers may cause your email to look broken, because the trackers are often contained within images. When the tracker is removed, the email looks like it’s been formatted wrong because images are missing. This can’t be fixed for emails you’ve already received. If this is preventing you from reading your emails properly, turn off tracker removal.
faq-question-trackerremoval-breakage-answer-2 = Sometimes removing trackers may cause your email to look broken because the trackers are often contained within images and links. When the tracker is removed, the email looks like it’s been formatted wrong because images are missing. This can’t be fixed for emails you’ve already received. If this is preventing you from reading your emails properly, turn off tracker removal.
