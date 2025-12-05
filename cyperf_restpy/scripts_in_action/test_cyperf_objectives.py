"""Test script for Cyperf Objectives API."""

import sys
import os

# Ensure the parent directory is in sys.path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyperf_scripts.cyperf_sessions import CyperfSessions
from cyperf_scripts.cyperf_objectives import CyperfObjectives
from cyperf_scripts.cyperf_authorization import CyperfAuthorization
import urllib3

urllib3.disable_warnings()

def main() -> None:
    """Main function to test Cyperf Objectives API."""
    try:
        cyperf_client = CyperfAuthorization(
            controller_ip="3.141.193.119",
            refresh_token=None,
            username="admin",
            password="mypassword"
        ).get_cyperf_client()
        cyperf_objectives = CyperfObjectives(cyperf_client)
        result = cyperf_objectives.get_all_primary_objectives_goals(
            session_id="appsec-d09bc450-8472-4e9c-9573-5859ae5ced57"
        )
        result = cyperf_objectives.get_all_secondary_objectives_goals(
            session_id="appsec-d09bc450-8472-4e9c-9573-5859ae5ced57"
        )
        result = cyperf_objectives.set_primary_objective_goals(
            session_id="appsec-d09bc450-8472-4e9c-9573-5859ae5ced57",
            primary_object_name="CONNECTIONS_PER_SECOND",
            primary_objective_duration=1234,
            primary_objective_goal=1234
        )
        print(result)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()