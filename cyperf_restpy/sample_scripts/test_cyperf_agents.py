"""Test script for Cyperf Agents API."""

import sys
import os

# Ensure the parent directory is in sys.path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyperf_scripts.cyperf_authorization import CyperfAuthorization
from cyperf_scripts.cyperf_agents import CyperfAgents
from cyperf_scripts.cyperf_network_profile import CyperfNetworkProfile
import urllib3

urllib3.disable_warnings()

def main() -> None:
    """Main function to test Cyperf Agents API."""
    try:
        cyperf_client = CyperfAuthorization(
            controller_ip="3.141.193.119",
            refresh_token=None,
            username="admin",
            password="mypassword"
        ).get_cyperf_client()
        cyperf_agents = CyperfAgents(cyperf_client)
        cyperf_network_profile = CyperfNetworkProfile(cyperf_client)
        result = cyperf_network_profile.get_ip_segments_details(
            session_id="appsec-d09bc450-8472-4e9c-9573-5859ae5ced57"
        )
        print(result)
        result = cyperf_agents.get_available_agents()
        print(result)
        agent_map = {
            "IP Network 1": ["2bd2daa0-cac6-4191-9a8b-2d2b3f646d1e", "172.16.2.11"],
            "IP Network 2": ["f1915655-6678-4d96-a0b7-da3c0c6dd95c", "172.16.0.3"]
        }
        result = cyperf_agents.assign_agents_to_network_elements(
            session_id="appsec-d09bc450-8472-4e9c-9573-5859ae5ced57",
            agent_map=agent_map
        )
        result = cyperf_agents.unassign_all_agents_for_session(
            session_id="appsec-d09bc450-8472-4e9c-9573-5859ae5ced57"
        )
        print(result)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()