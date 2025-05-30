import sys
import os

# Ensure the parent directory is in sys.path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyperf_scripts.cyperf_authorization import CyperfAuthorization
from cyperf_scripts.cyperf_sessions import CyperfSessions
from cyperf_scripts.cyperf_configurations import CyperfConfigurations
from cyperf_scripts.cyperf_network_profile import CyperfNetworkProfile
import urllib3; urllib3.disable_warnings()

def main():
    # Controller Authentication
    cyperf_client = CyperfAuthorization(controller_ip="3.141.193.119", 
                                        refresh_token=None, username="admin", 
                                        password="CyPerf&Keysight#1"
                                        ).get_cyperf_client()
    
    
    cyperf_network_profile = CyperfNetworkProfile(cyperf_client)

    result = cyperf_network_profile.get_dut_segments_details(session_id="appsec-f949b112-6059-42dd-9e4c-2cdd67739b75")
    print(result)

    result = cyperf_network_profile.get_ip_segments_details(session_id="appsec-f949b112-6059-42dd-9e4c-2cdd67739b75")
    print(result)

    result = cyperf_network_profile.add_ip_network_segment(session_id="appsec-f949b112-6059-42dd-9e4c-2cdd67739b75", 
                                                           ip_segment_name="IP Network 26", 
                                                           ip_segment_id="57", 
                                                           dut_connection_id="1")
    print(result)
    cyperf_network_profile.add_dut_network_segment(session_id="appsec-f949b112-6059-42dd-9e4c-2cdd67739b75", 
                                                    dut_segment_name="DUT Network 71", 
                                                    dut_segment_id="71")

    result = cyperf_network_profile.get_network_profiles_details(session_id="appsec-f949b112-6059-42dd-9e4c-2cdd67739b75")
    print(result)
    



if __name__ == "__main__":
    main()

