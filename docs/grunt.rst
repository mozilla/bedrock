.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _grunt:

===========
Using Grunt
===========

Introduction
------------

If you haven't used `Grunt <http://gruntjs.com/>`_ before, be sure to check
out the `Getting Started guide <http://gruntjs.com/getting-started>`_, as
it explains how to create a `Gruntfile <http://gruntjs.com/sample-gruntfile>`_
as well as install and use Grunt plugins.

Bedrock provides a Gruntfile.js in the root of the project to make local
development easier, by automating common tasks such as:

* Compiling CSS when a LESS file changes.
* Running `JSHint <http://www.jshint.com/>`_ when a JavaScript file changes.
* Live reloading in the browser whenever an HTML, CSS of JavaScript file changes.


Installation
------------

Grunt and Grunt plugins are installed and managed via `npm <https://npmjs.org/>`_,
the `Node <http://nodejs.org/>`_ package manager.

In order to get started, you'll want to install Grunt's command line interface
(CLI) globally. You may need to use sudo (for OSX, \*nix, BSD etc) or run your
command shell as Administrator (for Windows) to do this::

    npm install -g grunt-cli

You may also want to install JSHint globally using::

    npm install -g jshint

Finally, install the dependencies that the bedrock Gruntfile needs::

    npm install


Usage
-----

To start the grunt task runner, simply run::

    grunt

To enable live-reload in the browser you must set ``USE_GRUNT_LIVERELOAD`` to
``True`` in ``bedrock/settings/local.py``::

    USE_GRUNT_LIVERELOAD = True

In the root directory you will also find a ``.jshintrc-dist`` file which contains
a basic set of defaults for running JSHint. If you wish to use these defaults
with Grunt then copy the contents to a local ``.jshintrc`` file::

	cp .jshintrc-dist .jshintrc


Testing
-------

Bedrock has a suite of JavaScript unit tests written using `Jasmine <http://pivotal.github.io/jasmine/>`_
and `Sinon <http://sinonjs.org/>`_. You can run these tests on the command line using
`Karma <http://karma-runner.github.io>`_ test runner and `PhantomJS <http://phantomjs.org/>`_.

To perform a single run of the test suite, type the following command::

	grunt test

.. note::

    The Tabzilla tests require that you have your local bedrock development server running on port 8000.


Cleaning generated CSS files
----------------------------

Bedrock uses `Less <http://lesscss.org/>`_ to generate CSS files. Sometimes during development you may
want to clear out your cached CSS that gets generated. To make this easier, you can clear all
``*.less.css`` files located in ``media/css/`` directories with the following command::

    grunt clean



