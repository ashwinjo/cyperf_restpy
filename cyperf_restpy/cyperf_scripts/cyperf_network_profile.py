"""CyPerf Network Profile management utilities."""

import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf import ApplicationProfile, NetworkProfile, IPNetwork, AgentAssignments, ConfigId
from typing import Optional, Dict, Any, List, Union


class CyperfNetworkProfile:
    """CyPerf Network Profile management utilities."""
    def __init__(self, client: cyperf.ApiClient) -> None:
        """Initializes the CyperfNetworkProfile class with a CyPerf API client."""
        self.client = client
        self.session_client = SessionsApi(self.client)

    def get_network_profiles_details(self, session_id: Optional[str] = None) -> Union[Dict[str, Any], Exception]:
        """Get the details of the network profiles for a given session."""
        try:
            session = self.session_client.get_session_by_id(session_id=session_id)
            network_profiles = session.config.config.network_profiles[0]
            return network_profiles
        except Exception as e:
            return Exception(f"Failed to get network profiles details: {str(e)}")

    def get_dut_segments_details(self, session_id: Optional[str] = None) -> Union[List[Dict[str, Any]], Exception]:
        """Get the details of the DUT network segments for a given session."""
        try:
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
        except Exception as e:
            return Exception(f"Failed to get DUT segments details: {str(e)}")
    
    def get_ip_segments_details(self, session_id: Optional[str] = None) -> Union[List[Dict[str, Any]], Exception]:
        """Get the details of the IP network segments for a given session."""
        try:
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
        except Exception as e:
            return Exception(f"Failed to get IP segments details: {str(e)}")
    
    def add_ip_network_segment(
        self,
        session_id: Optional[str] = None,
        ip_segment_name: Optional[str] = None,
        ip_segment_id: Optional[str] = None,
        dut_connection_id: Optional[str] = None,
    ) -> Union[Dict[str, Any], Exception]:
        """Add an IP network segment to the network profile for a given session."""
        try:
            session = self.session_client.get_session_by_id(session_id=session_id)
            network_profile = session.config.config.network_profiles[0]
            if not dut_connection_id:
                dut_segments = self.get_dut_segments_details(session_id=session_id)
                if isinstance(dut_segments, Exception):
                    return dut_segments
                dut_connection_id = dut_segments[0]['id']
            ip_network_segment = cyperf.IPNetwork(
                name=ip_segment_name,
                id=ip_segment_id,
                dut_connection_id=[dut_connection_id],
                agentAssignments=cyperf.AgentAssignments(by_tag=[]),
                minAgents=1
            )
            network_profile.ip_network_segment.append(ip_network_segment)
            network_profile.ip_network_segment.update()
            return self.get_ip_segments_details(session_id=session_id)
        except Exception as e:
            return Exception(f"Failed to add IP network segment: {str(e)}")
    
    def add_dut_network_segment(
        self,
        session_id: Optional[str] = None,
        dut_segment_name: Optional[str] = None,
        dut_segment_id: Optional[str] = None,
    ) -> Union[Dict[str, Any], Exception]:
        """Add a DUT network segment to the network profile for a given session."""
        try:
            session = self.session_client.get_session_by_id(session_id=session_id)
            network_profile = session.config.config.network_profiles[0]
            dut_network_segment = cyperf.DUTNetwork(name=dut_segment_name, id=dut_segment_id)
            network_profile.dut_network_segment.append(dut_network_segment)
            network_profile.dut_network_segment.update()
            return self.get_dut_segments_details(session_id=session_id)
        except Exception as e:
            return Exception(f"Failed to add DUT network segment: {str(e)}")
        
