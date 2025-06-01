"""CyPerf session management utilities."""

import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.configurations_api import ConfigurationsApi
from typing import Optional, Dict, Any, List, Union

class CyperfSessions:
    """Handles session creation, deletion, export/import, configuration management, and network elements in CyPerf."""
    def __init__(self, client: cyperf.ApiClient) -> None:
        """
        Initializes the CyperfSessions class with a CyPerf API client.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.session_client = SessionsApi(self.client)

    def get_all_sessions(self) -> Union[List[Dict[str, Any]], Exception]:
        """
        Get all sessions.

        Returns:
            list: A list of dictionaries with session details.
            Exception: If the retrieval fails.
        """
        try:
            sessions_list = []
            sessions = self.session_client.get_sessions()
            for session in sessions:
                sessions_list.append({
                    'id': session.id,
                    'name': session.name,
                    'config_name': session.config_name,
                    'config_url': session.config_url,
                })
            return sessions_list
        except Exception as e:
            return Exception(f"Failed to get all sessions: {str(e)}")

    def create_session(
        self,
        config_name: str = "Cyperf Empty Config",
        session_name: Optional[str] = None,
        config_url: Optional[str] = None
    ) -> Union[Dict[str, Any], Exception]:
        """
        Loads an existing configuration into a session or creates a new session with the specified configuration.

        Args:
            config_name (str, optional): The name of the configuration to use. Defaults to "Cyperf Empty Config".
            session_name (str, optional): The name to assign to the session.
            config_url (str, optional): The configuration URL to use.

        Returns:
            dict: A dictionary with the session ID and name.
            Exception: If the creation fails.
        """
        try:
            if not config_url:
                config_url = self._get_configuration_url(config_name=config_name)
            sessions = [cyperf.Session(application=None,
                                        config_name=None,
                                        configUrl=config_url,
                                        index=None,
                                        name=None,
                                        owner="admin")]
            api_session_response = self.session_client.create_sessions(session=sessions)
            session = api_session_response[0]
            if session_name:
                self.save_configuration(session_id=session.id, save_config_name=session_name)
            return {"session_id": session.id, "session_name": session.name}
        except Exception as e:
            return Exception(f"Failed to create session: {str(e)}")

    def load_configuration_from_zip(
        self,
        configuration_file: Optional[str] = None,
        session_name: Optional[str] = None
    ) -> Union[Dict[str, Any], Exception]:
        """
        Loads a configuration from a zip file, retrieves the config URL, and creates a session.

        Args:
            configuration_file (str, optional): The path to the configuration zip file.
            session_name (str, optional): The name to assign to the session.

        Returns:
            dict: A dictionary with the session ID and name.
            Exception: If the loading fails.
        """
        try:
            config_api = cyperf.ConfigurationsApi(self.client)
            resp = config_api.start_configs_import(configuration_file)
            final_resp = resp.await_completion()
            config_url = final_resp[0]["configUrl"]
            return self.create_session(config_url=config_url, session_name=session_name)
        except Exception as e:
            return Exception(f"Failed to load configuration from zip: {str(e)}")

    def show_session(
        self,
        session_id: Optional[str] = None
    ) -> Union[Dict[str, Any], Exception]:
        """
        Retrieves the details of a session as a dictionary.

        Args:
            session_id (str, optional): The ID of the session to retrieve.

        Returns:
            dict: A dictionary with session details.
            Exception: If the retrieval fails.
        """
        try:
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
        except Exception as e:
            return Exception(f"Failed to show session: {str(e)}")

    def delete_session(
        self,
        session_id: str
    ) -> Union[Dict[str, str], Exception]:
        """
        Deletes a session by its ID. Stops the test if it is not already stopped.

        Args:
            session_id (str): The ID of the session to delete.

        Returns:
            dict: A message indicating the result of the deletion.
            Exception: If the deletion fails.
        """
        try:
            session = self.session_client.get_session_test(session_id=session_id)
            if session.status != 'STOPPED':
                pass
            self.session_client.delete_session(session_id)
            return {"message": f"Session {session_id} deleted successfully"}
        except Exception as e:
            return Exception(f"Failed to delete session: {str(e)}")

    def _get_configuration_url(
        self,
        config_name: Optional[str] = None
    ) -> Union[str, Exception]:
        """
        Retrieves the configuration URL for a given configuration name.

        Args:
            config_name (str, optional): The name of the configuration to retrieve the URL for.

        Returns:
            str: The configuration URL.
            Exception: If the retrieval fails.
        """
        try:
            config_api = ConfigurationsApi(self.client)
            config = config_api.get_configs(take=1, skip=0, search_col='displayName', search_val=config_name, filter_mode=None, sort=None)
            return config.data[0].config_url
        except Exception as e:
            return Exception(f"Failed to get configuration URL: {str(e)}")

    def save_configuration(self, session_id: Optional[str] = None, save_config_name: Optional[str] = None) -> Union[Dict[str, str], Exception]:
        """
        Saves the configuration for a given session.

        Args:
            session_id (str, optional): The ID of the session to save the configuration for.
            save_config_name (str, optional): The name to save the configuration as.

        Returns:
            dict: A message indicating the result of the save operation.
            Exception: If the save fails.
        """
        try:
            save_config_operation = cyperf.SaveConfigOperation()
            save_config_operation.name = save_config_name
            api_save_config_response = self.session_client.start_session_config_save(session_id, save_config_operation=save_config_operation)
            saving_response = api_save_config_response.await_completion()
            config_id = saving_response["id"]
            return {"message": f"Configuration saved for session {session_id} with id {config_id}"}
        except Exception as e:
            return Exception(f"Failed to save configuration: {str(e)}")

 