# -*- coding: utf-8 -*-

from collections import namedtuple

Grant = namedtuple('Grant', 'url, grantee, location, title, type, total_support, '
                            'year, description, break_down, urls')

GRANTS = [
    Grant(
        u'dream-yard',
        u'DreamYard Project',
        u'United States',
        u'Hive Fashion DreamYard Summer Intensive',
        u'learning-webmaking',
        u'$8,250',
        2012,
        u'<p> Mozilla provided a grant to <a href="http://www.dreamyard.com/">'
        u'DreamYard Arts Center</a> in the Bronx, NY, in conjunction with '
        u'<a href="http://explorecreateshare.org/2012/07/20/'
        u'next-seasons-hottest-trend-hive-fashion/">Hive Fashion</a>, '
        u'to support a DIY Fashion intensive for teens in August 2012.</p>',
        u'',
        u'',
    ),
    Grant(
        u'compumentor',
        u'Compumentor',
        u'United States',
        u'2007 TechSoup Netsquared Conference',
        u'free-culture-community',
        u'$2,000',
        2007,
        u'<p>Mozilla contributed to the 2007 TechSoup <a href="http://www.netsquared.org">'
        u'Netsquared Conference</a> Innovation Fund to support innovative software applications '
        u'created by and for non-profit organizations.</p>',
        u'',
        u'',
    ),
    Grant(
        u'codethink',
        u'Codethink Ltd.',
        u'United Kingdom',
        u'Accessibility Research',
        u'open-source-technology',
        u'$4,427',
        2007,
        u'<p>Mozilla made a grant to <a href="http://www.codethink.co.uk/">Codethink Ltd.</a> '
        u'to do a feasibility study for migrating the AT-SPI accessibility '
        u'interface to use D-Bus.</p>',
        u'',
        u'',
    ),
    Grant(
        u'charles-chen',
        u'Charles Chen',
        u'United States',
        u'Fire Vox',
        u'open-source-technology',
        u'$11,976',
        2007,
        u'<p>Mozilla supported the work of Charles Chen to implement ARIA widgets in the '
        u'<a href="http://www.accessfirefox.org/Fire_Vox.php">Fire Vox</a> open source '
        u'screen reader extension for Firefox.</p>',
        u'',
        u'',
    ),
    Grant(
        u'ariel-rios',
        u'Ariel Rios',
        u'United States',
        u'GNOME Accessibility',
        u'open-source-technology',
        u'$12,471',
        2007,
        u'<p>Mozilla supported the work of Ariel Rios to implement the AT-SPI Collection '
        u'interface for better Firefox accessibility on Linux.</p>',
        u'',
        u'',
    ),
    Grant(
        u'aapd',
        u'American Association of People with Disabilities',
        u'United States',
        u'AAPD',
        u'free-culture-community',
        u'$1,000',
        2007,
        u'<p>Mozilla sponsored the <a href="http://www.aapd.com/">AAPD</a> Leadership Gala '
        u'and related activities.</p>',
        u'',
        u'',
    ),
    Grant(
        u'peoples-production-house',
        u'People’s Production House',
        u'United States',
        u'World’s Fair 2.0 Design Intensive Incubator',
        u'learning-webmaking',
        u'$14,500',
        2012,
        u'<p>This grant to the <a href="http://peoplesproductionhouse.org/">'
        u'People’s Production House</a> supported the implementation of three '
        u'design workshops for youth in conjunction with World’s Fair 2.0, a '
        u'cell-phone based journalism scavenger hunt that investigates the borough '
        u'of Queens’ history - past and present. The final Design Intensive '
        u'took place during Maker Faire, and involved youth in the installation of '
        u'their work at the New York Hall of Science.</p>',
        u'',
        u'',
    ),
    Grant(
        u'participatory-culture-foundation',
        u'Participatory Culture Foundation',
        u'United States',
        u'NewsHour Open Election 2012',
        u'free-culture-community',
        u'$266,530.42',
        2012,
        u'<p>As part of the NewsHour Open Election 2012 project, supported by the '
        u'Corporation for Public Broadcasting, and in partnership with PBS NewsHour and '
        u'Mozilla, the <a href="http://pculture.org/">Participatory Culture Foundation</a> '
        u'has received support to develop crowd-sourcing technologies to enable citizen '
        u'volunteers to translate and caption 2012 election coverage into dozens of languages, '
        u'as well as for the deaf and hard-of-hearing. These technologies will make election '
        u'news, speeches and debates more accessible for diverse audiences, helping to increase '
        u'their understanding of, and engagement in, the political process.</p>',
        u'',
        u'',
    ),
    Grant(
        u'global-kids-inc',
        u'Global Kids Inc.',
        u'United States',
        u'PenPal News',
        u'learning-webmaking',
        u'$15,000',
        2012,
        u'<p> Mozilla provided a grant to <a href="http://www.globalkids.org/">'
        u'Global Kids Inc.</a>, in conjunction with Hive NYC, for the development of '
        u'PenPal News software. PenPal News is a web app that uses news as a '
        u'conversation-starter to connect middle and high school-aged youth '
        u'domestically and internationally.</p>',
        u'',
        u'',
    ),
    Grant(
        u'public_knowledge',
        u'Public Knowledge',
        u'United States',
        u'Public Knowledge',
        u'user-sovereignty',
        u'$5,000',
        2012,
        u'<p><a href="http://www.publicknowledge.org/">Public Knowledge</a> preserves the '
        u'openness of the Internet and the public’s access to knowledge, promotes creativity '
        u'through balanced copyright, and upholds and protects the rights of consumers to use '
        u'innovative technology lawfully.</p>',
        u'',
        u'',
    ),
    Grant(
        u'institute_of_play',
        u'Institute of Play',
        u'United States',
        u'Hive Activity Delivery Mechanism',
        u'learning-webmaking',
        u'$12,604',
        2012,
        u'<p>This grant to the <a href="http://www.instituteofplay.org/">Institute of Play</a> '
        u'provided support for the Hive Activity Delivery Mechanism Project, which seeks to '
        u'develop a sharing model for Hive-developed learning activities that represents the '
        u'collaboration, experimentation and youth-focus that typifies the '
        u'Hive and its members.</p>',
        u'',
        u'',
    ),
    Grant(
        u'cbc',
        u'CBC Radio Canada',
        u'Canada',
        u'Marshall McLuhan Project',
        u'free-culture-community',
        u'$10,000',
        2011,
        u'<p>This grant was given to the <a href="http://www.cbc.ca">'
        u'Canadian Broadcasting Corporation</a> to support the creation of on-line '
        u'content to engage Canadians in the celebration of the 100th anniversary of '
        u'the birth of Marshall McLuhan.</p>',
        u'',
        u'',
    ),
    Grant(
        u'big-blue-button',
        u'Blindside Networks',
        u'Canada',
        u'BigBlueButton',
        u'open-source-technology',
        u'$11,000',
        2011,
        u'<p><a href="http://www.blindsidenetworks.com/">Blindside Networks</a> '
        u'is a company dedicated to helping universities, colleges, and commercial '
        u'companies deliver a high-quality learning experience to remote students. '
        u'The goal of the BigBlueButton open source project is to enable remote students '
        u'to have a high-quality learning experience. This grant supported converting '
        u'BigBlueButton 0.8-beta to use popcorn.js, the HTML5 media framework designed '
        u'for synchronized playback of media.</p>',
        u'',
        u'',
    ),
    Grant(
        u'depaul-university',
        u'DePaul University',
        u'United States',
        u'Digital Youth Mentor',
        u'learning-webmaking',
        u'$25,000',
        2011,
        u'<p>This grant was made to <a href="http://www.depaul.edu">DePaul University</a> '
        u'to support the employment of a Digital Youth Mentor.</p>',
        u'',
        u'',
    ),
    Grant(
        u'new-youth-city',
        u'New Youth City Learning Network',
        u'United States',
        u'Hackasaurus',
        u'learning-webmaking',
        u'$25,000',
        2011,
        u'<p>This grant to the <a href="http://dmlcentral.net/projects/3658">'
        u'New Youth City Learning Network</a> at the Social Science Research Centre '
        u'supported the development of Hackasaurus. Hackasaurus is a set of tools that '
        u'are under development to help teenagers closely review, remix and redesign '
        u'the Web. Hackasaurus was prototyped with youth over the course of several '
        u'workshops and jam days in New York and Chicago.</p>',
        u'',
        u'',
    ),
    Grant(
        u'henrik-moltke',
        u'Henrik Moltke',
        u'Germany',
        u'Hyperaudio',
        u'free-culture-community',
        u'$10,000',
        2011,
        u'<p>This grant supported the development of a compelling concept and implementation '
        u'plan for the <a href="http://www.hyperaudio.org/">Hyperaudio</a> project.</p>',
        u'',
        u'',
    ),
    Grant(
        u'bay-area-video-coalition',
        u'Bay Area Video Coalition',
        u'United States',
        u'Zero Divide/Mozilla Youth Media Project',
        u'open-source-technology',
        u'$88,500',
        2012,
        u'<p>The <a href="http://www.bavc.org/">Bay Area Video Coalition (BAVC)</a> '
        u'was an implementation partner in the Mozilla Foundation/Zero Divide youth '
        u'media project in 2011. They worked together to test software prototypes for '
        u'Butter, a user interface for WebMadeMovies; to instruct and lead youth '
        u'participants to create 3-4 web-native productions with these tools; and to '
        u'create a modular, openly-licensed curriculum to make it easier for people to '
        u'create HTML5/open video projects of their own.</p><p>In 2012, Mozilla provided '
        u'a grant to BAVC to support the <a href="http://bavc.org/creative_code">'
        u'Open Source track at BAVC’s Digital Pathways</a>, as part of a broader partnership '
        u'between BAVC and Mozilla to encourage next-generation integrated '
        u'learning and career skills.</p>',
        {
            u'2011': ['Amount: $73,500'],
            u'2012': ['Amount: $15,000']
        },
        u'',
    ),
    Grant(
        u'universal-subtitles',
        u'Universal Subtitles',
        u'United States',
        u'Universal Subtitles',
        u'free-culture-community',
        u'$100,000',
        2011,
        u'<p>In 2011, Mozilla provided a grant to support the development of '
        u'<a href="http://www.universalsubtitles.org">Universal Subtitles</a> '
        u'(now known as Amara). Amara gives individuals, communities, and larger '
        u'organizations the power to overcome accessibility and language barriers '
        u'for online video. The tools are free and open source and make the work of '
        u'subtitling and translating video simpler, more appealing, and, most of all, '
        u'more collaborative.</p>',
        u'',
        u'',
    ),
    Grant(
        u'adaptive-technology-resource-centre',
        u'Adaptive Technology Resource Centre',
        u'Canada',
        u'Adaptive Technology Resource Centre',
        u'open-source-technology',
        u'$10,000',
        2006,
        u'<p>This grant was made to the Adaptive Technology Resource Centre at '
        u'the University of Toronto (now the <a href="http://idrc.ocad.ca/">'
        u'Inclusive Design Research Centre</a> at the Ontario College of Art and Design). '
        u'It enabled the development of an accessible Thunderbird user interface as well as '
        u'its adoption through evangelism, mentoring, community-building, and technical '
        u'leadership, with a focus on working with the jQuery community to implement ARIA '
        u'support in this popular toolkit.</p>',
        u'',
        u'',
    ),
    Grant(
        u'benetech',
        u'Benetech',
        u'United States',
        u'Benetech DAISY Reader for Firefox',
        u'free-culture-community',
        u'$50,000',
        2009,
        u'<p>Mozilla provided funding over two years to <a href="http://www.benetech.org/">'
        u'Benetech</a>, a corporation dedicated to leveraging technology innovation and '
        u'business expertise to solve unmet social needs. This funding supports the development '
        u'of an open source, browser-based DAISY reader that enables people with print '
        u'disabilities to read accessible text using Firefox.</p>',
        {
            u'2008': ['Amount: $25,000'],
            u'2009': ['Amount: $25,000']
        },
        u'',
    ),
    Grant(
        u'nvda',
        u'NV Access',
        u'Australia',
        u'NVDA Screen Reader',
        u'open-source-technology',
        u'$135,000',
        2010,
        u'<p>Mozilla made grants to <a href="http://www.nvaccess.org/">NV Access</a> '
        u'from 2007 to 2010 to support the development of '
        u'<a href="http://www.nvda-project.org/">NonVisual Desktop Access (NVDA)</a>, '
        u'a free and open source screen reader for the Microsoft Windows operating system. '
        u'Providing feedback via synthetic speech and Braille, it enables blind or vision '
        u'impaired people to access computers running Windows for no more '
        u'cost than a sighted person.</p>',
        {
            u'2007': ['Initial Support: $10,000', 'Support for full time work of James Teh: $80,000'],
            u'2009': ['Expanding work: $25,000'],
            u'2010': ['Growing influence: $20,000']
        },
        [
            u'http://www.nvda-project.org/blog/'
            u'Mozilla_Foundation_grant_allows_for_employment_of_NVDA_full-time_developer',
            u'http://www.nvda-project.org/blog/First_Work_on_Web_Access_Grant',
            u'http://www.nvda-project.org/blog/NewMozillaGrantFurthersNVDA',
            u'http://www.nvda-project.org/blog/NVDAPresentationAtCSUN2009'
        ]
    ),
    Grant(
        u'firebug-accessibility',
        u'University of Illinois Urbana-Champaign & The Paciello Group ',
        u'United States',
        u'Firebug Accessibility',
        u'open-source-technology',
        u'$120,009',
        2010,
        u'<p>This grant provided funds to the <a href="http://illinois.edu/">'
        u'University of Illinois Urbana-Champaign</a> and '
        u'<a href="http://www.paciellogroup.com/">The Paciello Group</a> in 2009 '
        u'and 2010 for their joint work on Firebug accessibility. The goal was to '
        u'mainstream accessibility for web applications by building accessibility '
        u'testing functions and associated test cases into '
        u'<a href="http://getfirebug.com/">Firebug</a>, a popular tool used by many '
        u'web developers.</p>',
        {
            u'2009': ['Phase One: $25,000', 'Phase Two: $25,000', 'Phase Three: $25,000'],
            u'2010': ['Phase Four: $25,000', 'Phase Five: $20,009']
        },
        u'',
    ),
    Grant(
        u'vquence',
        u'Vquence',
        u'Australia',
        u'Vquence',
        u'open-source-technology',
        u'$75,000',
        2010,
        u'<p>In the spring of 2008 Mozilla became concerned about the lack of '
        u'support for deaf and blind Firefox users. Mozilla identified '
        u'<a href="http://www.gingertech.net/">Dr. Silvia Pfeiffer</a> and her '
        u'company Vquence as the best resource for creating a plan for open '
        u'video accessibility. By providing grants in 2008, 2009 and 2010, '
        u'Mozilla supported the technology that implemented Firefox video '
        u'accessibility features, such as text subtitles for the hearing-impaired '
        u'and audio descriptions for blind users.</p>',
        {
            u'2008': ['Amount: $25,000'],
            u'2009': ['Amount: $25,000'],
            u'2010': ['Amount: $25,000']
        },
        [
            u'http://frankhecker.com/2009/06/30/new-mozilla-accessibility-projects/',
        ]
    ),
    Grant(
        u'web4all',
        u'World Wide Web Consortium',
        u'UK',
        u'Web4All Conference',
        u'free-culture-community',
        u'$4,000',
        2010,
        u'<p>Mozilla has sponsored the <a href="http://www.w4a.info/">Web4All Conference</a> '
        u'for several years, and has also sponsored several speakers to be able to attend. '
        u'The Web4All Conference is an annual cross-disciplinary gathering focused on '
        u'Scientific Enquiry, Research, Development and Engineering. Views bridge academia, '
        u'commerce and industry, and arguments encompassing a range of beliefs across the '
        u'design-accessibility spectrum are presented.</p>',
        {
            u'2007': ['Amount: $1,000'],
            u'2008': ['Amount: $1,000'],
            u'2009': ['Amount: $1,000'],
            u'2010': ['Amount: $1,000'],
        },
        u'',
    ),
    Grant(
        u'creative-commons',
        u'Creative Commons',
        u'United States',
        u'Creative Commons Pledge',
        u'free-culture-community',
        u'$300,000',
        2010,
        u'<p>In December 2007, Mozilla decided to participate in '
        u'<a href="http://creativecommons.org/">Creative Commons</a> "5x5 Challenge." '
        u'Beginning in 2008, Mozilla pledged $100,000 per year for five years to support '
        u'open licensing on the web, developing hybrid organizations, and maturing the '
        u'concept of the web as an ecology of shared ideas.</p>',
        {
            u'2008': ['Amount: $100,000'],
            u'2009': ['Amount: $100,000'],
            u'2010': ['Amount: $100,000'],
        },
        u'',
    ),
    Grant(
        u'foms',
        u'Annodex Association',
        u'Australia',
        u'Foundations of Open Media Software Workshop',
        u'free-culture-community',
        u'$15,000',
        2009,
        u'<p>These grants provided sponsorship for the 2007, 2008 and 2009 '
        u'<a href="http://www.foms-workshop.org">Foundations of Open Media Software (FOMS)</a> '
        u'workshop in Hobart, Australia. The bulk of these funds were used to cover the travel '
        u'expenses of key participants who otherwise would have been unable to attend. '
        u'This meeting hosts important discussions on open codecs, HTML specifications, '
        u'browsers and hands-on work towards specifications for video in browsers.</p>',
        {
            u'2007': ['Amount: $5,000'],
            u'2008': ['Amount: $5,000'],
            u'2009': ['Amount: $5,000']
        },
        u'',
    ),
    Grant(
        u'free-culture-conference',
        u'Berkeley Center for Law and Technology',
        u'United States',
        u'Free Culture Conference',
        u'free-culture-community',
        u'$5,000',
        2008,
        u'<p>This grant provided sponsorship for the Free Culture Conference put '
        u'on by the <a href="http://www.law.berkeley.edu/bclt.htm">'
        u'Berkeley Center for Law and Technology</a>, held October 11 and 12, 2008 '
        u'in Berkeley, California. The Free Culture Conference is a yearly touchstone '
        u'event for the advancement of free cultures, where members are free to '
        u'participate without artificial limits.</p>',
        u'',
        u'',
    ),
    Grant(
        u'fscons',
        u'FFKP',
        u'Sweden',
        u'Free Society Conference and Nordic Summit',
        u'free-culture-community',
        u'$1,300',
        2009,
        u'<p>This grant provided sponsorship for the third '
        u'<a href="https://fscons.org/2009/">Free Society Conference and '
        u'Nordic Summit (FSCONS)</a> held November 13-15, 2009, in Goteborg, Sweden. '
        u'FSCONS is jointly organized by Free Software Foundation Europe, '
        u'Creative Commons and Wikipedia Sverige.</p>',
        u'',
        u'',
    ),
    Grant(
        u'free-software-foundation',
        u'Free Software Foundation',
        u'United States',
        u'LinuxBIOS Support',
        u'free-culture-community',
        u'$10,000',
        2007,
        u'<p>In 2007, Mozilla provided $10,000 to support the LinuxBIOS-related '
        u'activities of the <a href="http://www.fsf.org/">Free Software Foundation</a>. '
        u'This grant went toward software development, infrastructure and communications. '
        u'The Free Software Foundation ported coreboot to the alix.2c3 board, a board '
        u'useful in building routers, firewalls, and wifi access points.</p>',
        u'',
        u'',
    ),
    Grant(
        u'gnome',
        u'GNOME',
        u'United States',
        u'GNOME Accessibility',
        u'open-source-technology',
        u'$48,000',
        2010,
        u'<p>Mozilla offered grants in support of '
        u'<a href="http://projects.gnome.org/outreach/a11y/">GNOME’s Outreach '
        u'Program for Accessibility</a>. The <a href="http://www.gnome.org/">'
        u'GNOME Foundation</a> sponsors the GNOME project to provide a free desktop '
        u'environment for Linux systems. Mozilla and GNOME have been longtime '
        u'collaborators on open source and accessibility issues.</p><p>See the '
        u'<a href="reports/gnome-haeger-report/">grant final report</a> for more details.</p>',
        {
            u'2007': ['General Accessibility Support: $10,000'],
            u'2008': ['Orca rich document browsing extension: $8,000'],
            u'2009': ['GNOME Outreach Program: Accessibility: $10,000', 'CSUN Accessibility Conference: $10,000'],
            u'2010': ['General Accessibility Support: $10,000']
        },
        [
            u'https://blog.mozilla.org/blog/2010/02/04/mozilla-gnome-accessibility/',
        ]
    ),
    Grant(
        u'ifosslr',
        u'International Free and Open Source Software Law Review (IFOSSLR)',
        u'Europe',
        u'IFOSSLR Launch',
        u'user-sovereignty',
        u'$10,000',
        2009,
        u'<p>This grant funded the launch of the <a href="http://www.ifosslr.org/">'
        u'International Free and Open Source Software Law Review (IFOSSLR)</a>, a '
        u'collaborative legal publication aiming to increase knowledge and understanding '
        u'among lawyers about Free and Open Source Software issues. Topics included copyright, '
        u'licence implementation, licence interpretation, software patents, open standards, '
        u'case law and statutory changes.</p>',
        u'',
        u'',
    ),
    Grant(
        u'mozdev',
        u'MozDev',
        u'United States',
        u'MozDev Support',
        u'open-source-technology',
        u'$90,000',
        2008,
        u'<p>Mozilla supported the <a href="http://www.mozdev.org/about.html">'
        u'MozDev Community Organization</a> by providing general funds to support '
        u'MozDev’s operations. MozDev is a software development community dedicated '
        u'to making quality applications and extensions freely available to all computer '
        u'users. Its goal is to help establish Mozilla as a viable application development '
        u'platform. Since 2006, Mozilla grants have funded the majority of MozDev’s budget. '
        u'This support gives back to the community that contributes so much to establishing '
        u'Mozilla as a viable application development platform and the community that builds '
        u'quality applications and extensions.</p>',
        {
            u'2006': ['Amount: $30,000'],
            u'2007': ['Amount: $30,000'],
            u'2008': ['Amount: $30,000']
        },
        u'',
    ),
    Grant(
        u'nonprofit-software-development-summit',
        u'Aspiration',
        u'United States',
        u'Nonprofit Software Development Summit',
        u'free-culture-community',
        u'$5,000',
        2009,
        u'<p>This grant supported the <a href="http://www.aspirationtech.org/events/devsummit09">'
        u'Nonprofit Software Development Summit</a>, held November 18-20, 2009 in Oakland. '
        u'This was the third annual convening of people and organizations developing software '
        u'tools, web applications and other technology to support nonprofits and social '
        u'justice causes. <a href="http://www.aspirationtech.org/">Aspiration</a>, '
        u'the conference organizer, is a non-profit organization that connects nonprofits '
        u'with software solutions that help them better carry out their work.</p>',
        u'',
        u'',
    ),
    Grant(
        u'open-source-software-institute',
        u'Open Source Software Institute',
        u'United States',
        u'OCSP Stapling',
        u'open-source-technology',
        u'$30,000',
        2007,
        u'<p>This grant to the <a href="http://www.oss-institute.org/">'
        u'Open Source Software Institute</a>, in cooperation with the NSS '
        u'development team and Mozilla developers, investigated the problem of '
        u'providing OCSP stapling support for Apache and other open source '
        u'SSL/TLS-enabled server software incorporating the OpenSSL library. '
        u'The Open Source Software Institute (OSSI) was identified as having '
        u'extensive experience with OpenSSL, and was the lead organization '
        u'responsible for getting US government FIPS 140-2 validation of OpenSSL.</p>',
        u'',
        u'',
    ),
    Grant(
        u'open-video-alliance',
        u'Open Video Alliance',
        u'United States',
        u'Open Video Alliance',
        u'free-culture-community',
        u'$30,000',
        2009,
        u'<p>Mozilla offered support to <a href="http://openvideoalliance.org/">'
        u'Open Video Alliance</a> activities in support of the open video movement. '
        u'Open Video Alliance is a coalition of organizations and individuals committed '
        u'to the idea that the power of the moving image should belong to everyone. '
        u'This grant funded various efforts in the open video movement, such as the '
        u'operations of openvideoalliance.org, the branding of open video products, '
        u'outreach to the public media, fundraising and video production.</p>',
        u'',
        u'',
    ),
    Grant(
        u'perl-foundation',
        u'Perl Foundation',
        u'United States',
        u'Perl6 Support',
        u'open-source-technology',
        u'$10,000',
        2007,
        u'<p>Mozilla provided a grant to the <a href="http://www.perlfoundation.org/">'
        u'Perl Foundation</a>, a non-profit dedicated to the advancement of the Perl '
        u'programming language through open discussion, collaboration, design and code. '
        u'This grant supported the development of Perl 6.</p>',
        u'',
        u'',
    ),
    Grant(
        u'personal-democracy-forum',
        u'Personal Democracy Forum',
        u'United States',
        u'Personal Democracy Forum',
        u'user-sovereignty',
        u'$15,000',
        2009,
        u'<p>For two years Mozilla sponsored the <a href="http://personaldemocracy.com/'
        u'pdf-conference/personal-democracy-forum-conference">Personal Democracy Forum</a>, '
        u'a forum for discussion on how politics and technology intersect. Each year top '
        u'opinion-makers, political practitioners, technologists and journalists come '
        u'together to network, exchange ideas and explore how technology and the internet '
        u'are changing politics, democracy and society.</p>',
        {
            u'2008': ['Amount: $10,000'],
            u'2009': ['Amount: $5,000']
        },
        u'',
    ),
    Grant(
        u'software-freedom-conservancy',
        u'Software Freedom Conservancy',
        u'United States',
        u'Software Freedom Conservancy',
        u'free-culture-community',
        u'$30,000',
        2012,
        u'<p>Mozilla provided funding to help the '
        u'<a href="http://conservancy.softwarefreedom.org/">Software Freedom Conservancy</a> '
        u'serve additional open source projects and work more closely with peer projects. '
        u'As from 2008, Mozilla\'s funding helped the Conservancy to provide administrative, '
        u'financial management, coordination and logistical services to twenty FLOSS '
        u'(Free, Libre and Open Source Software) projects including Foresight Linux, '
        u'Sugar Labs, jQuery, Amarok, Darcs, OpenInkpot, and K-3D.</p>',
        {
            u'2008': ['Amount: $10,000'],
            u'2009': ['Amount: $10,000'],
            u'2012': ['Amount: $10,000']
        },
        u'',
    ),
    Grant(
        u'seneca',
        u'Seneca College',
        u'Canada',
        u'Seneca College',
        u'learning-webmaking',
        u'$327,860',
        2011,
        u'<p>Since 2005, <a href="http://www.senecac.on.ca/">Seneca College</a> '
        u'in Toronto has worked closely with the Mozilla community to create a set '
        u'of Mozilla-specific courses, engage hundreds of students directly in Mozilla '
        u'development projects, and host and record dozens of Mozilla events and talks. '
        u'Seneca’s faculty and students are key contributors to the Mozilla project, '
        u'and have gained significant experience bootstrapping new contributors into the '
        u'Mozilla technology and culture. Seneca College of Applied Arts and Technology is a '
        u'community college for applied arts and technology in Toronto, Ontario. </p>',
        {
            u'2006': ['Amount: $50,000'],
            u'2007': ['Amount: $100,000'],
            u'2009': ['Amount: $80,910'],
            u'2011': ['Amount: $96,950']
        },
        u'',
    ),
    Grant(
        u'leigh-school',
        u'Leigh School',
        u'New Zealand',
        u'Leigh School',
        u'learning-webmaking',
        u'$2,500',
        2009,
        u'<p>This grant is supporting ICT components for courses and the purchase of '
        u'equipment and software to support the ICT components of courses at '
        u'<a href="http://www.leigh.school.nz/">Leigh School</a>, a primary school in '
        u'New Zealand dedicated to a broad curriculum that includes computers and technology.</p>',
        u'',
        u'',
    ),
    Grant(
        u'peer2peer-university',
        u'Phillip Schmidt (P2PU)',
        u'United States',
        u'Peer2Peer University',
        u'learning-webmaking',
        u'$25,500',
        2011,
        u'<p>Mozilla issued a grant to Phillip Schmidt in 2009 '
        u'(<a href="http://www.p2pu.org/">P2PU</a>) to enable the creation of '
        u'an online course called <a href="https://wiki.mozilla.org/Education/EduCourse">'
        u'Open|Web|Content|Education</a>, where educators learned about open content licensing, '
        u'open web technologies and open teaching methods. In 2011, Mozilla provided a '
        u'grant to P2PU to support <a href="https://p2pu.org/en/schools/school-of-webcraft/sets/'
        u'webmaking-101/">Webmaking 101</a> and the <a href="https://p2pu.org/en/groups/schools/'
        u'school-of-webcraft/">School of Webcraft</a> community coordination.</p><p>P2PU combines '
        u'open educational resources, structured courses, and recognition of knowledge and '
        u'learning to offer high-quality low-cost education opportunities. It is run and '
        u'governed by volunteers.</p>',
        {
            u'2009': ['Open|Web|Content|Education: $2,500'],
            u'2011': ['Webmaking 101 - Project Management & School of Webcraft - Community Coordination: $23,000']
        },
        u'',
    ),
    Grant(
        u'ushaidi-chile',
        u'Ushahidi',
        u'United States and Chile',
        u'Ushahidi Chile',
        u'free-culture-community',
        u'$10,000',
        2010,
        u'<p>In a crisis environment, maintaining lines of communication is critically important. '
        u'<a href="http://www.ushahidi.com/">Ushahidi</a> developed an open source platform that '
        u'enables citizen reporting in crisis situations. A deadly earthquake struck Chile on '
        u'February 27, 2010, cutting off many vulnerable people from traditional sources of '
        u'information. Mozilla awarded a grant to enable Ushahidi volunteers to train Chilean '
        u'civilians and government officials to utilize the Ushahidi platform during the relief '
        u'effort.</p><p>See the <a href="reports/ushahidi-chile-report/">final grant report</a> '
        u'for more details.</p>',
        u'',
        [
            u'http://blog.ushahidi.com/index.php/2010/03/15/mozilla-foundation-supports-ushahidi-chile/',
        ]
    ),
    Grant(
        u'atlan',
        u'Atlan Laboratories',
        u'United States',
        u'FIPS 140-2 Validation',
        u'open-source-technology',
        u'$25,000',
        2008,
        u'<p>This grant to Atlan Labs, along with funding from Red Hat and Sun Microsystems, '
        u'supported FIPS 140-2 validation for the latest version of Network Security Services '
        u'(NSS). Federal Information Processing Standards Publications (FIPS PUBS) '
        u'140-1 and 140-2 are US government standards for implementations of cryptographic '
        u'modules - that is, hardware or software that encrypts and decrypts data or '
        u'performs other cryptographic operations. Atlan Labs was a a cybersecurity '
        u'product testing firm based in McLean, Virginia that provided Federal Information '
        u'Processing Standard (FIPS) 140-2 and 201 validations. Atlan was acquired by '
        u'<a href="http://www.saic.com/infosec/testing-accreditation/">SAIC</a> in July 2009.</p>',
        u'',
        u'',
    ),
    Grant(
        u'automated-calendar-testing',
        u'Merike Sell',
        u'Estonia',
        u'Calendar Automated Testing',
        u'open-source-technology',
        u'$4,500',
        2009,
        u'<p>This grant is funding the development of calendar automated testing for the '
        u'Mozilla calendar code. This was originally an idea presented at the 2009 '
        u'Google Summer of Code, and Mozilla Calendar developers became interested in '
        u'funding technology that would enable automated testing. Merike Sell is an active '
        u'member of the Mozilla developer and localization communites who live in Estonia.</p>',
        u'',
        u'',
    ),
    Grant(
        u'w3c-validator',
        u'World Wide Web Consortium',
        u'International',
        u'W3C Validator',
        u'open-source-technology',
        u'$15,000',
        2009,
        u'<p>The Mozilla Foundation is a member of the <a href="http://www.w3.org/">'
        u'World Wide Web Consortium</a>, and various Mozilla people represent Mozilla in '
        u'W3C working groups and other W3C contexts. This grant was issued beyond Mozilla’s '
        u'existing W3C membership dues, and funded work on '
        u'<a href="http://jigsaw.w3.org/css-validator/">W3C CSS Validator</a> by giving to '
        u'ERCIM, the W3C’s donation program.</p>',
        u'',
        u'',
    ),
    Grant(
        u'jambu',
        u'Jambu',
        u'United States',
        u'Jambu',
        u'open-source-technology',
        u'$25,000',
        2007,
        u'<p><a href="www.oatsoft.org/Software/jambu">Jambu</a> is a pointer and switch '
        u'project that improves accessibility for people with physical disabilities. '
        u'This grant supported the improvement of switch access to Firefox on Windows, '
        u'with the greater goal of providing transparent alternative input access to computers. '
        u'Users served by this project may include adults who have experienced a debilitating '
        u'accident or stroke, people with congential physical disabilities, children with '
        u'multiple disabilities, and those with learning difficulties or limited education '
        u'who often need to learn to use a switch through specialist educational programs.</p>',
        {
            u'2006': ['Phase 1: $15,000'],
            u'2007': ['Phase 2: $10,000'],
        },
        u'',
    ),
    Grant(
        u'nu',
        u'Northeastern University',
        u'United States',
        u'Graduate-level work of PhD students at Northeastern University',
        u'open-source-technology',
        u'$283,085',
        2010,
        u'<p>Since 2009 Mozilla has supported the graduate-level work of PhD students at '
        u'<a href="http://www.ccs.neu.edu/">Northeastern University</a>, developing new tools '
        u'for the standardization, streamlining, and testing of JavaScript. In 2009 Mozilla '
        u'contributed $99,115 to the research efforts of '
        u'<a href="http://www.ccs.neu.edu/home/samth/">Sam Tobin-Hochstadt</a>. In 2010 '
        u'Mozilla made two gifts: one of $107,596 to further support Mr. Tobin-Hochstadt’s '
        u'research and another gift of $76,374 to <a href="http://www.ccs.neu.edu/home/dimvar/">'
        u'Demetrios Vardoulakis</a>.</p>',
        {
            u'2009': ['PhD Research of Sam Tobin-Hochstadt: $99,115'],
            u'2010': ['PhD research of Sam Tobin-Hochstadt and Demetrios Vardoulakis: $107,596 and $76,374']
        },
        u'',
    ),
    Grant(
        u'owasp',
        u'OWASP',
        u'United States',
        u'The Open Web Application Security Project',
        u'open-source-technology',
        u'$15,000',
        2010,
        u'<p>This grant supports the <a href="http://www.owasp.org/index.php/Main_Page">'
        u'Open Web Application Security Project</a>, which focuses on improving the security '
        u'of application software. OWASP\'s mission is to make application security visible, '
        u'so that people and organizations can make informed decisions about true '
        u'application security risks.</p>',
        u'',
        u'',
    ),
    Grant(
        u'webaim',
        u'WebAIM',
        u'United States',
        u'WebAIM',
        u'open-source-technology',
        u'$15,000',
        2006,
        u'<p>In 2006, Mozilla provided a grant to <a href="http://webaim.org/">WebAIM</a>, '
        u'an accessibility organization based at Utah State University, to develop XUL '
        u'accessibility guidelines and an accompanying evaluation tool. WebAIM has provided '
        u'comprehensive web accessibility solutions since 1999. These years of experience '
        u'have made WebAIM one of the leading providers of web accessibility expertise '
        u'internationally. WebAIM is a non-profit organization within the Center for '
        u'Persons with Disabilities at Utah State University.</p>',
        u'',
        u'',
    ),
]
