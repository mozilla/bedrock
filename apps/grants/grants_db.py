from collections import namedtuple

Grant = namedtuple('Grant', 'url, grantee, location, title, type, total_support, year, description, break_down, urls')

GRANTS = [
    Grant(
        "adaptive-technology-resource-centre",
        "Adaptive Technology Resource Centre",
        'Canada',
        "Adaptive Technology Resource Centre",
        "open-source-technology",
        "$10'000",
        2006,
        '<p>This grant was made to the Adaptive Technology Resource Centre at the University of Toronto (now the <a href="http://idrc.ocad.ca/">Inclusive Design Research Centre</a> at the Ontario College of Art and Design). It enabled the development of an accessible Thunderbird user interface as well as its adoption through evangelism, mentoring, community-building, and technical leadership, with a focus on working with the jQuery community to implement ARIA support in this popular toolkit.</p>',
        "",
        ""
    ),
    Grant(
        "benetech",
        "Benetech",
        "United States",
        "Benetech DAISY Reader for Firefox",
        "free-culture-community",
        "$50'000",
        2009,
        '<p>Mozilla provided funding over two years to <a href="http://www.benetech.org/">Benetech</a>, a corporation dedicated to leveraging technology innovation and business expertise to solve unmet social needs. This funding supports the development of an open source, browser-based DAISY reader that enables people with print disabilities to read accessible text using Firefox.</p>',
        {
            '2008': ['Amount: $25,000'],
            '2009': ['Amount: $25,000']
        },
        ""
    ),
    Grant(
        "nvda",
        "NV Access",
        "Australia",
        "NVDA Screen Reader",
        "open-source-technology",
        "$135'000",
        2010,
        '<p>Mozilla made grants to <a href="http://www.nvaccess.org/">NV Access</a> from 2007 to 2010 to support the development of <a href="http://www.nvda-project.org/">NonVisual Desktop Access (NVDA)</a>, a free and open source screen reader for the Microsoft Windows operating system. Providing feedback via synthetic speech and Braille, it enables blind or vision impaired people to access computers running Windows for no more cost than a sighted person.</p>',
        {
            '2007': ['Initial Support: $10,000', 'Support for full time work of James Teh: $80,000'],
            '2009': ['Expanding work: $25,000'],
            '2010': ['Growing influence: $20,000']
        },
        [
            'http://www.nvda-project.org/blog/Mozilla_Foundation_grant_allows_for_employment_of_NVDA_full-time_developer',
            'http://www.nvda-project.org/blog/First_Work_on_Web_Access_Grant',
            'http://www.nvda-project.org/blog/NewMozillaGrantFurthersNVDA',
            'http://www.nvda-project.org/blog/NVDAPresentationAtCSUN2009'
        ]
    ),
    Grant(
        "firebug-accessibility",
        "University of Illinois Urbana-Champaign & The Paciello Group ",
        "United States",
        "Firebug Accessibility",
        "open-source-technology",
        "$120'009",
        2010,
        '<p>This grant provided funds to the <a href="http://illinois.edu/">University of Illinois Urbana-Champaign</a> and <a href="http://www.paciellogroup.com/">The Paciello Group</a> in 2009 and 2010 for their joint work on Firebug accessibility. The goal was to mainstream accessibility for web applications by building accessibility testing functions and associated test cases into <a href="http://getfirebug.com/">Firebug</a>, a popular tool used by many web developers.</p>',
        {
            '2009': ['Phase One: $25,000', 'Phase Two: $25,000', 'Phase Three: $25,000'],
            '2010': ['Phase Four: $25,000', 'Phase Five: $20,009']
        },
        ""
    ),
    Grant(
        "vquence",
        "Vquence",
        "Australia",
        "Vquence",
        "open-source-technology",
        "$75'000",
        2010,
        '<p>In the spring of 2008 Mozilla became concerned about the lack of support for deaf and blind Firefox users. Mozilla identified <a href="http://www.gingertech.net/">Dr. Silvia Pfeiffer</a> and her company Vquence as the best resource for creating a plan for open video accessibility. By providing grants in 2008, 2009 and 2010, Mozilla supported the technology that implemented Firefox video accessibility features, such as text subtitles for the hearing-impaired and audio descriptions for blind users.</p>',
        {
            '2008': ['Amount: $25,000'],
            '2009': ['Amount: $25,000'],
            '2010': ['Amount: $25,000']
        },
        [
            'http://frankhecker.com/2009/06/30/new-mozilla-accessibility-projects/',
        ]
    ),
    Grant(
        "web4all",
        "World Wide Web Consortium",
        "UK",
        "Web4All Conference",
        "free-culture-community",
        "$4'000",
        2010,
        '<p>Mozilla has sponsored the <a href="http://www.w4a.info/">Web4All Conference</a> for several years, and has also sponsored several speakers to be able to attend. The Web4All Conference is an annual cross-disciplinary gathering focused on Scientific Enquiry, Research, Development and Engineering. Views bridge academia, commerce and industry, and arguments encompassing a range of beliefs across the design-accessibility spectrum are presented.</p>',
        {
            '2007': ['Amount: $1,000'],
            '2008': ['Amount: $1,000'],
            '2009': ['Amount: $1,000'],
            '2010': ['Amount: $1,000'],
        },
        ""
    ),
    Grant(
        "creative-commons",
        "Creative Commons",
        "United States",
        "Creative Commons Pledge",
        "free-culture-community",
        "$500'000",
        2012,
        '<p>In December 2007, Mozilla decided to participate in <a href="http://creativecommons.org/">Creative Commons</a> "5x5 Challenge." Beginning in 2008, Mozilla pledged $100,000 per year for five years to support open licensing on the web, developing hybrid organizations, and maturing the concept of the web as an ecology of shared ideas.</p>',
        {
            '2008': ['Amount: $100,000'],
            '2009': ['Amount: $100,000'],
            '2010': ['Amount: $100,000'],
            '2011': ['Amount: $100,000'],
            '2012': ['Amount: $100,000']
        },
        [
            'http://frankhecker.com/2009/06/30/new-mozilla-accessibility-projects/',
        ]
    ),
    Grant(
        "foms",
        "Annodex Association",
        "Australia",
        "Foundations of Open Media Software Workshop",
        "free-culture-community",
        "$10'000",
        2009,
        '<p>This grant provided sponsorship for the 2008 and 2009 <a href="http://www.foms-workshop.org">Foundations of the Open Media Software (FOMS)</a> workshop in Hobart, Australia. The bulk of these funds were used to cover the travel expenses of key participants who otherwise would have been unable to attend. This meeting hosts important discussions on open codecs, HTML specifications, browsers and hands-on work towards specifications for video in browsers.</p>',
        {
            '2008': ['Amount: $5,000'],
            '2009': ['Amount: $5,000'],
        },
        ""
    ),
    Grant(
        "free-culture-conference",
        "Berkeley Center for Law and Technology",
        "United States",
        "Free Culture Conference",
        "free-culture-community",
        "$5'000",
        2008,
        '<p>This grant provided sponsorship for the Free Culture Conference put on by the <a href="http://www.law.berkeley.edu/bclt.htm">Berkeley Center for Law and Technology</a>, held October 11 and 12, 2008 in Berkeley, California. The Free Culture Conference is a yearly touchstone event for the advancement of free cultures, where members are free to participate without artificial limits.</p>',
        "",
        ""
    ),
    Grant(
        "fscons",
        "FFKP",
        "Sweden",
        "Free Society Conference and Nordic Summit",
        "free-culture-community",
        "$1'300",
        2009,
        '<p>This grant provided sponsorship for the third <a href="https://fscons.org/2009/">Free Society Conference and Nordic Summit (FSCONS)</a> held November 13-15, 2009, in Goteborg, Sweden. FSCONS is jointly organized by Free Software Foundation Europe, Creative Commons and Wikipedia Sverige.</p>',
        "",
        ""
    ),
    Grant(
        "free-software-foundation",
        "Free Software Foundation",
        "United States",
        "LinuxBIOS Support",
        "free-culture-community",
        "$500'000",
        2007,
        '<p>In 2007, Mozilla provided $10,000 to support the LinuxBIOS-related activities of the <a href="http://www.fsf.org/">Free Software Foundation</a>. This grant went toward software development, infrastructure and communications. The Free Software Foundation ported coreboot to the alix.2c3 board, a board useful in building routers, firewalls, and wifi access points.</p>',
        "",
        ""
    ),
    Grant(
        "gnome",
        "GNOME",
        "United States",
        "GNOME Accessibility",
        "open-source-technology",
        "$38'000",
        2010,
        '<p>Mozilla offered this grant in support of <a href="http://projects.gnome.org/outreach/a11y/">GNOME\'s Outreach Program for Accessibility</a>. The <a href="http://www.gnome.org/">GNOME Foundation</a> sponsors the GNOME project to provide a free desktop environment for Linux systems. Mozilla and GNOME have been longtime collaborators on open source and accessibility issues.</p><p>See the <a href="reports/gnome-haeger-report/">grant final report</a> for more details.</p>',
        {
            '2008': ['Orca rich document browsing extension: $8,000'],
            '2009': ['GNOME Outreach Program: Accessibility: $10,000', 'CSUN Accessibility Conference: $10,000'],
            '2010': ['General Accessibility Support: $10,000']
        },
        [
            'https://blog.mozilla.org/blog/2010/02/04/mozilla-gnome-accessibility/',
        ]
    ),
    Grant(
        "ifosslr",
        "International Free and Open Source Software Law Review (IFOSSLR)",
        "Europe",
        "IFOSSLR Launch",
        "user-sovereignty",
        "$38'000",
        2009,
        '<p>This grant funded the launch of the <a href="http://www.ifosslr.org/">International Free and Open Source Software Law Review (IFOSSLR)</a>, a collaborative legal publication aiming to increase knowledge and understanding among lawyers about Free and Open Source Software issues. Topics included copyright, licence implementation, licence interpretation, software patents, open standards, case law and statutory changes.</p>',
        "",
        ""
    ),
    Grant(
        "mozdev",
        "MozDev",
        "United States",
        "MozDev Support",
        "open-source-technology",
        "$90'000",
        2008,
        '<p>Mozilla supported the <a href="http://www.mozdev.org/about.html">MozDev Community Organization</a> by providing general funds to support MozDev\'s operations. MozDev is a software development community dedicated to making quality applications and extensions freely available to all computer users. Its goal is to help establish Mozilla as a viable application development platform. Since 2006, Mozilla grants have funded the majority of MozDev\'s budget. This support gives back to the community that contributes so much to establishing Mozilla as a viable application development platform and the community that builds quality applications and extensions.</p>',
        {
            '2006': ['Amount: $30,000'],
            '2007': ['Amount: $30,000'],
            '2008': ['Amount: $30,000']
        },
        ""
    ),
    Grant(
        "nonprofit-software-development-summit",
        "Aspiration",
        "United States",
        "Nonprofit Software Development Summit",
        "free-culture-community",
        "$5'000",
        2009,
        'This grant supported the <a href="http://www.aspirationtech.org/events/devsummit09">Nonprofit Software Development Summit</a>, held November 18-20, 2009 in Oakland. This was the third annual convening of people and organizations developing software tools, web applications and other technology to support nonprofits and social justice causes. <a href="http://www.aspirationtech.org/">Aspiration</a>, the conference organizer, is a non-profit organization that connects nonprofits with software solutions that help them better carry out their work.',
        "",
        ""
    ),
    Grant(
        "open-source-software-institute",
        "Open Source Software Institute",
        "United States",
        "OCSP Stapling",
        "open-source-technology",
        "$30'000",
        2007,
        '<p>This grant to the <a href="http://www.oss-institute.org/">Open Source Software Institute</a>, in cooperation with the NSS development team and Mozilla developers, investigated the problem of providing OCSP stapling support for Apache and other open source SSL/TLS-enabled server software incorporating the OpenSSL library. The Open Source Software Institute (OSSI) was identified as having extensive experience with OpenSSL, and was the lead organization responsible for getting US government FIPS 140-2 validation of OpenSSL.</p>',
        "",
        ""
    ),
    Grant(
        "open-video-alliance",
        "Open Video Alliance",
        "United States",
        "Open Video Alliance",
        "free-culture-community",
        "$30'000",
        2009,
        '<p>Mozilla offered support to <a href="http://openvideoalliance.org/">Open Video Alliance</a> activities in support of the open video movement. Open Video Alliance is a coalition of organizations and individuals committed to the idea that the power of the moving image should belong to everyone. This grant funded various efforts in the open video movement, such as the operations of openvideoalliance.org, the branding of open video products, outreach to the public media, fundraising and video production.</p>',
        "",
        ""
    ),
    Grant(
        "perl-foundation",
        "Perl Foundation",
        "United States",
        "Perl6 Support",
        "open-source-technology",
        "$10'000",
        2007,
        '<p>Mozilla provided a grant to the <a href="http://www.perlfoundation.org/">Perl Foundation</a>, a non-profit dedicated to the advancement of the Perl programming language through open discussion, collaboration, design and code. This grant supported the development of Perl 6.</p>',
        "",
        ""
    ),
    Grant(
        "personal-democracy-forum",
        "Personal Democracy Forum",
        "United States",
        "Personal Democracy Forum",
        "user-sovereignty",
        "$15'000",
        2009,
        '<p>For two years Mozilla sponsored the <a href="http://personaldemocracy.com/pdf-conference/personal-democracy-forum-conference">Personal Democracy Forum</a>, a forum for discussion on how politics and technology intersect. Each year top opinion-makers, political practitioners, technologists and journalists come together to network, exchange ideas and explore how technology and the internet are changing politics, democracy and society.</p>',
        {
            '2008': ['Amount: $10,000'],
            '2009': ['Amount: $5,000'],
        },
        ""
    ),
    Grant(
        "software-freedom-conservancy",
        "Software Freedom Conservancy",
        "United States",
        "Software Freedom Conservancy",
        "free-culture-community",
        "$20'000",
        2009,
        '<p>This grant provided funding to help the <a href="http://conservancy.softwarefreedom.org/">Software Freedom Conservancy</a> serve additional open source projects and work more closely with peer projects. During the grant period, Mozilla\'s funding helped the Conservancy to provide administrative, financial management, coordination and logistical services to twenty FLOSS (Free, Libre and Open Source Software) projects including Foresight Linux, Sugar Labs, jQuery, Amarok, Darcs, OpenInkpot, and K-3D.</p>',
        {
            '2008': ['Amount: $10,000'],
            '2009': ['Amount: $10,000'],
        },
        ""
    ),
    Grant(
        "seneca",
        "Seneca College",
        "Canada",
        "Seneca College",
        "learning-webmaking",
        "$230'910",
        2009,
        '<p>Since 2005, <a href="http://www.senecac.on.ca/">Seneca College</a> in Toronto has worked closely with the Mozilla community to create a set of Mozilla-specific courses, engage hundreds of students directly in Mozilla development projects, and host and record dozens of Mozilla events and talks. Seneca\'s faculty and students are key contributors to the Mozilla project, and have gained significant experience bootstrapping new contributors into the Mozilla technology and culture. Seneca College of Applied Arts and Technology is a community college for applied arts and technology in Toronto, Ontario. </p>',
        {
            '2006': ['Amount: $50,000'],
            '2007': ['Amount: $100,000'],
            '2009': ['Amount: $80,910']
        },
        ""
    ),
    Grant(
        "leigh-school",
        "Leigh School",
        "New Zealand",
        "Leigh School",
        "learning-webmaking",
        "$2'500",
        2009,
        '<p>This grant is supporting ICT components for courses and the purchase of equipment and software to support the ICT components of courses at <a href="http://www.leigh.school.nz/">Leigh School</a>, a primary school in New Zealand dedicated to a broad curriculum that includes computers and technology.</p>',
        "",
        ""
    ),
    Grant(
        "peer2peer-university",
        "Phillip Schmidt (P2PU)",
        "South Africa",
        "Peer2Peer University",
        "learning-webmaking",
        "$2'500",
        2009,
        '<p>This grant to Phillip Schmidt (<a href="http://www.p2pu.org/">P2PU</a>), issued in 2009, enabled the creation of an online course called <a href="https://wiki.mozilla.org/Education/EduCourse">Open|Web|Content|Education</a>, a six-week online course where educators learned about open content licensing, open web technologies and open teaching methods. P2PU combines open educational resources, structured courses, and recognition of knowledge and learning to offer high-quality low-cost education opportunities. It is run and governed by volunteers.</p>',
        "",
        ""
    ),
    Grant(
        "ushaidi-chile",
        "Ushahidi",
        "United States and Chile",
        "Ushahidi Chile",
        "free-culture-community",
        "$10'00",
        2010,
        '<p>In a crisis environment, maintaining lines of communication is critically important. <a href="http://www.ushahidi.com/">Ushahidi</a> developed an open source platform that enables citizen reporting in crisis situations. A deadly earthquake struck Chile on February 27, 2010, cutting off many vulnerable people from traditional sources of information. Mozilla awarded a grant to enable Ushahidi volunteers to train Chilean civilians and government officials to utilize the Ushahidi platform during the relief effort.</p><p>See the <a href="reports/ushahidi-chile-report/">grant final report</a> for more details.</p>',
        "",
        [
            'http://blog.ushahidi.com/index.php/2010/03/15/mozilla-foundation-supports-ushahidi-chile/',
        ]
    ),
    Grant(
        "atlan",
        "Atlan Laboratories",
        "United States",
        "FIPS 140-2 Validation",
        "open-source-technology",
        "$25'00",
        2008,
        '<p>This grant to Atlan Labs, along with funding from Red Hat and Sun Microsystems, supported FIPS 140-2 validation for the latest version of Network Security Services (NSS). Federal Information Processing Standards Publications (FIPS PUBS) 140-1 and 140-2 are US government standards for implementations of cryptographic modules - that is, hardware or software that encrypts and decrypts data or performs other cryptographic operations. Atlan Labs was a a cybersecurity product testing firm based in McLean, Virginia that provided Federal Information Processing Standard (FIPS) 140-2 and 201 validations. Atlan was acquired by <a href="http://www.saic.com/infosec/testing-accreditation/">SAIC</a> in July 2009.</p>',
        "",
        ""
    ),
    Grant(
        "automated-calendar-testing",
        "Merike Sell",
        "Estonia",
        "Calendar Automated Testing",
        "open-source-technology",
        "$4'500",
        2009,
        '<p>This grant is funding the development of calendar automated testing for the Mozilla calendar code. This was originally an idea presented at the 2009 Google Summer of Code, and Mozilla Calendar developers became interested in funding technology that would enable automated testing. Merike Sell is an active member of the Mozilla developer and localization communites who live in Estonia.</p>',
        "",
        ""
    ),
    Grant(
        "w3c-validator",
        "World Wide Web Consortium",
        "International",
        "W3C Validator",
        "open-source-technology",
        "$15'000",
        2009,
        '<p>The Mozilla Foundation is a member of the <a href="http://www.w3.org/">World Wide Web Consortium</a>, and various Mozilla people represent Mozilla in W3C working groups and other W3C contexts. This grant was issued beyond Mozilla\'s existing W3C membership dues, and funded work on <a href="http://jigsaw.w3.org/css-validator/">W3C CSS Validator</a> by giving to ERCIM, the W3C\'s donation program.</p>',
        "",
        ""
    ),
    Grant(
        "jambu",
        "Jambu",
        "United States",
        "Jambu",
        "open-source-technology",
        "$25'000",
        2007,
        '<p><a href="www.oatsoft.org/Software/jambu">Jambu</a> is a pointer and switch project that improves accessibility for people with physical disabilities. This grant supported the improvement of switch access to Firefox on Windows, with the greater goal of providing transparent alternative input access to computers. Users served by this project may include adults who have experienced a debilitating accident or stroke, people with congential physical disabilities, children with multiple disabilities, and those with learning difficulties or limited education who often need to learn to use a switch through specialist educational programs.</p>',
        {
            '2006': ['Phase 1: $15,000'],
            '2007': ['Phase 2: $10,000'],
        },
        ""
    ),
    Grant(
        "nu",
        "Northeastern University",
        "United States",
        "Graduate-level work of PhD students at Northeastern University",
        "open-source-technology",
        "$283'085",
        2010,
        '<p>Since 2009 Mozilla has supported the graduate-level work of PhD students at <a href="http://www.ccs.neu.edu/">Northeastern University</a>, developing new tools for the standardization, streamlining, and testing of JavaScript. In 2009 Mozilla contributed $99,115 to the research efforts of <a href="http://www.ccs.neu.edu/home/samth/">Sam Tobin-Hochstadt</a>. In 2010 Mozilla made two gifts: one of $107,596 to further support Mr. Tobin-Hochstadt\'s research and another gift of $76,374 to <a href="http://www.ccs.neu.edu/home/dimvar/">Demetrios Vardoulakis</a>.</p>',
        {
            '2009': ['PhD Research of Sam Tobin-Hochstadt: $99,115'],
            '2010': ['PhD research of Sam Tobin-Hochstadt and Demetrios Vardoulakis: $107,596 and $76,374']
        },
        ""
    ),
    Grant(
        "owasp",
        "OWASP",
        "United States",
        "The Open Web Application Security Project",
        "open-source-technology",
        "$15'000",
        2010,
        '<p>This grant supports the <a href="http://www.owasp.org/index.php/Main_Page">Open Web Application Security Project</a>, which focuses on improving the security of application software. OWASP\'s mission is to make application security visible, so that people and organizations can make informed decisions about true application security risks.</p>',
        "",
        ""
    ),
    Grant(
        "webaim",
        "WebAIM",
        "United States",
        "WebAIM",
        "open-source-technology",
        "$15'000",
        2006,
        '<p>In 2006, Mozilla provided a grant to <a href="http://webaim.org/">WebAIM</a>, an accessibility organization based at Utah State University, to develop XUL accessibility guidelines and an accompanying evaluation tool. WebAIM has provided comprehensive web accessibility solutions since 1999. These years of experience have made WebAIM one of the leading providers of web accessibility expertise internationally. WebAIM is a non-profit organization within the Center for Persons with Disabilities at Utah State University.</p>',
        "",
        ""
    ),
]
