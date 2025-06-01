"""CyPerf traffic profile management utilities."""

import cyperf
from cyperf.api.sessions_api import SessionsApi
from typing import Optional, Dict, Any, Union

class CyperfTrafficProfile:
    """Handles traffic profile management for CyPerf sessions."""
    def __init__(self, client: cyperf.ApiClient) -> None:
        """
        Initializes the CyperfTrafficProfile class with a CyPerf API client.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.session_client = SessionsApi(self.client)

    def get_traffic_profile(self, session_id: Optional[str] = None) -> Union[Dict[str, Any], Exception]:
        """
        Gets the traffic profile for a given session.

        Args:
            session_id (str, optional): The ID of the session to query.

        Returns:
            dict: The traffic profile details.
            Exception: If the retrieval fails.
        """
        try:
            session = self.session_client.get_session_by_id(session_id=session_id)
            traffic_profile = session.config.config.traffic_profiles[0]
            return {"traffic_profile_name": traffic_profile.name, "traffic_profile_active": traffic_profile.active}
        except Exception as e:
            return Exception(f"Failed to get traffic profile: {str(e)}")

    def get_traffic_profile_applications(self, session_id: Optional[str] = None) -> Union[Dict[str, Any], Exception]:
        """
        Gets the applications for a given traffic profile.

        Args:
            session_id (str, optional): The ID of the session to query.

        Returns:
            dict: The applications in the traffic profile.
            Exception: If the retrieval fails.
        """
        try:
            session = self.session_client.get_session_by_id(session_id=session_id)
            traffic_profile = session.config.config.traffic_profiles[0]
            return {"number_of_apps": len(traffic_profile.applications), "traffic_profile_applications": [app.name for app in traffic_profile.applications]}
        except Exception as e:
            return Exception(f"Failed to get traffic profile applications: {str(e)}")
