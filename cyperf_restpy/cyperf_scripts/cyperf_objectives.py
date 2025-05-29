import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.configurations_api import ConfigurationsApi

class CyperfObjectives:
    """
    Manages primary objectives and timelines in CyPerf sessions.
    """
    def __init__(self, client: cyperf.ApiClient):
        """
        Initializes the CyperfObjectives class with a CyPerf API client.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.session_client = SessionsApi(self.client)

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

    def get_all_primary_objectives_goals(
        self,
        session_id: str = None
    ) -> list:
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