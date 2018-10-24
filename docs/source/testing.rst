Testing
=======

.. toctree::

Important locations for testing
-------------------------------

**ONLY FOR LOCAL TESTING.  FOR AUTOMATED TESTING SEE BELOW...**
tests/configs: You'll find a file here called
portal.yaml.  Copy it to portal.yaml.local and complete the information
inside with your API key and secret.  the .gitignore settings will keep you
from checking in your creds if you put them in the .local file.  This file
(portal.yaml.local) is referenced directly by all tests requiring interaction
with the API.

tests/policies: These are Halo policies, used primarily for integration
tests.

tests/tests: This is where you'll find the actual tests.

Tests are written for pytest.


Environmental Requirements
--------------------------

  You'll need to have a CloudPassage Halo account available for running the
  tests, as many are integration-focused.  These are the things you need to have
  (at the very least) to get a clean testing run:

  * Servers:
      * Have at least one active Linux and active Windows server.
      * One deactivated server of any type.
  * Policies:
      * One firewall policy
      * One alert profile
      * One Linux CSM policy
      * One Linux FIM policy
      * One Windows FIM policy
      * One LIDS policy
  * Scans:
      * CSM (Failed scan)
      * FIM (active baseline and successful scan)
      * One CVE exception
  * Events:
      * One event produced by a Windows server.
  * Server Group:
      * Using the default group is fine.
      * Assign the policies mentioned above to the group.
      * Run FIM baselines against the Linux and Windows servers.
      * Kick off a CSM scan if it doesn't happen automatically


Running tests automagically
---------------------------

Build the container and run it.

::
 docker build -t cloudpassage_halo_python_sdk .

 docker run \
     -it \
     --rm \
     -e HALO_API_KEY=${HALO_API_KEY} \
     -e HALO_API_SECRET_KEY=${HALO_API_SECRET_KEY} \
     -e HALO_API_HOSTNAME=${HALO_API_HOSTNAME} \
     -e HALO_API_PORT=${HALO_API_PORT} \
     cloudpassage_halo_python_sdk \
     /source/codeclimate.sh

If you run it with no environment variables,
it will only run unit and style tests.  If you pass in `$HALO_API_KEY` and
`$HALO_API_SECRET_KEY`, it will run integration tests as well.  You can use
`$HALO_API_HOSTNAME` and `$HALO_API_PORT` to override the default settings
of `api.cloudpassage.com` and `443`, respectively.  These variables are
written into the `tests/config/portal.yaml.local` file using envsubst.
The exit code encountered in testing is what you'll get out when the container
exits.

For more detailed information, check out the .travis.yml file in the github
repository.
