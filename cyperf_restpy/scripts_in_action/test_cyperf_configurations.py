"""Test script for Cyperf Configurations API."""

from cyperf_scripts.cyperf_authorization import CyperfAuthorization
from cyperf_scripts.cyperf_configurations import CyperfConfigurations


def main() -> None:
    """Main function to test Cyperf Configurations API."""
    try:
        cyperf_client = CyperfAuthorization(
            controller_ip="3.141.193.119",
            refresh_token=None,
            username="admin",
            password="mypassword"
        ).get_cyperf_client()
        cyperf_configurations = CyperfConfigurations(cyperf_client)
        # Get the configuration based on exact name match
        result = cyperf_configurations.get_configuration(config_name="IntegrationTestSessionLoaded")
        result = cyperf_configurations.get_keyword_based_configuration_match(config_name="Chrome")
        print(result)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()