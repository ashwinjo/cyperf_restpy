# CyPerf REST Python Client (`cyperf_restpy`)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-level Python wrapper library that simplifies interaction with **Keysight CyPerf** for network and application performance testing. Built on top of the [official CyPerf API wrapper](https://github.com/Keysight/cyperf-api-wrapper), this library groups low-level API calls into intuitive, task-oriented modules.

---

## Why This Wrapper?

The official [CyPerf API wrapper](https://github.com/Keysight/cyperf-api-wrapper) is auto-generated from OpenAPI specifications—powerful but verbose. Running a simple test requires understanding dozens of API calls, model objects, and their relationships.

**`cyperf_restpy` addresses this by:**

| Challenge with Raw SDK | Solution in `cyperf_restpy` |
|------------------------|----------------------------|
| Multiple API calls to perform one logical operation | Single method calls that orchestrate complex workflows |
| Need to understand internal model relationships | Abstracted into domain-specific classes (Sessions, Agents, Applications, etc.) |
| Boilerplate code for common tasks | Pre-built utilities for authentication, configuration, and test execution |
| Scattered error handling | Consistent return types with unified exception handling |
| Learning curve for new users | Intuitive, Pythonic interface with comprehensive docstrings |

### Before vs After

**Without `cyperf_restpy` (raw SDK):**
```python
# ~50 lines to create a session, add an application, assign agents, and start test
config = cyperf.Configuration(host=f"https://{ip}", refresh_token=token)
config.verify_ssl = False
client = cyperf.ApiClient(config)
session_api = cyperf.SessionsApi(client)
config_api = cyperf.ConfigurationsApi(client)
# ... dozens more lines
```

**With `cyperf_restpy`:**
```python
from cyperf_restpy.cyperf_scripts import CyperfAuthorization, CyperfSessions, CyperfAgents

client = CyperfAuthorization(controller_ip="10.0.0.1", username="admin", password="pass").get_cyperf_client()
session = CyperfSessions(client).create_session(config_name="My Config")
CyperfAgents(client).assign_agents_to_network_elements(session_id=session["session_id"])
```

---

## Features

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

---

## Installation

### Prerequisites

- Python 3.8+
- Access to a CyPerf Controller

### Install from source

```bash
git clone https://github.com/your-username/cyperf_restpy.git
cd cyperf_restpy
pip install -r requirements.txt
pip install -e .
```

### Dependencies

```
cyperf          # Official CyPerf SDK
pandas          # Statistics visualization
sphinx          # Documentation generation
sphinx-rtd-theme # Read the Docs theme
```

---

## Quick Start

### 1. Authentication

```python
from cyperf_restpy.cyperf_scripts.cyperf_authorization import CyperfAuthorization

# Option A: Username/Password
client = CyperfAuthorization(
    controller_ip="10.0.0.1",
    username="admin",
    password="your_password"
).get_cyperf_client()

# Option B: Refresh Token
client = CyperfAuthorization(
    controller_ip="10.0.0.1",
    refresh_token="eyJhbGciOiJIUzI1NiIs..."
).get_cyperf_client()
```

### 2. Create a Test Session

```python
from cyperf_restpy.cyperf_scripts.cyperf_sessions import CyperfSessions

sessions = CyperfSessions(client)

# Create from existing configuration
session = sessions.create_session(
    config_name="HTTP Performance Test",
    session_name="My Test Run"
)
print(f"Session ID: {session['session_id']}")

# Or load from a zip file
session = sessions.load_configuration_from_zip(
    configuration_file="/path/to/config.zip",
    session_name="Imported Test"
)
```

### 3. Assign Agents

```python
from cyperf_restpy.cyperf_scripts.cyperf_agents import CyperfAgents

agents = CyperfAgents(client)

# Discover available agents
available = agents.get_available_agents()
print(available)
# [{'id': 'abc123', 'ip': '172.16.0.10', 'hostname': 'agent-1', 'status': 'IDLE'}, ...]

# Assign agents to network segments
agent_map = {
    "IP Network 1": [available[0]['id'], available[0]['ip']],
    "IP Network 2": [available[1]['id'], available[1]['ip']]
}
agents.assign_agents_to_network_elements(
    session_id=session['session_id'],
    agent_map=agent_map
)
```

### 4. Configure Test Objectives

```python
from cyperf_restpy.cyperf_scripts.cyperf_objectives import CyperfObjectives

objectives = CyperfObjectives(client)

# Set primary objective
objectives.set_primary_objective_goals(
    session_id=session['session_id'],
    primary_object_name='SIMULATED_USERS',  # or 'THROUGHPUT', 'CONNECTIONS_PER_SECOND'
    primary_objective_duration=60,
    primary_objective_goal=1000
)
```

### 5. Run Test and Collect Statistics

```python
from cyperf_restpy.cyperf_scripts.cyperf_test_runs import CyperfTestRuns
from cyperf_restpy.cyperf_scripts.cyperf_statistics import CyperfStatistics

# Start the test
test_runner = CyperfTestRuns(client)
test_runner.start_test_run(session_id=session['session_id'])

# Collect statistics
import time
time.sleep(30)  # Wait for data collection

stats = CyperfStatistics(client)
processed_stats = stats.collect_test_run_stats(session_id=session['session_id'])

# View as pandas DataFrame
df = stats.view_stats(
    session_id=session['session_id'],
    processed_stats=processed_stats,
    stat_name='client-throughput'
)
print(df)

# Stop the test
test_runner.stop_test_run(session_id=session['session_id'])
```

### 6. Generate Reports

```python
from cyperf_restpy.cyperf_scripts.cyperf_reports import CyperfReports

reports = CyperfReports(client)

# Download PDF report
pdf_result = reports.download_pdf_report(session_id=session['session_id'])
print(f"Report saved to: {pdf_result['saved_file_location']}")

# Download CSV report
csv_result = reports.download_csv_report(session_id=session['session_id'])
```

---

## Module Reference

| Module | Class | Description |
|--------|-------|-------------|
| `cyperf_authorization` | `CyperfAuthorization` | Authentication and API client creation |
| `cyperf_sessions` | `CyperfSessions` | Session lifecycle management (create, delete, save, export/import) |
| `cyperf_agents` | `CyperfAgents` | Agent discovery and assignment to network segments |
| `cyperf_applications` | `CyperfApplications` | Application profile and traffic configuration |
| `cyperf_attacks` | `CyperfAttacks` | Attack profile management for security testing |
| `cyperf_objectives` | `CyperfObjectives` | Primary/secondary test objective configuration |
| `cyperf_network_profile` | `CyperfNetworkProfile` | IP segments, DUT networks, and topology |
| `cyperf_traffic_profile` | `CyperfTrafficProfile` | Traffic profile queries and configuration |
| `cyperf_configurations` | `CyperfConfigurations` | Configuration save, export, import, and search |
| `cyperf_test_runs` | `CyperfTestRuns` | Test execution control (start, stop, abort) |
| `cyperf_statistics` | `CyperfStatistics` | Real-time statistics collection and visualization |
| `cyperf_results` | `CyperfResults` | Test result generation and retrieval |
| `cyperf_reports` | `CyperfReports` | PDF/CSV report generation |
| `cyperf_licensing` | `CyperfLicensing` | License server management and activation |

---

## Project Structure

```
cyperf_restpy/
├── cyperf_restpy/
│   ├── cyperf_scripts/           # Core wrapper modules
│   │   ├── cyperf_authorization.py
│   │   ├── cyperf_sessions.py
│   │   ├── cyperf_agents.py
│   │   ├── cyperf_applications.py
│   │   ├── cyperf_attacks.py
│   │   ├── cyperf_objectives.py
│   │   ├── cyperf_network_profile.py
│   │   ├── cyperf_traffic_profile.py
│   │   ├── cyperf_configurations.py
│   │   ├── cyperf_test_runs.py
│   │   ├── cyperf_statistics.py
│   │   ├── cyperf_results.py
│   │   ├── cyperf_reports.py
│   │   └── cyperf_licensing.py
│   ├── scripts_in_action/        # Example/test scripts
│   └── tests/                    # Unit tests
├── docs/                         # Sphinx documentation
│   ├── conf.py
│   ├── index.rst
│   └── *.rst                     # API reference docs
├── requirements.txt
├── setup.py
└── README.md
```

---

## Documentation

Full API documentation is available via Sphinx and is compatible with [Read the Docs](https://readthedocs.org/).

### Build Documentation Locally

```bash
cd docs
pip install sphinx sphinx-rtd-theme
make html
```

Open `docs/_build/html/index.html` in your browser.

### Hosted Documentation

*Coming soon on Read the Docs*

---

## Available Statistics

When collecting test statistics, the following stat names are available:

| Category | Stat Name | Description |
|----------|-----------|-------------|
| **Throughput** | `client-throughput` | Overall client throughput |
| | `server-throughput` | Overall server throughput |
| | `client-l23-throughput` | Layer 2/3 client throughput |
| | `server-l23-throughput` | Layer 2/3 server throughput |
| | `client-application-throughput` | Per-application throughput |
| **Connections** | `client-application-connection-rate` | Connection rate metrics |
| | `client-application-concurrent-connections` | Concurrent connection counts |
| **HTTP** | `http-requests-rate` | Overall HTTP request rate |
| | `http-requests-rate-per-app` | Per-application HTTP rate |
| | `client-http-statistics` | Client-side HTTP stats |
| | `server-http-statistics` | Server-side HTTP stats |
| **Latency** | `client-latency` | Client-side latency |
| | `client-traffic-profile-latency` | Latency profile metrics |
| **Agents** | `agent-metrics-cpu` | Agent CPU utilization |
| | `agent-metrics-memory` | Agent memory usage |
| | `agent-metrics-network` | Agent network I/O |

---

## Error Handling

All methods return either:
- A **dict/list** on success with relevant data
- An **Exception object** on failure (not raised, returned)

```python
result = sessions.create_session(config_name="NonExistent")

if isinstance(result, Exception):
    print(f"Error: {result}")
else:
    print(f"Success: {result}")
```

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Related Projects

- [CyPerf API Wrapper (Official SDK)](https://github.com/Keysight/cyperf-api-wrapper) – Auto-generated Python client from OpenAPI spec
- [Keysight CyPerf](https://www.keysight.com/us/en/products/network-test/network-test-hardware/cyperf.html) – Official product page

---

## Support

For issues related to:
- **This wrapper library**: Open an issue in this repository
- **CyPerf SDK/API**: Contact [support@keysight.com](mailto:support@keysight.com)
