"""CyPerf Licensing management utilities."""

import cyperf
from cyperf.api.licensing_api import LicensingApi
from cyperf.api.license_servers_api import LicenseServersApi
from cyperf.models.license_server_metadata import LicenseServerMetadata


from typing import Optional, Dict, Any, List, Union
from cyperf.models.fulfillment_request import FulfillmentRequest

class CyperfLicensing:
    """CyPerf Licensing management utilities."""
    def __init__(self, client: cyperf.ApiClient) -> None:
        """
        Initializes the CyperfLicensing class with a CyPerf API client.
        Args:
            client (cyperf.ApiClient): The CyPerf API client.           
        """
        self.client = client
        self.licensing_api = LicensingApi(self.client)
        self.license_servers_api = LicenseServersApi(self.client)
    
    def get_host_id(self): 
        """
        Get the host ID for the current controller as license server.
        Returns:
            dict: A dictionary with the host ID.
        """
        try:
            host_id = self.licensing_api.get_hostid()
            return {"host_id": host_id.hostid}
        except Exception as e:
            return Exception(f"Failed to get host ID: {str(e)}")
        
    def get_installed_licenses(self):
        """
        Get the installed licenses for the current controller as license server.
        Returns:
            dict: A dictionary with the installed licenses.
        """
        try:
            installed_licenses = self.licensing_api.get_installed_licenses()
            import pdb; pdb.set_trace()
            return {"installed_licenses": installed_licenses.data}
        except Exception as e:
            return Exception(f"Failed to get installed licenses: {str(e)}")

    def get_license_features(self):
        """
        Get the license features for the current controller as license server.
        Returns:
            dict: A dictionary with the license features.
        """
        try:
            license_features = self.licensing_api.get_counted_feature_stats()
            return {"license_features": license_features}
        except Exception as e:
            return Exception(f"Failed to get license features: {str(e)}")
    
    def activate_license(self, activation_code: str, quantity: int = 1):
        """
        Activate a license for the current machine.
        Args:
            activation_code (str): The activation code to activate.
            quantity (int): The quantity to activate.
        Returns:
            dict: A dictionary with the activated license.
        """
        try:
            fulfillment_request = FulfillmentRequest(
                activation_code=activation_code,
                quantity=quantity
            )
            self.licensing_api.activate_licenses(fulfillment_request=[fulfillment_request])
            return {"license_activated": True}
        except Exception as e:
            return Exception(f"Failed to activate license: {str(e)}")
    
    def deactivate_licenses(self, activation_code: str, quantity: int = 1):
        """
        Deactivate licenses for the current controller as license server.
        Args:
            activation_code (str): The activation code to deactivate.
            quantity (int): The quantity to deactivate.
        Returns:
            dict: A dictionary with the deactivated licenses.
        """
        try:
            fulfillment_request = FulfillmentRequest(
                activation_code=activation_code,
                quantity=quantity
            )
            self.licensing_api.deactivate_licenses(fulfillment_request=[fulfillment_request])
            return {"licenses_deactivated": True}
        except Exception as e:
            return Exception(f"Failed to deactivate licenses: {str(e)}")
        
    def get_license_server_status(self):
        """
        Get the license server status for the current controller as license server.
        Returns:
            dict: A dictionary with the license server status.
        """
        try:
            license_server_status = self.licensing_api.create_license_server()
            return {"license_server_status": license_server_status}
        except Exception as e:
            return Exception(f"Failed to get license server status: {str(e)}")
    

    def get_license_servers(self):
        """
        Get the license servers for the current controller as license server.
        Returns:
            dict: A dictionary with the license servers.
        """
        try:
            license_servers = self.license_servers_api.get_license_servers()
            return [{"host_name": server.host_name, "id": server.id} for server in license_servers]
            
        except Exception as e:
            return Exception(f"Failed to get license servers: {str(e)}")
        
    def add_license_server(self, license_server: str, license_user: str, license_password: str):
        """
        Get the license servers for the current controller as license server.
        Returns:
            dict: A dictionary with the license servers.
        """
        try:
            lServer = LicenseServerMetadata(host_name=license_server,
                                            trust_new=True,
                                            user=license_user,
                                            password=license_password,
                                            id=None)
            self.license_servers_api.create_license_servers(lServer)
            return {"license_servers_after_addition": self.get_license_servers()}
        except Exception as e:
            return Exception(f"Failed to get license servers: {str(e)}")
        
    def delete_license_server(self, license_server_id: str):
        """
        Delete a license server for the current controller as license server.
        Returns:
            dict: A dictionary with the deleted license server.
        """
        try:
            self.license_servers_api.delete_license_server(license_server_id=license_server_id)
            return {"license_servers_after_deletion": self.get_license_servers()}
        except Exception as e:
            return Exception(f"Failed to delete license server: {str(e)}")
        
    def get_license_server_by_id(self, license_server_id: str):
        """
        Get a license server by ID for the current controller as license server.
        Returns:
            dict: A dictionary with the license server.
        """     
        try:
            license_server = self.license_servers_api.get_license_server_by_id(license_server_id=license_server_id)
            return {"license_server": license_server}
        except Exception as e:
            return Exception(f"Failed to get license server by ID: {str(e)}")
        
    def update_license_server(self, license_server_id: str, license_server: str, license_user: str, license_password: str):
        """
        Update a license server for the current controller as license server.
        Returns:
            dict: A dictionary with the updated license server.
        """
        try:
            lServer = LicenseServerMetadata(host_name=license_server,
                                            trust_new=True,
                                            user=license_user,
                                            password=license_password,
                                            id=None)
            license_server = self.license_servers_api.patch_license_server(license_server_id=license_server_id, license_server_metadata=lServer)
            return {"license_server": license_server}
        except Exception as e:
            return Exception(f"Failed to update license server: {str(e)}")