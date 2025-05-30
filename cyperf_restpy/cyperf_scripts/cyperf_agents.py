import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.agents_api import AgentsApi

class CyperfAgents:
    """
    Provides agent management utilities for CyPerf, including discovery and assignment.
    """
    def __init__(
        self,
        client: cyperf.ApiClient
    ):
        """
        Initializes the CyperfAgents class with a CyPerf API client.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.session_client = SessionsApi(self.client)

    def get_available_agents(
        self
    ) -> list:
        """
        Retrieves the available agents for the current session.

        Returns:
            list: A list of dictionaries containing agent information.
        """
        api_agents_instance = AgentsApi(self.client)
        available_agents = api_agents_instance.get_agents(exclude_offline='true')
        agent_list = []
        for agent in available_agents:
            agent_dict = {
                'id': agent.id,
                'ip': agent.ip,
                'hostname': agent.hostname,
                'status': agent.status
            }
            agent_list.append(agent_dict)
        return agent_list

    def assign_agents_to_network_elements(
        self,
        session_id: str = None,
        agent_map: dict = None,
        unassign_existing_agents: bool = True
    ) -> None:
        """
        Assigns agents to network elements for a given session.

        Args:
            session_id (str, optional): The ID of the session to assign agents to. Defaults to None.
            agent_map (dict, optional): A dictionary mapping network names to agent IDs and IPs. Defaults to None.
        """
        config = self.session_client.get_session_config(session_id=session_id, include='Config, NetworkProfiles, Agents, AttackProfiles, ApplicationProfiles, Applications')
        
        # If user wants to unassign existing agents, unassign them first
        if unassign_existing_agents:
            self.unassign_all_agents_for_session(session_id=session_id)
        
        # If user does not provide agent map, get all available agents and assign them to the first two IP networks
        if not agent_map:
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

    def unassign_all_agents_for_session(
        self,
        session_id: str = None
    ) -> None:
        """
        Unassigns all agents for a given session.
        """
        config = self.session_client.get_session_config(session_id=session_id, include='Config, NetworkProfiles, Agents, AttackProfiles, ApplicationProfiles, Applications')
        for net_profile in config.config.network_profiles:
            for ip_net in net_profile.ip_network_segment:
                if ip_net.agent_assignments:
                    ip_net.agent_assignments.by_id = []
                    ip_net.update()
        print("Unassigning agents completed.\n")    