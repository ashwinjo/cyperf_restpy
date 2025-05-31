import sys
import os
from pprint import pprint

# Ensure the parent directory is in sys.path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyperf_scripts.cyperf_authorization import CyperfAuthorization
from cyperf_scripts.cyperf_sessions import CyperfSessions
from cyperf_scripts.cyperf_configurations import CyperfConfigurations
import urllib3; urllib3.disable_warnings()

def main():
    # Controller Authentication
    cyperf_client = CyperfAuthorization(controller_ip="3.141.193.119", 
                                        refresh_token=None, username="admin", 
                                        password="mypassword"
                                        ).get_cyperf_client()

    cyperf_sessions = CyperfSessions(cyperf_client)
    cyperf_configurations = CyperfConfigurations(cyperf_client)

    # Create a session Blank Config
    result = cyperf_sessions.create_session(config_name="Cyperf Empty Config", session_name="IntegrationTestSession")
    """
    {'session_id': 'appsec-e4d87134-8843-461c-b40e-ea07ca5d8c82', 'session_name': '178 CyPerf Empty Config'}
    """

    # Create a session existing config
    result = cyperf_sessions.create_session(config_name="AppMix-Users", 
                                            session_name="IntegrationTestSessionLoaded")
    """
    {'session_id': 'appsec-0e5cbcef-08b8-4c0c-a8fb-30a699310c64', 'session_name': '179 AppMix-Users'}
    """


    # Create a session from zip file
    result = cyperf_configurations.load_configuration_from_zip(configuration_file="/Users/ashwjosh/Downloads/SU-obj-APPMIX-with-10-apps-pdff.zip", 
                                                session_name="Ashwin-SU-obj-APPMIX-with-10-apps-pdff")
    """
    {'session_id': 'appsec-a46cd243-ef72-42a5-b567-1b846bf402d5', 
    'session_name': '181 SU-obj-APPMIX-with-10-apps-pdff (copy from May 29 21:15:49)'}
    """

    # Import configuration
    result = cyperf_configurations.import_configuration(cofig_file_path="/Users/ashwjosh/Downloads/SU-obj-APPMIX-with-10-apps-pdff.zip")
    print(result)


    # Show session
    cyperf_sessions.show_session(session_id="appsec-e4d87134-8843-461c-b40e-ea07ca5d8c82")
    """{'id': 'appsec-e4d87134-8843-461c-b40e-ea07ca5d8c82', 
    'name': '178 IntegrationTestSession', 
    'application': 'appsec', 
    'config_name': 'IntegrationTestSession', 
    'config_url': 'appsec-1698', 
    'index': 178, 
    'owner': '', 
    'owner_id': 'cc4d0f59-1045-4b41-9b8c-507bc1a61c86', 
    'state': 'CREATED'}
    """

    # Delete session
    cyperf_sessions.delete_session(session_id="appsec-e4d87134-8843-461c-b40e-ea07ca5d8c82")
    """
    {"message": f"Session appsec-e4d87134-8843-461c-b40e-ea07ca5d8c82 deleted successfully"}
    """

if __name__ == "__main__":
    main()






