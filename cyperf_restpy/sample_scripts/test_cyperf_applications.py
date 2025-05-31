"""Test script for Cyperf Applications API."""

import sys
import os

# Ensure the parent directory is in sys.path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyperf_scripts.cyperf_authorization import CyperfAuthorization
from cyperf_scripts.cyperf_applications import CyperfApplications
import urllib3

urllib3.disable_warnings()

def main() -> None:
    """Main function to test Cyperf Applications API."""
    try:
        cyperf_client = CyperfAuthorization(
            controller_ip="3.141.193.119",
            refresh_token=None,
            username="admin",
            password="mypassword"
        ).get_cyperf_client()
        cyperf_applications = CyperfApplications(cyperf_client)
        result = cyperf_applications.get_all_application_for_session(
            session_id="appsec-d09bc450-8472-4e9c-9573-5859ae5ced57"
        )
        result = cyperf_applications.add_application_profile_to_session(
            session_id="appsec-d09bc450-8472-4e9c-9573-5859ae5ced57",
            application_profile_name="Shaktimaan"
        )
        result = cyperf_applications.add_application_to_application_profile(
            session_id="appsec-d09bc450-8472-4e9c-9573-5859ae5ced57",
            application_name="AI LLM over Generic HTTP",
            application_objective_weight=100
        )
        result = cyperf_applications.get_all_cyperf_applications_avaialble(
            keyword="AI"
        )
        result = cyperf_applications.add_multiple_applications_to_session(
            session_id="appsec-d09bc450-8472-4e9c-9573-5859ae5ced57",
            application_list=[],
            keyword="Zoom"
        )
        print(result)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()