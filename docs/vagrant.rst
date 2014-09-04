.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _vagrant:


========================
Vagrant Installation
========================

The Vagrant installation will help you work on the Python bedrock codebase
and the PHP legacy codebase with a minimum amount of effort (hopefully).

This entire process will take between 30-50 minutes. For most of this time you will
not be doing anything, Vagrant will be automagically downloading and configuring.
This is a good time to have a cup of tea and/or coffee, possibly walk the dog.

Preparing Your System
---------------------

#. **Install Vagrant.**

    Vagrant is a manager of VMs for development.

    Based on a configuration file, Vagrant will create a Virtual Machine, downloading
    and configuring everything you need to have a local environment running.

    This installation is tested using version: v1.4.3

    Visit `Vagrant's download page <http://downloads.vagrantup.com/>`_.

    Do not install via apt-get, the version (at the time of writing) installed
    in debian wheezy appears broken.

#. **Install Virtualbox.**

    You are required to have virtualbox installed.

    This installation is tested with version 4.2.18 and can be downloaded

    at the `virtualbox download page <https://www.virtualbox.org/>`_.

    - For Debian based systems::

      ~$ sudo apt-get install virtualbox


#. **Install git.**

    The bedrock code is revisioned using `git <http://git-scm.org>`.

    - For Debian based systems::

      ~$ sudo apt-get install git

    For other Linux distributions or operating systems visit `Git's
    download page <http://git-scm.com/downloads>`_.

#. **Install svn.**

    The legacy php code is revisioned using SVN.

    - For Debian based systems::

      ~$ sudo apt-get install subversion

    For other Linux distributions or operating systems visit `SVN's
    download page <http://subversion.apache.org/packages.html>`_.



Build The Environment
---------------------

#. **Directory Setup.**

    Create a top level directory to hold both bedrock and the legacy file system.
    You could call this directory 'bedrock-legacy'. The following steps take
    place under that directory.

#. **Using Git Clone Bedrock Repository.**

      Bedrock is hosted at `<http://github.com/mozilla/bedrock>`_.

      Clone the repository locally::

      ~bedrock-legacy$ git clone --recursive http://github.com/mozilla/bedrock

      .. note::

        Make sure you use ``--recursive`` when checking the repo out!
        If you didn't, you can load all the submodules with ``git
        submodule update --init --recursive``.

#. **Using SVN Checkout The Locale Repository. (Optional)**

      If you would like to see localized versions of the site you will need to
      checkout the locale directory to the root of the bedrock directory you just cloned.

      Clone the repository locally::

      ~$ cd bedrock
      ~bedrock-legacy/bedrock$ svn checkout https://svn.mozilla.org/projects/mozilla.com/trunk/locales/ locale

      .. note::

        You can read more details about how to localize content :ref:`here<l10n>`.

#. **Using SVN Checkout Mozilla.com PHP Repository.**

    Mozilla.com PHP is hosted on `<https://svn.mozilla.org/projects/mozilla.com/trunk>`_.

    Clone the repository locally::

      ~bedrock-legacy$ svn co https://svn.mozilla.org/projects/mozilla.com/trunk mozilla.com

    .. note::

      At this stage you should have two directories side-by-side. `bedrock` and `mozilla.com`.


Configure The Environment
-------------------------

#. **Configure Bedrock.**

    Configure Bedrock by creating and editing the local settings file::

      ~bedrock-legacy$ cp bedrock/bedrock/settings/local.py-dist bedrock/bedrock/settings/local.py

    Add this line below LESS_PREPROCESS::

      LESS_BIN = '/usr/local/bin/lessc'

#. **Configure Mozilla PHP.**

    Configure the legacy site by creating and editing the local settings file::

      cd mozilla.com/includes
      cp config.inc.php-dist config.inc.php

    Set the following values::

      $config['server_name'] = 'mozilla.local';

      $config['file_root'] = '/srv/legacy';

#. **Set A Host Name.**

    We need to set a host name that you will use to access vagrant from a web-browser.
    You will need to add the following to your hosts file (note you may need
    sudo permissions). ::

      192.168.10.55    mozilla.local

    The hosts file can be found in the following directories.

    - For Debian & OS X based systems::

      /etc/hosts

    - For Windows based systems ::

        c:\windows\system32\drivers\etc\hosts


Start Your Machine
---------------------

#. **Fire up vagrant.**

    Now you need to build the virtual machine where Mozilla will live. Change into the
    cloned git directory and run vagrant. Note you must run this command in the
    directory that contains the Vagrantfile. ::

      ~$ cd bedrock
      ~bedrock-legacy/bedrock$ vagrant up --provision

    .. note::
      The first time you run vagrant a VM image will be downloaded
      and the guest machine will be configured. You will be
      downloading more than 300Mb for the linux image and a bunch of additional
      downloading and configuration is going to happen. The total install can
      take 20 minutes on a fast machine. A decent internet connection is
      recommended.

    .. note::
      Often the initial installation will time out while
      compiling node.

      If this happens just run the following command to re-sume the install: ::

      ~bedrock-legacy/bedrock$ vagrant provision


#. **Update Product Details**
    Bedrock needs to grab some information about Mozilla products to run. This is a
    one time update. To run the update you need to SSH into your Vagrant install
    and run the update script.

    SSH into your vagrant install ::

      ~bedrock-legacy/bedrock$ vagrant ssh

    CD Into The Top Level Bedrock Directory::

      ~$ cd /vagrant/

    Update Product Details::

      /vagrant$ python manage.py update_product_details

    Exit ::

      /vagrant$ exit


#. **Confirm Everything Is Setup.**

    Confirm both bedrock and the legacy PHP site are working by visiting
    these urls. If everything looks right you are good to go!

    http://mozilla.local
    The mozilla homepage loading from bedrock.


    http://mozilla.local/en-US/about/legal.html
    A legacy page loading from PHP

    .. note::
      The first time you load a page the CSS may not load. This is likely
      due to the CSS not being compiled. Doing a refresh will solve this problem.

Working & Workflow
---------------------

    At this stage you should have a fully functional dev environment. You can work
    on files in your regular manner and follow the normal git workflow.



Tips & Tricks
---------------------

#. **Connect to your vagrant machine.**

    You can connect to your vagrant machine, when it's running, using: ::

      bedrock-legacy/bedrock$ vagrant ssh

#. **Starting & Stopping Vagrant.**

    Start ::

      ~$ vagrant up --provision

    Stop (vagrant is memory intensive - so if you are not using it best to stop it)::

      ~$ vagrant halt


Troubleshooting
---------------------
  Find us on irc in #webprod


