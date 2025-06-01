"""Handles starting, stopping, and aborting test runs in CyPerf sessions."""

import cyperf
from cyperf.api.test_operations_api import TestOperationsApi
from typing import Optional, Dict, Any, Union

class CyperfTestRuns:
    """Handles starting, stopping, and aborting test runs in CyPerf sessions."""
    def __init__(self, client: cyperf.ApiClient) -> None:
        """
        Initializes the CyperfTestRuns class with a CyPerf API client.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client

    def start_test_run(self, session_id: Optional[str] = None) -> Union[Dict[str, str], Exception]:
        """
        Starts a test run for a given session.

        Args:
            session_id (str, optional): The ID of the session to start the test run for.

        Returns:
            dict: A message indicating the result of the operation.
            Exception: If the start fails.
        """
        try:
            test_execution_api = TestOperationsApi(self.client)
            start_run_operation = test_execution_api.start_test_run_start(session_id=session_id)
            resp = start_run_operation.await_completion()
            return {"message": f"Test run started for session {session_id}"}
        except Exception as e:
            return Exception(f"Failed to start test run: {str(e)}")

    def stop_test_run(self, session_id: Optional[str] = None) -> Union[Dict[str, str], Exception]:
        """
        Stops a test run for a given session.

        Args:
            session_id (str, optional): The ID of the session to stop the test run for.

        Returns:
            dict: A message indicating the result of the operation.
            Exception: If the stop fails.
        """
        try:
            test_execution_api = TestOperationsApi(self.client)
            stop_run_operation = test_execution_api.start_test_run_stop(session_id=session_id)
            resp = stop_run_operation.await_completion()
            return {"message": f"Test run stopped for session {session_id}"}
        except Exception as e:
            return Exception(f"Failed to stop test run: {str(e)}")

    def abort_test_run(self, session_id: Optional[str] = None) -> Union[Dict[str, str], Exception]:
        """
        Aborts a test run for a given session.

        Args:
            session_id (str, optional): The ID of the session to abort the test run for.

        Returns:
            dict: A message indicating the result of the operation.
            Exception: If the abort fails.
        """
        try:
            test_execution_api = TestOperationsApi(self.client)
            abort_run_operation = test_execution_api.start_test_run_abort(session_id=session_id)
            resp = abort_run_operation.await_completion()
            return {"message": f"Test run aborted for session {session_id}"}
        except Exception as e:
            return Exception(f"Failed to abort test run: {str(e)}") 