from collections import namedtuple

Grant = namedtuple('Grant', 'url, grantee, title, type, amount, year, summary, description')

GRANTS = [
    Grant(
        "foo",
        "Test 1",
        "Test 1",
        "learning-webmaking",
        "$100'000",
        2012,
        "Lorem ipsum, lorem ipsum",
        "<p>Lorem ipsum, lorem ipsum</p>"
    ),
    Grant(
        "bar",
        "Sample data 1",
        "Sample data 1",
        "open-source-technology",
        "$200'000",
        2012,
        "Sample data 1",
        "<p>Sample data 1</p>"
    ),
    Grant(
        "foobar",
        "Sample data 2",
        "Sample data 2",
        "free-culture-community",
        "$500'000",
        2012,
        "Sample data 2",
        "<p>Sample data 2</p>"
    ),
    Grant(
        "bahbah",
        "Sample data 3",
        "Sample data 3",
        "user-sovereignty",
        "$150'000",
        2012,
        "Sample data 3",
        "<p>Sample data 3</p>"
    ),
    Grant(
        "sheeps",
        "Sample data 4",
        "Sample data 4",
        "open-source-technology",
        "$500'000",
        2011,
        "Sample data 4",
        "<p>Sample data 4</p>"
    ),
    Grant(
        "feebar",
        "Sample data 5",
        "Sample data 5",
        "learning-webmaking",
        "$300'000",
        2011,
        "Sample data 5",
        "<p>Sample data 5</p>"
    ),
    Grant(
        "cheese",
        "Sample data 6",
        "Sample data 6",
        "open-source-technology",
        "$200'000",
        2011,
        "Sample data 6",
        "<p>Sample data 6</p>"
    ),
    Grant(
        "hoorah",
        "Sample data 7",
        "Sample data 7",
        "open-source-technology",
        "$500'000",
        2011,
        "Sample data 7",
        "<p>Sample data 7</p>"
    ),
    Grant(
        "feeble",
        "Sample data 8",
        "Sample data 8",
        "user-sovereignty",
        "$150'000",
        2011,
        "Sample data 8",
        "<p>Sample data 8</p>"
    ),
    Grant(
        "java",
        "Sample data 9",
        "Sample data 9",
        "open-source-technology",
        "$450'000",
        2010,
        "Sample data 9",
        "<p>Sample data 9</p>"
    )
]
