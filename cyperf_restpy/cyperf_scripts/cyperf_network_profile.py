import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf import ApplicationProfile, NetworkProfile, IPNetwork, AgentAssignments, ConfigId


class CyperfNetworkProfile: 
    def __init__(self, client: cyperf.ApiClient):
        """
        Initializes the CyperfNetworkProfile class with a CyPerf API client.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.session_client = SessionsApi(self.client)

    def get_network_profiles_details(self, session_id: str = None) -> dict:
        """
        Get the details of the network profiles for a given session.

        Args:
            session_id (str): The ID of the session to get the network profiles for.

        Returns:
            dict: A dictionary containing the details of the network profiles.
        """
        session = self.session_client.get_session_by_id(session_id=session_id)
        network_profiles = session.config.config.network_profiles[0]
        return network_profiles

    def get_dut_segments_details(self, session_id: str = None) -> dict:
        """
        Get the details of the DUT network segments for a given session.

        Args:
            session_id (str): The ID of the session to get the DUT network segments for.

        Returns:
            dict: A dictionary containing the details of the DUT network segments.
        """
        dut_elements = []
        session = self.session_client.get_session_by_id(session_id=session_id)
        network_profiles = session.config.config.network_profiles[0]
        for dut_seg in network_profiles.dut_network_segment:
            dut_element = {
                'id': dut_seg.id,
                'name': dut_seg.name
            }
            dut_elements.append(dut_element)
        return dut_elements
    
    def get_ip_segments_details(self, session_id: str = None) -> dict:
        """
        Get the details of the IP network segments for a given session.

        Args:
            session_id (str): The ID of the session to get the IP network segments for.

        Returns:
            dict: A dictionary containing the details of the IP network segments.
        """
        ip_elements = []
        session = self.session_client.get_session_by_id(session_id=session_id)
        network_profiles = session.config.config.network_profiles[0]
        for ip_seg in network_profiles.ip_network_segment:
            ip_element = {
                'id': ip_seg.id,
                'name': ip_seg.name
            }
            ip_elements.append(ip_element)
        return ip_elements
    
    def add_ip_network_segment(
        self,
        session_id: str = None,
        ip_segment_name: str = None,
        ip_segment_id: str = None,
        dut_connection_id: str = None,
    ) -> dict:
        """
        Add an IP network segment to the network profile for a given session.

        Args:
            session_id (str): The ID of the session to add the IP network segment to.
            ip_segment_name (str): The name of the IP network segment.
            ip_segment_id (str): The ID of the IP network segment.
            dut_connection_id (str): The DUT connection ID to associate with the IP network segment.

        Returns:
            dict: A dictionary containing the updated details of the IP network segments.
        """
        session = self.session_client.get_session_by_id(session_id=session_id)
        network_profile = session.config.config.network_profiles[0]

        # Make it configurable for one or more DUT
        if not dut_connection_id:
            dut_connection_id = self.get_dut_segments_details(session_id=session_id)[0]['id']

        # Create IP Network Segment Object
        ip_network_segment = cyperf.IPNetwork(name=ip_segment_name, 
                                      id=ip_segment_id, 
                                      dut_connection_id=[dut_connection_id],
                                      agentAssignments=AgentAssignments(by_tag=[]), 
                                      minAgents=1)
        

         # Adding IP Networks to the new network profile
        network_profile.ip_network_segment.append(ip_network_segment)
        network_profile.ip_network_segment.update()
        return self.get_ip_segments_details(session_id=session_id)
    
    def add_dut_network_segment(
        self,
        session_id: str = None,
        dut_segment_name: str = None,
        dut_segment_id: str = None,
    ) -> dict:
        """
        Add a DUT network segment to the network profile for a given session.

        Args:
            session_id (str): The ID of the session to add the DUT network segment to.
            dut_segment_name (str): The name of the DUT network segment.
            dut_segment_id (str): The ID of the DUT network segment.

        Returns:
            dict: A dictionary containing the updated details of the DUT network segments.
        """
        session = self.session_client.get_session_by_id(session_id=session_id)
        network_profile = session.config.config.network_profiles[0]
        
        dut_network_segment = cyperf.DUTNetwork(name=dut_segment_name, id=dut_segment_id)
        network_profile.dut_network_segment.append(dut_network_segment)
        network_profile.dut_network_segment.update()

        return self.get_dut_segments_details(session_id=session_id)
        
