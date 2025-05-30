import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.configurations_api import ConfigurationsApi

class CyperfTrafficProfile:
    def __init__(self, client: cyperf.ApiClient):
        self.client = client
        self.session_client = SessionsApi(self.client)
       

    def get_traffic_profile(self, session_id: str = None) -> dict:
        """
        Get the traffic profile for a given session.
        """
        session = self.session_client.get_session_by_id(session_id=session_id)
        traffic_profile = session.config.config.traffic_profiles[0]

        return {"traffic_profile_name": traffic_profile.name, 
                "traffic_profile_active": traffic_profile.active}
    
    def get_traffic_profile_applications(self, session_id: str = None) -> dict:
        """
        Get the applications for a given traffic profile.
        """
        session = self.session_client.get_session_by_id(session_id=session_id)
        traffic_profile = session.config.config.traffic_profiles[0]

        return {"number_of_apps": len(traffic_profile.applications), 
                "traffic_profile_applications": [app.name for app in traffic_profile.applications]}
