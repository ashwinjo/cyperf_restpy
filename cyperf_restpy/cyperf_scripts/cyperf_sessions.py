import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.configurations_api import ConfigurationsApi


class CyperfSessions:
    """
    Handles session creation, deletion, export/import, configuration management, and network elements in CyPerf.
    """
    def __init__(self, client: cyperf.ApiClient):
        """
        Initializes the CyperfSessions class with a CyPerf API client.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.session_client = SessionsApi(self.client)

    def create_session(
        self,
        config_name: str = "Cyperf Empty Config",
        session_name: str = None,
        config_url: str = None
    ) -> dict:
        """
        Loads an existing configuration into a session or creates a new session with the specified configuration.

        Args:
            config_name (str, optional): The name of the configuration to load. Defaults to "Cyperf Empty Config".
            session_name (str, optional): The name of the session to create. Defaults to None.
            config_url (str, optional): The URL of the configuration to load. Defaults to None.

        Returns:
            dict: A dictionary containing the session ID and session name.
        """
        api_session_instance = cyperf.SessionsApi(self.client)
        if not config_url:
            config_url = self._get_configuration_url(config_name=config_name)
        sessions = [cyperf.Session(application=None,
                                    config_name=None,
                                    configUrl=config_url,
                                    index=None,
                                    name=None,
                                    owner="admin")]
        print("Creating cyperf session...")
        api_session_response = api_session_instance.create_sessions(session=sessions)
        session = api_session_response[0]
        if session_name:
            self.save_configuration(session_id=session.id, save_config_name=session_name)
        return {"session_id": session.id, "session_name": session.name}

    def load_configuration_from_zip(
        self,
        configuration_file: str = None,
        session_name: str = None
    ) -> dict:
        """
        Loads a configuration from a zip file, retrieves the config URL, and creates a session.

        Args:
            configuration_file (str, optional): The path to the configuration file. Defaults to None.
            session_name (str, optional): The name of the session to create. Defaults to None.

        Returns:
            dict: A dictionary containing the session ID and session name.
        """
        config_api = cyperf.ConfigurationsApi(self.client)
        resp = config_api.start_configs_import(configuration_file)
        final_resp = resp.await_completion()
        config_url = final_resp[0]["configUrl"]
        return self.create_session(config_url=config_url, session_name=session_name)

    def show_session(
        self,
        session_id: str = None
    ) -> dict:
        """
        Retrieves the details of a session as a dictionary.

        Args:
            session_id (str, optional): The ID of the session to get the details of. Defaults to None.

        Returns:
            dict: A dictionary containing the session details.
        """
        session = self.session_client.get_session_by_id(session_id=session_id)
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

    def delete_session(
        self,
        session_id: str
    ) -> None:
        """
        Deletes a session by its ID. Stops the test if it is not already stopped.

        Args:
            session_id (str): The ID of the session to delete.
        """
        session = self.session_client.get_session_test(session_id=session_id)
        if session.status != 'STOPPED':
            pass
            # Need to implement this yet
            # self.stop_test(session)
        self.session_client.delete_session(session_id)
        return {"message": f"Session {session_id} deleted successfully"}

    def add_network_element(
        self,
        session_id: str = None,
        number_of_ip_networks: int = 1
    ) -> dict:
        """
        Adds network elements to a session's configuration.

        Args:
            session_id (str, optional): The ID of the session to modify. Defaults to None.
            number_of_ip_networks (int, optional): The number of IP network elements to add. Defaults to 1.

        Returns:
            dict: A message indicating the result of the operation.
        """
        print("Adding network elements...")
        session = self.session_client.get_session_by_id(session_id=session_id)
        network_profiles = session.config.config.network_profiles
        network_profiles.update()
        network_profiles.append(cyperf.NetworkProfile(DUTNetworkSegment=[], id="12"))
        network_profiles.append(cyperf.NetworkProfile(IPNetworkSegment=[], id="13"))
        for iface in session.config.config.network_profiles:
            print(iface.id)
        network_profiles.update()
        return {"message": f"IP network elements added to session {session_id} - {session.name}"}

    def _get_configuration_url(
        self,
        config_name: str = None
    ) -> str:
        """
        Retrieves the configuration URL for a given configuration name.

        Args:
            config_name (str, optional): The name of the configuration. Defaults to None.

        Returns:
            str: The configuration URL.
        """
        config_api = ConfigurationsApi(self.client)
        config = config_api.get_configs(take=1, skip=0, search_col='displayName', search_val=config_name, filter_mode=None, sort=None)
        return config.data[0].config_url

    def save_configuration(self, session_id: str = None, save_config_name: str = None) -> dict:
        """
        Saves the configuration for a given session.

        Args:
            session_id (str, optional): The ID of the session to save. Defaults to None.
            save_config_name (str, optional): The name to save the configuration as. Defaults to None.

        Returns:
            dict: A message indicating the result of the operation.
        """
        save_config_operation = cyperf.SaveConfigOperation()
        save_config_operation.name = save_config_name
        print("Saving the configuration...")
        api_save_config_response = self.session_client.start_session_config_save(session_id, save_config_operation=save_config_operation)
        saving_response = api_save_config_response.await_completion()
        print("Configuration saved successfully.\n")
        config_id = saving_response["id"]
        return {"message": f"Configuration saved for session {session_id} with id {config_id}"}


        """
        Imports a configuration to be used in a CyPerf session.

        Args:
            config_url (str, optional): The name or path of the configuration to import. Defaults to None. Eg: 'appsec-865' OR URL

        Returns:
            dict: A message indicating the result of the operation.
        """
        api_configurations_instance = cyperf.ConfigurationsApi(self.client)
        api_configurations_response = api_configurations_instance.start_configs_import(body=cofig_file_path)
        api_configurations_response.await_completion()
        return {"message": f"Config from path: '{cofig_file_path}' imported successfully"} 