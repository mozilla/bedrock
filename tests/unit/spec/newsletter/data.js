/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const userData = {
    email: 'example@example.com',
    country: 'us',
    format: 'H',
    lang: 'en',
    newsletters: ['about-mozilla', 'mozilla-and-you', 'mozilla-foundation'],
    has_fxa: true,
    status: 'ok'
};

const newsletterData = {
    'firefox-accounts-journey': {
        title: 'Firefox Account Tips',
        description: 'Get the most out of your Firefox Account.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Firefox_Accounts_Journey__c',
        languages: ['de', 'en', 'es', 'fr', 'id', 'pt', 'ru', 'pl', 'zh-TW'],
        requires_double_optin: false,
        firefox_confirm: true,
        is_mofo: false,
        order: 1
    },
    'knowledge-is-power': {
        title: 'Knowledge is Power',
        description:
            'Get all the knowledge you need to stay safer and smarter online.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Knowledge_is_Power__c',
        languages: ['en', 'de', 'fr'],
        requires_double_optin: false,
        firefox_confirm: false,
        is_mofo: false,
        order: 2
    },
    'test-pilot': {
        title: 'New Product Testing',
        description:
            'Help us make a better Firefox for you by test-driving our latest products and features.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Test_Pilot__c',
        languages: ['en', 'de', 'fr'],
        requires_double_optin: false,
        firefox_confirm: true,
        is_mofo: false,
        order: 3
    },
    'take-action-for-the-internet': {
        title: 'Take Action for the Internet',
        description:
            'Add your voice to petitions, events and initiatives that fight for the future of the web.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Take_Action_for_Internet__c',
        languages: ['en', 'de', 'fr'],
        requires_double_optin: false,
        firefox_confirm: false,
        is_mofo: false,
        order: 4
    },
    'mozilla-and-you': {
        title: 'Firefox News',
        description:
            'Get how-tos, advice and news to make your Firefox experience work best for you.',
        show: true,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Firefox_And_You__c',
        languages: ['de', 'en', 'es', 'fr', 'id', 'pt', 'ru', 'pl', 'zh-TW'],
        requires_double_optin: true,
        firefox_confirm: true,
        is_mofo: false,
        order: 5
    },
    'security-privacy-news': {
        title: 'Security & Privacy News from Mozilla',
        description:
            'Stay informed of the latest trends in privacy & security products from Mozilla, the makers of Firefox.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_security_privacy_news',
        languages: ['de', 'en', 'es', 'fr', 'id', 'pt', 'ru', 'pl', 'zh-TW'],
        requires_double_optin: true,
        firefox_confirm: true,
        is_mofo: false,
        order: 6
    },
    'firefox-sweepstakes': {
        title: 'Firefox Sweepstakes',
        description:
            'Special announcements about our contests including notifications to contest winners and promotional content',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Firefox_Sweepstakes__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: true,
        is_mofo: false,
        order: 6
    },
    'app-dev': {
        title: 'Developer Newsletter',
        description:
            "A developer's guide to highlights of Web platform innovations, best practices, new documentation and more.",
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Apps_And_Hacks__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: true,
        is_mofo: false,
        order: 7
    },
    'mozilla-foundation': {
        title: 'Mozilla News',
        description:
            'Regular updates to keep you informed and active in our fight for a better internet.',
        show: true,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Mozilla_Foundation__c',
        languages: ['de', 'en', 'es', 'fr', 'id', 'pt', 'ru', 'pl', 'zh-TW'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: true,
        order: 8
    },
    'mozilla-festival': {
        title: 'Mozilla Festival',
        description:
            "Special announcements about Mozilla's annual, hands-on festival dedicated to forging the future of the open Web.",
        show: true,
        active: true,
        private: false,
        indent: true,
        vendor_id: 'Sub_Mozilla_Festival__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: true,
        order: 9
    },
    'internet-health-report': {
        title: 'Internet Health Report',
        description:
            'Keep up with our annual compilation of research and stories on the issues of privacy & security, openness, digital inclusion, decentralization, and web literacy.',
        show: true,
        active: true,
        private: false,
        indent: true,
        vendor_id: 'Sub_Internet_Health_Report__c',
        languages: ['en', 'de', 'es', 'fr'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: true,
        order: 10
    },
    'open-leadership': {
        title: 'Open Leadership',
        description:
            'Monthly updates, resources and opportunities to develop your open leadership skills and engage with a vibrant community of collaborators.',
        show: false,
        active: true,
        private: false,
        indent: true,
        vendor_id: 'Interest_Open_Leadership__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: false,
        order: 11
    },
    'common-voice': {
        title: 'Common Voice',
        description:
            'Stay informed about our open-source voice database to help make voice recognition open to everyone.',
        show: true,
        active: true,
        private: false,
        indent: true,
        vendor_id: 'Sub_Common_Voice__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: true,
        order: 12
    },
    'mixed-reality': {
        title: 'Mixed Reality',
        description:
            'Keep up with all the latest in Virtual and Augmented Reality.',
        show: false,
        active: true,
        private: false,
        indent: true,
        vendor_id: 'Sub_Mixed_Reality__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: false,
        order: 14
    },
    hubs: {
        title: 'Hubs',
        description:
            'Mozilla Hubs - Stay up to date on the latest news from Hubs, Mozilla’s 3D virtual events platform',
        show: false,
        active: true,
        private: false,
        indent: true,
        vendor_id: 'Sub_Hubs__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: false,
        order: 15
    },
    'about-addons': {
        title: 'Add-ons Developer Newsletter',
        description:
            'Stay up-to-date on news and events relevant to Firefox extension developers.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'AMO_Email_Opt_In__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: true,
        is_mofo: false,
        order: 16
    },
    'about-mozilla': {
        title: 'Mozilla Community',
        description:
            'Join Mozillians all around the world and learn about impactful opportunities to support Mozilla’s mission.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_About_Mozilla__c',
        languages: ['en', 'de', 'es', 'fr', 'pt', 'ru'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: false,
        order: 17
    },
    'mozilla-phone': {
        title: 'Mozillians',
        description: 'Email updates for vouched Mozillians on mozillians.org.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Mozillians__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: false,
        is_mofo: false,
        order: 18
    },
    'mozillians-nda': {
        title: 'Mozillians - NDA',
        description: "Email updates for NDA'd Mozillians on mozillians.org.",
        show: false,
        active: true,
        private: true,
        indent: false,
        vendor_id: 'Sub_Mozillians_NDA__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: false,
        is_mofo: false,
        order: 19
    },
    'mozilla-fellowship-awardee-alumni': {
        title: 'Mozilla Fellowship & Awardee Alumni',
        description:
            'Stay up to date on news, opportunities, and events for awards and fellowship alumni, including hearing about alumni impact around the world.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Fellowship_and_Awardee__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: true,
        order: 20
    },
    'firefox-friends': {
        title: 'Firefox Friends',
        description:
            'Bringing easy engagement opportunities to Firefox supporters.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Firefox_Friends__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: true,
        is_mofo: false,
        order: 21
    },
    ambassadors: {
        title: 'Firefox Student Ambassadors',
        description:
            'A monthly newsletter on how to get involved with Mozilla on your campus.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Student_Ambassador__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: true,
        is_mofo: false,
        order: 22
    },
    webmaker: {
        title: 'Webmaker',
        description:
            'Special announcements helping you get the most out of Webmaker.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Webmaker__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: false,
        is_mofo: false,
        order: 23
    },
    'developer-events': {
        title: 'Developer Events',
        description:
            'Mozilla hosts events around the world for developers; stay connected to updates from our events team.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Dev_Events__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: false,
        order: 24
    },
    'view-source-conference-north-america': {
        title: 'View Source Conference North America',
        description:
            "Updates about View Source North America, Mozilla's conference for front-end web developers.",
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_View_Source_NAmerica__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: false,
        order: 25
    },
    'view-source-conference-global': {
        title: 'View Source Conference Global',
        description:
            "Updates about View Source Global, Mozilla's conference for front-end web developers.",
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_View_Source_Global__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: false,
        order: 26
    },
    'game-developer-conference': {
        title: 'Game Developer Conference',
        description:
            "Hear about Mozilla's most recent updates from the annual Game Developers Conference.",
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Game_Dev_Conference__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: false,
        is_mofo: false,
        order: 27
    },
    'ios-beta-test-flight': {
        title: 'iOS Beta Test Flight',
        description: '',
        show: false,
        active: false,
        private: false,
        indent: false,
        vendor_id: 'Sub_Test_Flight__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: true,
        is_mofo: false,
        order: 28
    },
    'mozilla-learning-network': {
        title: 'Mozilla Learning Network',
        description:
            'Updates from our global community, helping people learn the most important skills of our age: the ability to read, write and participate in the digital world.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Mozilla_Learning_Network__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: false,
        is_mofo: false,
        order: 29
    },
    'mozilla-leadership-network': {
        title: 'Mozilla Leadership Network',
        description:
            'Learn about the people and projects working toward a healthy Internet, and how you can get involved.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Mozilla_Leadership_Network__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: false,
        order: 30
    },
    'open-innovation-challenge': {
        title: 'Open Innovation Challenge',
        description:
            'Mozilla is inviting entrepreneurs and innovators to help connect all people to the open Internet in the Equal Rating Innovation Challenge.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Open_Innovation_Subscriber__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: false,
        is_mofo: false,
        order: 31
    },
    miti: {
        title: 'Mozilla Information Trust Initiative',
        description:
            'Find out more about our work to surface new ideas that seek to address misinformation, disinformation, and so-called “fake news.”',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_MITI_Subscriber__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: false,
        order: 32
    },
    inhuman: {
        title: 'Inhuman Ads',
        description:
            'Get updates from the neighborhood watch for the web. Learn more about how we’re calling out the worst ads and improving the online experience for everyone.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Inhuman_Ads__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: false,
        order: 33
    },
    'get-involved': {
        title: 'Get Involved',
        description: '',
        show: false,
        active: false,
        private: false,
        indent: false,
        vendor_id: 'Sub_Get_Involved__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: false,
        is_mofo: false,
        order: 34
    },
    'firefox-desktop': {
        title: 'Firefox for desktop',
        description:
            'Don’t miss the latest announcements about our desktop browser.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Interest_Firefox_Desktop__c',
        languages: ['de', 'en', 'es', 'fr', 'id', 'pt', 'ru', 'pl', 'zh-TW'],
        requires_double_optin: true,
        firefox_confirm: true,
        is_mofo: false,
        order: 35
    },
    mobile: {
        title: 'Firefox for Android',
        description:
            'Keep up with releases and news about Firefox for Android.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Interest_Android__c',
        languages: ['de', 'en', 'es', 'fr', 'id', 'pt', 'ru', 'pl', 'zh-TW'],
        requires_double_optin: true,
        firefox_confirm: true,
        is_mofo: false,
        order: 36
    },
    'firefox-ios': {
        title: 'Firefox iOS',
        description:
            'Be the first to know when Firefox is available for iOS devices.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Interest_Firefox_iOS__c',
        languages: ['de', 'en', 'es', 'fr', 'id', 'pt', 'ru', 'pl', 'zh-TW'],
        requires_double_optin: true,
        firefox_confirm: true,
        is_mofo: false,
        order: 37
    },
    'mozilla-general': {
        title: 'Mozilla',
        description:
            'Special announcements and messages from the team dedicated to keeping the Web free and open.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Interest_Mozilla__c',
        languages: ['de', 'en', 'es', 'fr', 'id', 'pt', 'ru', 'pl', 'zh-TW'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: false,
        order: 38
    },
    'firefox-os': {
        title: 'Firefox OS smartphone owner?',
        description:
            'Don’t miss important news and updates about your Firefox OS device.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_FirefoxOS_Owner__c',
        languages: ['de', 'en', 'es', 'fr', 'id', 'pt', 'ru', 'pl', 'zh-TW'],
        requires_double_optin: true,
        firefox_confirm: true,
        is_mofo: false,
        order: 39
    },
    'shape-web': {
        title: 'Shape of the Web',
        description: 'News and information related to the health of the web.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Shape_Of_The_Web__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: false,
        is_mofo: false,
        order: 40
    },
    'maker-party': {
        title: 'Maker Party',
        description:
            "Mozilla's largest celebration of making and learning on the web.",
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Maker_Party__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: false,
        is_mofo: false,
        order: 41
    },
    'connected-devices': {
        title: 'Connected Devices',
        description:
            'Get updates from the Connected Devices team and receive invitations to participate in the development of devices powered by Mozilla.',
        show: false,
        active: false,
        private: false,
        indent: false,
        vendor_id: 'Sub_Connected_Devices__c',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: false,
        order: 42
    },
    'firefox-welcome': {
        title: 'Firefox Welcome',
        description:
            'Learn how to get the most out of Firefox, the browser that sets you free online.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Firefox_Welcome__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: true,
        is_mofo: false,
        order: 43
    },
    'mozilla-welcome': {
        title: 'Mozilla Welcome',
        description:
            'Learn how to get the most out of Firefox, the browser made by Mozilla.',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Mozilla_Welcome__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: false,
        is_mofo: false,
        order: 44
    },
    'member-idealo': {
        title: 'Firefox Membership: Ideologically Engaged',
        description: '',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Member_Ideal__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: true,
        is_mofo: false,
        order: 45
    },
    'member-comm': {
        title: 'Firefox Membership: Community Minded',
        description: '',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Member_Comm__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: true,
        is_mofo: false,
        order: 46
    },
    'member-tech': {
        title: 'Firefox Membership: Tech-Forward',
        description: '',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Member_Tech__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: true,
        is_mofo: false,
        order: 47
    },
    'member-tk': {
        title: 'Firefox Membership: TK',
        description: '',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Member_Tk__c',
        languages: ['en'],
        requires_double_optin: false,
        firefox_confirm: true,
        is_mofo: false,
        order: 48
    },
    'guardian-vpn-waitlist': {
        title: 'Mozilla VPN Waitlist',
        description: 'The Mozilla VPN waitinglist indication',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'Sub_Guardian_VPN_Waitlist__c',
        languages: ['en', 'de', 'fr'],
        requires_double_optin: false,
        firefox_confirm: false,
        is_mofo: false,
        order: 49
    },
    'mozilla-rally': {
        title: 'Mozilla Rally News',
        description:
            'Mozilla Rally is a data contribution platform for people to put their data to work for a better Internet and society. Join our community!',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'sub_rally',
        languages: ['en'],
        requires_double_optin: true,
        firefox_confirm: false,
        is_mofo: false,
        order: 50
    },
    'relay-waitlist': {
        title: 'Firefox Relay Waitlist',
        description: 'Waiting list for Firefox Relay',
        show: false,
        active: true,
        private: false,
        indent: false,
        vendor_id: 'relay_waitlist',
        languages: ['de', 'en', 'es', 'fr', 'id', 'pt', 'ru', 'pl', 'zh-TW'],
        requires_double_optin: true,
        firefox_confirm: true,
        is_mofo: false,
        order: 60
    }
};

const stringData = {
    'about-mozilla': {
        description:
            'Join Mozillians all around the world and learn about impactful opportunities to support Mozilla’s mission.',
        title: 'Mozilla Community'
    },
    'about-standards': {
        title: 'About Standards'
    },
    'addon-dev': {
        title: 'Add-on Development'
    },
    affiliates: {
        description:
            'A monthly newsletter to keep you up to date with the Firefox Affiliates program.',
        title: 'Firefox Affiliates'
    },
    ambassadors: {
        description:
            'A monthly newsletter on how to get involved with Mozilla on your campus.',
        title: 'Firefox Student Ambassadors'
    },
    'app-dev': {
        description:
            'A developer’s guide to highlights of Web platform innovations, best practices, new documentation and more.',
        title: 'Developer Newsletter'
    },
    aurora: {
        description: 'Aurora',
        title: 'Aurora'
    },
    beta: {
        description:
            'Read about the latest features for Firefox desktop and mobile before the final release.',
        title: 'Beta News'
    },
    'download-firefox-android': {
        title: 'Download Firefox for Android'
    },
    'download-firefox-androidsn': {
        title: 'Get Firefox for Android'
    },
    'download-firefox-androidsnus': {
        title: 'Get Firefox for Android'
    },
    'download-firefox-ios': {
        title: 'Download Firefox for iOS'
    },
    'download-firefox-mobile': {
        title: 'Download Firefox for Mobile'
    },
    drumbeat: {
        title: 'Drumbeat Newsgroup'
    },
    'firefox-accounts-journey': {
        description: 'Get the most out of your Firefox Account.',
        title: 'Firefox Accounts Tips'
    },
    'firefox-desktop': {
        description:
            'Don’t miss the latest announcements about our desktop browser.',
        title: 'Firefox for desktop'
    },
    'firefox-flicks': {
        description:
            'Periodic email updates about our annual international film competition.',
        title: 'Firefox Flicks'
    },
    'firefox-ios': {
        description:
            'Be the first to know when Firefox is available for iOS devices.',
        title: 'Firefox iOS'
    },
    'firefox-os': {
        description:
            'Don’t miss important news and updates about your Firefox OS device.',
        title: 'Firefox OS smartphone owner?'
    },
    'firefox-os-news': {
        description:
            'A monthly newsletter and special announcements on how to get the most from your Firefox OS device, including the latest features and coolest Firefox Marketplace apps.',
        title: 'Firefox OS + You'
    },
    'firefox-tips': {
        description:
            'Get a weekly tip on how to super-charge your Firefox experience.',
        title: 'Firefox Weekly Tips'
    },
    'get-android-embed': {
        title: 'Get Firefox for Android'
    },
    'get-android-notembed': {
        title: 'Get Firefox for Android'
    },
    'get-involved': {
        title: 'Get Involved'
    },
    'internet-health-report': {
        title: 'Insights',
        description:
            'Mozilla publishes articles and deep dives on issues around internet health and trustworthy AI, including our annual Internet Health Report.'
    },
    'join-mozilla': {
        title: 'Join Mozilla'
    },
    'knowledge-is-power': {
        description:
            'Get all the knowledge you need to stay safer and smarter online.',
        title: 'Knowledge is Power'
    },
    labs: {
        title: 'About Labs'
    },
    'maker-party': {
        description:
            'Mozilla’s largest celebration of making and learning on the web.',
        title: 'Maker Party'
    },
    marketplace: {
        description: 'Discover the latest, coolest HTML5 apps on Firefox OS.',
        title: 'Firefox OS'
    },
    'marketplace-android': {
        title: 'Android'
    },
    'marketplace-desktop': {
        title: 'Desktop'
    },
    mobile: {
        description:
            'Keep up with releases and news about Firefox for Android.',
        title: 'Firefox for Android'
    },
    'mozilla-and-you': {
        description:
            'Get how-tos, advice and news to make your Firefox experience work best for you.',
        title: 'Firefox News'
    },
    'mozilla-festival': {
        description:
            'Special announcements about our annual festival dedicated to forging the future of the open web.',
        title: 'Mozilla Festival'
    },
    'mozilla-foundation': {
        description:
            'Regular updates to help you get smarter about your online life and active in our fight for a better internet.',
        title: 'Mozilla News'
    },
    'mozilla-general': {
        description:
            'Special announcements and messages from the team dedicated to keeping the Web free and open.',
        title: 'Mozilla'
    },
    'mozilla-learning-network': {
        description:
            'Updates from our global community, helping people learn the most important skills of our age: the ability to read, write and participate in the digital world.',
        title: 'Mozilla Learning Network'
    },
    'mozilla-phone': {
        description: 'Email updates for vouched Mozillians on mozillians.org.',
        title: 'Mozillians'
    },
    os: {
        description:
            'Firefox OS news, tips, launch information and where to buy.',
        title: 'Firefox OS'
    },
    'shape-web': {
        description: 'News and information related to the health of the web.',
        title: 'Shape of the Web'
    },
    'student-reps': {
        description:
            'Former University program from 2008-2011, now retired and relaunched as the Firefox Student Ambassadors program.',
        title: 'Student Reps'
    },
    'take-action-for-the-internet': {
        description:
            'Add your voice to petitions, events and initiatives that fight for the future of the web.',
        title: 'Take Action for the Internet'
    },
    'test-pilot': {
        description:
            'Help us make a better Firefox for you by test-driving our latest products and features.',
        title: 'New Product Testing'
    },
    webmaker: {
        description:
            'Special announcements helping you get the most out of Webmaker.',
        title: 'Webmaker'
    },
    'subscribe-copy': {
        title: 'Subscribe'
    }
};

export { userData, newsletterData, stringData };
