# cloudpassage-halo-python-sdk

## Python SDK for CloudPassage Halo API

[![Documentation Status](https://readthedocs.org/projects/cloudpassage-halo-python-sdk/badge/?version=latest)](http://cloudpassage-halo-python-sdk.readthedocs.io/en/latest/?badge=latest)

### Branch: master

[![Code Climate](https://codeclimate.com/github/cloudpassage/cloudpassage-halo-python-sdk/badges/gpa.svg)](https://codeclimate.com/github/cloudpassage/cloudpassage-halo-python-sdk)

[![Test Coverage](https://codeclimate.com/github/cloudpassage/cloudpassage-halo-python-sdk/badges/coverage.svg)](https://codeclimate.com/github/cloudpassage/cloudpassage-halo-python-sdk/coverage)

[![Build Status](https://travis-ci.org/cloudpassage/cloudpassage-halo-python-sdk.svg?branch=master)](https://travis-ci.org/cloudpassage/cloudpassage-halo-python-sdk)

### Branch: develop

[![Build Status](https://travis-ci.org/cloudpassage/cloudpassage-halo-python-sdk.svg?branch=develop)](https://travis-ci.org/cloudpassage/cloudpassage-halo-python-sdk)


### Installation

[![PyPI version](https://badge.fury.io/py/cloudpassage.svg)](https://pypi.python.org/pypi/cloudpassage/)

Requirements:

* Python 2.7.10+ or 3.7
* OpenSSL 1.0.2 or newer
* requests 2.18 or newer
* pyaml


Install from pip with ```sudo pip install cloudpassage```.  If you want to make
modifications to the SDK you can install it in editable mode by downloading
the source from this github repo, navigating to the top directory within the
archive and running ```sudo pip install -e .``` (note the . at the end).

### Quick Start

Here's the premise: you store your session configuration information (API
credentials, proxy settings, etc) in the cloudpassage.HaloSession object.
This object gets passed into the various class methods which allow you
to interact with the CloudPassage Halo API.

Practical example:
We'll print a list of all servers in our account:

```python
import cloudpassage

api_key = MY_HALO_API_KEY
api_secret = MY_API_SECRET
session = cloudpassage.HaloSession(api_key, api_secret)
server = cloudpassage.Server(session)

list_of_servers = server.list_all()
for s in list_of_servers:
    print "ID: %s   Name: %s" % (s["id"], s["hostname"])

```

### Docs

#### Browsing and downloading
Built documentation can be found at http://cloudpassage-halo-python-sdk.readthedocs.io/en/latest/

#### Building documentation
1. Clone the repository locally
1. Navigate to `cloudpassage-halo-python-sdk/docs`
1. run `sphinx-build -b pdf source build/pdf`
1. Docs will be located at `cloudpassage-halo-python-sdk/docs/build/pdf/CloudPassage_Python_SDK_$VERSION.pdf`

### Testing
Testing procedure is documented at: http://cloudpassage-halo-python-sdk.readthedocs.io/en/latest/testing.html

<!---
#CPTAGS:community-supported integration api-example
#TBICON:images/python_icon.png
-->
