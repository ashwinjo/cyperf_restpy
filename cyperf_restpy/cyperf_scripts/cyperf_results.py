"""CyPerf test results management utilities."""

import cyperf
from cyperf.api.test_results_api import TestResultsApi
from cyperf.api.sessions_api import SessionsApi
from typing import Optional, Dict, Any, Union

class CyperfResults:
    """CyPerf test results management utilities."""
    def __init__(self, client: cyperf.ApiClient) -> None:
        """
        Initialize the CyperfResults class.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.test_results_api = TestResultsApi(self.client)
        self.session_client = SessionsApi(self.client)

    def start_result_generate_all(self, session_id: str) -> Union[Dict[str, str], Exception]:
        """
        Start the generation of all results for a given session.

        Args:
            session_id (str): The ID of the session to generate results for.

        Returns:
            dict: A dictionary with the saved file location.
            Exception: If the generation fails.
        """
        try:
            test_id = self._get_test_id(session_id=session_id)
            generation_op = self.test_results_api.start_result_generate_all(result_id=test_id)
            return {"saved_file_location": generation_op.await_completion()}
        except Exception as e:
            return Exception(f"Failed to generate all results: {str(e)}")

    def start_result_generate_results(self, session_id: str) -> Union[Dict[str, str], Exception]:
        """
        Start the generation of results for a given session.

        Args:
            session_id (str): The ID of the session to generate results for.

        Returns:
            dict: A dictionary with the saved file location.
            Exception: If the generation fails.
        """
        try:
            test_id = self._get_test_id(session_id=session_id)
            generation_op = self.test_results_api.start_result_generate_results(result_id=test_id)
            return {"saved_file_location": generation_op.await_completion()}
        except Exception as e:
            return Exception(f"Failed to generate results: {str(e)}")
        
    def load_all_results(self, session_id: Optional[str] = None) -> Union[Dict[str, Any], Exception]:
        """
        Loads the results for a given session.

        Args:
            session_id (str, optional): The ID of the session to load the results for.

        Returns:
            dict: A dictionary with the loaded results.
        """
        try:
            test_id = self._get_test_id(session_id=session_id)
            results = self.test_results_api.start_result_load(result_id=test_id)
            return {"loaded_results": results.await_completion()}
        except Exception as e:
            return Exception(f"Failed to load results: {str(e)}")
    
    def show_all_available_results(self, session_id: Optional[str] = None) -> Union[Dict[str, Any], Exception]:
        """
        Get all the available results.

        Args:
            session_id (str, optional): The ID of the session to get the results for.

        Returns:
            dict: A dictionary with the results.
        """
        try:
            results = self.test_results_api.get_results()
            #import pdb; pdb.set_trace()
            results_list = [{"id": result.id, 
                             "test_id": result.test_name, 
                             "test_name":result.display_name} for result in results.data]
            return {"results": results_list}
        except Exception as e:
            return Exception(f"Failed to get results: {str(e)}")

    def _get_test_id(self, session_id: Optional[str] = None) -> Union[str, Exception]:
        """
        Retrieve the test ID for a given session.

        Args:
            session_id (str, optional): The ID of the session to retrieve the test ID for.

        Returns:
            str: The test ID.
            Exception: If the retrieval fails.
        """
        try:
            test = self.session_client.get_session_test(session_id=session_id)
            test_id = [a[1] for a in test if a[0] == 'test_id'][0]
            return test_id
        except Exception as e:
            return Exception(f"Failed to get test id: {str(e)}")
   