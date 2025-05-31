"""
CyPerf authorization and API client configuration utilities.

This module provides the CyperfAuthorization class for handling authentication and API client creation for CyPerf.
"""

import cyperf
from typing import Optional

class CyperfAuthorization:
    """
    Handles CyPerf authorization and client configuration.

    Args:
        controller_ip (str): The IP address of the CyPerf controller.
        refresh_token (str, optional): The refresh token for authentication.
        username (str, optional): The username for authentication.
        password (str, optional): The password for authentication.
    """
    def __init__(
        self,
        controller_ip: str = "3.141.193.119",
        refresh_token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> None:
        """
        Initializes the CyperfAuthorization instance.

        Args:
            controller_ip (str): The IP address of the CyPerf controller.
            refresh_token (str, optional): The refresh token for authentication.
            username (str, optional): The username for authentication.
            password (str, optional): The password for authentication.
        """
        self.controller_ip = controller_ip
        self.refresh_token = refresh_token
        self.username = username
        self.password = password

    def get_cyperf_client(self) -> cyperf.ApiClient:
        """
        Create and return a CyPerf API client.

        Returns:
            cyperf.ApiClient: A configured CyPerf API client, or Exception on error.
        """
        try:
            config = cyperf.Configuration(
                host=f"https://{self.controller_ip}",
                refresh_token=self.refresh_token,
                username=self.username,
                password=self.password
            )
            config.verify_ssl = False
            return cyperf.ApiClient(config)
        except Exception as e:
            return Exception(f"Failed to create CyPerf API client: {str(e)}")
       
    