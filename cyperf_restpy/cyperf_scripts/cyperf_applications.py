import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.application_resources_api import ApplicationResourcesApi

class CyperfApplications:
    """
    Manages application profiles and application assignment in CyPerf sessions.
    """
    def __init__(self, client: cyperf.ApiClient):
        """
        Initializes the CyperfApplications class with a CyPerf API client.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.session_client = SessionsApi(self.client)

    def add_application_profile_to_session(
        self,
        session_id: str = None,
        application_profile_name: str = 'Application Profile'
    ) -> dict:
        """
        Adds an application profile to a session's traffic profiles.

        Args:
            session_id (str, optional): The ID of the session to add the application profile to. Defaults to None.
            application_profile_name (str, optional): The name of the application profile. Defaults to 'Application Profile'.

        Returns:
            dict: A message indicating the result of the operation.
        """
        session = self.session_client.get_session_by_id(session_id=session_id)
        traffic_profiles = session.config.config.traffic_profiles
        traffic_profiles.append(cyperf.ApplicationProfile(Name=application_profile_name))
        traffic_profiles.update()
        return {"message": f"Application profile added to session {session_id} - {session.name}"}

    def add_application_to_application_profile(
        self,
        session_id: str = None,
        application_name: str = 'AI LLM over Generic HTTP',
        application_objective_weight: int = 100
    ) -> dict:
        """
        Adds an application to the first application profile in a session and sets its objective weight.

        Args:
            session_id (str, optional): The ID of the session to modify. Defaults to None.
            application_name (str, optional): The name of the application to add. Defaults to 'AI LLM over Generic HTTP'.
            application_objective_weight (int, optional): The objective weight for the application. Defaults to 100.

        Returns:
            dict: A message indicating the result of the operation.
        """
        print("Adding the applications...")
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
        print(f"Applications {application_name} added successfully. with weight {application_objective_weight}\n")
        return {"message": f"Applications {application_name} added successfully. with weight {application_objective_weight}"}

    def get_all_application_for_session(
        self,
        session_id: str = None
    ) -> list:
        """
        Retrieves all application names for the first application profile in a session.

        Args:
            session_id (str, optional): The ID of the session to query. Defaults to None.

        Returns:
            list: A list of application names in the session.
        """
        session = self.session_client.get_session_by_id(session_id=session_id)
        return [app.name for app in session.config.config.traffic_profiles[0].applications]

    def get_all_cyperf_applications_avaialble(
        self,
        keyword: str = None
    ) -> tuple:
        """
        Retrieves all available CyPerf applications from the controller and writes their IDs and names to a file.

        Returns:
            tuple: A tuple containing a list of application IDs and a list of application names.
        """
        application_resources_api = ApplicationResourcesApi(self.client)
        take = None
        skip = 0
        search_col = 'Name'
        if keyword:
            search_val = keyword
        else:
            search_val = None
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
        print(f"{len(api_application_resources_response.data)} applications found.\n")

        application_ids = [app.id for app in api_application_resources_response.data]
        application_names = [app.name for app in api_application_resources_response.data]
        application_descriptions = [app.description for app in api_application_resources_response.data]

        application_list = [{"app_id": app_id, "app_name": app_name, "app_description": app_description} for app_id, app_name, app_description in zip(application_ids, application_names, application_descriptions)]
        
        return application_list
    

    def add_multiple_applications_to_session(
        self,
        session_id: str = None,
        application_list: list = None,
        keyword: str = None
    ) -> dict:
        """
        Adds applications to a session.
        """

        if keyword:
            application_list = self.get_all_cyperf_applications_avaialble(keyword=keyword)
            message = f"Added {len(application_list)} applications to session {session_id}"
        else:
            message = f"Added {len(application_list)} applications to session {session_id}"
        
        for app in application_list:
            self.add_application_to_application_profile(session_id=session_id, 
                                                        application_name=app["app_name"], 
                                                        application_objective_weight=100)
            
        
        return {"message": message, 
                "applications": self.get_all_application_for_session(session_id=session_id)}
        