# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.mozorg.util import page

urlpatterns = (
    # Older annual report financial faqs - these are linked from blog posts
    # was e.g.: http://www.mozilla.org/foundation/documents/mozilla-2008-financial-faq.html
    page("documents/mozilla-2006-financial-faq/", "foundation/documents/mozilla-2006-financial-faq.html"),
    page("documents/mozilla-2007-financial-faq/", "foundation/documents/mozilla-2007-financial-faq.html"),
    page("documents/mozilla-2008-financial-faq/", "foundation/documents/mozilla-2008-financial-faq.html"),
    # ported from PHP in Bug 960689
    page("documents/bylaws-amendment-1/", "foundation/documents/bylaws-amendment-1.html"),
    page("documents/bylaws-amendment-2/", "foundation/documents/bylaws-amendment-2.html"),
    page("documents/articles-of-incorporation/", "foundation/documents/articles-of-incorporation.html"),
    page("documents/articles-of-incorporation/amendment/", "foundation/documents/articles-of-incorporation-amendment.html"),
    page("documents/bylaws/", "foundation/documents/bylaws.html"),
    # was https://www.mozilla.org/foundation/annualreport/2009/
    page("annualreport/2009/", "foundation/annualreport/2009/index.html"),
    # was .html
    page("annualreport/2009/a-competitive-world/", "foundation/annualreport/2009/a-competitive-world.html"),
    # was .html
    page("annualreport/2009/broadening-our-scope/", "foundation/annualreport/2009/broadening-our-scope.html"),
    # was .html
    page("annualreport/2009/sustainability/", "foundation/annualreport/2009/sustainability.html"),
    # was         https://www.mozilla.org/foundation/annualreport/2009/faq.html
    # changing to https://www.mozilla.org/foundation/annualreport/2009/faq/
    page("annualreport/2009/faq/", "foundation/annualreport/2009/faq.html"),
    page("annualreport/2010/", "foundation/annualreport/2010/index.html"),
    page("annualreport/2010/ahead/", "foundation/annualreport/2010/ahead.html"),
    page("annualreport/2010/opportunities/", "foundation/annualreport/2010/opportunities.html"),
    page("annualreport/2010/people/", "foundation/annualreport/2010/people.html"),
    page("annualreport/2010/faq/", "foundation/annualreport/2010/faq.html"),
    page("annualreport/2011/", "foundation/annualreport/2011.html"),
    page("annualreport/2011/faq/", "foundation/annualreport/2011faq.html"),
    page("annualreport/2012/", "foundation/annualreport/2012/index.html"),
    page("annualreport/2012/faq/", "foundation/annualreport/2012/faq.html"),
    page("annualreport/2013/", "foundation/annualreport/2013/index.html"),
    page("annualreport/2013/faq/", "foundation/annualreport/2013/faq.html"),
    page("annualreport/2014/", "foundation/annualreport/2014/index.html"),
    page("annualreport/2014/faq/", "foundation/annualreport/2014/faq.html"),
    page("annualreport/2015/", "foundation/annualreport/2015/index.html"),
    page("annualreport/2015/faq/", "foundation/annualreport/2015/faq.html"),
    page("annualreport/2016/", "foundation/annualreport/2016/index.html"),
    page("annualreport/2017/", "foundation/annualreport/2017/index.html"),
    page("annualreport/2018/", "foundation/annualreport/2018/index.html"),
    page("annualreport/2019/", "foundation/annualreport/2019/index.html"),
    page("annualreport/2020/", "foundation/annualreport/2020/index.html"),
    page("annualreport/2021/", "foundation/annualreport/2021/index.html"),
    page("annualreport/2021/article/angela-and-eric/", "foundation/annualreport/2021/article/angela-and-eric.html"),
    page("annualreport/2021/article/team/", "foundation/annualreport/2021/article/team.html"),
    page("annualreport/2021/article/innovation/", "foundation/annualreport/2021/article/innovation.html"),
    page("annualreport/2021/article/mark-surman/", "foundation/annualreport/2021/article/mark-surman.html"),
    page("annualreport/2021/article/mitchell-baker/", "foundation/annualreport/2021/article/mitchell-baker.html"),
    page("annualreport/2021/article/mozilla-ventures/", "foundation/annualreport/2021/article/mozilla-ventures.html"),
    page("annualreport/2021/article/people/", "foundation/annualreport/2021/article/people.html"),
    page("annualreport/2021/article/products/", "foundation/annualreport/2021/article/products.html"),
    # SoM 2024 landing page
    page("annualreport/2024/", "foundation/annualreport/2024/index.html"),
    # Opening section: Mark Surman
    page(
        "annualreport/2024/article/evolving-together-redefining-mozilla-in-the-ai-era/", "foundation/annualreport/2024/article/0-1-mark-surman.html"
    ),
    # Section 1: Reinventing Mozilla
    page(
        "annualreport/2024/article/for-the-sake-of-our-digital-future-open-source-must-win/",
        "foundation/annualreport/2024/article/1-1-mitchell-baker.html",
    ),
    page("annualreport/2024/article/financing-an-open-internet-mozillas-path-forward/", "foundation/annualreport/2024/article/1-2-eric-angela.html"),
    page(
        "annualreport/2024/article/how-mozilla-is-meeting-the-challenge-of-transformation-on-the-internet/",
        "foundation/annualreport/2024/article/1-3-suba-vasudevan.html",
    ),
    page(
        "annualreport/2024/article/a-rebrand-and-a-call-to-action-reclaim-the-internet/",
        "foundation/annualreport/2024/article/1-4-lindsey-obrien.html",
    ),
    # Section 2: Building a balanced portfolio
    page(
        "annualreport/2024/article/imagining-co-creating-and-translating-our-way-to-a-better-tech-future/",
        "foundation/annualreport/2024/article/2-1-nabiha-syed.html",
    ),
    page("annualreport/2024/article/strategic-innovation-a-25-year-mission/", "foundation/annualreport/2024/article/2-2-laura-chambers.html"),
    page(
        "annualreport/2024/article/empowering-developers-with-open-ai-tools-for-a-trustworthy-future/",
        "foundation/annualreport/2024/article/2-3-jane-silber.html",
    ),
    page(
        "annualreport/2024/article/backing-bold-ideas-mozilla-venturesa-and-responsible-innovation/",
        "foundation/annualreport/2024/article/2-4-mohamed-nanabhay.html",
    ),
    page(
        "annualreport/2024/article/success-through-two-way-conversations-with-our-community/",
        "foundation/annualreport/2024/article/2-5-ryan-sipes.html",
    ),
    # Section 3: A path for growth
    page(
        "annualreport/2024/article/products-built-for-people-a-vision-for-internet-safety-and-privacy/",
        "foundation/annualreport/2024/article/3-1-adam-fishman.html",
    ),
    page("annualreport/2024/article/leading-browsing-innovation-for-a-complex-web/", "foundation/annualreport/2024/article/3-2-vicky-chin.html"),
    # Section 4: A vision for AI and Data
    page("annualreport/2024/article/shaping-ai-we-can-trust-mozillas-portfolio-at-work/", "foundation/annualreport/2024/article/4-1-ayah-bdeir.html"),
    page("annualreport/2024/article/scaling-local-ai-innovation-for-real-world-impact/", "foundation/annualreport/2024/article/4-2-imo-udom.html"),
    # Section 5: A New Way of Advertising
    page(
        "annualreport/2024/article/reimagining-the-ad-ecosystem-balancing-privacy-and-relevance/",
        "foundation/annualreport/2024/article/5-1-orville-mcdonald.html",
    ),
    page(
        "annualreport/2024/article/a-privacy-first-solution-that-meets-advertisers-needs/",
        "foundation/annualreport/2024/article/5-2-brad-graham.html",
    ),
    # Section 6: Mozilla Community
    page(
        "annualreport/2024/article/building-in-public-with-community-and-openness/", "foundation/annualreport/2024/article/6-1-monica-chambers.html"
    ),
    page(
        "annualreport/2024/article/global-collaboration-for-a-fairer-healthier-internet/",
        "foundation/annualreport/2024/article/6-2-zeina-abi-assy.html",
    ),
    # Section 7: Case Studies
    page("annualreport/2024/article/mozilla-venture-companies/", "foundation/annualreport/2024/article/7-1-mozilla-venture-companies.html"),
    page("annualreport/2024/article/why-i-joined-mozilla/", "foundation/annualreport/2024/article/7-2-why-i-joined-mozilla.html"),
    page("annualreport/2024/article/mozilla-fellows/", "foundation/annualreport/2024/article/7-3-mozilla-fellows.html"),
    page("annualreport/2024/article/rise25-winners/", "foundation/annualreport/2024/article/7-4-rise25-winners.html"),
    # End Som 2024
    page("feed-icon-guidelines/", "foundation/feed-icon-guidelines/index.html"),
    page("feed-icon-guidelines/faq/", "foundation/feed-icon-guidelines/faq.html"),
    page("licensing/", "foundation/licensing.html"),
    page("licensing/website-content/", "foundation/licensing/website-content.html"),
    page("licensing/website-markup/", "foundation/licensing/website-markup.html"),
    page("licensing/binary-components/", "foundation/licensing/binary-components/index.html"),
    page("licensing/binary-components/rationale/", "foundation/licensing/binary-components/rationale.html"),
    page("moco/", "foundation/moco.html"),
    page("openwebfund/more/", "foundation/openwebfund/more.html"),
    page("openwebfund/thanks/", "foundation/openwebfund/thanks.html"),
    page("trademarks/policy/", "foundation/trademarks/policy.html"),
    page("trademarks/list/", "foundation/trademarks/list.html"),
    page("trademarks/distribution-policy/", "foundation/trademarks/distribution-policy.html"),
    page("trademarks/community-edition-permitted-changes/", "foundation/trademarks/community-edition-permitted-changes.html"),
    page("trademarks/community-edition-policy/", "foundation/trademarks/community-edition-policy.html"),
    page("reimagine-open/", "foundation/reimagine-open.html"),
)
