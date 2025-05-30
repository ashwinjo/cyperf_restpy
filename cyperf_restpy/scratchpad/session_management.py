import cyperf
import json
from cyperf.configuration import Configuration
from cyperf.api_client import ApiClient
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.authorization_api import AuthorizationApi
from cyperf.api.brokers_api import BrokersApi
from cyperf.api.configurations_api import ConfigurationsApi
from cyperf.api.data_migration_api import DataMigrationApi
from cyperf.api.diagnostics_api import DiagnosticsApi
from cyperf.api.license_servers_api import LicenseServersApi
from cyperf.api.licensing_api import LicensingApi
from cyperf.api.notifications_api import NotificationsApi
from cyperf.api.reports_api import ReportsApi
from cyperf.api.statistics_api import StatisticsApi
from cyperf.api.test_operations_api import TestOperationsApi
from cyperf.api.test_results_api import TestResultsApi
from cyperf.api.utils_api import UtilsApi

config = Configuration(host="https://3.141.193.119",
                       refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzOTMyN2I4OC0xYzkyLTRlYjktYTI0My01MTE3NTczNTBlNjIifQ.eyJpYXQiOjE3NDg0NDI1MzQsImp0aSI6Ijg0MmRmMGM1LTk0NDAtNGI1OS1iNWFmLTA5MjYwZWRmZGUyOCIsImlzcyI6Imh0dHBzOi8vMy4xNDEuMTkzLjExOS9hdXRoL3JlYWxtcy9rZXlzaWdodCIsImF1ZCI6Imh0dHBzOi8vMy4xNDEuMTkzLjExOS9hdXRoL3JlYWxtcy9rZXlzaWdodCIsInN1YiI6ImNjNGQwZjU5LTEwNDUtNGI0MS05YjhjLTUwN2JjMWE2MWM4NiIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJjbHQtd2FwIiwibm9uY2UiOiI0ZjQyODM2Ny00ZGNiLTRlZTItOWZlYy1kZWZiODQxNDNkMWUiLCJzZXNzaW9uX3N0YXRlIjoiYWFjYTI5ZjgtMzA3Mi00YWM1LThmMjQtZTJlMzI1YWYwMDNmIiwic2NvcGUiOiJvcGVuaWQgZW1haWwgb2ZmbGluZV9hY2Nlc3MgcHJvZmlsZSIsInNpZCI6ImFhY2EyOWY4LTMwNzItNGFjNS04ZjI0LWUyZTMyNWFmMDAzZiJ9.s4hb7kx7sHjviwdFZuoxNK4gqWljbVByS0Lo1AfjwAc")
# if you don't have a valid HTTPS certificate for controller, uncomment this line
config.verify_ssl = False
CLIENT = ApiClient(config)



def get_all_sessions():
    sessions_api = SessionsApi(CLIENT)
    sessions = sessions_api.get_sessions()
    """application='appsec' config=None config_name='CyPerf AppMix' config_url='appsec-appmix' created=1747060168 data_model_url='/api/v2/sessions/appsec-ab11c5dc-c8dd-4054-b11c-97f636cb4d19/config' id='appsec-ab11c5dc-c8dd-4054-b11c-97f636cb4d19' index=151 last_visited=1747969261 links=[APILink(content_type=None, href='/api/v2/sessions/appsec-ab11c5dc-c8dd-4054-b11c-97f636cb4d19', method='GET', name=None, references_count=None, rel='self', type='self'), APILink(content_type=None, href='/api/v2/sessions/appsec-ab11c5dc-c8dd-4054-b11c-97f636cb4d19/$options', method='GET', name=None, references_count=None, rel='meta', type='meta'), APILink(content_type=None, href='/api/v2/sessions/appsec-ab11c5dc-c8dd-4054-b11c-97f636cb4d19/meta', method='GET', name='meta', references_count=None, rel='child', type='child'), APILink(content_type=None, href='/api/v2/sessions/appsec-ab11c5dc-c8dd-4054-b11c-97f636cb4d19/test', method='GET', name='test', references_count=None, rel='child', type='child'), APILink(content_type=None, href='/api/v2/sessions/appsec-ab11c5dc-c8dd-4054-b11c-97f636cb4d19/config', method='GET', name='config', references_count=None, rel='child', type='child')] meta=None name='151 CyPerf AppMix' owner='' owner_id='cc4d0f59-1045-4b41-9b8c-507bc1a61c86' pinned=False state='CREATED' test=None
    """
    return [{
            'id': s.id,
            'name': s.name, 
            'config_name': s.config_name,
            'config_url': s.config_url,
            'state': s.state,
            'created': s.created,
            'last_visited': s.last_visited,
            'index': s.index,
            'owner': s.owner,
            'owner_id': s.owner_id,
            'application': s.application
        } for s in sessions]

def get_session_by_id(session_id):
    """Get a session by its ID.

    Args:
        session_id (str): The ID of the session to get.

    Returns:
        dict: A dictionary containing the session ID and name.
    """
    sessions_api = cyperf.SessionsApi(CLIENT)
    session = sessions_api.get_session_by_id(session_id)
    print(session)
    return {
        'id': session.id,   
        'name': session.name,
        'application': session.application,
        'config_name': session.config_name,
        'config_url': session.config_url,
        'index': session.index,
        'owner': session.owner,
        'owner_id': session.owner_id,
        'state': session.state,
    }

def get_session_network_profile(session_id):
    """Get a session config by its ID.

    Args:
        session_id (str): The ID of the session to get.

    Returns:
        dict: A dictionary containing the session ID and config.
    """
    network_profiles = {}
    sessions_api = cyperf.SessionsApi(CLIENT)
    config = sessions_api.get_session_config(session_id, include = 'Config, TrafficProfiles, NetworkProfiles, AttackProfiles' )

    for item in config.config.network_profiles: 

        for idx, dutseg in enumerate(item.dut_network_segment):
            network_profiles.update({f"dut_network_segment_{idx+1}": dutseg.name})

        for idx, nwseg in enumerate(item.ip_network_segment):
            network_profiles.update({f"ip_network_segment_{idx+1}": nwseg.name})

    return network_profiles


def get_session_traffic_profile(session_id):
    """Get a session config by its ID.

    Args:
        session_id (str): The ID of the session to get.

    Returns:
        dict: A dictionary containing the session ID and config.
    """
    sessions_api = cyperf.SessionsApi(CLIENT)
    config = sessions_api.get_session_config(session_id, include = 'Config, TrafficProfiles, NetworkProfiles, AttackProfiles, ObjectivesAndTimeline' )
    for item in config.config.traffic_profiles: 
         # Name of the objective
        # primary_objective = item.objectives_and_timeline.primary_objective
        # primary_objective.type = cyperf.ObjectiveType.SIMULATED_USERS
        # primary_objective.unit = cyperf.ObjectiveUnit.EMPTY
        # primary_objective.update()

        for segment in item.objectives_and_timeline.primary_objective.timeline:
            if segment.enabled and (segment.segment_type == cyperf.SegmentType.STEADYSEGMENT or segment.segment_type == cyperf.SegmentType.NORMALSEGMENT):
                segment.duration        = 1550
                segment.objective_value = 1250
                segment.objective_unit  = cyperf.ObjectiveUnit.EMPTY
        item.objectives_and_timeline.primary_objective.update()
        
        # This update does not exist
        #import pdb; pdb.set_trace()
        
        #segmenttimeline.update()
    
       
       
def create_session(session_name, session_config):
    """Create a session.
    """

    sessions_api = cyperf.SessionsApi(CLIENT)
    application	= None                                          # str | The user-friendly name for the application that controls this session (optional)
    config_name	= None                                          # str | The display name of the configuration loaded in the session (optional)
    config_url = 'appsec-appmix'                                # str | The external URL of the configuration loaded in the session (optional)
    index = None                                                # int | The session's index (optional) (readonly)
    name = None                                                 # str | The user-visible name of the session (optional)
    owner = None                                                # str | The user-visible name of the session's owner (optional) (readonly)
    sessions = [cyperf.Session(application=application,
                                config_name=config_name,
                                configUrl=config_url,
                                index=index,
                                name=session_name,
                                owner=owner)]

    session = sessions_api.create_sessions(sessions)
    print("Session created.\n" + str(session[0]))
    return session

# print(get_all_sessions())
# print(get_session_by_id("appsec-f7aabfd8-c8d6-42c6-b981-7aa70be05df3"))
# print(create_session("test", "test"))

#network_profile = get_session_network_profile(session_id="appsec-f7aabfd8-c8d6-42c6-b981-7aa70be05df3")
traffic_profile = get_session_traffic_profile(session_id="appsec-bd410df1-67e6-41d3-8953-93f5a5fe27a5")




