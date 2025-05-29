# Installing Bedrock {: #install }

## Installation Methods

There are two primary methods of installing bedrock: Docker and Local. Whichever you choose, you'll start by getting the source.

The codebase lives at <https://github.com/mozilla/bedrock/>

Only Mozilla staff have write access to that repository; community contributors do not, so should instead make a fork of the repo to work from. You will still be able to make pull requests from your fork into `mozilla/bedrock`.

Get the source code:

``` bash
# If you're a Mozilla staff member with write access to the repo
$ git clone https://github.com/mozilla/bedrock.git

# Or if you lack write access to the repo
$ git clone https://github.com/YOUR_GITHUB_USERNAME_HERE/bedrock.git
```

Once the codebase is cloned, switch into it:

``` bash
$ cd bedrock
```

After these basic steps you can choose your install method below.

Docker is the easiest and recommended way, but local installation directly onto your machine is also possible and may be preferred, particularly if you're doing frontend work, which is currently slower when using Docker.

!!! note
    You should also install our git pre-commit hooks. These are checks that automatically run before a git commit is allowed. You don't have to do this in order to get bedrock running locally, but it's recommended to do before you start making contributions.

    The Bedrock project uses the [pre-commit](https://pre-commit.com/) framework that makes managing git hooks easier across all contributors by ensuring everyone has the same ones set up.

    Install the framework by running `pip install pre-commit`, then - ensuring you are in your `bedrock` directory -run `pre-commit install` in your terminal, followed by `pre-commit install-hooks`. This will set up the hooks that are specified in `bedrock/.precommit.yaml`

    After that setup, whenever you try to make a commit, the 'hooks' will check/lint your Python, JS, and CSS files beforehand and report on problems that need to be fixed before the commit can be made. This will save you time waiting for the tests to run in our `CI (Continuous Integration)`{.interpreted-text role="abbr"} before noticing a linting error.

### Docker Installation

!!! note
    This method assumes you have [Docker installed for your platform](https://www.docker.com/). If not please do that now or skip to the `Local Installation` section.

This is the simplest way to get started developing for bedrock. If you're on Linux or Mac (and possibly Windows 10 with the Linux subsystem) you can run a script that will pull our production and development docker images and start them:

    $ make clean run

!!! note
    You can start the server any other time with:

        $ make run

You should see a number of things happening, but when it's done it will output something saying that the server is running at [localhost:8000](http://localhost:8000/). Go to that URL in a browser and you should see the mozilla.org home page. In this mode the site will refresh itself when you make changes to any template or media file. Simply open your editor of choice and modify things and you should see those changes reflected in your browser.

!!! note
    It's a good idea to run `make pull` from time to time. This will pull down the latest Docker images from our repository ensuring that you have the latest dependencies installed among other things. If you see any strange errors after a `git pull` then `make pull` is a good thing to try for a quick fix.

If you don't have or want to use Make you can call the docker and compose commands directly

``` bash
$ docker compose pull
```

``` bash
$ [[ ! -f .env ]] && cp .env-dist .env
```

Then starting it all is simply

``` bash
$ docker compose up app assets
```

All of this is handled by the `Makefile` script and called by Make if you follow the above directions. You **DO NOT** need to do both.

These directions pull and use the pre-built images that our deployment process has pushed to the [Docker Hub](https://hub.docker.com/u/mozorg/). If you need to add or change any dependencies for Python or Node then you'll need to build new images for local testing. You can do this by updating the requirements files and/or package.json file then simply running:

    $ make build

!!! note
    **For Apple Silicon / M1 users**

    If you find that when you're building you hit issues compiling assets, try unchecking `Use Rosetta for x86_64/amd64 emulation on Apple Silicon` in the Docker Desktop settings.

**Asset bundles**

If you make a change to `media/static-bundles.json`, you'll need to restart Docker.

!!! note
    Sometimes stopping Docker doesn't actually kill the images. To be safe, after stopping docker, run `docker ps` to ensure the containers were actually stopped. If they have not been stopped, you can force them by running `docker compose kill` to stop all containers, or `docker kill <container_name>` to stop a single container, e.g. `docker kill bedrock_app_1`.

### Local Installation

These instructions assume you have Python, pip, and NodeJS installed. If you don't have ``pip`` installed (you probably do) you can install it with the instructions in [the pip docs](https://pip.pypa.io/en/stable/installing/).

Bedrock currently uses Python 3.13.x. The recommended way to install and use that version is with [pyenv](https://github.com/pyenv/pyenv) and to create a virtualenv using [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) that will isolate Bedrock's dependencies from other things installed on the system.

The following assumes you are on MacOS, using `zsh` as your shell and [Homebrew](https://brew.sh/) as your package manager. If you are not, there are installation instructions for a variety of platforms and shells in the READMEs for the two pyenv projects.

**Install Python 3.13.x with pyenv**

1.  Install `pyenv` itself :

        $ brew install pyenv

2\. Configure your shell to init `pyenv` on start - this is noted in the project's [own docs](https://github.com/pyenv/pyenv), in more detail, but omits that setting ``PYENV_ROOT`` and adding it to the path is needed:

    $ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    $ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    $ echo 'eval "$(pyenv init -)"' >> ~/.zshrc

3\. Restart your login session for the changes to profile files to take effect - if you're not using `zsh`, the `pyenv` docs have other routes :

    $ zsh -l

4.  Install the latest Python 3.13.x (e.g. 3.13.3), then test it's there:

        $ pyenv install 3.13.3

    If you'd like to make Python 3.13 your default globally, you can do so with:

        $ pyenv global 3.13.3

    If you only want to make Python 3.13 available in the current shell, while you set up the Python virtualenv (below), you can do so with:

        $ pyenv shell 3.13.3

5.  Verify that you have the correct version of Python installed:

        $ python --version
        Python 3.13.3

**Install a plugin to manage virtualenvs via pyenv and create a virtualenv for Bedrock's dependencies**

1.  Install `pyenv-virtualenv` :

        $ brew install pyenv-virtualenv

2\. Configure your shell to init `pyenv-virtualenv` on start - again, this is noted in the `pyenv-virtualenv` project's [own documentation](https://github.com/pyenv/pyenv-virtualenv), in more detail. The following will slot in a command that will work as long as you have pyenv-virtualenv installed:

    $ echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc

3.  Restart your login session for the changes to profile files to take effect :

        $ zsh -l

4.  Make a virtualenv we can use - in this example we'll call it `bedrock` but use whatever you want :

        $ pyenv virtualenv 3.13.3 bedrock

**Use the virtualenv**

1.  Switch to the virtualenv - this is the command you will use any time you need this virtualenv :

        $ pyenv activate bedrock

2\. If you'd like to auto activate the virtualenv when you cd into the bedrock directory, and deactivate it when you exit the directory, you can do so with:

    $ echo 'bedrock' > .python-version

3.  Securely upgrade pip :

        $ pip install --upgrade pip

4.  Install / update Python dependencies :

        $ make install-local-python-deps

!!! note
    If you are on OSX and some of the compiled dependencies fails to compile, try explicitly setting the arch flags and try again. The following are relevant to Intel Macs only. If you're on Apple Silicon, 3.13.3 should 'just work':

    ``` bash
    $ export ARCHFLAGS="-arch i386 -arch x86_64"
    ```

    ``` bash
    $ make install-local-python-deps
    ```

    If you are on Linux, you may need at least the following packages or their equivalent for your distro:

        python3-dev libxslt-dev

**Download a fresh copy of the sqlite database that Bedrock uses locally** This contains product-details, security-advisories, credits, release notes, localizations, legal-docs etc. We also download the latest translations of site content in many languages:

    $ bin/bootstrap.sh

**Install the node dependencies to run the site**. This will only work if you already have [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/) installed:

    $ npm install

!!! note
    Bedrock uses npm to ensure that Node.js packages that get installed are the exact ones we meant (similar to pip hash checking mode for python). Refer to the [npm documentation](https://docs.npmjs.com/) for adding or upgrading Node.js dependencies.

!!! note
    As a convenience, there is a `make preflight` command which calls some of the commands above to bring your installed Python and NPM dependencies up to date and also fetches the latest DB containing the latest site content. This is a good thing to run after pulling in latest changes from the `main` branch.

    IMPORTANT: if you do not want to replace your local DB with a fresher one, use `make preflight -- --retain-db` instead.

    We also have an optional git hook that will alert you if `make preflight` needs to be run. You can install that with `make install-custom-git-hooks`.


## Run the tests {: #run-python-tests }

Now that we have everything installed, let's make sure all of our tests pass. This will be important during development so that you can easily know when you've broken something with a change.

### Docker

We manage our local docker environment with docker compose and Make. All you need to do here is run:

    $ make test

If you don't have Make you can simply run `docker compose run test`.

If you'd like to run only a subset of the tests or only one of the test commands you can accomplish that with a command like the following:

    $ docker compose run test pytest bedrock/firefox

This example will run only the unit tests for the `firefox` app in bedrock. You can substitute `pytest bedrock/firefox` with most any shell command you'd like and it will run in the Docker container and show you the output. You can also just run `bash` to get an interactive shell in the container which you can then use to run any commands you'd like and inspect the file system:

    $ docker compose run test bash

### Local

From the local install instructions above you should still have your virtualenv activated, so running the tests is as simple as:

    $ pytest lib bedrock

To test a single app, specify the app by name in the command above. e.g.:

    $ pytest bedrock/firefox

## Run a local server

!!! info
    Regardless of whether you run Bedrock via Docker or directly on your machine, the URL of the site is `http://localhost:8000` - ``not`` `8080`

### Docker

You can simply run the `make run` script mentioned above, or use docker compose directly:

    $ docker compose up app assets

### Local

To make the server run, make sure your virtualenv is activated with `pyenv activate bedrock`, and then run the server:

    $ npm start

Wait for the server to start up and then browse to <http://localhost:8000>

Congratulations, you should now have your own copy of www.mozilla.org running locally!

### Prod Mode

There are certain things about the site that behave differently when running locally in dev mode using Django's development server than they do when running in the way it runs in production. Static assets that work fine locally can be a problem in production if referenced improperly, and the normal error pages won't work unless `DEBUG=False` and doing that will make the site throw errors since the Django server doesn't have access to all of the built static assets. So we have a couple of extra Docker commands (via make) that you can use to run the site locally in a more prod-like way.

First you should ensure that your `.env` file is setup the way you need. This usually means adding `DEBUG=False` and `DEV=False`, though you may want `DEV=True` if you want the site to act more like www-dev.allizom.org in that all feature switches are `On` and all locales are active for every page. After that you can run the following:

``` bash
$ make run-prod
```

This will run the latest bedrock image using your local bedrock files and templates, but not your local static assets. If you need an updated image just run `make pull`.

If you need to include the changes you've made to your local static files (images, css, js, etc.) then you have to build the image first:

``` bash
$ make build-prod run-prod
```

### Documentation

This is a great place for coders and non-coders alike to contribute!

If you see a typo or similarly small change, you can use the "Edit in GitHub" link to propose a fix through GitHub. Note: you will not see your change directly committed to the main branch. You will commit the change to a separate branch so it can be reviewed by a staff member before merging to main.

If you want to make a bigger change or [find a Documentation issue on the repo](https://github.com/mozilla/bedrock/labels/Documentation), it is best to edit and preview locally before submitting a pull request. Run the commands from your root folder. They will build documentation and start a live server to auto-update any changes you make to a documentation file.

#### Docker
``` bash
make docs
```

#### Local
``` bash
# docs-setup installs the docs requirements
# only need to run this the first time
make docs-setup
make livedocs
```

## Localization

Localization (or L10n) files were fetched by the ``bootstrap.sh`` command your ran earlier and are included in the docker images. If you need to update them or switch to a different repo or branch after changing settings you can run the following command:

    $ ./manage.py l10n_update

You can read more details about how to localize content [here](l10n.md).

## Feature Flipping (aka Switches, or waffle switches)

Switches are managed using django-waffle and are stored in the database. These switches control behavior and/or features of select pages on Bedrock, and their state (active or inactive) is based on an `active` boolean field in the database.

### Defining and Using Switches

The `switch()` template helper function allows you to check whether a specific switch is active. You pass a name to the function (using only letters, numbers, and dashes), which is automatically converted to uppercase and with dashes replaced by underscores for the lookup in the database. For example, `switch('the-dude')` will look for a switch named `THE_DUDE` in the database.

### Locale-Specific Switches

You can provide a list of locale codes to limit the switch's activation to specific locales. If the page is viewed in a locale not included in the list, the switch will return False. You can also use "Locale Groups," which apply to all locales with a common prefix (e.g., "en-US, en-GB" or "zh-CN, zh-TW"). To use these groups, pass the prefix. For example, `switch('the-dude', ['en', 'de'])` will activate the switch for German and any English locale supported by the site.

### Managing Switches

Switches are managed through the Django Admin interface, where you can add, edit, or remove switches from the database directly. This interface allows for easy management of feature toggles without modifying environment variables or code. There is also a Django management command to toggle switches from the command line, as detailed below.

### Deploy switches with code

You can deploy switches directly through code by creating a data migration. This approach ensures switches are consistently created or updated during deployment, rather than requiring manual configuration through the Django Admin interface.

To implement a switch via data migration, create an empty migration file:

``` bash
./manage.py makemigrations base --empty
```

Then add the following code to the generated migration file, which can be found in the `bedrock/base/migrations` directory:

``` python
from django.db import migrations

from waffle.models import Switch

# The name of the switch must be unique.
SWITCH_NAME = "RELEASE_THE_KRAKEN"


def create_switch(apps, schema_editor):
    Switch.objects.get_or_create(
        name=SWITCH_NAME,
        defaults={"active": True},  # Set initial state, True or False.
    )


def remove_switch(apps, schema_editor):
    Switch.objects.filter(name=SWITCH_NAME).delete()


class Migration(migrations.Migration):
    dependencies = [
        (
            "base",
            "0001_initial",
        ),  # Keep whatever the makemigrations command generated here.
    ]

    operations = [
        migrations.RunPython(create_switch, remove_switch),
    ]
```

The migration will run during deployment and ensure the switch exists in the database. The `remove_switch` function allows the migration to be reversed if needed.

To test this locally, run the following command:

``` bash
./manage.py migrate base
```

Verify the switch exists in the database by running:

``` bash
./manage.py waffle_switch -l
```

You should see the switch listed in the output.

To test reversing the migration, run the following command but replace `0001` with whatever the previous migration number is:

``` bash
./manage.py migrate base 0001
```

### Example Usage in Templates

You can use the `switch()` helper function in your templates as follows:

``` html
{% if switch('the-dude') %}
    <!-- Feature-specific HTML goes here -->
{% endif %}
```

### Example Usage in Python

You may also use switches in Python code (though locale support is unavailable in this context):

!!! note
    **Avoid using switch() outside the request/response cycle** (e.g., during module-level imports or in a urls.py file), as the switch's state is managed in the database and can be changed via the admin interface. Using it outside the request cycle would prevent the switch value from reflecting real-time updates.

``` python
from bedrock.base.waffle import switch


def home_view(request):
    title = "Staging Home" if switch("staging-site") else "Prod Home"
    ...
```

### Testing

If the environment variable `DEV` is set to a "true" value, then all switches will be considered active unless they are explicitly set as not active in the database. `DEV` defaults to "true" in local development and demo servers.

To test switches locally, add the switch to the database. This can be done in one of two ways.

1. Add the switch via the Django management command:

    ``` bash
    ./manage.py waffle_switch --create SWITCH_NAME on
    ```

    If the switch already exists, you can toggle it using:

    ``` bash
    ./manage.py waffle_switch SWITCH_NAME on ./manage.py waffle_switch SWITCH_NAME off
    ```

    And you can view all the switches via:

    ``` bash
    ./manage.py waffle_switch -l
    ```

    To delete a switch, run:

    ``` bash
    ./manage.py waffle_delete --switches SWITCH_NAME
    ```

2. Add the switch in the Django admin at `/django-admin/`. There you will see the "Django-Waffle" module with the "Switches" table. Click through to view the switches and add/edit/delete as needed.

### Traffic Cop

Currently, these switches are used to enable/disable [Traffic Cop](https://github.com/mozmeao/trafficcop/) experiments on many pages of the site. We only add the Traffic Cop JavaScript snippet to a page when there is an active test.

To work with/test these experiment switches locally, you must add the switches to your local database.

### Notes

A shortcut for activating virtual envs in zsh or bash is ``. venv/bin/activate``. The dot is the same as ``source``.

There's a project called [pew](https://pypi.org/project/pew/) that provides a better interface for managing/activating virtual envs, so you can use that if you want. Also if you need help managing various versions of Python on your system, the [pyenv](https://github.com/pyenv/pyenv) project can help.
