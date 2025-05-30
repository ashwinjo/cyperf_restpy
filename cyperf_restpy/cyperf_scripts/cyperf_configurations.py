import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.configurations_api import ConfigurationsApi


class CyperfConfigurations:
    """
    Handles configuration management for CyPerf sessions, including save, export, import, and URL retrieval.
    """
    def __init__(self, client: cyperf.ApiClient):
        """
        Initializes the CyperfConfigurations class with a CyPerf API client.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.session_client = SessionsApi(self.client)

    def get_configuration(
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
        config = config_api.get_configs(take=1, 
                                        skip=0, 
                                        search_col='displayName', 
                                        search_val=config_name, 
                                        filter_mode=None,
                                        sort=None)
        print(config.data[0])
        return {"config_name": config.data[0].display_name, 
                "config_url": config.data[0].config_url,
                "config_id": config.data[0].id}
    
    def get_keyword_based_configuration_match(
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
        config = config_api.get_configs(take=1000, skip=0, search_col='displayName', 
                                        search_val=config_name, 
                                        filter_mode=None,
                                        sort=None)
        import pdb; pdb.set_trace()
        return {"number_of_configs": len(config.data), 
                "list_of_matching_configs": [ {"config_name": c.display_name, 
                "config_url": c.config_url,
                "config_id": c.id} for c in config.data]}

    def save_configuration(self, session_id: str = None, save_config_name: str = None) -> dict:
        """
        Saves the configuration for a given session.

        Args:
            session_client: The SessionsApi client instance.
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

    def export_configuration(self, session_client, session_id: str = None, export_config_name: str = None) -> dict:
        """
        Exports the configuration for a given session.

        Args:
            session_client: The SessionsApi client instance.
            session_id (str, optional): The ID of the session to export. Defaults to None.
            export_config_name (str, optional): The name to export the configuration as. Defaults to None.

        Returns:
            dict: A message indicating the result of the operation.
        """
        config = self.session_client.get_session_config(session_id=session_id, include='Config')
        api_configurations_instance = ConfigurationsApi(self.client)
        export_all_operation = cyperf.ExportAllOperation(configIds=[cyperf.ConfigId(id=config.template_id)])
        api_configurations_response = api_configurations_instance.start_configs_export_all(export_all_operation=export_all_operation)
        file_path = api_configurations_response.await_completion()
        if '\\' in file_path:
            last_separator_index = file_path.rfind('\\')
        else:
            last_separator_index = file_path.rfind('/')
        directory = file_path[:last_separator_index]
        file_name = file_path[last_separator_index + 1:]
        return {"message": f"Exported as: '{file_name}' at {directory}\n"}

    def import_configuration(self, config_file_path: str = None) -> dict:
        """
        Imports a configuration to be used in a CyPerf session.

        Args:
            config_file_path (str, optional): The path of the configuration to import. Defaults to None.

        Returns:
            dict: A message indicating the result of the operation.
        """
        api_configurations_instance = ConfigurationsApi(self.client)
        import_all_operation = cyperf.ImportAllOperation(configs=[cyperf.ConfigMetadata(config_url=config_file_path)])
        api_configurations_response = api_configurations_instance.start_configs_import_all(import_all_operation=import_all_operation)
        file_path = api_configurations_response.await_completion()
        return {"message": f"Imported as: '{file_path}'"} 