import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.reports_api import ReportsApi

class CyperfReports:
    def __init__(self, client: cyperf.ApiClient):
        """
        Initialize the CyperfReports class.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.reports_api = ReportsApi(self.client)
        self.session_client = SessionsApi(self.client)
        

    def download_pdf_report(self, session_id: str = None):
        """
        Download the PDF report for a given session.

        Args:
            session_id (str): The ID of the session to download the PDF report for.

        Returns:
            dict: A dictionary containing the PDF report.
        """
        test_id = self._get_test_id(session_id=session_id)
        download_op = self.reports_api.start_result_generate_pdf(result_id=test_id)
        return {"saved_file_location": download_op.await_completion()}
    
    def download_csv_report(self, session_id: str = None):
        """
        Download the CSV report for a given session.

        Args:
            session_id (str): The ID of the session to download the CSV report for.

        Returns:
            dict: A dictionary containing the CSV report.
        """ 
        test_id = self._get_test_id(session_id=session_id)
        download_op = self.reports_api.start_result_generate_csv(result_id=test_id)
        return {"saved_file_location": download_op.await_completion()}

    def _get_test_id(self, session_id: str = None):
        test = self.session_client.get_session_test(session_id=session_id)
        self.test_id = [a[1] for a in test if a[0] == 'test_id'][0]
        return self.test_id
   