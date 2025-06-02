
import sys
import os

# Ensure the parent directory is in sys.path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyperf_scripts.cyperf_authorization import CyperfAuthorization
from cyperf_scripts.cyperf_licensing import CyperfLicensing

import urllib3

urllib3.disable_warnings()

def main() -> None:
    """Main function to test Cyperf Licensing API."""
    try:
        cyperf_client = CyperfAuthorization(
            controller_ip="3.141.193.119",
            refresh_token=None,
            username="admin",
            password="CyPerf&Keysight#1"
        ).get_cyperf_client()

        cyperf_licensing = CyperfLicensing(cyperf_client)
        
        result = cyperf_licensing.get_host_id()
        print(result)


        """Failed to get installed licenses: 1 validation error for License
        links
        Input should be a valid list [type=list_type, input_value=None, input_type=NoneType]
            For further information visit https://errors.pydantic.dev/2.11/v/list_type
        """
        result = cyperf_licensing.get_installed_licenses()
        print(result)

        result = cyperf_licensing.get_license_features()
        print(result)
    
        result = cyperf_licensing.get_license_servers() 
        print(result)

        result = cyperf_licensing.add_license_server(license_server="3.141.193.119", 
                                                     license_user="admin", 
                                                     license_password="mypassword")
        print(result)

        result = cyperf_licensing.activate_license(activation_code="1234567890", 
                                                   quantity=1)
        print(result)

        result = cyperf_licensing.deactivate_licenses(activation_code="1234567890", 
                                                      quantity=1)   
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()