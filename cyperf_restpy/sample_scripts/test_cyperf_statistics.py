import sys
import os

# Ensure the parent directory is in sys.path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyperf_scripts.cyperf_authorization import CyperfAuthorization
from cyperf_scripts.cyperf_statistics import CyperfStatistics

import urllib3; urllib3.disable_warnings()

def main():
    cyperf_client = CyperfAuthorization(controller_ip="3.141.193.119", 
                                        refresh_token=None, username="admin", 
                                        password="CyPerf&Keysight#1"
                                        ).get_cyperf_client()
    
    cyperf_statistics = CyperfStatistics(cyperf_client)
    # result = cyperf_statistics.show_available_stats(session_id="appsec-9d25e7bb-f165-495e-82b2-278d6c1573d2")
    # print(result)

    result = cyperf_statistics.collect_test_run_stats(session_id="appsec-9d25e7bb-f165-495e-82b2-278d6c1573d2",
                                                      stats_name="http-server-application")

    result = cyperf_statistics.view_stats(session_id="appsec-9d25e7bb-f165-495e-82b2-278d6c1573d2",
                                          processed_stats=result,
                                          stat_name="http-server-application")
    print(result)

    
if __name__ == "__main__":
    main()