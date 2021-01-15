from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

manifesto = "mozorg/about/manifesto.lang"

def migrate(ctx):
    """Migrate bedrock/mozorg/templates/mozorg/about/manifesto.html, part {index}."""

    ctx.add_transforms(
        "mozorg/about/manifesto.ftl",
        "mozorg/about/manifesto.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("manifesto-the-mozilla-manifesto"),
                value=REPLACE(
                    manifesto,
                    "The Mozilla Manifesto",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-these-are-the-principles = {COPY(manifesto, "These are the principles that guide our mission to promote openness, innovation & opportunity on the web.",)}
manifesto-the-internet-is-an-integral = {COPY(manifesto, "The internet is an integral part of modern life—a key component in education, communication, collaboration, business, entertainment and society as a whole.",)}
manifesto-the-internet-is-a-global = {COPY(manifesto, "The internet is a global public resource that must remain open and accessible.",)}
manifesto-the-internet-must-enrich = {COPY(manifesto, "The internet must enrich the lives of individual human beings.",)}
manifesto-individuals-security-and = {COPY(manifesto, "Individuals’ security and privacy on the internet are fundamental and must not be treated as optional.",)}
manifesto-individuals-must-have = {COPY(manifesto, "Individuals must have the ability to shape the internet and their own experiences on it.",)}
manifesto-the-effectiveness-of-the = {COPY(manifesto, "The effectiveness of the internet as a public resource depends upon interoperability (protocols, data formats, content), innovation and decentralized participation worldwide.",)}
manifesto-free-and-open-source-software = {COPY(manifesto, "Free and open source software promotes the development of the internet as a public resource.",)}
manifesto-transparent-community = {COPY(manifesto, "Transparent community-based processes promote participation, accountability and trust.",)}
manifesto-commercial-involvement = {COPY(manifesto, "Commercial involvement in the development of the internet brings many benefits; a balance between commercial profit and public benefit is critical.",)}
manifesto-magnifying-the-public = {COPY(manifesto, "Magnifying the public benefit aspects of the internet is an important goal, worthy of time, attention and commitment.",)}
manifesto-principle-1 = {COPY(manifesto, "Principle 1",)}
manifesto-principle-2 = {COPY(manifesto, "Principle 2",)}
manifesto-principle-3 = {COPY(manifesto, "Principle 3",)}
manifesto-principle-4 = {COPY(manifesto, "Principle 4",)}
manifesto-principle-5 = {COPY(manifesto, "Principle 5",)}
manifesto-principle-6 = {COPY(manifesto, "Principle 6",)}
manifesto-principle-7 = {COPY(manifesto, "Principle 7",)}
manifesto-principle-8 = {COPY(manifesto, "Principle 8",)}
manifesto-principle-9 = {COPY(manifesto, "Principle 9",)}
manifesto-principle-10 = {COPY(manifesto, "Principle 10",)}
manifesto-01 = {COPY(manifesto, "01",)}
manifesto-02 = {COPY(manifesto, "02",)}
manifesto-03 = {COPY(manifesto, "03",)}
manifesto-04 = {COPY(manifesto, "04",)}
manifesto-05 = {COPY(manifesto, "05",)}
manifesto-06 = {COPY(manifesto, "06",)}
manifesto-07 = {COPY(manifesto, "07",)}
manifesto-08 = {COPY(manifesto, "08",)}
manifesto-09 = {COPY(manifesto, "09",)}
manifesto-10 = {COPY(manifesto, "10",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-the-mozilla-manifesto-addendum"),
                value=REPLACE(
                    manifesto,
                    "The Mozilla Manifesto Addendum",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-pledge-for-a-healthy-internet = {COPY(manifesto, "Pledge for a Healthy Internet",)}
manifesto-the-open-global-internet = {COPY(manifesto, "The open, global internet is the most powerful communication and collaboration resource we have ever seen. It embodies some of our deepest hopes for human progress. It enables new opportunities for learning, building a sense of shared humanity, and solving the pressing problems facing people everywhere.",)}
manifesto-over-the-last-decade-we = {COPY(manifesto, "Over the last decade we have seen this promise fulfilled in many ways. We have also seen the power of the internet used to magnify divisiveness, incite violence, promote hatred, and intentionally manipulate fact and reality. We have learned that we should more explicitly set out our aspirations for the human experience of the internet. We do so now.",)}
manifesto-we-are-committed-to-people = {COPY(manifesto, "We are committed to an internet that includes all the peoples of the earth — where a person’s demographic characteristics do not determine their online access, opportunities, or quality of experience.",)}
manifesto-we-are-committed-to-discourse = {COPY(manifesto, "We are committed to an internet that promotes civil discourse, human dignity, and individual expression.",)}
manifesto-we-are-committed-to-thinking = {COPY(manifesto, "We are committed to an internet that elevates critical thinking, reasoned argument, shared knowledge, and verifiable facts.",)}
manifesto-we-are-committed-to-diverse = {COPY(manifesto, "We are committed to an internet that catalyzes collaboration among diverse communities working together for the common good.",)}
manifesto-show-your-support = {COPY(manifesto, "Show Your Support",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-an-internet-with-these"),
                value=REPLACE(
                    manifesto,
                    "An internet with these qualities will not come to life on its own. Individuals and organizations must embed these aspirations into internet technology and into the human experience with the internet. The Mozilla Manifesto and Addendum represent Mozilla’s commitment to advancing these aspirations. We aim to work together with people and organizations everywhere who share these goals to make the internet an even better place for everyone.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-i-support-the-vision-of = {COPY(manifesto, "I support the vision of a better, healthier internet from @mozilla, will you join me?",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-share-on-twitter"),
                value=REPLACE(
                    manifesto,
                    "Share on Twitter",
                    {
                        "Twitter": TERM_REFERENCE("brand-name-twitter"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-our-10-principles = {COPY(manifesto, "<strong>Our 10</strong> Principles",)}
manifesto-use-open-badges-to-share = {COPY(manifesto, "Use Open Badges to share your skills and interests",)}
manifesto-explore-how-the-web-impacts = {COPY(manifesto, "Explore how the web impacts science",)}
manifesto-learn-about-open-source = {COPY(manifesto, "Learn about open source code in journalism",)}
manifesto-read-about-open-internet = {COPY(manifesto, "Read about open internet policy initiatives and developments",)}
manifesto-explore-how-to-help-keep = {COPY(manifesto, "Explore how to help keep the web open",)}
manifesto-see-how-the-web-can-connect = {COPY(manifesto, "See how the web can connect the world to healthcare",)}
manifesto-explore-how-the-web-works = {COPY(manifesto, "Explore how the web works",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-see-how-mozilla-works"),
                value=REPLACE(
                    manifesto,
                    "See how Mozilla works to put your privacy first",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-read-about-developments = {COPY(manifesto, "Read about developments in privacy and data safety",)}
manifesto-learn-more-about-how-to = {COPY(manifesto, "Learn more about how to protect yourself online",)}
manifesto-use-these-free-tools-to = {COPY(manifesto, "Use these free tools to teach the web",)}
manifesto-learn-about-creating-and = {COPY(manifesto, "Learn about creating and curating content for the web",)}
manifesto-add-new-voices-to-open = {COPY(manifesto, "Add new voices to open source technology",)}
manifesto-set-your-do-not-track = {COPY(manifesto, "Set your Do Not Track preference",)}
manifesto-understand-the-web-ecosystem = {COPY(manifesto, "Understand the web ecosystem",)}
manifesto-explore-how-open-practices = {COPY(manifesto, "Explore how open practices keep the web accessible",)}
manifesto-learn-how-to-remix-content = {COPY(manifesto, "Learn how to remix content to create something new",)}
manifesto-learn-how-to-maximize = {COPY(manifesto, "Learn how to maximize the interactive potential of the web",)}
manifesto-participate-in-our-governance = {COPY(manifesto, "Participate in our governance forum",)}
manifesto-join-us-as-a-volunteer = {COPY(manifesto, "Join us as a volunteer",)}
manifesto-learn-how-to-collaborate = {COPY(manifesto, "Learn how to collaborate online",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-visualize-who-you-interact"),
                value=REPLACE(
                    manifesto,
                    "Visualize who you interact with on the web with Lightbeam",
                    {
                        "Lightbeam": TERM_REFERENCE("brand-name-lightbeam"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-learn-about-creating-web = {COPY(manifesto, "Learn about creating web resources with others",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-host-or-join-a-maker-party"),
                value=REPLACE(
                    manifesto,
                    "Host or join a Maker Party",
                    {
                        "Maker Party": TERM_REFERENCE("brand-name-maker-party"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-learn-how-to-build-online = {COPY(manifesto, "Learn how to build online collaboration skills",)}
manifesto-read-the-entire-manifesto = {COPY(manifesto, "Read the entire manifesto",)}
manifesto-love-the-web = {COPY(manifesto, "Love the web?",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-get-the-mozilla-newsletter"),
                value=REPLACE(
                    manifesto,
                    "Get the Mozilla newsletter and help us keep it open and free.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ]
        )

    ctx.add_transforms(
        "mozorg/about/manifesto.ftl",
        "mozorg/about/manifesto.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("manifesto-details-the-mozilla-manifesto"),
                value=REPLACE(
                    manifesto,
                    "The Mozilla Manifesto",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-details-introduction = {COPY(manifesto, "Introduction",)}
manifesto-details-the-internet-is-becoming = {COPY(manifesto, "The Internet is becoming an increasingly important part of our lives.",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-details-the-mozilla-project-global"),
                value=REPLACE(
                    manifesto,
                    "The Mozilla project is a global community of people who believe that openness, innovation, and opportunity are key to the continued health of the Internet. We have worked together since 1998 to ensure that the Internet is developed in a way that benefits everyone. We are best known for creating the Mozilla Firefox web browser.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("manifesto-details-the-mozilla-project-community"),
                value=REPLACE(
                    manifesto,
                    "The Mozilla project uses a community-based approach to create world-class open source software and to develop new types of collaborative activities. We create communities of people involved in making the Internet experience better for all of us.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-details-as-a-result-of = {COPY(manifesto, "As a result of these efforts, we have distilled a set of principles that we believe are critical for the Internet to continue to benefit the public good as well as commercial aspects of life. We set out these principles below.",)}
manifesto-details-the-goals-for = {COPY(manifesto, "The goals for the Manifesto are to:",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-details-articulate-a-vision"),
                value=REPLACE(
                    manifesto,
                    "articulate a vision for the Internet that Mozilla participants want the Mozilla Foundation to pursue;",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Mozilla Foundation": TERM_REFERENCE("brand-name-mozilla-foundation"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-details-speak-to-people = {COPY(manifesto, "speak to people whether or not they have a technical background;",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-details-make-mozilla-contributors"),
                value=REPLACE(
                    manifesto,
                    "make Mozilla contributors proud of what we're doing and motivate us to continue; and",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-details-provide-a-framework = {COPY(manifesto, "provide a framework for other people to advance this vision of the Internet.",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-details-these-principles"),
                value=REPLACE(
                    manifesto,
                    "These principles will not come to life on their own. People are needed to make the Internet open and participatory - people acting as individuals, working together in groups, and leading others. The Mozilla Foundation is committed to advancing the principles set out in the Mozilla Manifesto. We invite others to join us and make the Internet an ever better place for everyone.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Mozilla Foundation": TERM_REFERENCE("brand-name-mozilla-foundation"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-details-principles = {COPY(manifesto, "Principles",)}
manifesto-details-the-internet-is-integral = {COPY(manifesto, "The Internet is an integral part of modern life—a key component in education, communication, collaboration, business, entertainment and society as a whole.",)}
manifesto-details-the-internet-is-global = {COPY(manifesto, "The Internet is a global public resource that must remain open and accessible.",)}
manifesto-details-the-internet-must = {COPY(manifesto, "The Internet must enrich the lives of individual human beings.",)}
manifesto-details-individuals-security = {COPY(manifesto, "Individuals’ security and privacy on the Internet are fundamental and must not be treated as optional.",)}
manifesto-details-individuals-must = {COPY(manifesto, "Individuals must have the ability to shape the Internet and their own experiences on the Internet.",)}
manifesto-details-the-effectiveness = {COPY(manifesto, "The effectiveness of the Internet as a public resource depends upon interoperability (protocols, data formats, content), innovation and decentralized participation worldwide.",)}
manifesto-details-free-and-open = {COPY(manifesto, "Free and open source software promotes the development of the Internet as a public resource.",)}
manifesto-details-transparent-community = {COPY(manifesto, "Transparent community-based processes promote participation, accountability and trust.",)}
manifesto-details-commercial-involvement = {COPY(manifesto, "Commercial involvement in the development of the Internet brings many benefits; a balance between commercial profit and public benefit is critical.",)}
manifesto-details-magnifying-the = {COPY(manifesto, "Magnifying the public benefit aspects of the Internet is an important goal, worthy of time, attention and commitment.",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-details-advancing-the"),
                value=REPLACE(
                    manifesto,
                    "Advancing the Mozilla Manifesto",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("manifesto-details-there-are-many"),
                value=REPLACE(
                    manifesto,
                    "There are many different ways of advancing the principles of the Mozilla Manifesto. We welcome a broad range of activities, and anticipate the same creativity that Mozilla participants have shown in other areas of the project. For individuals not deeply involved in the Mozilla project, one basic and very effective way to support the Manifesto is to use Mozilla Firefox and other products that embody the principles of the Manifesto.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("manifesto-details-mozilla-foundation"),
                value=REPLACE(
                    manifesto,
                    "Mozilla Foundation Pledge",
                    {
                        "Mozilla Foundation": TERM_REFERENCE("brand-name-mozilla-foundation"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("manifesto-details-the-mozilla-foundation-pleges"),
                value=REPLACE(
                    manifesto,
                    "The Mozilla Foundation pledges to support the Mozilla Manifesto in its activities. Specifically, we will:",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Mozilla Foundation": TERM_REFERENCE("brand-name-mozilla-foundation"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-details-build-and-enable = {COPY(manifesto, "build and enable open-source technologies and communities that support the Manifesto’s principles;",)}
manifesto-details-build-and-deliver = {COPY(manifesto, "build and deliver great consumer products that support the Manifesto’s principles;",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-details-use-the-mozilla"),
                value=REPLACE(
                    manifesto,
                    "use the Mozilla assets (intellectual property such as copyrights and trademarks, infrastructure, funds, and reputation) to keep the Internet an open platform;",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-details-promote-models = {COPY(manifesto, "promote models for creating economic value for the public benefit; and",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-details-promote-the-mozilla"),
                value=REPLACE(
                    manifesto,
                    "promote the Mozilla Manifesto principles in public discourse and within the Internet industry.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                    }
                )
            ),
            FTL.Message(
                id=FTL.Identifier("manifesto-details-some-foundation"),
                value=REPLACE(
                    manifesto,
                    "Some Foundation activities—currently the creation, delivery and promotion of consumer products—are conducted primarily through the Mozilla Foundation’s wholly owned subsidiary, the Mozilla Corporation.",
                    {
                        "Mozilla Corporation": TERM_REFERENCE("brand-name-mozilla-corporation"),
                        "Mozilla Foundation": TERM_REFERENCE("brand-name-mozilla-foundation"),
                    }
                )
            ),
        ] + transforms_from("""
manifesto-details-invitation = {COPY(manifesto, "Invitation",)}
""", manifesto=manifesto) + [
            FTL.Message(
                id=FTL.Identifier("manifesto-details-the-mozilla-foundation-invites"),
                value=REPLACE(
                    manifesto,
                    "The Mozilla Foundation invites all others who support the principles of the Mozilla Manifesto to join with us, and to find new ways to make this vision of the Internet a reality.",
                    {
                        "Mozilla": TERM_REFERENCE("brand-name-mozilla"),
                        "Mozilla Foundation": TERM_REFERENCE("brand-name-mozilla-foundation"),
                    }
                )
            ),
        ]
        )
