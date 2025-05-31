import cyperf
from cyperf.api.test_results_api import TestResultsApi
from cyperf.api.sessions_api import SessionsApi 

class CyperfResults:
    def __init__(self, client: cyperf.ApiClient):
        """
        Initialize the CyperfResults class.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.test_results_api = TestResultsApi(self.client)
        self.session_client = SessionsApi(self.client)

    def start_result_generate_all(self, session_id: str):
        """
        Start the generation of all results for a given session.

        Args:
            session_id (str): The ID of the session to generate results for.

        Returns:
            dict: A dictionary containing the saved file location.
        """
        test_id = self._get_test_id(session_id=session_id)
        generation_op = self.test_results_api.start_result_generate_all(result_id=test_id)
        return {"saved_file_location": generation_op.await_completion()}
    
    def start_result_generate_results(self, session_id: str):   
        """
        Start the generation of results for a given session.

        Args:
            session_id (str): The ID of the session to generate results for.

        Returns:
            dict: A dictionary containing the saved file location.
        """
        test_id = self._get_test_id(session_id=session_id)
        generation_op = self.test_results_api.start_result_generate_results(result_id=test_id)
        return {"saved_file_location": generation_op.await_completion()}
    
    def _get_test_id(self, session_id: str = None):
        test = self.session_client.get_session_test(session_id=session_id)
        self.test_id = [a[1] for a in test if a[0] == 'test_id'][0]
        return self.test_id
   