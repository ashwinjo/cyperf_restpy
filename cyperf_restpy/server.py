from mcp.server.fastmcp import FastMCP
import sys

from cyperf_scripts.cyperf_authorization import CyperfAuthorization
from cyperf_scripts.cyperf_sessions import CyperfSessions
from cyperf_scripts.cyperf_network_profile import CyperfNetworkProfile
from cyperf_scripts.cyperf_agents import CyperfAgents
from cyperf_scripts.cyperf_test_runs import CyperfTestRuns
from cyperf_scripts.cyperf_statistics import CyperfStatistics
from cyperf_scripts.cyperf_applications import CyperfApplications


def get_cyperf_client():
        try: 
            return CyperfAuthorization(
                controller_ip="3.141.193.119",
                refresh_token=None,
                username="admin",
                password="CyPerf&Keysight#1"
            ).get_cyperf_client()
        except Exception as e:
            print(f"[lifespan error] Failed to create cyperf client: {e}", file=sys.stderr)
            raise

# Create MCP app with lifespan
mcp = FastMCP("CyPerf RESTPy MCP Server")


@mcp.tool()
def get_all_cyperf_sessions() -> str:
    """
    Gets all CyPerf sessions.
    Returns:
        A list of CyPerf sessions.
        Example:
            [
                {
                    "id": "appsec-f949b112-6059-42dd-9e4c-2cdd67739b75",    
                    "name": "CyPerf Session 1",
                    "config_name": "CyPerf Config 1",
                    "config_url": "https://cyperf.com/config/1"
                },
                {
                    "id": "appsec-f949b112-6059-42dd-9e4c-2cdd67739b75",        
                    "name": "CyPerf Session 2",
                    "config_name": "CyPerf Config 2",
                    "config_url": "https://cyperf.com/config/2"
                }
            ]
    """
    # Call the factory function from lifespan to get the client
    cyperf_client = get_cyperf_client()
    cyperf_sessions = CyperfSessions(cyperf_client)
    return cyperf_sessions.get_all_sessions()

@mcp.tool()
def get_cyperf_session_by_id(session_id: str) -> str:
    """
    Gets a CyPerf session by ID.
    Args:
        session_id: The ID of the session to get.
        Example:
            "appsec-f949b112-6059-42dd-9e4c-2cdd67739b75"
        Returns:
            A dictionary with the session ID and name.
    """
    cyperf_client = get_cyperf_client()
    cyperf_sessions = CyperfSessions(cyperf_client)
    return cyperf_sessions.get_session_by_id(session_id)

@mcp.tool()
def create_blank_cyperf_session(session_name: str) -> str:
    """
    Creates a CyPerf session.
    Args:
        session_name: The name of the session to create.
        Example:
            "appsec-f949b112-6059-42dd-9e4c-2cdd67739b75"
        Returns:
            A dictionary with the session ID and name.
    """
    cyperf_client = get_cyperf_client()
    cyperf_sessions = CyperfSessions(cyperf_client)
    return cyperf_sessions.create_session(session_name=session_name)

@mcp.tool()
def create_cyperf_session_from_config(session_name: str, config_name: str) -> str:
    """
    Creates a CyPerf session from a configuration.
    Args:
        session_name: The name of the session to create.
        config_name: The name of the configuration to use.
        Example:
            "appsec-f949b112-6059-42dd-9e4c-2cdd67739b75"
        Returns:
            A dictionary with the session ID and name.
    """
    cyperf_client = get_cyperf_client()
    cyperf_sessions = CyperfSessions(cyperf_client)
    return cyperf_sessions.create_session(session_name=session_name, config_name=config_name)

@mcp.tool()
def show_network_profile(session_id: str) -> str:
    """
    Shows the IP network segments for a CyPerf session.
    Args:
        session_id: The ID of the session to show the network profile for.
        Example:
            "appsec-f949b112-6059-42dd-9e4c-2cdd67739b75"
        Returns:
            A list of IP network segments.
    """
    cyperf_client = get_cyperf_client()
    network_profile = CyperfNetworkProfile(cyperf_client)
    return network_profile.get_ip_segments_details(session_id)

@mcp.tool()
def show_available_agents(session_id: str) -> str:
    """
    Shows the DUT segments for a CyPerf session.
    Args:
        session_id: The ID of the session to show the available agents for.
        Example:
            "appsec-f949b112-6059-42dd-9e4c-2cdd67739b75"
        Returns:
            A list of available agents.
            Example:
                [
                    {
                        "id": "agent_id1",
                        "ip": "agent_ip1"
                    },
                    {
                        "id": "agent_id2",
                        "ip": "agent_ip2"
                    }
                ]
    """
    cyperf_client = get_cyperf_client()
    agents = CyperfAgents(cyperf_client)
    return agents.get_available_agents()

@mcp.tool()
def assign_agents_to_network_elements(session_id: str, 
                                      agent_map: dict,
                                      unassign_existing_agents: bool = True) -> str:
    """
    Assigns agents to network elements for a CyPerf session.
    Example:
        {
            "Network1": ["agent_id1", "agent_ip1"],
            "Network2": ["agent_id2", "agent_ip2"]
        }
    Args:
        session_id: The ID of the session to assign agents to.
        agent_map: A dictionary mapping network names to agent IDs and IPs.     
        unassign_existing_agents: Whether to unassign existing agents before assignment.
    """
    cyperf_client = get_cyperf_client()
    agents = CyperfAgents(cyperf_client)
    return agents.assign_agents_to_network_elements(session_id, agent_map)

@mcp.tool()
def start_test(session_id: str) -> str:
    """
    Starts a test for a CyPerf session.
    """
    cyperf_client = get_cyperf_client()
    test = CyperfTestRuns(cyperf_client)
    return test.start_test_run(session_id)

@mcp.tool()
def stop_test(session_id: str) -> str:
    """
    Stops a test for a CyPerf session.
    """
    cyperf_client = get_cyperf_client()
    test = CyperfTestRuns(cyperf_client)
    return test.stop_test_run(session_id)

@mcp.tool()
def get_test_statistics(session_id: str, stat_name: str) -> str:
    """
    Gets the statistics for a test for a CyPerf session.
    Args:
        session_id: The ID of the session to get the statistics for.
        Example:
            "appsec-f949b112-6059-42dd-9e4c-2cdd67739b75"
        Returns:
            A dictionary with the statistics.   
    """
    cyperf_client = get_cyperf_client()
    statistics = CyperfStatistics(cyperf_client)
    return statistics.view_stats(session_id, stat_name=stat_name)

@mcp.tool()
def get_available_stats(session_id: str) -> str:
    """
    Gets the available statistics for a test for a CyPerf session.
    Args:
        session_id: The ID of the session to get the available statistics for.
        Example:
            "appsec-f949b112-6059-42dd-9e4c-2cdd67739b75"
        Returns:
            A list of available statistics.
    """
    cyperf_client = get_cyperf_client()
    statistics = CyperfStatistics(cyperf_client)
    return statistics.show_available_stats(session_id)

@mcp.tool()
def get_all_cyperf_applications_avaialble(keywords: str) -> str:
    """
    Gets the available applications for a test for a CyPerf session.
    Args:
        keywords: The keywords to filter the applications by.
        Example:
            "http"
        Returns:
            A list of available applications.
    """
    cyperf_client = get_cyperf_client()
    applications = CyperfApplications(cyperf_client)
    return applications.get_all_cyperf_applications_avaialble(keyword=None)


if __name__ == "__main__":
    #print(get_all_cyperf_sessions())
    mcp.run(transport="stdio")
