import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.test_operations_api import TestOperationsApi

class CyperfTestRuns:
    """
    Handles starting, stopping, and aborting test runs in CyPerf sessions.
    """
    def __init__(self, client: cyperf.ApiClient):
        """
        Initializes the CyperfTestRuns class with a CyPerf API client.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client

    def start_test_run(
        self,
        session_id: str = None
    ) -> dict:
        """
        Starts a test run for a given session.

        Args:
            session_id (str, optional): The ID of the session to start the test run for. Defaults to None.

        Returns:
            dict: A message indicating the result of the operation.
        """
        test_execution_api = TestOperationsApi(self.client)
        start_run_operation = test_execution_api.start_test_run_start(session_id=session_id)
        try:
            resp = start_run_operation.await_completion()
            print(resp)
        except cyperf.ApiException as e:
            raise (e)
        return {"message": f"Test run started for session {session_id}"}

    def stop_test_run(
        self,
        session_id: str = None
    ) -> dict:
        """
        Stops a test run for a given session.

        Args:
            session_id (str, optional): The ID of the session to stop the test run for. Defaults to None.

        Returns:
            dict: A message indicating the result of the operation.
        """
        test_execution_api = TestOperationsApi(self.client)
        stop_run_operation = test_execution_api.start_test_run_stop(session_id=session_id)
        try:
            resp = stop_run_operation.await_completion()
            print(resp)
        except cyperf.ApiException as e:
            raise (e)
        return {"message": f"Test run stopped for session {session_id}"}

    def abort_test_run(
        self,
        session_id: str = None
    ) -> dict:
        """
        Aborts a test run for a given session.

        Args:
            session_id (str, optional): The ID of the session to abort the test run for. Defaults to None.

        Returns:
            dict: A message indicating the result of the operation.
        """
        test_execution_api = TestOperationsApi(self.client)
        abort_run_operation = test_execution_api.start_test_run_abort(session_id=session_id)
        try:
            resp = abort_run_operation.await_completion()
            print(resp)
        except cyperf.ApiException as e:
            raise (e)
        return {"message": f"Test run aborted for session {session_id}"} 