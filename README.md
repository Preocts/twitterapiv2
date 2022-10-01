[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/twitterapiv2/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/twitterapiv2/main)
[![Python package](https://github.com/Preocts/twitterapiv2/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/twitterapiv2/actions/workflows/python-tests.yml)

# twitterapiv2 - Custom API wrapper

### Requirements:

- [Python>=3.8](https://www.python.org/)
- [httpx==0.23.0]

During a re-write of [this project](https://github.com/Preocts/twwordmap) I
started writing a wrapper for the Twitter API v2. It was fun enough to create
that now its a stand-alone project. We'll see how far this goes!

### Work
- [x] Authentication for bearer token
- [x] `tweets/search/recent` endpoint
- [x] `tweets/counts/recent` endpoint
- [x] `tweets/lookup` endpoint
- [x] Interface for `/tweets/` endpoint clients
- [] TUI User Authentication
- [] Better documentation
- [] Internal rate limit handlers

---

## Authenticating with Twitter API v2 as an application

The authentication client of included in the `twitterapiv2/` library requires
your applications consumer credentials to be loaded in the environment variables
before an authentication attempt is made. The consumer credentials are your
client key and client secret as found in the application dashboard of the
Twitter Dev panel.

Create four environmental variables as follows:
```env
TW_CONSUMER_KEY=[client key]
TW_CONSUMER_SECRET=[client secret]
TW_ACCESS_TOKEN=[access key]
TW_ACCESS_SECRET=[access secret]
```

A 'TW_BEARER_TOKEN' will be created in the environment on successful
authentication. This key should be stored securely and loaded to the environment
on subsequent calls. When this token already exists, the request for a bearer
token can be skipped.

Additional calls to the authentication process **will not** result in a new
bearer token if the same consumer credentials are provided. The former bearer
token must be invalided to obtain a new one.

## SearchRecent provider

The search client performs a "Search Recent" from the Twitter V2 API. This
search is limited to seven days of history and has a large number of inner
objects to select from. By default, the search only returns the `text` of the
tweet and the `id` of the tweet.

After declaring a base `SearchRecent()` the fields of the search query can be
set using the builder methods. When executing a `.fetch()` the `page_token` is
automatically set to the next results. Checking the `.more` property after the
first `.fetch()` will indicate if more results remain. Fetch loops should stop
when `.more` is `False`.

Rate limiting must be handled outside of the library.
`SearchRecent.limit_remaining` will be an `int` representing the number of API
calls remaining for requests are refused. `SearchRecent.limit_reset` is an
unaware UTC `datetime` object of the next reset time (typically 15 minutes). If
a search has not been invoked the `.limit_remaining` will default to `-1` and
`limit_reset` to `.utcnow()`.

**NOTE**: The search recent endpoint is a monthly rate limited endpoint. Be sure
to test the expected result counts of your queries and see the Twitter
development dashboard for updated requests remaining.

Full API details:

https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent#Default

Use example:
```py
from datetime import datetime
from time import sleep

from secretbox import SecretBox
from twitterapiv2.auth_client import AuthClient
from twitterapiv2.exceptions import InvalidResponseError
from twitterapiv2.exceptions import ThrottledError
from twitterapiv2.search_recent import SearchRecent


SecretBox(auto_load=True)

auth = AuthClient()
auth.set_bearer_token()

mysearch = SearchRecent()
mysearch.start_time("2021-11-23T00:00:00Z")
mysearch.expansions("author_id,attachments.poll_ids")
mysearch.max_results(10)
mysearch.query("#100DaysOfCode -is:retweet")

while True:
    print("Retrieving Tweets...")
    try:
        response = mysearch.fetch()
    except InvalidResponseError as err:
        print(f"Invalid response from HTTP: '{err}'")
        break
    except ThrottledError:
        print(f"Rate limit reached, resets at: {mysearch.limit_reset} UTC")
        while datetime.utcnow() <= mysearch.limit_reset:
            print(f"Waiting for limit reset, currently: {datetime.utcnow()} UTC...")
            sleep(60)
        continue

    # Do something with pulled data in response

    if not mysearch.more:
        print("No additional pages to poll.")
        break
```

---

## Local developer installation

It is **highly** recommended to use a `venv` for installation. Leveraging a
`venv` will ensure the installed dependency files will not impact other python
projects.

Clone this repo and enter root directory of repo:
```bash
$ git clone https://github.com/Preocts/twitterapiv2
$ cd twitterapiv2
```

Create the `venv`:

```bash
python -m venv venv
```

Activate the `venv`:

```bash
# Linux/Mac
. venv/bin/activate

# Windows
venv\Scripts\activate
```

The command prompt should now have a `(venv)` prefix on it. `python` will now
call the version of the interpreter used to create the `venv`

Install editable library and development requirements:

```bash
# Update pip and tools
python -m pip install --upgrade pip

# Install editable version of library
python -m pip install --editable .[dev]
```

Install pre-commit [(see below for details)](#pre-commit):

```bash
pre-commit install
```

---

## Misc Steps

Run pre-commit on all files:

```bash
pre-commit run --all-files
```

Run tests:

```bash
tox [-r] [-e py3x]
```

Build dist:

```bash
python -m pip install --upgrade build

python -m build
```

To deactivate (exit) the `venv`:

```bash
deactivate
```
---

## Note on flake8:

`flake8` is included in the `requirements-dev.txt` of the project. However it
disagrees with `black`, the formatter of choice, on max-line-length and two
general linting errors. `.pre-commit-config.yaml` is already configured to
ignore these. `flake8` doesn't support `pyproject.toml` so be sure to add the
following to the editor of choice as needed.

```ini
--ignore=W503,E203
--max-line-length=88
```

---

## [pre-commit](https://pre-commit.com)

> A framework for managing and maintaining multi-language pre-commit hooks.

This repo is setup with a `.pre-commit-config.yaml` with the expectation that
any code submitted for review already passes all selected pre-commit checks.
`pre-commit` is installed with the development requirements and runs seemlessly
with `git` hooks.

---

## Makefile

This repo has a Makefile with some quality of life scripts if the system
supports `make`.  Please note there are no checks for an active `venv` in the
Makefile.

| PHONY             | Description                                                      |
| ----------------- | ---------------------------------------------------------------- |
| `init`            | Update pip to newest version                                     |
| `install`         | install the project                                              |
| `install-dev`     | install development requirements and project as editable install |
| `build-dist`      | Build source distribution and wheel distribution                 |
| `clean-artifacts` | Deletes python/mypy artifacts, cache, and pyc files              |
| `clean-tests`     | Deletes tox, coverage, and pytest artifacts                      |
| `clean-build`     | Deletes build artifacts                                          |
| `clean-all`       | Runs all clean scripts                                           |
