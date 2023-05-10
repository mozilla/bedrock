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
faq-question-trackerremoval-breakage-answer-2 = Sometimes removing trackers may cause your email to look broken because the trackers are often contained within images and links. When the tracker is removed, the email looks like it’s been formatted wrong because images are missing. This can’t be fixed for emails you’ve already received. If this is preventing you from reading your emails properly, turn off tracker removal.


## Frequently Asked Questions about Phone plans
phone-masking-faq-question-what-is = What is a phone number mask?
phone-masking-faq-answer-what-is = Similar to an email mask, a phone number mask is a phone number that can forward texts and calls to your true phone number without revealing what your true number is to the person calling or texting you.

phone-masking-faq-question-where-is = Where is phone masking available?
phone-masking-faq-answer-where-is = At this time, phone number masking is only available in the United States and Canada. This means you can only receive forwarded calls and texts from US or Canadian numbers. We’re working on finding a way to offer phone number masking outside these two countries.

phone-masking-faq-question-how-many = How many phone masks do I get?
phone-masking-faq-answer-how-many = You only get one phone number mask at this time. Once you choose your phone number mask, you cannot change it later.

phone-masking-faq-question-change-phone-mask = Can I change my phone mask?
phone-masking-faq-answer-change-phone-mask = No, you cannot change your phone number mask once you’ve chosen it. We are exploring this option.

phone-masking-faq-question-can-reply = Can I reply to texts?
phone-masking-faq-answer-can-reply = Yes, you can reply to the last text you received. Just reply as you would for any text message.

phone-masking-faq-question-forwarded-texts = What kinds of texts will be forwarded?
phone-masking-faq-answer-forwarded-texts = Only SMS text messages can be forwarded. MMS texts that include photos, videos, etc. will not be forwarded.

phone-masking-faq-question-pictures = Can I send or receive pictures via text?
phone-masking-faq-answer-pictures = No, only SMS text messages can be forwarded or sent as replies.

phone-masking-faq-question-historical = Can I reply to historical text messages?
phone-masking-faq-answer-historical = You can’t currently reply to texts you received previously, though this feature is on the way.

phone-masking-faq-question-can-i-send = Can I send a text without replying to one?
phone-masking-faq-answer-can-i-send = No, you can’t yet send texts that aren’t replies. You can only reply to forwarded texts.

phone-masking-faq-question-limit = Is there a limit to how many text messages I get?
phone-masking-faq-answer-limit = You can receive and reply up to 75 text messages per month total. Any additional texts sent to your phone number mask will not be forwarded to your true number. Any additional replies will not be delivered. The month turns over on your billing date, not the calendar date. Once your billing month has turned over, you will start receiving text messages again.

phone-masking-faq-question-call-length = How long can I talk when I get a call?
phone-masking-faq-answer-call-length = Each month you get 50 minutes of talking. Once these minutes are used up, you won’t be able to receive forwarded calls until the next month on your billing cycle.

phone-masking-faq-question-can-i-call = Can I call someone with my phone mask?
phone-masking-faq-answer-can-i-call = No, you can only pick up a forwarded call.

phone-masking-faq-question-can-i-see = Can I see who texted or called me?
phone-masking-faq-answer-can-i-see = Yes, you can see the number that texted or called you. You can also disable the storage of these records, but you will lose the ability to reply to or block individual callers & texters.

phone-masking-faq-question-can-i-block = Can I block a call or text?
phone-masking-faq-answer-can-i-block = You can block all forwarding from a single number.

phone-masking-faq-question-spam = What if my phone mask starts getting spam?
phone-masking-faq-answer-spam = If you start getting spam, you can block the numbers sending you spam.

phone-masking-faq-question-disable-logging = Can I disable the logging of callers or text senders?
phone-masking-faq-answer-disable-logging = Yes, you can disable logging of numbers from the { -brand-name-relay } dashboard. However, you will no longer be able to reply to texts or block specific numbers, because the log is how we are able to track who sent you a text message.

phone-masking-faq-question-can-i-share = Can I share the number that forwards me text messages?
phone-masking-faq-answer-can-i-share = If you share this number, nothing will happen — this number is not your phone number mask. It is just the contact number from which { -brand-name-relay } will forward your texts and calls.

phone-masking-faq-question-how-i-save-card = How do I save the { -brand-name-relay } contact card?
phone-masking-faq-answer-how-i-save-card = Once you upgrade to { -brand-name-relay } phone number masking, we will text you a contact card that contains the number from which you will receive forwarded calls and texts, similar to any contact card that stores the phone number of people who contact you. On most devices, you can select that contact card and save it like any other contact on your phone.

phone-masking-faq-question-install-app = Do I need to install an app to use { -brand-name-relay } phone masking?
phone-masking-faq-answer-install-app = No, { -brand-name-relay } phone masking works using your device’s standard text messaging and calling apps.
phone-masking-faq-question-data = What kinds of data does { -brand-name-relay } phone masking store?
#   $url (url) - link to Firefox Relay's Privacy Policy, i.e. https://www.mozilla.org/privacy/firefox-relay/
#   $attrs (string) - specific attributes added to external links
phone-masking-faq-answer-data = Please see the <a href="{ $url }" { $attrs }>{ -brand-name-firefox-relay } Privacy Policy</a>.


# Deprecated
faq-question-trackerremoval-breakage-answer = Sometimes removing trackers may cause your email to look broken, because the trackers are often contained within images. When the tracker is removed, the email looks like it’s been formatted wrong because images are missing. This can’t be fixed for emails you’ve already received. If this is preventing you from reading your emails properly, turn off tracker removal.
phone-masking-faq-answer-forwarded-texts-2 = Only text messages can be forwarded. MMS texts that include photos, videos, etc. will not be forwarded.
phone-masking-faq-answer-pictures-2 = No, only text messages can be forwarded or sent as replies.
