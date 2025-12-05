Overview
========

Introduction
------------

**cyperf_restpy** is a high-level Python wrapper library that simplifies interaction with 
Keysight CyPerf for network and application performance testing. Built on top of the 
`official CyPerf API wrapper <https://github.com/Keysight/cyperf-api-wrapper>`_, this library 
groups low-level API calls into intuitive, task-oriented modules.

What is CyPerf?
---------------

CyPerf is a Keysight product—an agent-based network application and security test solution 
that meticulously recreates realistic workloads across diverse physical and cloud environments 
to deliver insights into:

- **End-user Quality of Experience (QoE)**
- **Security posture**
- **Performance bottlenecks of distributed networks**

A licensed CyPerf product is compatible with multiple environments:

- AWS
- Azure
- GCP
- Kubernetes
- Containers

Why This Wrapper?
-----------------

The official `cyperf-api-wrapper <https://github.com/Keysight/cyperf-api-wrapper>`_ is 
auto-generated from OpenAPI specifications—powerful but verbose. Running a simple test 
requires understanding dozens of API calls, model objects, and their relationships.

**cyperf_restpy** addresses this by:

+----------------------------------------+----------------------------------------------+
| Challenge with Raw SDK                 | Solution in cyperf_restpy                    |
+========================================+==============================================+
| Multiple API calls for one operation   | Single method calls that orchestrate         |
|                                        | complex workflows                            |
+----------------------------------------+----------------------------------------------+
| Need to understand model relationships | Abstracted into domain-specific classes      |
+----------------------------------------+----------------------------------------------+
| Boilerplate code for common tasks      | Pre-built utilities for auth, config, tests  |
+----------------------------------------+----------------------------------------------+
| Scattered error handling               | Consistent return types with unified errors  |
+----------------------------------------+----------------------------------------------+
| Steep learning curve                   | Intuitive, Pythonic interface with docstrings|
+----------------------------------------+----------------------------------------------+

Architecture
------------

The library is organized into modular components, each handling a specific domain:

.. code-block:: text

   cyperf_restpy/
   ├── cyperf_scripts/
   │   ├── cyperf_authorization.py   # Authentication & client setup
   │   ├── cyperf_sessions.py        # Session lifecycle management
   │   ├── cyperf_agents.py          # Agent discovery & assignment
   │   ├── cyperf_applications.py    # Application profile management
   │   ├── cyperf_attacks.py         # Security/attack testing
   │   ├── cyperf_objectives.py      # Test objectives configuration
   │   ├── cyperf_network_profile.py # Network topology management
   │   ├── cyperf_traffic_profile.py # Traffic profile configuration
   │   ├── cyperf_configurations.py  # Config save/export/import
   │   ├── cyperf_test_runs.py       # Test execution control
   │   ├── cyperf_statistics.py      # Real-time stats collection
   │   ├── cyperf_results.py         # Test result retrieval
   │   ├── cyperf_reports.py         # PDF/CSV report generation
   │   └── cyperf_licensing.py       # License management

Key Features
------------

- 🔐 **Simple Authentication** – Token-based or username/password auth with a single class
- 📦 **Session Management** – Create, load, save, export, and delete test sessions
- 🤖 **Agent Management** – Discover, assign, and unassign test agents
- 📊 **Application Profiles** – Add and configure application traffic profiles
- ⚔️ **Attack Profiles** – Configure security/attack testing scenarios
- 🎯 **Objectives & Timelines** – Set primary/secondary test objectives
- 🌐 **Network Profiles** – Manage IP segments, DUT networks, and topology
- 📈 **Statistics Collection** – Real-time stats with pandas DataFrame support
- 📄 **Reports** – Generate and download PDF/CSV test reports
- 🔑 **Licensing** – Manage license servers and activations

Related Resources
-----------------

- `CyPerf API Wrapper (Official SDK) <https://github.com/Keysight/cyperf-api-wrapper>`_ – Auto-generated Python client from OpenAPI spec
- `Keysight CyPerf Product Page <https://www.keysight.com/us/en/products/network-test/network-test-hardware/cyperf.html>`_ – Official product documentation
- Swagger API Documentation – Available from your CyPerf Controller at ``https://<controller-ip>/api/v2``
