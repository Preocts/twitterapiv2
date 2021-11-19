[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/twitterapiv2/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/twitterapiv2/main)
[![Python package](https://github.com/Preocts/twitterapiv2/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/twitterapiv2/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/gh/Preocts/twitterapiv2/branch/main/graph/badge.svg?token=5GE4T7XU3L)](https://codecov.io/gh/Preocts/twitterapiv2)

# twitterapiv2 - Custom API wrapper

### Requirements:

- [Python>=3.8](https://www.python.org/)
- [secretbox>=2.1.0](https://pypi.org/project/secretbox/)
- [urllib3>=1.26.7](https://pypi.org/project/urllib3/)

During a re-write of [this project](https://github.com/Preocts/twwordmap) I started writing a wrapper for the Twitter API v2. It was fun enough to create that now its a stand-alone project. We'll see how far this goes!

### Implemented
- Authentication for bearer token
- `tweets/search/recent` endpoint

### On Deck
- `tweets/counts/recent` endpoint
- Internal rate limit handlers

---

## Authenticating with Twitter API v2 as an application

The authentication client of included in the `twitterapiv2/` library requires your applications consumer credentials to be loaded in the environment variables before an authentication attempt is made. The consumer credentials are your client key and client secret as found in the application dashboard of the Twitter Dev panel.

Create two environmental variables as follows:
```env
TW_CONSUMER_KEY=[client key]
TW_CONSUMER_SECRET=[client secret]
```

A 'TW_BEARER_TOKEN' will be created in the environment on successful authentication. This key should be stored securely and loaded to the environment on subsequent calls. When this token already exists, the request for a bearer token can be skipped.

Additional calls to the authentication process **will not** result in a new bearer token if the same consumer credentials are provided. The former bearer token must be invalided to obtain a new one.

## SearchRecent provider

The search client performs a "Search Recent" from the Twitter V2 API. This search is limited to seven days of history and has a large number of inner objects to select from. By default, the search only returns the `text` of the tweet and the `id` of the tweet.

After declaring a base `SearchRecent()` the fields of the search query can be set using the builder methods. These can be chained as they return a new `SearchRecent` with the fields carried forward. When executing a `.search()` the `page_token` allows for pagination of results.

Rate limiting must be handled outside of the library. `SearchRecent.limit_remaining` will be an `int` representing the number of API calls remaining for requests are refused. `SearchRecent.limit_reset` is an unaware UTC `datetime` object of the next reset time (typically 15 minutes). If a search has not been invoked the `.limit_remaining` will default to `-1` and `limit_reset` to `.utcnow()`.

**NOTE**: The search recent endpoint is a monthly rate limited endpoint. Be sure to test the expected result counts of your queries and see the Twitter development dashboard for updated requests remaining.

Full API details:

https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent#Default

Use example:
```py
from datetime import datetime
from twitterapiv2.auth_client import AuthClient
from twitterapiv2.search_recent import SearchRecent
from secretbox import SecretBox

SecretBox(auto_load=True)

auth = AuthClient()
auth.set_bearer_token()
search_string = "#100DaysOfCode -is:retweet"

mysearch = (
    SearchRecent()
    .start_time("2021-11-10T00:00:00Z")
    .expansions("author_id,attachments.poll_ids")
    .max_results(100)
)
while True:
    log.info("Retrieving Tweets...")
    try:
        response = client.search(search_string, page_token=client.next_token)
    except InvalidResponseError as err:
        print(f"Invalid response from HTTP: '{err}'")
        break
    except ThrottledError:
        print(f"Rate limit reached, resets at: {client.limit_reset} UTC")
        while datetime.utcnow() <= client.limit_reset:
            print(f"Waiting for limit reset, currently: {datetime.utcnow()} UTC...")
            sleep(SLEEP_TIME)
        continue
    # Do something with pulled data in response
    if not client.next_token:
        print("No additional pages to poll.")
        break
```

---

## Local developer installation

It is **highly** recommended to use a `venv` for installation. Leveraging a `venv` will ensure the installed dependency files will not impact other python projects.

Clone this repo and enter root directory of repo:
```bash
$ git clone https://github.com/Preocts/twitterapiv2
$ cd twitterapiv2
```

Create and activate `venv`:
```bash
# Linux/MacOS
python3 -m venv venv
. venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate.bat
# or
py -m venv venv
venv\Scripts\activate.bat
```

Your command prompt should now have a `(venv)` prefix on it.

Install editable library and development requirements:
```bash
# Linux/MacOS
pip install -r requirements-dev.txt
pip install --editable .

# Windows
python -m pip install -r requirements-dev.txt
python -m pip install --editable .
# or
py -m pip install -r requirements-dev.txt
py -m pip install --editable .
```

Install pre-commit hooks to local repo:
```bash
pre-commit install
pre-commit autoupdate
```

Run tests
```bash
tox
```

To exit the `venv`:
```bash
deactivate
```

---

### Makefile

This repo has a Makefile with some quality of life scripts if your system supports `make`.

- `update` : Clean all artifacts, update pip, update requirements, install everything
- `build-dist` : Build source distribution and wheel distribution
- `clean-artifacts` : Deletes python/mypy artifacts including eggs, cache, and pyc files
- `clean-tests` : Deletes tox, coverage, and pytest artifacts
- `clean-build` : Deletes build artifacts
- `clean-all` : Runs all clean scripts
