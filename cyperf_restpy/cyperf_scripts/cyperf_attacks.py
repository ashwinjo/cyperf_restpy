import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.application_resources_api import ApplicationResourcesApi

class CyperfAttacks:
    """
    Manages attack profiles and attack assignment in CyPerf sessions.
    """
    def __init__(self, client: cyperf.ApiClient):
        """
        Initializes the CyperfAttacks class with a CyPerf API client.
                
        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.session_client = SessionsApi(self.client)

    def add_attack_profile_to_session(
        self,
        session_id: str = None,
        attack_profile_name: str = 'Attack Profile'
    ) -> dict:
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

    def add_attack_to_attack_profile(
        self,
        session_id: str = None,
        attack_profile_name: str = 'Attack Profile',
        attack_name: str = None
    ) -> None:
        """
        Adds an attack to an attack profile.

        Args:
            session_id (str, optional): The ID of the session to add the attack to. Defaults to None.
            attack_profile_name (str, optional): The name of the attack profile. Defaults to None.
            attack_name (str, optional): The name of the attack to add. Defaults to None.
        """
        print("Adding the applications...")
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

    def get_all_attack_for_session(
        self,
        session_id: str = None
    ) -> list:
        """
        Retrieves all attack names for the first attack profile in a session.

        Args:
            session_id (str, optional): The ID of the session to query. Defaults to None.

        Returns:
            list: A list of attack names in the session.
        """
        session = self.session_client.get_session_by_id(session_id=session_id)
        return [attack.name for attack in session.config.config.attack_profiles[0].attacks]

    def get_all_attack_primary_objectives_goals_for_session(
        self,
        session_id: str = None
    ) -> dict:
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