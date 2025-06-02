Usage Guide
===========

Basic Usage
----------

Here's a basic example of how to use the CyPerf REST Python Client:

.. code-block:: python

   from cyperf_scripts.cyperf_authorization import CyperfAuthorization
   
   # Initialize the client
   auth = CyperfAuthorization(
       controller_ip="your_controller_ip",
       refresh_token="your_refresh_token",
       password="cyperfpasswd"
   )
   
   # Get the API client
   client = auth.get_cyperf_client()


Sample Scripts
==============

The following sample scripts demonstrate how to use various features of the CyPerf REST Python Client. To avoid import issues, always run these scripts as a module from the project root:

.. code-block:: bash

   cd /Users/ashwjosh/Desktop/cyperf_restpy
   python -m cyperf_restpy.sample_scripts.<script_name>

Replace `<script_name>` with the script you want to run (e.g., `test_cyperf_applications`).

---

test_cyperf_applications.py
--------------------------
.. literalinclude:: ../cyperf_restpy/sample_scripts/test_cyperf_applications.py
   :language: python
   :caption: Sample: Application Management
   :lines: 1-35


test_cyperf_agents.py
--------------------
.. literalinclude:: ../cyperf_restpy/sample_scripts/test_cyperf_agents.py
   :language: python
   :caption: Sample: Agent Management
   :lines: 1-37


test_cyperf_statistics.py
------------------------
.. literalinclude:: ../cyperf_restpy/sample_scripts/test_cyperf_statistics.py
   :language: python
   :caption: Sample: Statistics Collection
   :lines: 1-32


test_cyperf_sessions.py
----------------------
.. literalinclude:: ../cyperf_restpy/sample_scripts/test_cyperf_sessions.py
   :language: python
   :caption: Sample: Session Management
   :lines: 1-77


test_cyperf_network_profile.py
-----------------------------
.. literalinclude:: ../cyperf_restpy/sample_scripts/test_cyperf_network_profile.py
   :language: python
   :caption: Sample: Network Profile Management
   :lines: 1-47


test_cyperf_objectives.py
------------------------
.. literalinclude:: ../cyperf_restpy/sample_scripts/test_cyperf_objectives.py
   :language: python
   :caption: Sample: Objectives Management
   :lines: 1-31


test_cyperf_traffic_profile.py
-----------------------------
.. literalinclude:: ../cyperf_restpy/sample_scripts/test_cyperf_traffic_profile.py
   :language: python
   :caption: Sample: Traffic Profile Management
   :lines: 1-26


test_cyperf_configurations.py
----------------------------
.. literalinclude:: ../cyperf_restpy/sample_scripts/test_cyperf_configurations.py
   :language: python
   :caption: Sample: Configuration Management
   :lines: 1-24


test_cyperf_tests.py
-------------------
.. literalinclude:: ../cyperf_restpy/sample_scripts/test_cyperf_tests.py
   :language: python
   :caption: Sample: Test Run Management
   :lines: 1-29


test_cyperf_reports.py
---------------------
.. literalinclude:: ../cyperf_restpy/sample_scripts/test_cyperf_reports.py
   :language: python
   :caption: Sample: Reports Management
   :lines: 1-33


test_cyperf_results.py
---------------------
.. literalinclude:: ../cyperf_restpy/sample_scripts/test_cyperf_results.py
   :language: python
   :caption: Sample: Results Management
   :lines: 1-37


test_cyperf_licensing.py
------------------------
.. literalinclude:: ../cyperf_restpy/sample_scripts/test_cyperf_licensing.py
   :language: python
   :caption: Sample: Licensing Management
   :lines: 1-37
