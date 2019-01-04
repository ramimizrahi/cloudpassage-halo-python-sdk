Getting Started
===============

.. toctree::

Usage abstract:

Here's the premise: you store your session configuration information (API
credentials, proxy settings, etc) in the cloudpassage.HaloSession object.
This object gets passed into the various class methods which allow you
to interact with the CloudPassage Halo API.

Practical example:
We'll print a list of all servers in our account:

::

  import cloudpassage

  api_key = MY_HALO_API_KEY
  api_secret = MY_API_SECRET
  session = cloudpassage.HaloSession(api_key, api_secret)
  server = cloudpassage.Server(session)
  list_of_servers = server.list_all()
  for s in list_of_servers:
      print("ID: {}   Name: {}".format(s["id"], s["hostname"]))
