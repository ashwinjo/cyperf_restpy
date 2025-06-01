"""Manages primary and secondary objectives in CyPerf sessions."""

import cyperf
from cyperf.api.sessions_api import SessionsApi
from typing import Optional, Dict, Any, List, Union

class CyperfObjectives:
    """Manages primary objectives and timelines in CyPerf sessions."""
    def __init__(self, client: cyperf.ApiClient) -> None:
        """
        Initializes the CyperfObjectives class with a CyPerf API client.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.session_client = SessionsApi(self.client)

    def set_primary_objective_goals(
        self,
        session_id: Optional[str] = None,
        primary_object_name: str = 'SIMULATED_USERS',
        primary_objective_duration: int = 123,
        primary_objective_goal: int = 1234
    ) -> Union[Dict[str, Any], Exception]:
        """
        Sets the primary objective goals for a given session.

        Args:
            session_id (str, optional): The ID of the session to set objectives for.
            primary_object_name (str, optional): The name of the primary objective.
            primary_objective_duration (int, optional): The duration for the primary objective.
            primary_objective_goal (int, optional): The goal value for the primary objective.

        Returns:
            dict: The updated primary objectives goals.
            Exception: If the operation fails.
        """
        try:
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
            for _ in range(2):
                primary_objective = config.config.traffic_profiles[0].objectives_and_timeline.primary_objective
                primary_objective.type = objective_to_be_configured
                primary_objective.timeline[1].duration = primary_objective_duration
                primary_objective.timeline[1].objective_value = primary_objective_goal
                primary_objective.timeline[1].objective_unit = objectives_unit
                primary_objective.update()
            return self.get_all_primary_objectives_goals(session_id=session_id)
        except Exception as e:
            return Exception(f"Failed to set primary objective goals: {str(e)}")

    def get_all_primary_objectives_goals(self, session_id: Optional[str] = None) -> Union[List[Dict[str, Any]], Exception]:
        """
        Retrieves all primary objective goals for a given session.

        Args:
            session_id (str, optional): The ID of the session to retrieve objectives for.

        Returns:
            list: A list of dictionaries with primary objective details.
            Exception: If the retrieval fails.
        """
        try:
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
                out_list.append({
                    "type":  primary_objective.type.value,
                    "duration": primary_objective.timeline[1].duration,
                    "objective_value": primary_objective.timeline[1].objective_value,
                    "objective_unit": primary_objective.timeline[1].objective_unit
                })
            return out_list
        except Exception as e:
            return Exception(f"Failed to get all primary objectives goals: {str(e)}")

    def get_all_secondary_objectives_goals(self, session_id: Optional[str] = None) -> Union[Dict[str, Any], Exception]:
        """
        Retrieves all secondary objective goals for a given session.

        Args:
            session_id (str, optional): The ID of the session to retrieve secondary objectives for.

        Returns:
            dict: A dictionary with secondary objective details.
            Exception: If the retrieval fails.
        """
        try:
            include = 'Config, TrafficProfiles'
            config = self.session_client.get_session_config(session_id=session_id, include=include)
            secondary_objective = config.config.traffic_profiles[0].objectives_and_timeline.secondary_objective
            out_list = {
                "type":  secondary_objective.type.value,
                "objective_value": secondary_objective.objective_value,
                "objective_unit": secondary_objective.objective_unit
            }
            if out_list:
                return out_list
            else:
                return "No secondary objectives found"
        except Exception as e:
            return Exception(f"Failed to get all secondary objectives goals: {str(e)}")