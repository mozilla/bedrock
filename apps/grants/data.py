CURRENCY_OPTIONS = (
    ('USD', '$%d'),
    ('GBP', '&pound;%d'),
    ('EUR', '&euro;%d'),
    ('JPY', '&yen;%d'),
)

FOCUS_OPTIONS = (
    ('learning', 'Learning & Webmaking'),
    ('open_source', 'Open Source Technology'),
    ('users', 'User Sovereignty'),
    ('culture', 'Free Culture & Community'),
)

GRANT_LIST = (
    {
        'grantee': 'Someone',
        'title': 'Yet Another Grant',
        'amount': 1500,
        'year': 2013,
        'focus': 'culture',
        'summary': 'A brief summary of this grant.',
        'slug': 'yet-another-grant'
    },
    {
        'grantee': 'Someone',
        'title': 'Test Grant',
        'amount': 150,
        'currency': 'GBP',
        'year': 2012,
        'focus': 'learning',
        'summary': 'A brief summary of this grant.',
        'slug': 'test-grant'
    },
    {
        'grantee': 'Someone',
        'title': 'Another Grant',
        'amount': 1500,
        'year': 2012,
        'focus': 'users',
        'summary': 'A brief summary of this grant.',
        'slug': 'another-grant'
    },
)