from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

browser_history = "firefox/browsers/browser-history.lang"
browser_history = "mozorg/browser-history.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/browsers/browser-history.html, part {index}."""

    ctx.add_transforms(
        "firefox/browsers/history/browser-history.ftl",
        "firefox/browsers/history/browser-history.ftl",
        transforms_from("""
browser-history-browser-history = {COPY(browser_history, "Browser History: Epic power struggles that brought us modern browsers",)}
browser-history-the-browser-wars-underdogs-giants = {COPY(browser_history, "The browser wars, underdogs vs giants, and moments that changed the world. Read about the history of the web browser.",)}
browser-history-the-history-of-web = {COPY(browser_history, "The History of Web Browsers",)}
browser-history-world-history-is = {COPY(browser_history, "World history is rife with epic power struggles, world-conquering tyrants, and heroic underdogs. The history of web browsers isn’t very different. University pioneers wrote simple software that sparked an information revolution, and battle for browser superiority and internet users.",)}
browser-history-before-web-era = {COPY(browser_history, "Before Web Era",)}
browser-history-in-1950-computers = {COPY(browser_history, "In 1950, computers took up whole rooms and were dumber than today’s pocket calculators. But progress was swift, and by 1960 they were able to run complex programs. Governments and universities across the globe thought it would be great if the machines could talk, nurturing collaboration and scientific breakthroughs.",)}
""", browser_history=browser_history) + [
            FTL.Message(
                id=FTL.Identifier("browser-history-arpanet-was-the"),
                value=REPLACE(
                    browser_history,
                    "<a href=\"%(arpanet)s\">ARPANET</a> was the first successful networking project and in 1969 the first message was sent from the computer science lab at University of California, Los Angeles (UCLA) to Stanford Research Institute (SRI), also in California.",
                    {
                        "%%": "%",
                        "%(arpanet)s": VARIABLE_REFERENCE("arpanet"),
                    }
                )
            ),
        ] + transforms_from("""
browser-history-that-sparked-a-revolution = {COPY(browser_history, "That sparked a revolution in computer networking. New networks formed, connecting universities and research centers across the globe. But for the next 20 years, the internet wasn’t accessible to the public. It was restricted to university and government researchers, students, and private corporations. There were dozens of programs that could trade information over telephone lines, but none of them were easy to use. The real open internet, and the first web browser, wasn’t created until 1990.",)}
browser-history-web-era = {COPY(browser_history, "Web Era",)}
""", browser_history=browser_history) + [
            FTL.Message(
                id=FTL.Identifier("browser-history-british-computer"),
                value=REPLACE(
                    browser_history,
                    "British computer scientist Tim Berners-Lee created the first web server and graphical web browser in 1990 while <a href=\"%(cern)s\">working at CERN</a>, the European Organization for Nuclear Research, in Switzerland. He called his new window into the internet “WorldWideWeb.” It was an easy-to-use graphical interface created for the NeXT computer. For the first time, text documents were linked together over a public network—the web as we know it.",
                    {
                        "%%": "%",
                        "%(cern)s": VARIABLE_REFERENCE("cern"),
                    }
                )
            ),
        ] + transforms_from("""
browser-history-a-year-later-berners = {COPY(browser_history, "A year later, Berners-Lee asked CERN math student Nicola Pellow to write the Line Mode Browser, a program for basic computer terminals.",)}
""", browser_history=browser_history) + [
            FTL.Message(
                id=FTL.Identifier("browser-history-by-1993-the-web"),
                value=REPLACE(
                    browser_history,
                    "By 1993, the web exploded. Universities, governments, and private corporations all saw opportunity in the open internet. Everyone needed new computer programs to access it. That year, Mosaic was created at the National Center for Supercomputing Applications (NCSA) at the University of Illinois Urbana-Champaign by computer scientist Marc Andreessen. It was the very first popular web browser and the early ancestor of <a href=\"%(firefox)s\">Mozilla Firefox</a>.",
                    {
                        "%%": "%",
                        "%(firefox)s": VARIABLE_REFERENCE("firefox"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("browser-history-ncsa-mosaic-ran"),
                value=REPLACE(
                    browser_history,
                    "NCSA Mosaic ran on Windows computers, was easy to use, and gave anyone with a PC access to early web pages, chat rooms, and image libraries. The next year (1994), Andreessen founded <a href=\"%(netscape)s\">Netscape</a> and released Netscape Navigator to the public. It was wildly successful, and the first browser for the people. It was also the first move in a new kind of war for internet users.",
                    {
                        "%%": "%",
                        "%(netscape)s": VARIABLE_REFERENCE("netscape"),
                        "Netscape": TERM_REFERENCE("brand-name-netscape"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    }
                )
            ),
        ] + transforms_from("""
browser-history-the-browser-wars = {COPY(browser_history, "The Browser Wars",)}
""", browser_history=browser_history) + [
            FTL.Message(
                id=FTL.Identifier("browser-history-by-1995-netscape"),
                value=REPLACE(
                    browser_history,
                    "By 1995, Netscape Navigator wasn’t the only way to get online. Computer software giant Microsoft licensed the old Mosaic code and built its own window to the web, <a href=\"%(ie)s\">Internet Explorer</a>. The release sparked a war. Netscape and Microsoft worked feverishly to make new versions of their programs, each attempting to outdo the other with faster, better products.",
                    {
                        "%%": "%",
                        "%(ie)s": VARIABLE_REFERENCE("ie"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Netscape": TERM_REFERENCE("brand-name-netscape"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("browser-history-netscape-created"),
                value=REPLACE(
                    browser_history,
                    "Netscape created and released JavaScript, which gave websites powerful computing capabilities they never had before. (They also made the infamous <a href=\"%(blink)s\">&lt;blink&gt; tag</a>.) Microsoft countered with Cascading Style Sheets (CSS), which became the standard for web page design.",
                    {
                        "%%": "%",
                        "%(blink)s": VARIABLE_REFERENCE("blink"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Netscape": TERM_REFERENCE("brand-name-netscape"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("browser-history-things-got-a-little"),
                value=REPLACE(
                    browser_history,
                    "Things got a little out of hand in 1997 when Microsoft released Internet Explorer 4.0. The team built a giant letter “e” and snuck it on the lawn of Netscape headquarters. The Netscape team promptly knocked the giant “e” over and <a href=\"%(dino)s\">put their own Mozilla dinosaur mascot on top of it</a>.",
                    {
                        "%%": "%",
                        "%(dino)s": VARIABLE_REFERENCE("dino"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Netscape": TERM_REFERENCE("brand-name-netscape"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("browser-history-then-microsoft-began"),
                value=REPLACE(
                    browser_history,
                    "Then Microsoft began shipping Internet Explorer with their Windows operating system. Within 4 years, it had 75%% of the market and by 1999 it had 99%% of the market. The company faced antitrust litigation over the move, and Netscape decided to open source its codebase and created the not-for-profit <a href=\"%(mozilla)s\">Mozilla</a>, which went on to create and release Firefox in 2002. Realizing that having a browser monopoly wasn’t in the best interests of users and the open web, Firefox was created to provide choice for web users. By 2010, Mozilla Firefox and others had <a href=\"%(marketshare)s\">reduced Internet Explorer’s market share to 50%%</a>.",
                    {
                        "%%": FTL.TextElement("%"),
                        "%(mozilla)s": VARIABLE_REFERENCE("mozilla"),
                        "%(marketshare)s": VARIABLE_REFERENCE("marketshare"),
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "Netscape": TERM_REFERENCE("brand-name-netscape"),
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("browser-history-other-competitors"),
                value=REPLACE(
                    browser_history,
                    "Other competitors emerged during the late ‘90s and early 2000s, including Opera, Safari, and Google Chrome. Microsoft Edge replaced Internet Explorer with the release of Windows 10 in 2015.",
                    {
                        "Internet Explorer": TERM_REFERENCE("brand-name-ie"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                    }
                )
            ),
        ] + transforms_from("""
browser-history-browsing-the-web = {COPY(browser_history, "Browsing the Web Today",)}
""", browser_history=browser_history) + [
            FTL.Message(
                id=FTL.Identifier("browser-history-today-there-are"),
                value=REPLACE(
                    browser_history,
                    "Today there are just a handful of ways to access the internet. Firefox, Google Chrome, Microsoft Edge, Safari and Opera are the main competitors. Mobile devices have emerged during the past decade as the preferred way to access the internet. Today, most internet users only use mobile browsers and <a href=\"%(applications)s\">applications</a> to get online. Mobile versions of the major browsers are available for iOS and Android devices. While these apps are very useful for specific purposes, they only provide limited access to the web.",
                    {
                        "%%": "%",
                        "%(applications)s": VARIABLE_REFERENCE("applications"),
                        "Microsoft": TERM_REFERENCE("brand-name-microsoft"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Android": TERM_REFERENCE("brand-name-android"),
                        "Google": TERM_REFERENCE("brand-name-google"),
                        "Chrome": TERM_REFERENCE("brand-name-chrome"),
                        "Safari": TERM_REFERENCE("brand-name-safari"),
                        "Opera": TERM_REFERENCE("brand-name-opera"),
                        "Edge": TERM_REFERENCE("brand-name-edge"),
                        "iOS": TERM_REFERENCE("brand-name-ios"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("browser-history-in-the-future-the"),
                value=REPLACE(
                    browser_history,
                    "In the future, the web will likely stray further from its hypertext roots to become a vast sea of interactive experiences. Virtual reality has been on the horizon for decades (at least since the release of Lawnmower Man in 1992 and the Nintendo Virtual Boy in 1995), but the web may finally bring it to the masses. Firefox now has support for <a href=\"%(vr)s\">WebVR and A-Frame</a>, which let developers quickly and easily build virtual reality websites. Most modern mobile devices support <a href=\"%(vr)s\">WebVR</a>, and can easily be used as headsets with simple cardboard cases. A 3D virtual reality web like the one imagined by science fiction author Neal Stephenson may be just around the corner. If that’s the case, the web browser itself may completely disappear and become a true window into another world.",
                    {
                        "%%": "%",
                        "%(vr)s": VARIABLE_REFERENCE("vr"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("browser-history-whatever-the-future"),
                value=REPLACE(
                    browser_history,
                    "Whatever the future of the web holds, Mozilla and Firefox will be there for users, ensuring that they have powerful tools to experience the web and all it has to offer. The web is for everyone, and everyone should have control of their online experience. That’s why we give Firefox tools to protect user privacy and we never sell user data to advertisers.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ] + transforms_from("""
browser-history-resources = {COPY(browser_history, "Resources",)}
browser-history-take-control-of = {COPY(browser_history, "Take control of your browser.",)}
""", browser_history=browser_history)
        )
