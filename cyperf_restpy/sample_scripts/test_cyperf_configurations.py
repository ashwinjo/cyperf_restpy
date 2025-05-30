import sys
import os

# Ensure the parent directory is in sys.path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyperf_scripts.cyperf_authorization import CyperfAuthorization
from cyperf_scripts.cyperf_configurations import CyperfConfigurations

def main():
    cyperf_client = CyperfAuthorization(controller_ip="3.141.193.119", 
                                        refresh_token=None, username="admin", 
                                        password="CyPerf&Keysight#1"
                                        ).get_cyperf_client()
    
    cyperf_configurations = CyperfConfigurations(cyperf_client) 

    # Get the configuration based on exact name match
    result = cyperf_configurations.get_configuration(config_name="IntegrationTestSessionLoaded")
    result = cyperf_configurations.get_keyword_based_configuration_match(config_name="Chrome")
    print(result)

if __name__ == "__main__":
    main()