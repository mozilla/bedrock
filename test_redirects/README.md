# mozilla.org redirection tests

A test suite intended as a reference of the redirects we expect to work
on www.mozilla.org. This will become a base for implementing these
redirects in the [bedrock][] app and allow us to test them there before
release.

## Setup

 1. [Install bedrock](http://bedrock.readthedocs.org/en/latest/install.html)
 2. Activate or switch to your bedrock [virtualenv][] environment
 3. Install the redirect test dependencies: `./bin/peep.py install -r requirements/test_redirects.txt`

## Running the tests

Run the tests from within your bedrock [virtualenv][] environment.

```bash
$ py.test test_redirects
```

By default the suite is run against your local copy of bedrock. If you wish to run
it against another instance of the site (e.g. www.mozilla.org) you can set the
`--mozorg-url` command line switch.

```bash
$ py.test test_redirects --mozorg-url=https://www.mozilla.org
```

**Note**: If you intend to run the suite against a remote instance of the site (e.g. production) it will run a lot quicker if you install [pytest-xdist][] and have it use multiple processes (e.g. `py.test test_redirects -n auto`).

[bedrock]: https://github.com/mozilla/bedrock/
[virtualenv]: https://virtualenv.pypa.io/
[pytest-xdist]: http://pytest.org/latest/xdist.html
