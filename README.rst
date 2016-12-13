Accessing GaaP Services Gateway Service
=======================================

.. image:: https://travis-ci.org/crossgovernmentservices/ags_gateway.svg?branch=master
  :alt: Test result

Web service and OIDC Broker which provides an Identity Provider selection user
interface for Accessing GaaP Services.


Installation
------------

.. code-block:: bash

    git clone git@github.com:crossgovernmentservices/ags_gateway.git


Usage
-----


Quick Start
~~~~~~~~~~~

.. code-block:: bash

    cd ags_gateway
    ./run-app


Configuration
-------------

The gateway service looks for certain environment variables for settings. The
following variables are **REQUIRED**:

``OIDC_CLIENT_ISSUER``
    The base URL of the OIDC broker

``OIDC_CLIENT_ID``
    The client ID that you have been issued

``OIDC_CLIENT_SECRET``
    The client secret that you have been issued

The following variables are **OPTIONAL**:

``PORT``
    The port number the gateway app will listen on - defaults to ``5000``

``SERVER_NAME``
    The hostname (and port number, if not 80) of the gateway server - defaults
    to ``localhost:$PORT``

``SECRET_KEY``
    The secret used to encrypt session cookies - override this if deploying to
    multiple hosts - WARNING defaults to an insecure secret


Support
-------

This source code is provided as-is, with no incident response or support levels.
Please log all questions, issues, and feature requests in the Github issue
tracker for this repo, and we'll take a look as soon as we can. If you're
reporting a bug, then it really helps if you can provide the smallest possible
bit of code that reproduces the issue. A failing test is even better!


Contributing
------------

* Check out the latest master to make sure the feature hasn't been implemented
  or the bug hasn't been fixed
* Check the issue tracker to make sure someone hasn't already requested
  and/or contributed the feature
* Fork the project
* Start a feature/bugfix branch
* Commit and push until you are happy with your contribution
* Make sure your changes are covered by unit tests, so that we don't break it
  unintentionally in the future.
* Please don't mess with setup.py, version or history.


Copyright
---------

Copyright |copy| 2015 HM Government (Government Digital Service). See
LICENSE for further details.

.. |copy| unicode:: 0xA9 .. copyright symbol
