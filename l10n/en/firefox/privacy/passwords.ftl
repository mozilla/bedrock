# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

### URL: https://www-dev.allizom.org/firefox/privacy/safe-passwords

# HTML page title
privacy-passwords-security-guide-to = Security guide to safer logins and passwords

# HTML page description
privacy-passwords-more-and-more-desc = More and more of the sensitive, valuable things in our life are guarded through password-protected online accounts. How should we protect our logins?

# page content
privacy-passwords-a-security-guide = A security guide to safer logins and passwords
privacy-passwords-protecting-your-accounts = Protecting your accounts doesn’t have to be complicated — and { -brand-name-firefox } can help.
privacy-passwords-more-and-more = More and more of the sensitive, valuable things in our life are guarded through password-protected online accounts — love letters, medical records, bank accounts and more. Websites use login procedures to protect those valuable things. Generally, as long as someone can’t log into your account, they can’t read your email or transfer money out of your bank account. As we live our lives online, how should we protect our logins?

# tl;dr is an abbreviation for "Too long; didn't read". This is a playful way to say "summary" or "overview"
privacy-passwords-tldr = tl;dr:
privacy-passwords-use-random-passwords = Use random passwords, and use a different password for every site
privacy-passwords-pay-attention-to = Pay attention to the browser’s security signals, and be suspicious
privacy-passwords-make-your-answers = Make your answers to security questions just as strong as your passwords
privacy-passwords-use-a-password = Use a password manager to make creating and remembering passwords easier
privacy-passwords-use-twofactor-authentication = Use “two-factor authentication” wherever you can
privacy-passwords-its-hard-out = It’s hard out there for a password
privacy-passwords-most-logins-today = Most logins today are protected by a password. If an attacker can get your password, they can access your account and do anything you could do with that account. So when you ask how secure your account is, you should really be thinking about how safe your password is. And that means you have to think about all the different ways that an attacker could access your account’s password:
privacy-passwords-seeing-you-use = Seeing you use it with an unencrypted website
privacy-passwords-guessing-it = Guessing it
privacy-passwords-stealing-a-file = Stealing a file that has your password in it
privacy-passwords-using-password-recovery = Using password recovery to reset it
privacy-passwords-tricking-you-into = Tricking you into giving it to them
privacy-passwords-to-keep-your = To keep your login safe, you need to prevent as many of these as possible. Each risk has a different corresponding mitigation.
privacy-passwords-look-for-the = Look for the lock in your browser
privacy-passwords-its-easy-to = It’s easy to prevent attackers from stealing your password when you log into an unencrypted website: Think twice before you type your password if you don’t see a lock icon in the URL bar, like this:
privacy-passwords-a-closed-lock = A closed padlock appears just before the website address in the URL bar in all major browsers.
privacy-passwords-the-lock-means = The lock means that the website you’re using is encrypted, so that even if someone is watching your browsing on the network (like another person on a public WiFi hotspot), they won’t be able to see your password. { -brand-name-firefox } will try to warn you when you’re about to enter your password on an unencrypted site.
privacy-passwords-a-padlock-with = A padlock with a line through it indicates the connection is not secure.
privacy-passwords-your-browser-also = Your browser also helps keep you informed about how trustworthy sites are, to help keep you safe from phishing. On the one hand, when you try to visit a website that is known to be a phishing site, { -brand-name-firefox } (and any major browser) will display a full-screen warning — <strong>pay attention and think twice about using that site!</strong>

privacy-passwords-firefox-will-v2 = { -brand-name-firefox } will display a warning instead of the website if it is known to be a phishing site.

# Obsolete string
privacy-passwords-firefox-will = Firefox will display a warning instead of the website if it is known to be a phishing site.

privacy-passwords-in-general-the = In general, the best defense against phishing is to <strong>be suspicious of what you receive</strong>, whether it shows up in email, a text message or on the phone. Instead of taking action on what someone sent you, visit the site directly. For example, if an email says you need to reset your PayPal password, don’t click the link. Type in paypal.com yourself. If the bank calls, call them back.
privacy-passwords-strength-in-diversity = Strength in diversity
privacy-passwords-the-secret-to = The secret to preventing guessing, theft or password reset is a whole lot of randomness. When attackers try to guess passwords, they usually do two things: 1) Use “dictionaries” — lists of common passwords that people use all the time, and 2) make some random guesses. The <strong>longer and more random your password is</strong>, the less likely that either of these guessing techniques will find it.

#   $url_linkedin (string) - link to https://blog.linkedin.com/2012/06/06/linkedin-member-passwords-compromised with additional attributes for analytics
#   $url_yahoo (string) - link to https://www.wired.com/2016/12/yahoo-hack-billion-users/ with additional attributes for analytics
privacy-passwords-when-an-attacker = When an attacker steals the password database for a site that you use (like <a { $url_linkedin }>LinkedIn</a> or <a { $url_yahoo }>Yahoo</a>), there’s nothing you can do but change your password for that site. That’s bad, but the damage can be much worse if you’ve re-used that password with other websites — then the attacker can access your accounts on those sites as well. To keep the damage contained, <strong>always use different passwords for different websites.</strong>

#   $url_monitor (string) - link to https://monitor.firefox.com/ with additional attributes for analytics
privacy-passwords-use-firefox-monitor = Use <a { $url_monitor }>{ -brand-name-firefox-monitor }</a> to keep an eye on email addresses associated with your accounts. If your email address appears in a known corporate data breach, you’ll be alerted and provided steps to follow to protect the affected account.
privacy-passwords-security-questions-my = Security Questions: My mother’s maiden name is “Ff926AKa9j6Q”
privacy-passwords-finally-most-websites = Finally, most websites let you recover your password if you’ve forgotten it. Usually these systems make you answer some “security questions” before you can reset your password. <strong>The answers to these questions need to be just as secret as your password.</strong> Otherwise, an attacker can guess the answers and set your password to something they know.
privacy-passwords-randomness-can-be = Randomness can be a problem, since the security questions that sites often use are also things people tend to know about you, like your birthplace, your birthday, or your relatives’ names, or that can be gleaned from sources such as social media. The good news is that the website doesn’t care whether the answer is real or not — you can lie! But lie productively: <strong>Give answers to the security questions that are long and random,</strong> like your passwords.
privacy-passwords-get-help-from = Get help from a password manager
privacy-passwords-now-all-of = Now, all of this sounds pretty intimidating. The human mind isn’t good at coming up with long sequences of random letters, let alone remembering them. That’s where a password manager comes in. Built right into the browser, { -brand-name-firefox } will ask if you want to generate a unique, complex password, then securely save your login information, which you can access anytime in about:logins.

#   $url_sumo-manager (string) - link to https://support.mozilla.org/kb/password-manager-remember-delete-edit-logins with additional attributes for analytics
privacy-passwords-when-youre-logged = When you’re logged into { -brand-name-firefox } with your { -brand-name-firefox } account, you can sync across all your devices and access your passwords from a { -brand-name-firefox } mobile browser. Learn more about <a { $url_sumo-manager }>how to use the built-in password manager</a> to the fullest here.
privacy-passwords-twofactor-authentication-2fa = Two-Factor Authentication (2FA)
privacy-passwords-2fa-is-a = 2FA is a great way to level-up your security. When setting up a new account, some sites will give you the option to add a “second factor” to the login process. Often, this means linking your phone number to your account, so after you enter your password, you will be prompted to enter a secure code texted directly to you. This way, if a hacker has managed to get your password, they still won’t be able to get into your account, since they don’t have your phone.

#   $url_sumo_2fa (string) - link to https://support.mozilla.org/kb/secure-firefox-account-two-step-authentication with additional attributes for analytics
privacy-passwords-your-firefox-account = Your { -brand-name-firefox } account, for instance, can be protected with 2FA, <a { $url_sumo_2fa }>which you can learn more about here</a>.

#   $url_2fa (string) - link to https://2fa.directory with additional attributes for analytics
privacy-passwords-2fa-provides-much = 2FA provides much better security than passwords alone, but not every website supports it. You can find a list of websites that support 2FA at <a { $url_2fa }>https://2fa.directory</a>, as well as a list of sites that don’t support 2FA and ways you can ask them to add support.
privacy-passwords-strong-diverse-and = Strong, diverse, and multi-factor
privacy-passwords-for-better-or = For better or worse, we’re going to be using passwords to protect our online accounts for the foreseeable future. Use passwords that are <strong>strong</strong> and <strong>different for each site</strong>, and use a <strong>password manager</strong> to help you remember them safely. Set <strong>long, random answers</strong> for security questions (even if they’re not the truth). And <strong>use two-factor authentication</strong> on any site that supports it.

#   $url_privacy_products (string) - link to https://www.mozilla.org/firefox/privacy/products/ with additional attributes for analytics
#   $url_about_manifesto (string) - link to https://www.mozilla.org/about/manifesto/ with additional attributes for analytics
privacy-passwords-in-todays-internet-v2 = In today’s internet, where thousands of passwords are stolen every day and accounts are traded on the black market, it’s worth the effort to keep your online life safe. When you use { -brand-name-firefox } products, some of the effort is taken off your plate, because all our products are built to uphold our <a { $url_privacy_products }>privacy promise</a>. And { -brand-name-firefox } is always guided by <a { $url_about_manifesto }>{ -brand-name-mozilla }’s mission</a>, the not-for-profit we are backed by, to build a better internet.

# Obsolete string
#   $url_privacy_products (string) - link to https://www.mozilla.org/firefox/privacy/products/ with additional attributes for analytics
#   $url_about_manifesto (string) - link to https://www.mozilla.org/about/manifesto/ with additional attributes for analytics
privacy-passwords-in-todays-internet = In today’s internet, where thousands of passwords are stolen every day and accounts are traded on the black market, it’s worth the effort to keep your online life safe. When you use { -brand-name-firefox } products, some of the effort is taken off your plate, because all our products are built to uphold our <a { $url_privacy_products }>privacy promise</a>. And { -brand-name-firefox } is always guided by <a { $url_about_manifesto }>Mozilla’s mission</a>, the not-for-profit we are backed by, to build a better internet.
