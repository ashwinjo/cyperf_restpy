"""Test script for Cyperf Results API."""

import sys
import os

# Ensure the parent directory is in sys.path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyperf_scripts.cyperf_authorization import CyperfAuthorization
from cyperf_scripts.cyperf_results import CyperfResults
import urllib3

urllib3.disable_warnings()

def main() -> None:
    """Main function to test Cyperf Results API."""
    try:
        cyperf_client = CyperfAuthorization(
            controller_ip="3.141.193.119",
            refresh_token=None,
            username="admin",
            password="CyPerf&Keysight#1"
        ).get_cyperf_client()

        cyperf_results = CyperfResults(cyperf_client)
        result = cyperf_results.start_result_generate_all(
            session_id="appsec-9d25e7bb-f165-495e-82b2-278d6c1573d2"
        )
        print(result)
        result = cyperf_results.start_result_generate_results(
            session_id="appsec-9d25e7bb-f165-495e-82b2-278d6c1573d2"
        )
        print(result)

        result = cyperf_results.load_all_results(
            session_id="appsec-9d25e7bb-f165-495e-82b2-278d6c1573d2"
        )
        print(result)

        result = cyperf_results.show_all_available_results()
        print(result)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()