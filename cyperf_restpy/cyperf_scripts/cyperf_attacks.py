"""
CyPerf attack management utilities.

This module provides the CyperfAttacks class for managing attack profiles and attacks in CyPerf sessions.
"""

import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.application_resources_api import ApplicationResourcesApi
from typing import Optional, Dict, Any, List, Union

class CyperfAttacks:
    """
    Handles attack management for CyPerf sessions.

    Args:
        client (cyperf.ApiClient): The CyPerf API client instance.
    """
    def __init__(self, client: cyperf.ApiClient) -> None:
        """
        Initializes the CyperfAttacks class with a CyPerf API client.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.session_client = SessionsApi(self.client)

    def add_attack_profile_to_session(
        self,
        session_id: Optional[str] = None,
        attack_profile_name: str = 'Attack Profile'
    ) -> Union[Dict[str, str], Exception]:
        """
        Adds an attack profile to a session's attack profiles.

        Args:
            session_id (str, optional): The ID of the session to add the attack profile to.
            attack_profile_name (str, optional): The name of the attack profile.

        Returns:
            dict: A message indicating the result of the operation.
        """
        try:
            session = self.session_client.get_session_by_id(session_id=session_id)
            attack_profiles = session.config.config.attack_profiles
            attack_profiles.append(cyperf.AttackProfile(Name=attack_profile_name))
            attack_profiles.update()
            return {"message": f"Attack profile added to session {session_id} - {session.name}"}
        except Exception as e:
            return Exception(f"Failed to add attack profile: {str(e)}")

    def add_attack_to_attack_profile(
        self,
        session_id: Optional[str] = None,
        attack_profile_name: str = 'Attack Profile',
        attack_name: Optional[str] = None
    ) -> Union[Dict[str, str], Exception]:
        """
        Adds an attack to an attack profile.

        Args:
            session_id (str, optional): The ID of the session to add the attack to.
            attack_profile_name (str, optional): The name of the attack profile.
            attack_name (str, optional): The name of the attack to add.

        Returns:
            dict: A message indicating the result of the operation.
        """
        try:
            application_resources_api = ApplicationResourcesApi(self.client)
            take = 1
            skip = 0
            search_col = "Name"
            search_val = attack_name
            sort = 'Name:asc'
            api_application_attacks_response = application_resources_api.get_resources_attacks(
                take=take,
                skip=skip,
                search_col=search_col,
                search_val=search_val,
                filter_mode=None,
                sort=sort
            )
            if api_application_attacks_response.data[0].id:
                app_id = api_application_attacks_response.data[0].id
                config = self.session_client.get_session_config(
                    session_id=session_id,
                    include='Config, TrafficProfiles, ApplicationProfiles, AttackProfiles'
                )
                config.config.attack_profiles[0].attacks.append(cyperf.Attack(name=attack_name))
                config.config.attack_profiles[0].attacks.update()
            return {"message": f"Attack {attack_name} added to session {session_id}"}
        except Exception as e:
            return Exception(f"Failed to add attack to attack profile: {str(e)}")

    def get_all_attack_for_session(
        self,
        session_id: Optional[str] = None
    ) -> Union[List[str], Exception]:
        """
        Retrieves all attack names for the first attack profile in a session.

        Args:
            session_id (str, optional): The ID of the session to query.

        Returns:
            list: A list of attack names in the session.
        """
        try:
            session = self.session_client.get_session_by_id(session_id=session_id)
            return [attack.name for attack in session.config.config.attack_profiles[0].attacks]
        except Exception as e:
            return Exception(f"Failed to get attacks for session: {str(e)}")

    def get_all_attack_primary_objectives_goals_for_session(
        self,
        session_id: Optional[str] = None
    ) -> Union[Dict[str, Any], Exception]:
        """
        Retrieves the primary objectives and goals for the first attack profile in a session.

        Args:
            session_id (str, optional): The ID of the session to query.

        Returns:
            dict: A dictionary containing the attack rate, max concurrent attack, and duration.
        """
        try:
            session = self.session_client.get_session_by_id(session_id=session_id)
            obj_and_time_line = session.config.config.attack_profiles[0].objectives_and_timeline
            return {
                'attack_rate': obj_and_time_line.timeline_segments[0].attack_rate,
                'max_concurrent_attack': obj_and_time_line.timeline_segments[0].max_concurrent_attack,
                'duration': obj_and_time_line.timeline_segments[0].duration
            }
        except Exception as e:
            return Exception(f"Failed to get attack primary objectives and goals: {str(e)}")

    def set_attack_primary_objectives_goals_for_session(
        self,
        session_id: Optional[str] = None,
        attack_rate: Optional[int] = None,
        max_concurrent_attack: Optional[int] = None,
        duration: Optional[int] = None
    ) -> Union[Dict[str, str], Exception]:
        """
        Sets the attack primary objectives and goals for a given session.

        Args:
            session_id (str, optional): The ID of the session to update.
            attack_rate (int, optional): The attack rate to set.
            max_concurrent_attack (int, optional): The max concurrent attack to set.
            duration (int, optional): The duration to set.

        Returns:
            dict: A message indicating the result of the operation.
        """
        try:
            session = self.session_client.get_session_by_id(session_id=session_id)
            session.config.config.attack_profiles[0].objectives_and_timeline.timeline_segments[0].attack_rate = attack_rate
            session.config.config.attack_profiles[0].objectives_and_timeline.timeline_segments[0].max_concurrent_attack = max_concurrent_attack
            session.config.config.attack_profiles[0].objectives_and_timeline.timeline_segments[0].duration = duration
            session.config.config.attack_profiles[0].objectives_and_timeline.update()
            return {"message": f"Attack primary objectives and goals set for session {session_id}"}
        except Exception as e:
            return Exception(f"Failed to set attack primary objectives and goals: {str(e)}")

    def start_attack(self, session_id: Optional[str] = None, attack_type: Optional[str] = None) -> Union[Dict[str, Any], Exception]:
        """
        Starts an attack for a given session and attack type.

        Args:
            session_id (str, optional): The ID of the session to start the attack for.
            attack_type (str, optional): The type of attack to start.

        Returns:
            dict: A message indicating the result of the operation.
        """
        try:
            # Replace with actual attack logic
            return {"message": f"Attack {attack_type} started for session {session_id}"}
        except Exception as e:
            return Exception(f"Failed to start attack: {str(e)}")

    # Add more methods as needed, following the same pattern 