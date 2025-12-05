Usage Guide
===========

This guide provides comprehensive examples of how to use the CyPerf REST Python Client
for common testing workflows.

Authentication
--------------

The library supports two authentication methods:

**Username/Password Authentication:**

.. code-block:: python

   from cyperf_restpy.cyperf_scripts.cyperf_authorization import CyperfAuthorization
   
   auth = CyperfAuthorization(
       controller_ip="10.0.0.1",
       username="admin",
       password="your_password"
   )
   client = auth.get_cyperf_client()

**Refresh Token Authentication:**

.. code-block:: python

   from cyperf_restpy.cyperf_scripts.cyperf_authorization import CyperfAuthorization
   
   auth = CyperfAuthorization(
       controller_ip="10.0.0.1",
       refresh_token="eyJhbGciOiJIUzI1NiIs..."
   )
   client = auth.get_cyperf_client()

.. note::
   Refresh tokens can be obtained from the CyPerf UI under User Settings > API Tokens.

Complete Test Workflow
----------------------

Here's a complete example showing how to run a test from start to finish:

.. code-block:: python

   from cyperf_restpy.cyperf_scripts.cyperf_authorization import CyperfAuthorization
   from cyperf_restpy.cyperf_scripts.cyperf_sessions import CyperfSessions
   from cyperf_restpy.cyperf_scripts.cyperf_agents import CyperfAgents
   from cyperf_restpy.cyperf_scripts.cyperf_applications import CyperfApplications
   from cyperf_restpy.cyperf_scripts.cyperf_objectives import CyperfObjectives
   from cyperf_restpy.cyperf_scripts.cyperf_test_runs import CyperfTestRuns
   from cyperf_restpy.cyperf_scripts.cyperf_statistics import CyperfStatistics
   from cyperf_restpy.cyperf_scripts.cyperf_reports import CyperfReports
   import time
   import urllib3
   
   urllib3.disable_warnings()
   
   # 1. Authenticate
   client = CyperfAuthorization(
       controller_ip="10.0.0.1",
       username="admin",
       password="password"
   ).get_cyperf_client()
   
   # 2. Create session from existing configuration
   sessions = CyperfSessions(client)
   session = sessions.create_session(
       config_name="HTTP Performance Test",
       session_name="Automated Test Run"
   )
   session_id = session['session_id']
   print(f"Created session: {session_id}")
   
   # 3. Discover and assign agents
   agents = CyperfAgents(client)
   available_agents = agents.get_available_agents()
   
   agent_map = {
       "IP Network 1": [available_agents[0]['id'], available_agents[0]['ip']],
       "IP Network 2": [available_agents[1]['id'], available_agents[1]['ip']]
   }
   agents.assign_agents_to_network_elements(
       session_id=session_id,
       agent_map=agent_map
   )
   
   # 4. Configure test objectives
   objectives = CyperfObjectives(client)
   objectives.set_primary_objective_goals(
       session_id=session_id,
       primary_object_name='SIMULATED_USERS',
       primary_objective_duration=60,
       primary_objective_goal=100
   )
   
   # 5. Run the test
   test_runner = CyperfTestRuns(client)
   test_runner.start_test_run(session_id=session_id)
   
   # 6. Wait and collect statistics
   time.sleep(60)
   
   stats = CyperfStatistics(client)
   processed_stats = stats.collect_test_run_stats(session_id=session_id)
   df = stats.view_stats(
       processed_stats=processed_stats,
       stat_name='client-throughput'
   )
   print(df)
   
   # 7. Stop test and generate reports
   test_runner.stop_test_run(session_id=session_id)
   
   reports = CyperfReports(client)
   pdf_result = reports.download_pdf_report(session_id=session_id)
   print(f"Report saved: {pdf_result['saved_file_location']}")
   
   # 8. Cleanup (optional)
   sessions.delete_session(session_id=session_id)

Session Management
------------------

**Create a session from existing configuration:**

.. code-block:: python

   sessions = CyperfSessions(client)
   session = sessions.create_session(config_name="My Config")

**Load configuration from a ZIP file:**

.. code-block:: python

   session = sessions.load_configuration_from_zip(
       configuration_file="/path/to/config.zip",
       session_name="Imported Test"
   )

**List all sessions:**

.. code-block:: python

   all_sessions = sessions.get_all_sessions()
   for s in all_sessions:
       print(f"{s['id']}: {s['name']}")

**Save configuration:**

.. code-block:: python

   sessions.save_configuration(
       session_id=session_id,
       save_config_name="Updated Config"
   )

Agent Management
----------------

**Discover available agents:**

.. code-block:: python

   agents = CyperfAgents(client)
   available = agents.get_available_agents()
   
   for agent in available:
       print(f"Agent: {agent['hostname']} ({agent['ip']}) - Status: {agent['status']}")

**Assign agents to network segments:**

.. code-block:: python

   agent_map = {
       "IP Network 1": ["agent-uuid-1", "172.16.0.10"],
       "IP Network 2": ["agent-uuid-2", "172.16.0.11"]
   }
   agents.assign_agents_to_network_elements(
       session_id=session_id,
       agent_map=agent_map
   )

**Unassign all agents:**

.. code-block:: python

   agents.unassign_all_agents_for_session(session_id=session_id)

Application Management
----------------------

**List available applications:**

.. code-block:: python

   apps = CyperfApplications(client)
   available_apps = apps.get_all_cyperf_applications_avaialble()
   
   # Filter by keyword
   http_apps = apps.get_all_cyperf_applications_avaialble(keyword="HTTP")

**Add application to session:**

.. code-block:: python

   apps.add_application_to_application_profile(
       session_id=session_id,
       application_name="AI LLM over Generic HTTP",
       application_objective_weight=100
   )

**Add multiple applications:**

.. code-block:: python

   apps.add_multiple_applications_to_session(
       session_id=session_id,
       keyword="HTTP"  # Adds all HTTP-related applications
   )

Test Objectives
---------------

**Set primary objective:**

.. code-block:: python

   objectives = CyperfObjectives(client)
   
   # Available objective types:
   # - SIMULATED_USERS
   # - THROUGHPUT
   # - CONNECTIONS_PER_SECOND
   # - CONCURRENT_CONNECTIONS
   
   objectives.set_primary_objective_goals(
       session_id=session_id,
       primary_object_name='THROUGHPUT',
       primary_objective_duration=120,  # seconds
       primary_objective_goal=1000000000  # 1 Gbps
   )

**Get current objectives:**

.. code-block:: python

   current = objectives.get_all_primary_objectives_goals(session_id=session_id)
   print(current)

Statistics Collection
---------------------

**Collect all statistics:**

.. code-block:: python

   stats = CyperfStatistics(client)
   processed_stats = stats.collect_test_run_stats(session_id=session_id)

**View available statistics:**

.. code-block:: python

   available_stats = stats.show_available_stats(session_id=session_id)
   print(available_stats)

**View specific statistic as DataFrame:**

.. code-block:: python

   df = stats.view_stats(
       processed_stats=processed_stats,
       stat_name='client-throughput'
   )
   print(df.tail(10))

Common Statistics
^^^^^^^^^^^^^^^^^

+------------------------------------------+----------------------------------+
| Stat Name                                | Description                      |
+==========================================+==================================+
| ``client-throughput``                    | Overall client throughput        |
+------------------------------------------+----------------------------------+
| ``server-throughput``                    | Overall server throughput        |
+------------------------------------------+----------------------------------+
| ``client-application-connection-rate``   | Connection rate per application  |
+------------------------------------------+----------------------------------+
| ``http-requests-rate``                   | HTTP requests per second         |
+------------------------------------------+----------------------------------+
| ``client-latency``                       | Client-side latency metrics      |
+------------------------------------------+----------------------------------+
| ``agent-metrics-cpu``                    | Agent CPU utilization            |
+------------------------------------------+----------------------------------+

Error Handling
--------------

All methods return either a **dict/list** on success or an **Exception object** on failure:

.. code-block:: python

   result = sessions.create_session(config_name="NonExistent")
   
   if isinstance(result, Exception):
       print(f"Error: {result}")
   else:
       print(f"Success: {result}")

Running Sample Scripts
----------------------

Sample scripts are located in ``cyperf_restpy/scripts_in_action/``. Run them as modules:

.. code-block:: bash

   cd /path/to/cyperf_restpy
   python -m cyperf_restpy.scripts_in_action.test_cyperf_agents

Available Sample Scripts
^^^^^^^^^^^^^^^^^^^^^^^^

* ``test_cyperf_agents.py`` – Agent discovery and assignment
* ``test_cyperf_applications.py`` – Application management
* ``test_cyperf_configurations.py`` – Configuration management
* ``test_cyperf_licensing.py`` – License management
* ``test_cyperf_network_profile.py`` – Network profile configuration
* ``test_cyperf_objectives.py`` – Test objectives
* ``test_cyperf_reports.py`` – Report generation
* ``test_cyperf_results.py`` – Test results
* ``test_cyperf_sessions.py`` – Session management
* ``test_cyperf_statistics.py`` – Statistics collection
* ``test_cyperf_tests.py`` – Test execution
* ``test_cyperf_traffic_profile.py`` – Traffic profile management
