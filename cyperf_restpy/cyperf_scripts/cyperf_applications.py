"""
CyPerf application profile and assignment utilities.

This module provides the CyperfApplications class for managing application profiles and assignments in CyPerf sessions.
"""

import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.application_resources_api import ApplicationResourcesApi
from typing import Optional, List, Dict, Any, Tuple, Union

class CyperfApplications:
    """
    Manages application profiles and application assignment in CyPerf sessions.

    Args:
        client (cyperf.ApiClient): The CyPerf API client instance.
    """
    def __init__(self, client: cyperf.ApiClient) -> None:
        """
        Initializes the CyperfApplications class with a CyPerf API client.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.session_client = SessionsApi(self.client)

    def add_application_profile_to_session(
        self,
        session_id: Optional[str] = None,
        application_profile_name: str = 'Application Profile'
    ) -> Union[Dict[str, str], Exception]:
        """
        Adds an application profile to a session's traffic profiles.

        Args:
            session_id (str, optional): The ID of the session to add the application profile to.
            application_profile_name (str, optional): The name of the application profile.

        Returns:
            dict: A message indicating the result of the operation.
        """
        try:
            session = self.session_client.get_session_by_id(session_id=session_id)
            traffic_profiles = session.config.config.traffic_profiles
            traffic_profiles.append(cyperf.ApplicationProfile(Name=application_profile_name))
            traffic_profiles.update()
            return {"message": f"Application profile added to session {session_id} - {session.name}"}
        except Exception as e:
            return Exception(f"Failed to add application profile: {str(e)}")

    def add_application_to_application_profile(
        self,
        session_id: Optional[str] = None,
        application_name: str = 'AI LLM over Generic HTTP',
        application_objective_weight: int = 100
    ) -> Union[Dict[str, str], Exception]:
        """
        Adds an application to the first application profile in a session and sets its objective weight.

        Args:
            session_id (str, optional): The ID of the session to modify.
            application_name (str, optional): The name of the application to add.
            application_objective_weight (int, optional): The objective weight for the application.

        Returns:
            dict: A message indicating the result of the operation.
        """
        try:
            application_resources_api = ApplicationResourcesApi(self.client)
            take = 1
            skip = 0
            search_col = "Name"
            search_val = application_name
            sort = 'Name:asc'
            api_application_resources_response = application_resources_api.get_resources_apps(
                take=take,
                skip=skip,
                search_col=search_col,
                search_val=search_val,
                filter_mode=None,
                sort=sort
            )
            app_id = api_application_resources_response.data[0].id
            external_resource_info = [cyperf.ExternalResourceInfo(externalResourceURL=app_id)]
            config = self.session_client.get_session_config(session_id=session_id, include='Config, TrafficProfiles, ApplicationProfiles, Applications')
            api_session_response = self.session_client.start_config_add_applications(session_id, traffic_profile_id='1', external_resource_info=external_resource_info)
            api_session_response.await_completion()
            for app in config.config.traffic_profiles[0].applications:
                if app.name == application_name:
                    app.objective_weight = application_objective_weight
                    app.update()
            return {"message": f"Applications {application_name} added successfully. with weight {application_objective_weight}"}
        except Exception as e:
            return Exception(f"Failed to add application to profile: {str(e)}")

    def get_all_application_for_session(
        self,
        session_id: Optional[str] = None
    ) -> Union[List[str], Exception]:
        """
        Retrieves all application names for the first application profile in a session.

        Args:
            session_id (str, optional): The ID of the session to query.

        Returns:
            list: A list of application names in the session.
        """
        try:
            session = self.session_client.get_session_by_id(session_id=session_id)
            return [app.name for app in session.config.config.traffic_profiles[0].applications]
        except Exception as e:
            return Exception(f"Failed to get applications for session: {str(e)}")

    def get_all_cyperf_applications_avaialble(
        self,
        keyword: Optional[str] = None
    ) -> Union[List[Dict[str, Any]], Exception]:
        """
        Retrieves all available CyPerf applications from the controller and writes their IDs and names to a file.

        Args:
            keyword (str, optional): Keyword to filter applications by name.

        Returns:
            list: A list of dictionaries with application details.
        """
        try:
            application_resources_api = ApplicationResourcesApi(self.client)
            take = None
            skip = 0
            search_col = 'Name'
            search_val = keyword if keyword else None
            filter_mode = None
            sort = 'Name:asc'
            api_application_resources_response = application_resources_api.get_resources_apps(
                take=take,
                skip=skip,
                search_col=search_col,
                search_val=search_val,
                filter_mode=filter_mode,
                sort=sort
            )
            application_ids = [app.id for app in api_application_resources_response.data]
            application_names = [app.name for app in api_application_resources_response.data]
            application_descriptions = [app.description for app in api_application_resources_response.data]
            application_list = [{"app_id": app_id, "app_name": app_name, "app_description": app_description} for app_id, app_name, app_description in zip(application_ids, application_names, application_descriptions)]
            return application_list
        except Exception as e:
            return Exception(f"Failed to get available applications: {str(e)}")

    def add_multiple_applications_to_session(
        self,
        session_id: Optional[str] = None,
        application_list: Optional[List[Dict[str, Any]]] = None,
        keyword: Optional[str] = None
    ) -> Union[Dict[str, Any], Exception]:
        """
        Adds applications to a session.

        Args:
            session_id (str, optional): The ID of the session to add applications to.
            application_list (list, optional): List of application dicts to add.
            keyword (str, optional): Keyword to filter applications by name.

        Returns:
            dict: A message and the list of applications in the session.
        """
        try:
            if keyword:
                application_list = self.get_all_cyperf_applications_avaialble(keyword=keyword)
                if isinstance(application_list, Exception):
                    return application_list
                message = f"Added {len(application_list)} applications to session {session_id}"
            else:
                message = f"Added {len(application_list)} applications to session {session_id}"
            for app in application_list or []:
                self.add_application_to_application_profile(
                    session_id=session_id,
                    application_name=app["app_name"],
                    application_objective_weight=100
                )
            return {
                "message": message,
                "applications": self.get_all_application_for_session(session_id=session_id)
            }
        except Exception as e:
            return Exception(f"Failed to add multiple applications: {str(e)}")
        