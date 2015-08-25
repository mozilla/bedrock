# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from bedrock.mozorg.util import page
from bedrock.redirects.util import redirect

urlpatterns = (
    page('', 'foundation/index.html'),
    page('about', 'foundation/about.html'),

    # Bug 1102336 /foundation/annualreport/ ->
    # /foundation/annualreport/2013/
    redirect(r'^foundation/annualreport/$',
             'foundation.annualreport.2013.index',
             name='foundation.annualreport', locale_prefix=False),

    # Older annual report financial faqs - these are linked from blog posts
    # was e.g.: http://www.mozilla.org/foundation/documents/mozilla-2008-financial-faq.html
    page('documents/mozilla-2006-financial-faq', 'foundation/documents/mozilla-2006-financial-faq.html'),
    page('documents/mozilla-2007-financial-faq', 'foundation/documents/mozilla-2007-financial-faq.html'),
    page('documents/mozilla-2008-financial-faq', 'foundation/documents/mozilla-2008-financial-faq.html'),

    # ported from PHP in Bug 960689
    page('documents/bylaws-amendment-1', 'foundation/documents/bylaws-amendment-1.html'),
    page('documents/bylaws-amendment-2', 'foundation/documents/bylaws-amendment-2.html'),
    page('documents/articles-of-incorporation', 'foundation/documents/articles-of-incorporation.html'),
    page('documents/articles-of-incorporation/amendment', 'foundation/documents/articles-of-incorporation-amendment.html'),
    page('documents/bylaws', 'foundation/documents/bylaws.html'),

    # was https://www.mozilla.org/foundation/annualreport/2009/
    page('annualreport/2009', 'foundation/annualreport/2009/index.html'),
    # was .html
    page('annualreport/2009/a-competitive-world', 'foundation/annualreport/2009/a-competitive-world.html'),
    # was .html
    page('annualreport/2009/broadening-our-scope', 'foundation/annualreport/2009/broadening-our-scope.html'),
    # was .html
    page('annualreport/2009/sustainability', 'foundation/annualreport/2009/sustainability.html'),

    # was         https://www.mozilla.org/foundation/annualreport/2009/faq.html
    # changing to https://www.mozilla.org/foundation/annualreport/2009/faq/
    page('annualreport/2009/faq', 'foundation/annualreport/2009/faq.html'),

    page('annualreport/2010', 'foundation/annualreport/2010/index.html'),
    page('annualreport/2010/ahead', 'foundation/annualreport/2010/ahead.html'),
    page('annualreport/2010/opportunities', 'foundation/annualreport/2010/opportunities.html'),
    page('annualreport/2010/people', 'foundation/annualreport/2010/people.html'),
    page('annualreport/2010/faq', 'foundation/annualreport/2010/faq.html'),

    page('annualreport/2011', 'foundation/annualreport/2011.html'),
    page('annualreport/2011/faq', 'foundation/annualreport/2011faq.html'),

    page('annualreport/2012', 'foundation/annualreport/2012/index.html'),
    page('annualreport/2012/faq', 'foundation/annualreport/2012/faq.html'),

    page('annualreport/2013', 'foundation/annualreport/2013/index.html'),
    page('annualreport/2013/faq', 'foundation/annualreport/2013/faq.html'),

    page('feed-icon-guidelines', 'foundation/feed-icon-guidelines/index.html'),
    page('feed-icon-guidelines/faq', 'foundation/feed-icon-guidelines/faq.html'),

    page('licensing', 'foundation/licensing.html'),
    page('licensing/website-content', 'foundation/licensing/website-content.html'),
    page('licensing/website-markup', 'foundation/licensing/website-markup.html'),
    page('licensing/binary-components', 'foundation/licensing/binary-components/index.html'),
    page('licensing/binary-components/rationale', 'foundation/licensing/binary-components/rationale.html'),
    page('moco', 'foundation/moco.html'),
    page('mocosc', 'foundation/mocosc.html'),

    page('openwebfund/more', 'foundation/openwebfund/more.html'),
    page('openwebfund/thanks', 'foundation/openwebfund/thanks.html'),

    page('trademarks', 'foundation/trademarks/index.html'),
    page('trademarks/policy', 'foundation/trademarks/policy.html'),
    page('trademarks/list', 'foundation/trademarks/list.html'),
    page('trademarks/faq', 'foundation/trademarks/faq.html'),
    page('trademarks/l10n-website-policy', 'foundation/trademarks/l10n-website-policy.html'),
    page('trademarks/distribution-policy', 'foundation/trademarks/distribution-policy.html'),
    page('trademarks/community-edition-permitted-changes', 'foundation/trademarks/community-edition-permitted-changes.html'),
    page('trademarks/community-edition-policy', 'foundation/trademarks/community-edition-policy.html'),
    page('trademarks/poweredby/faq', 'foundation/trademarks/poweredby/faq.html'),

    # documents
    page('documents', 'foundation/documents/index.html'),
)
