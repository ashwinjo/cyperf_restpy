CyPerf REST Python Client Documentation
=======================================

**cyperf_restpy** is a high-level Python wrapper library that simplifies interaction 
with Keysight CyPerf for network and application performance testing.

Built on top of the `official CyPerf API wrapper <https://github.com/Keysight/cyperf-api-wrapper>`_, 
this library groups low-level API calls into intuitive, task-oriented modules.

Quick Example
-------------

.. code-block:: python

   from cyperf_restpy.cyperf_scripts import CyperfAuthorization, CyperfSessions, CyperfAgents
   
   # Connect to CyPerf Controller
   client = CyperfAuthorization(
       controller_ip="10.0.0.1",
       username="admin",
       password="password"
   ).get_cyperf_client()
   
   # Create a test session
   session = CyperfSessions(client).create_session(config_name="My Test Config")
   
   # Assign agents
   CyperfAgents(client).assign_agents_to_network_elements(session_id=session["session_id"])

Features
--------

- 🔐 Simple authentication (token or username/password)
- 📦 Session lifecycle management
- 🤖 Agent discovery and assignment
- 📊 Application and attack profile configuration
- 🎯 Test objectives and timeline management
- 📈 Real-time statistics with pandas support
- 📄 PDF/CSV report generation

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   overview
   installation
   usage

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api_reference

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Links
=====

* `GitHub Repository <https://github.com/your-username/cyperf_restpy>`_
* `CyPerf Official SDK <https://github.com/Keysight/cyperf-api-wrapper>`_
* `Keysight CyPerf <https://www.keysight.com/us/en/products/network-test/network-test-hardware/cyperf.html>`_
