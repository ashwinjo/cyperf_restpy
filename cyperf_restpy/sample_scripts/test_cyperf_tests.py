import sys
import os

# Ensure the parent directory is in sys.path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyperf_scripts.cyperf_authorization import CyperfAuthorization
from cyperf_scripts.cyperf_test_runs import CyperfTestRuns
import urllib3; urllib3.disable_warnings()

def main():
    cyperf_client = CyperfAuthorization(controller_ip="3.141.193.119", 
                                        refresh_token=None, username="admin", 
                                        password="CyPerf&Keysight#1"
                                        ).get_cyperf_client()
    

    import time
    cyperf_test_runs = CyperfTestRuns(cyperf_client)
    #cyperf_test_runs.start_test_run(session_id="appsec-d09bc450-8472-4e9c-9573-5859ae5ced57")
    #time.sleep(30)
    cyperf_test_runs.stop_test_run(session_id="appsec-9d25e7bb-f165-495e-82b2-278d6c1573d2")
    time.sleep(30)
    cyperf_test_runs.abort_test_run(session_id="appsec-9d25e7bb-f165-495e-82b2-278d6c1573d2")
    
    #print(result)

if __name__ == "__main__":
    main()  