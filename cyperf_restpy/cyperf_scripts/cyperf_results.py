"""CyPerf test results management utilities."""

import cyperf
from cyperf.api.test_results_api import TestResultsApi
from cyperf.api.sessions_api import SessionsApi
from typing import Optional, Dict, Any, Union

class CyperfResults:
    """CyPerf test results management utilities."""
    def __init__(self, client: cyperf.ApiClient) -> None:
        """Initialize the CyperfResults class."""
        self.client = client
        self.test_results_api = TestResultsApi(self.client)
        self.session_client = SessionsApi(self.client)

    def start_result_generate_all(self, session_id: str) -> Union[Dict[str, str], Exception]:
        """Start the generation of all results for a given session."""
        try:
            test_id = self._get_test_id(session_id=session_id)
            generation_op = self.test_results_api.start_result_generate_all(result_id=test_id)
            return {"saved_file_location": generation_op.await_completion()}
        except Exception as e:
            return Exception(f"Failed to generate all results: {str(e)}")

    def start_result_generate_results(self, session_id: str) -> Union[Dict[str, str], Exception]:
        """Start the generation of results for a given session."""
        try:
            test_id = self._get_test_id(session_id=session_id)
            generation_op = self.test_results_api.start_result_generate_results(result_id=test_id)
            return {"saved_file_location": generation_op.await_completion()}
        except Exception as e:
            return Exception(f"Failed to generate results: {str(e)}")

    def _get_test_id(self, session_id: Optional[str] = None) -> Union[str, Exception]:
        try:
            test = self.session_client.get_session_test(session_id=session_id)
            test_id = [a[1] for a in test if a[0] == 'test_id'][0]
            return test_id
        except Exception as e:
            return Exception(f"Failed to get test id: {str(e)}")
   