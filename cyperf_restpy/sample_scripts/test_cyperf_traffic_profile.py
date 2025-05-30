import sys
import os

# Ensure the parent directory is in sys.path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyperf_scripts.cyperf_authorization import CyperfAuthorization
from cyperf_scripts.cyperf_traffic_profile import CyperfTrafficProfile
from cyperf_scripts.cyperf_applications import CyperfApplications
import urllib3; urllib3.disable_warnings()

def main():
    cyperf_client = CyperfAuthorization(controller_ip="3.141.193.119", 
                                        refresh_token=None, username="admin", 
                                        password="CyPerf&Keysight#1"
                                        ).get_cyperf_client()
    
    cyperf_traffic_profile = CyperfTrafficProfile(cyperf_client)
    #Get the configuration based on exact name match
    result = cyperf_traffic_profile.get_traffic_profile(session_id="appsec-d09bc450-8472-4e9c-9573-5859ae5ced57")
    result = cyperf_traffic_profile.get_traffic_profile_applications(session_id="appsec-d09bc450-8472-4e9c-9573-5859ae5ced57")
    print(result)


if __name__ == "__main__":
    main()