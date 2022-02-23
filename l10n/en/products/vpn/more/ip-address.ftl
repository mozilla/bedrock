# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

### URL: https://www-dev.allizom.org/products/vpn/more/what-is-an-ip-address/

# HTML page title and main title
vpn-ip-address-what-is-an-ip-address = What is an IP address?

# HTML page description and intro
vpn-ip-address-mozilla-answers-all-of = { -brand-name-mozilla } answers all of your questions about IP addresses from what is an IP address, to how it works, and if you should hide it.

vpn-ip-address-every-time-you = Every time you are on the internet, IP addresses are playing an essential role in the information exchange to help you see the sites you are requesting. Yet, there is a chance you don’t know what one is, so we are breaking down the most commonly asked questions below.
vpn-ip-address-your-ip-address = Your IP address is a unique identifier, kind of like a mailing address, associated with your online activity. Any time that you use the internet (shopping online, sending emails, streaming TV), you’re requesting access to a specific online destination, and in return, information is sent back to you. How does that work? Well the IP stands for Internet Protocol, which lays out the standards and rules (yes, otherwise known as the protocol) for routing data and connecting to the internet. This protocol is a set of rules each party needs to follow to allow for a bi-directional flow of data.

# Used as an accessible text alternative for an image
vpn-ip-address-an-example-of-an-ip = An example of an IP address that is a sequence of four numbers, separated by decimals: 123.45.67.89
vpn-ip-address-if-you-look-up-your = If you look up your IP address, it will look something like this.
vpn-ip-address-does-it-travel = Does it travel with you?

# Variables
#   $url (url) - https://www.mozilla.org/products/vpn/more/when-to-use-a-vpn/
vpn-ip-address-no-your-ip-v2 = No. Your IP address is only associated with one location unless you are using a VPN (we will get more into that later). When you are at your home and connecting to the internet you pay for, you are using one. However, if you check your email at home in the morning, then scan the news at a local coffee shop while waiting for your coffee, and then work from an office, you will have used different IP addresses at each location.
# Outdated string
vpn-ip-address-no-your-ip = No. Your IP address is only associated with one location unless you are <a href="{ $url }">using a VPN</a> (we will get more into that later). When you are at your home and connecting to the internet you pay for, you are using one. However, if you check your email at home in the morning, then scan the news at a local coffee shop while waiting for your coffee, and then work from an office, you will have used different IP addresses at each location.
vpn-ip-address-does-your-ip = Does your IP address change?
vpn-ip-address-yes-even-if = Yes. Even if you are only using the internet at home, the IP address for your home can change. You can contact your internet service provider (ISP) to change it, but even something as routine as restarting your modem or router because of internet connection problems could result in a change.
vpn-ip-address-can-more-than = Can more than one device have the same IP address?
vpn-ip-address-this-is-a = This is a bit of a tricky question — the answer is both yes and no. More than one device can share the same external (public) IP address, but each device will have its own local (private) IP address. For example, your ISP (internet service provider) sets your home up with one external IP address. Since your router is what actually connects to the internet, the IP address is assigned to your router. Your router then assigns a local IP address to each device that is connected to the internet at a time. The external IP address is what is shared with the outside world. Your local IP address is not shared outside of your private home network.
vpn-ip-address-can-we-run = Can we run out of them?

# Variables
#   $sr (url) - https://www.siliconrepublic.com/comms/ip-addresses-running-out
#   $variety (url) - https://variety.com/2019/digital/news/u-s-households-have-an-average-of-11-connected-devices-and-5g-should-push-that-even-higher-1203431225/
vpn-ip-address-when-the-internet = When the Internet was first designed, it used “version 4” addresses. These are 32 bits, which means that we could have up to <a href="{ $sr }">4.2bn addresses</a>. This seemed like enough at the time, but is nowhere near enough in a world where the average U.S. household had <a href="{ $variety }">11 connected devices</a>.
vpn-ip-address-we-now-have = We now have version 6 IP addresses, which have 128 bits per address. Unfortunately, version 4 and version 6 can’t talk to each other directly, so people are going to need version 4 addresses for a long time.
vpn-ip-address-should-you-hide = Should you hide your IP address?

# Variables
#   $congress (url) - https://blog.mozilla.org/en/mozilla/internet-policy/u-s-broadband-privacy-rules-will-fight-protect-user-privacy/
#   $doh (url) - https://support.mozilla.org/kb/firefox-dns-over-https
#   $firefox (url) - https://www.mozilla.org/firefox/new/
vpn-ip-address-you-dont-need = You don’t need to hide your IP address, but there are some times where you may want to. The most common reason is privacy. In the U.S., <a href="{ $congress }">Congress overruled</a> privacy regulations designed to protect the privacy of broadband users. Internet service providers can see your browsing habits, what you are using the internet for, and how long you spend on each page. This communication is not encrypted, so third-parties can see what website you’re visiting. One way to combat this is <a href="{ $doh }">DNS-over-HTTPS</a> (DoH). This encrypts your DNS (Domain Name System) traffic, making it harder for ISPs to see the websites you are trying to visit. For US <a href="{ $firefox }">{ -brand-name-firefox } users</a>, by default your DoH queries are directed to trusted DNS servers, making it harder to associate you with the websites you try to visit.

# Variables
#   $url (url) - https://www.mozilla.org/products/vpn/more/when-to-use-a-vpn/
vpn-ip-address-there-are-also = There are also situational reasons to hide your IP address. You may want to hide it when traveling. A VPN will also give you <a href="{ $url }">more privacy</a> when connecting to WiFi to stream and shop while you explore the world.
vpn-ip-address-how-do-you = How do you hide it?

# Variables
#   $vpn (url)- https://www.mozilla.org/products/vpn/more/what-is-a-vpn/
#   $mozvpn (url) - https://www.mozilla.org/products/vpn/
#   $countries (number) - number of countries where Mozilla VPN has servers, e.g. "30". The + after indicates the number may be higher, where "30+" means "30 or more".
vpn-ip-address-a-vpn-is-v2 = A VPN is a way to hide your IP address. <a href="{ $vpn }">When you use a VPN</a>, your external IP address will be coming from the VPN server’s external IP, rather than your location’s external IP address. So if your connecting VPN server is located in California, your external IP will look like it’s connected from California, no matter where you actually are. Plus, your online activity is sent over an encrypted, secure connection to your VPN server, giving you additional security and privacy. <a href="{ $mozvpn }">{ -brand-name-mozilla-vpn }</a> is one way to hide your IP address. We don’t keep your network activity logs, and we don’t partner with third parties who build profiles of what you do online. We offer full-device protection for up to five devices with servers in { $countries }+ countries, you can connect to anywhere, from anywhere.

# Obsolete string
# Variables
#   $vpn (url)- https://www.mozilla.org/products/vpn/more/what-is-a-vpn/
#   $mozvpn (url) - https://www.mozilla.org/products/vpn/
#   $countries (number) - number of countries where Mozilla VPN has servers, e.g. "30". The + after indicates the number may be higher, where "30+" means "30 or more".
vpn-ip-address-a-vpn-is = A VPN is a way to hide your IP address. <a href="{ $vpn }">When you use a VPN</a>, your external IP address will be coming from the VPN server’s external IP, rather than your location’s external IP address. So if your connecting VPN server is located in California, your external IP will look like it’s connected from California, no matter where you actually are. Plus, your online activity is sent over an encrypted, secure connection to your VPN server, giving you additional security and privacy. <a href="{ $mozvpn }">{ -brand-name-mozilla-vpn }</a> is one way to hide your IP address. We don’t keep activity logs or partner with third-party analytics platforms. We offer full-device protection for up to five devices with servers in { $countries }+ countries, you can connect to anywhere, from anywhere.
