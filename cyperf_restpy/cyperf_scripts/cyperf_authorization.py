import cyperf

class CyperfAuthorization:
    """
    Aggregates all CyPerf submodules and provides a unified interface for test automation.
    """
    def __init__(self, controller_ip: str = "3.141.193.119", refresh_token: str = None):
        """
        Initializes the CyperfTestRunner and all submodules with the given controller IP and refresh token.

        Args:
            controller_ip (str, optional): The IP address of the CyPerf controller. Defaults to "3.141.193.119".
            refresh_token (str, optional): The refresh token for authentication. Defaults to None.
        """
        self.controller_ip = controller_ip
        self.refresh_token = refresh_token

    def get_cyperf_client(self) -> cyperf.ApiClient:
        """
        Creates and returns a CyPerf API client for the specified controller IP and refresh token.

        Args:
            controller_ip (str, optional): The IP address of the CyPerf controller. Defaults to "3.141.193.119".
            refresh_token (str, optional): The refresh token for authentication. Defaults to None.

        Returns:
            cyperf.ApiClient: The configured CyPerf API client.
        """
        config = cyperf.Configuration(host=f"https://{self.controller_ip}", 
                                      refresh_token=self.refresh_token)
        config.verify_ssl = False
        return cyperf.ApiClient(config) 
    
    