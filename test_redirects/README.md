# mozilla.org redirection tests

A test suite intended as a reference of the redirects we expect to work
on www.mozilla.org. This will become a base for implementing these
redirects in the [bedrock][] app and allow us to test them there before
release.

## Setup

1. CD to the directory: `cd test_redirects`
2. Install dependencies: `pip install -r requirements.txt`

Note: You'll need to have installed the dev requirements from bedrock as well.
Also it's a really good idea to do the `pip install` step above in a [virtualenv][].

By default the suite is run against <https://www.mozilla.org>. If you wish to run
it against another instance of the site (e.g. a local copy) you can set the
`MOZORG_URL` environment variable, or add that to a file called `.env` in the test
suite directory.

```bash
# .env
MOZORG_URL="http://localhost:8000"
```

## Running the tests

```bash
$ py.test
```

[bedrock]: https://github.com/mozilla/bedrock/
[virtualenv]: https://virtualenv.pypa.io/
