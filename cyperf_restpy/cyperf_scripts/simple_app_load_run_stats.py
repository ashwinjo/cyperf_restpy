"""
CyPerf Configuration and Test Management
======================================

This module provides a comprehensive set of utilities and classes for managing CyPerf test configurations,
execution, and analysis. It includes functionality for:

- Creating and managing test sessions
- Configuring application and attack profiles 
- Executing test runs
- Collecting and analyzing test statistics
- Managing network elements and objectives

The module serves as the core building block for automating CyPerf testing workflows.

Author: Ashwin Joshi
Created: May 28, 2025
Last Modified: May 28, 2025
"""
import cyperf
import pandas as pd

from cyperf.api.sessions_api import SessionsApi
from cyperf.api.configurations_api import ConfigurationsApi
from cyperf.api.test_operations_api import TestOperationsApi
from cyperf.api.statistics_api import StatisticsApi
from cyperf.api.diagnostics_api import DiagnosticsApi
from cyperf.api.license_servers_api import LicenseServersApi
from cyperf.api.application_resources_api import ApplicationResourcesApi


import urllib3; urllib3.disable_warnings()

class CyperfTestRunner:
    """This class is used to run a simple app load test."""
    def __init__(self, controller_ip: str = "3.141.193.119", refresh_token: str = None):
        """
        Initializes the CyperfTestRunner with the specified controller IP and refresh token.

        Args:
            controller_ip (str, optional): The IP address of the CyPerf controller. Defaults to "3.141.193.119".
            refresh_token (str, optional): The refresh token for authentication. Defaults to None.
        """
        self.controller_ip = controller_ip
        self.refresh_token = refresh_token
        self.client = self.get_cyperf_client(controller_ip, refresh_token)
        self.session_client = SessionsApi(self.client)


    def get_cyperf_client(self, controller_ip: str = "3.141.193.119", refresh_token: str = None) -> cyperf.ApiClient:
        """
        Creates and returns a CyPerf API client for the specified controller IP and refresh token.

        Args:
            controller_ip (str, optional): The IP address of the CyPerf controller. Defaults to "3.141.193.119".
            refresh_token (str, optional): The refresh token for authentication. Defaults to None.

        Returns:
            cyperf.ApiClient: The configured CyPerf API client.
        """
        config = cyperf.Configuration(host=f"https://{controller_ip}",
                        refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzOTMyN2I4OC0xYzkyLTRlYjktYTI0My01MTE3NTczNTBlNjIifQ.eyJpYXQiOjE3NDg1MzEzODQsImp0aSI6Ijk2ODUzNzBlLTkzZDUtNDBlZi1iZWY4LTA0ZTIxYTIyMGRjNCIsImlzcyI6Imh0dHBzOi8vMy4xNDEuMTkzLjExOS9hdXRoL3JlYWxtcy9rZXlzaWdodCIsImF1ZCI6Imh0dHBzOi8vMy4xNDEuMTkzLjExOS9hdXRoL3JlYWxtcy9rZXlzaWdodCIsInN1YiI6ImNjNGQwZjU5LTEwNDUtNGI0MS05YjhjLTUwN2JjMWE2MWM4NiIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJjbHQtd2FwIiwibm9uY2UiOiIxMjM4ZDEzZC05NjNlLTRlYmMtOGY5Yi0wNWNmYzM1MTVlNGIiLCJzZXNzaW9uX3N0YXRlIjoiYWFjYTI5ZjgtMzA3Mi00YWM1LThmMjQtZTJlMzI1YWYwMDNmIiwic2NvcGUiOiJvcGVuaWQgZW1haWwgb2ZmbGluZV9hY2Nlc3MgcHJvZmlsZSIsInNpZCI6ImFhY2EyOWY4LTMwNzItNGFjNS04ZjI0LWUyZTMyNWFmMDAzZiJ9.-NE9O07AhtHhrk4RbwGGTwitw3Fxy6olZiUVgCI5QVU")
        config.verify_ssl = False   
        return cyperf.ApiClient(config)


    def create_session(self, config_name: str = "Cyperf Empty Config", session_name: str = None, config_url: str = None) -> dict:
        """
        Loads an existing configuration into a session or creates a new session with the specified configuration.

        If config_name is provided, it searches for the configuration in WAP and loads it. If not provided, it loads the default empty configuration.

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


    def load_configuration_from_zip(self, configuration_file: str = None, session_name: str = None) -> dict:
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
    
    def show_session(self, session_id: str = None) -> dict:
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
    
    def delete_session(self, session_id: str) -> None:
        """
        Deletes a session by its ID. Stops the test if it is not already stopped.

        Args:
            session_id (str): The ID of the session to delete.
        """
        session = self.session_client.get_session_test(session_id=session_id)
        if session.status != 'STOPPED':
            pass
            # Need to implement this yet
            self.stop_test(session)
        self.session_client.delete_session(session.id)

    
    def add_application_profile_to_session(self, session_id: str = None, application_profile_name: str = 'Application Profile') -> dict:
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
    
    def add_application_to_application_profile(self, session_id: str = None, application_name: str = 'AI LLM over Generic HTTP', application_objective_weight: int = 100) -> dict:
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
        # TODO: Make Application name a list
        application_resources_api = ApplicationResourcesApi(self.client)
        take = 1                                                    
        skip = 0                                                    
        search_col = "Name"                                         
        search_val = application_name                                                                       
        sort = 'Name:asc'                                           
        api_application_resources_response = application_resources_api.get_resources_apps(take=take, 
                                                                                          skip=skip, 
                                                                                          search_col=search_col, 
                                                                                          search_val=search_val, 
                                                                                          filter_mode=None, 
                                                                                          sort=sort)
        
        app_id = api_application_resources_response.data[0].id
        external_resource_info = [cyperf.ExternalResourceInfo(externalResourceURL=app_id)]
        

        config = self.session_client.get_session_config(session_id=session_id, include='Config, TrafficProfiles, Applications')
        
        
        # config.config.traffic_profiles[0].applications.append(cyperf.Application(id=app_id, 
        #                                                                          objective_weight=application_objective_weight))

        # config.config.traffic_profiles[0].applications.update()

       
        api_session_response = self.session_client.start_config_add_applications(session_id, 
                                                                                 traffic_profile_id = '1', 
                                                                                 external_resource_info=external_resource_info)
        
        api_session_response.await_completion()
        for app in config.config.traffic_profiles[0].applications:
            if app.name == application_name:
                app.objective_weight = application_objective_weight
                app.update()

        print(f"Applications {application_name} added successfully. with weight {application_objective_weight}\n")
        return {"message": f"Applications {application_name} added successfully. with weight {application_objective_weight}"}
    
    def get_all_application_for_session(self, session_id: str = None) -> list:
        """
        Retrieves all application names for the first application profile in a session.

        Args:
            session_id (str, optional): The ID of the session to query. Defaults to None.

        Returns:
            list: A list of application names in the session.
        """
        session = self.session_client.get_session_by_id(session_id=session_id)
        return [app.name for app in session.config.config.traffic_profiles[0].applications]
    

    
    def get_all_cyperf_applications_avaialble(self) -> tuple:
        """
        Retrieves all available CyPerf applications from the controller and writes their IDs and names to a file.

        Returns:
            tuple: A tuple containing a list of application IDs and a list of application names.
        """
        # Get some applications
        application_resources_api = ApplicationResourcesApi(self.client)
        take = None                                                    
        skip = 0                                                    
        search_col = None                                         
        search_val = None                               
        filter_mode = None                                          
        sort = 'Name:asc'                                           

        application_ids = []
        application_names = []
        api_application_resources_response = application_resources_api.get_resources_apps(take=take, 
                                                                                          skip=skip, 
                                                                                          search_col=search_col, 
                                                                                          search_val=search_val, 
                                                                                          filter_mode=filter_mode, 
                                                                                          sort=sort)
        print(f"{len(api_application_resources_response.data)} applications found.\n")
        
        application_ids = [app.id for app in api_application_resources_response.data]
        application_names = [app.name for app in api_application_resources_response.data]
        with open("application_cyperf_list.txt", "w") as f:
            for app_id, app_name in zip(application_ids, application_names):
                f.write(f"{app_id} - {app_name}\n")
        return application_ids, application_names

    def add_network_element(self, session_id: str = None, number_of_ip_networks: int = 1) -> dict:
        """
        Adds network elements to a session's configuration.

        Args:
            session_id (str, optional): The ID of the session to modify. Defaults to None.
            number_of_ip_networks (int, optional): The number of IP network elements to add. Defaults to 1.

        Returns:
            dict: A message indicating the result of the operation.
        """
        # Create a Network Profile
        print("Adding network elements...")
        session = self.session_client.get_session_by_id(session_id=session_id)
        #print(cyperf.NetworkProfile(DUTNetworkSegment=[], id="1"))
        network_profiles = session.config.config.network_profiles
        network_profiles.update()
        network_profiles.append(cyperf.NetworkProfile(DUTNetworkSegment=[], id="12"))
        network_profiles.append(cyperf.NetworkProfile(IPNetworkSegment=[], id="13"))   
        for iface in session.config.config.network_profiles:
            print(iface.id)
        import pdb; pdb.set_trace()
        network_profiles.update()

        return {"message": f"IP network elements added to session {session_id} - {session.name}"}

    
    def _get_configuration_url(self, config_name: str = None) -> str:
        """
        Retrieves the configuration URL for a given configuration name.

        Args:
            config_name (str, optional): The name of the configuration. Defaults to None.

        Returns:
            str: The configuration URL.
        """
        config_api = ConfigurationsApi(self.client)
        config = config_api.get_configs(take=1, skip=0, 
                                        search_col='displayName', 
                                        search_val=config_name, 
                                        filter_mode=None, 
                                        sort=None)
        return config.data[0].config_url
   
    
    def set_primary_objective_goals(
        self,
        session_id: str = None,
        primary_object_name: str = 'SIMULATED_USERS',
        primary_objective_duration: int = 123,
        primary_objective_goal: int = 1234
    ) -> dict:
        """
        Sets the primary objective goals for a given session.

        Args:
            session_id (str, optional): The ID of the session to update. Defaults to None.
            primary_object_name (str, optional): The name of the primary objective (e.g., 'SIMULATED_USERS', 'THROUGHPUT'). Defaults to None.
            primary_objective_duration (int, optional): The duration for the primary objective. Defaults to None.
            primary_objective_goal (int, optional): The goal value for the primary objective. Defaults to None.

        Returns:
            dict: A message indicating the result of the operation.
        """
        objectives_dict = {
            "SIMULATED_USERS": cyperf.ObjectiveType.SIMULATED_USERS,
            "THROUGHPUT": cyperf.ObjectiveType.THROUGHPUT,
            "CONNECTIONS_PER_SECOND": cyperf.ObjectiveType.CONNECTIONS_PER_SECOND,
            "CONCURRENT_CONNECTIONS": cyperf.ObjectiveType.CONCURRENT_CONNECTIONS,
        }
        objectives_dict_unit = {
            "SIMULATED_USERS": cyperf.ObjectiveUnit.EMPTY,
            "THROUGHPUT": cyperf.ObjectiveUnit.BPS,
            "CONNECTIONS_PER_SECOND": cyperf.ObjectiveUnit.EMPTY,
            "CONCURRENT_CONNECTIONS": cyperf.ObjectiveUnit.EMPTY,
        }
        objective_to_be_configured = objectives_dict[primary_object_name]
        objectives_unit = objectives_dict_unit[primary_object_name]
        include = 'Config, TrafficProfiles'

        config = self.session_client.get_session_config(session_id=session_id, include=include)
        
        primary_objective = config.config.traffic_profiles[0].objectives_and_timeline.primary_objective
        primary_objective.type = objective_to_be_configured
        primary_objective.timeline[1].duration = primary_objective_duration
        primary_objective.timeline[1].objective_value = primary_objective_goal
        primary_objective.timeline[1].objective_unit = objectives_unit
        primary_objective.update()
        return {"message": f"Primary objective goals set for session {session_id} for {primary_object_name}"}

    def get_all_primary_objectives_goals(self, session_id: str = None) -> list:
        """
        Retrieves all primary objective goals for a given session.

        Args:
            session_id (str, optional): The ID of the session to query. Defaults to None.

        Returns:
            list: A list of dictionaries containing the primary objective goals.
        """
        include = 'Config, TrafficProfiles'
        config = self.session_client.get_session_config(session_id=session_id, include=include)
        primary_objective = config.config.traffic_profiles[0].objectives_and_timeline.primary_objective
        out_list = []
        objectives_list = [
            cyperf.ObjectiveType.SIMULATED_USERS,
            cyperf.ObjectiveType.THROUGHPUT,
            cyperf.ObjectiveType.CONNECTIONS_PER_SECOND,
            cyperf.ObjectiveType.CONCURRENT_CONNECTIONS
        ]
        for objective in objectives_list:
            primary_objective.type = objective
            primary_objective.timeline[1].duration
            primary_objective.timeline[1].objective_value
            primary_objective.timeline[1].objective_unit
            out_list.append({
                "type":  primary_objective.type.value,
                "duration": primary_objective.timeline[1].duration,
                "objective_value": primary_objective.timeline[1].objective_value,
                "objective_unit": primary_objective.timeline[1].objective_unit
            })
        return out_list
    
    
    def get_available_agents(self) -> list:
        """
        Retrieves the available agents for the current session.

        Returns:
            list: A list of dictionaries containing agent information.
        """
        api_agents_instance = cyperf.AgentsApi(self.client)
        available_agents = api_agents_instance.get_agents(exclude_offline='true')
        agent_list = []
        for agent in available_agents:
            agent_dict = {
                'id': agent.id,
                'ip': agent.ip,
                'hostname': agent.hostname,
                'mgmt_interface': agent.mgmt_interface,
                'status': agent.status
            }
            agent_list.append(agent_dict)
        return agent_list
    
    def assign_agents_to_network_elements(self, session_id: str = None, agent_map: dict = None) -> None:
        """
        Assigns agents to network elements for a given session.

        Args:
            session_id (str, optional): The ID of the session to assign agents to. Defaults to None.
            agent_map (dict, optional): A dictionary mapping network names to agent IDs and IPs. Defaults to None.
        """
        config = self.session_client.get_session_config(session_id=session_id, include='Config, NetworkProfiles')
        agents = self.get_available_agents()
        agent_map = {
            'IP Network 1': [agents[0]['id'], agents[0]['ip']],
            'IP Network 2': [agents[1]['id'], agents[1]['ip']]
        }
        print("Assigning agents ...")
        for net_profile in config.config.network_profiles:
            for ip_net in net_profile.ip_network_segment:
                if ip_net.name in agent_map:
                    agent_id = agent_map[ip_net.name][0]
                    agent_ip = agent_map[ip_net.name][1]
                    print(f"Agent {agent_ip} with {agent_id} assigned to {ip_net.name}.")
                    agentDetails = [cyperf.AgentAssignmentDetails(agent_id=agent_id, capture_setting='true', id=agent_id, interfaces=None, links=None)]
                    if not ip_net.agent_assignments:
                        by_id = None
                        by_port = None
                        by_tag = []
                        links = None
                        ip_net.agent_assignments = cyperf.AgentAssignments(by_id=by_id, by_port=by_port, by_tag=by_tag, links=links)
                    ip_net.agent_assignments.by_id.extend(agentDetails)
                    ip_net.update()
        print("Assigning agents completed.\n")

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
    
    def export_configuration(self, session_id: str = None, export_config_name: str = None) -> dict:
        """
        Exports the configuration for a given session.

        Args:
            session_id (str, optional): The ID of the session to export. Defaults to None.
            export_config_name (str, optional): The name to export the configuration as. Defaults to None.

        Returns:
            dict: A message indicating the result of the operation.
        """
        config = self.session_client.get_session_config(session_id=session_id, include='Config')
        api_configurations_instance = cyperf.ConfigurationsApi(self.client)
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
    
    def import_configuration(self, import_config_name: str = None) -> dict:
        """
        Imports a configuration to be used in a CyPerf session.

        Args:
            import_config_name (str, optional): The name or path of the configuration to import. Defaults to None.

        Returns:
            dict: A message indicating the result of the operation.
        """
        api_configurations_instance = cyperf.ConfigurationsApi(self.client)
        import_all_operation = cyperf.ImportAllOperation(configs=[cyperf.ConfigMetadata(config_url='appsec-865')])
        api_configurations_response = api_configurations_instance.start_configs_import_all(import_all_operation=import_all_operation)
        file_path = api_configurations_response.await_completion()
        return {"message": f"Imported as: '{file_path}'"}
    
    def start_test_run(self, session_id: str = None) -> dict:
        """
        Starts a test run for a given session.

        Args:
            session_id (str, optional): The ID of the session to start the test run for. Defaults to None.

        Returns:
            dict: A message indicating the result of the operation.
        """
        test_execution_api = TestOperationsApi(self.client)
        start_run_operation = test_execution_api.start_test_run_start(session_id=session_id)
        try:
            resp = start_run_operation.await_completion()
            print(resp)
        except cyperf.ApiException as e:
            raise (e)
        return {"message": f"Test run started for session {session_id}"}
    
    def stop_test_run(self, session_id: str = None) -> dict:
        """
        Stops a test run for a given session.

        Args:
            session_id (str, optional): The ID of the session to stop the test run for. Defaults to None.

        Returns:
            dict: A message indicating the result of the operation.
        """
        test_execution_api = TestOperationsApi(self.client)
        stop_run_operation = test_execution_api.start_test_run_stop(session_id=session_id)
        try:
            resp = stop_run_operation.await_completion()
            print(resp)
        except cyperf.ApiException as e:
            raise (e)
        return {"message": f"Test run stopped for session {session_id}"}
    
    def abort_test_run(self, session_id: str = None) -> dict:
        """
        Aborts a test run for a given session.

        Args:
            session_id (str, optional): The ID of the session to abort the test run for. Defaults to None.

        Returns:
            dict: A message indicating the result of the operation.
        """
        test_execution_api = TestOperationsApi(self.client)
        abort_run_operation = test_execution_api.start_test_run_abort(session_id=session_id)
        try:
            resp = abort_run_operation.await_completion()
            print(resp)
        except cyperf.ApiException as e:
            raise (e)
        return {"message": f"Test run aborted for session {session_id}"}

    def collect_test_run_stats(
        self,
        session_id: str = None,
        stats_name: str = None,
        time_from: int = None,
        time_to: int = None
    ) -> dict:
        """
        Collects test run statistics for a given session.

        Args:
            session_id (str, optional): The ID of the session to collect stats for. Defaults to None.
            stats_name (str, optional): The name of the statistic to collect. Defaults to None.
            time_from (int, optional): The start time for stats collection. Defaults to None.
            time_to (int, optional): The end time for stats collection. Defaults to None.

        Returns:
            dict: A dictionary containing the processed statistics.
        """
        test = self.session_client.get_session_test(session_id=session_id)
        test_id = [a[1] for a in test if a[0] == 'test_id'][0]
        stats_api = StatisticsApi(self.client)
        stats = stats_api.get_result_stats(test_id)
        if time_from:
            if time_to > time_from:
                stats = [stats_api.get_result_stat_by_id(test_id, stat.name, var_from=time_from, to=time_to) for stat in stats]
            else:
                stats = [stats_api.get_result_stat_by_id(test_id, stat.name, var_from=time_from) for stat in stats]
        else:
            stats_final = []
            for stat in stats:
                try:
                    b = stats_api.get_result_stat_by_id(test_id, stat.name)
                    stats_final.append(b)
                except cyperf.ApiException as e:
                    continue
        processed_stats = {}
        for stat in stats_final:
            if stat.snapshots:
                processed_stats[stat.name] = {}
                for snapshot in stat.snapshots:
                    time_stamp = snapshot.timestamp
                    processed_stats[stat.name][time_stamp] = []
                    d = {}
                    for idx, stat_name in enumerate(stat.columns):
                        d[stat_name] = [val[idx].actual_instance for val in snapshot.values]
                    processed_stats[stat.name][time_stamp] = d
        return processed_stats

    def view_stats(self, processed_stats: dict, stat_name: str = None) -> pd.DataFrame:
        """
        Visualizes the selected stat as a time series using pandas and prints available columns.

        Args:
            processed_stats (dict): The processed stats dictionary (as returned by collect_test_run_stats).
            stat_name (str, optional): The stat name to visualize (e.g., 'client-application-connection-rate'). Defaults to None.

        Returns:
            pd.DataFrame: The last 50 records of the selected stat as a DataFrame.
        """
        if stat_name not in list(processed_stats.keys()):
            raise ValueError(f"Stats name {stat_name} not found in available stats")
        stats_dict = processed_stats[stat_name]
        df = pd.DataFrame.from_dict(stats_dict, orient='index')
        for col in df.columns:
            df[col] = df[col].apply(lambda x: x[0] if isinstance(x, list) and len(x) == 1 else x)
        columns_to_show = [col for col in df.columns if col != 'filter']
        print("\nAvailable columns:")
        for col in columns_to_show:
            print(f"- {col}")
        if 'filter' in df.columns:
            df = df.drop(columns=['filter'])
        return df.tail(50)
    


    def add_attack_profile_to_session(self, session_id: str = None, attack_profile_name: str = 'Attack Profile') -> dict:
        """
        Adds an attack profile to a session's attack profiles.

        Args:
            session_id (str, optional): The ID of the session to add the attack profile to. Defaults to None.
            attack_profile_name (str, optional): The name of the attack profile. Defaults to 'Attack Profile'.

        Returns:
            dict: A message indicating the result of the operation.
        """
        session = self.session_client.get_session_by_id(session_id=session_id)
        attack_profiles = session.config.config.attack_profiles
        attack_profiles.append(cyperf.AttackProfile(Name=attack_profile_name))
        attack_profiles.update()
        return {"message": f"Attack profile added to session {session_id} - {session.name}"}

    def add_attack_to_attack_profile(self, session_id: str = None, attack_profile_name: str = None, attack_name: str = None) -> None:
        """
        Adds an attack to an attack profile. (Not implemented)

        Args:
            session_id (str, optional): The ID of the session to add the attack to. Defaults to None.
            attack_profile_name (str, optional): The name of the attack profile. Defaults to None.
            attack_name (str, optional): The name of the attack to add. Defaults to None.
        """
        pass
        

    def get_all_attack_for_session(self, session_id: str = None) -> list:
        """
        Retrieves all attack names for the first attack profile in a session.

        Args:
            session_id (str, optional): The ID of the session to query. Defaults to None.

        Returns:
            list: A list of attack names in the session.
        """
        session = self.session_client.get_session_by_id(session_id=session_id)
        return [attack.name for attack in session.config.config.attack_profiles[0].attacks]
    
    def get_all_attack_primary_objectives_goals_for_session(self, session_id: str = None) -> dict:
        """
        Retrieves the primary objectives and goals for the first attack profile in a session.

        Args:
            session_id (str, optional): The ID of the session to query. Defaults to None.

        Returns:
            dict: A dictionary containing the attack rate, max concurrent attack, and duration.
        """
        session = self.session_client.get_session_by_id(session_id=session_id)
        obj_and_time_line = session.config.config.attack_profiles[0].objectives_and_timeline
        return {
            'attack_rate': obj_and_time_line.timeline_segments[0].attack_rate,
            'max_concurrent_attack': obj_and_time_line.timeline_segments[0].max_concurrent_attack,
            'duration': obj_and_time_line.timeline_segments[0].duration
        }
    
    def set_attack_primary_objectives_goals_for_session(
        self,
        session_id: str = None,
        attack_rate: int = None,
        max_concurrent_attack: int = None,
        duration: int = None
    ) -> dict:
        """
        Sets the attack primary objectives and goals for a given session.

        Args:
            session_id (str, optional): The ID of the session to update. Defaults to None.
            attack_rate (int, optional): The attack rate to set. Defaults to None.
            max_concurrent_attack (int, optional): The max concurrent attack to set. Defaults to None.
            duration (int, optional): The duration to set. Defaults to None.

        Returns:
            dict: A message indicating the result of the operation.
        """
        session = self.session_client.get_session_by_id(session_id=session_id)
        session.config.config.attack_profiles[0].objectives_and_timeline.timeline_segments[0].attack_rate = attack_rate
        session.config.config.attack_profiles[0].objectives_and_timeline.timeline_segments[0].max_concurrent_attack = max_concurrent_attack
        session.config.config.attack_profiles[0].objectives_and_timeline.timeline_segments[0].duration = duration
        session.config.config.attack_profiles[0].objectives_and_timeline.update()
        return {"message": f"Attack primary objectives and goals set for session {session_id}"}



ctr = CyperfTestRunner()

#print(ctr.get_all_attack_primary_objectives_goals_for_session(session_id="appsec-9780af4a-edc6-4b66-8a81-eb2abf60e716"))

#print(ctr.create_session(config_name="VLAN with Simulated Users", session_name="Repro_For_Obj_Bug"))
# a = ctr.show_session_details(session_id="appsec-414b2a8a-3ef5-4d80-af40-8b9370256b30")
# print(a)

# a = ctr.add_application_profile_to_session(session_id="appsec-45fb0679-6b71-4c59-9833-86d6a4e3c696", 
#                                            application_profile_name="Shaktimaan")
# print(a)

# a = ctr.add_attack_profile_to_session(session_id="appsec-414b2a8a-3ef5-4d80-af40-8b9370256b30", 
#                                       attack_profile_name="Tamraj Kilvish")
# print(a)


# ========= Not able to add Network Elements =========
# a = ctr.test_network_profile()
# print(a)

ctr.set_primary_objective_goals(session_id="appsec-34778570-0e66-40d2-90d5-2c0841349924")

#print(ctr.get_all_primary_objectives_goals(session_id="appsec-34778570-0e66-40d2-90d5-2c0841349924"))
# print(ctr.get_available_agents())

#print(ctr.save_configuration(session_id="appsec-414b2a8a-3ef5-4d80-af40-8b9370256b30", save_config_name="Ashwin Save Config"))

#print(ctr.export_configuration(session_id="appsec-414b2a8a-3ef5-4d80-af40-8b9370256b30", export_config_name="Ashwin Export Config 12345"))

# === Import Configuration not able to make this work===
#print(ctr.import_configuration(import_config_name="/Users/ashwjosh/Downloads/SU-obj-APPMIX-with-10-apps-pdff.zip"))    

# print(ctr.load_configuration_from_zip(configuration_file="/Users/ashwjosh/Downloads/SU-obj-APPMIX-with-10-apps-pdff.zip", session_name="ShaktimaanAttacks"))

# print(ctr.start_test_run(session_id="appsec-9780af4a-edc6-4b66-8a81-eb2abf60e716"))
# import time
# time.sleep(20)
# #print(ctr.stop_test_run(session_id="appsec-9780af4a-edc6-4b66-8a81-eb2abf60e716"))
# time.sleep(10)
# print(ctr.abort_test_run(session_id="appsec-9780af4a-edc6-4b66-8a81-eb2abf60e716"))
# #print(ctr.collect_test_run_stats(session_id="appsec-414b2a8a-3ef5-4d80-af40-8b9370256b30"))
# processed_stats = ctr.collect_test_run_stats(session_id="appsec-9780af4a-edc6-4b66-8a81-eb2abf60e716")
# print(ctr.view_stats(processed_stats, stat_name="client-l23-throughput"))

#print(ctr.get_all_cyperf_applications_avaialble())
# print(ctr.add_application_to_application_profile(session_id="appsec-9780af4a-edc6-4b66-8a81-eb2abf60e716", 
#                                                  application_name='AI LLM over Generic HTTP'))



"""
# Available statistics:
# - agent-metrics-network: Network metrics for agents
# - AI-2 (copy from May 29 01:07:10) - P-2: Custom panel 2
# - AI-2 (copy from May 29 01:07:10) - Panel 1: Custom panel 1
# - http-requests-rate-per-app: HTTP request rate per application
# - client-throughput: Overall client throughput
# - client-traffic-profile: Client traffic profile metrics
# - traffic-agents-instant: Instantaneous traffic agent metrics
# - client-application-throughput: Application-level client throughput
# - client-application-user-count-per-app: User count per application
# - client-http-statistics: HTTP statistics from client perspective
# - traffic-agents-client-applications: Client application traffic metrics
# - client-application-concurrent-connections: Concurrent connection counts
# - client-l23-throughput: Layer 2/3 client throughput
# - server-http-statistics: HTTP statistics from server perspective
# - client-traffic-profile-tcp: TCP traffic profile metrics
# - server-tcp: Server TCP metrics
# - server-throughput: Overall server throughput
# - agent-metrics-cpu: CPU metrics for agents
# - agent-metrics-memory: Memory metrics for agents
# - client-traffic-profile-latency: Latency profile metrics
# - http-client-application: HTTP client application metrics
# - http-requests-rate: Overall HTTP request rate
# - traffic-agents-l23-instant: Instantaneous L2/3 agent metrics
# - client-action-statistics: Client action statistics
# - client-application-connection-rate: Connection rate metrics
# - client-application-user-count: Overall user count
# - server-agents-number: Number of server agents
# - server-l23-throughput: Layer 2/3 server throughput
# - server-profile: Server profile metrics
# - traffic-agents: Overall traffic agent metrics
# - traffic-agents-arp: ARP-related traffic metrics
# - agent-clock-offset: Agent clock synchronization metrics
# - client-latency: Client-side latency metrics
# - client-traffic-profile-latency-per-network-segment: Per-segment latency
# - traffic-agents-dns: DNS-related traffic metrics
# - traffic-agents-l23: Layer 2/3 traffic metrics
# - client-action-http-statistics: HTTP action statistics
# - client-agents-number: Number of client agents
# - http-server-application: HTTP server application metrics
"""
