"""CyPerf reports management utilities."""

import cyperf
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.reports_api import ReportsApi
from typing import Optional, Dict, Any, Union

class CyperfReports:
    """CyPerf reports management utilities."""
    def __init__(self, client: cyperf.ApiClient) -> None:
        """Initialize the CyperfReports class."""
        self.client = client
        self.reports_api = ReportsApi(self.client)
        self.session_client = SessionsApi(self.client)
        

    def download_pdf_report(self, session_id: Optional[str] = None) -> Union[Dict[str, str], Exception]:
        """Download the PDF report for a given session."""
        try:
            test_id = self._get_test_id(session_id=session_id)
            download_op = self.reports_api.start_result_generate_pdf(result_id=test_id)
            return {"saved_file_location": download_op.await_completion()}
        except Exception as e:
            return Exception(f"Failed to download PDF report: {str(e)}")
    
    def download_csv_report(self, session_id: Optional[str] = None) -> Union[Dict[str, str], Exception]:
        """Download the CSV report for a given session."""
        try:
            test_id = self._get_test_id(session_id=session_id)
            download_op = self.reports_api.start_result_generate_csv(result_id=test_id)
            return {"saved_file_location": download_op.await_completion()}
        except Exception as e:
            return Exception(f"Failed to download CSV report: {str(e)}")

    def _get_test_id(self, session_id: Optional[str] = None) -> Union[str, Exception]:
        try:
            test = self.session_client.get_session_test(session_id=session_id)
            test_id = [a[1] for a in test if a[0] == 'test_id'][0]
            return test_id
        except Exception as e:
            return Exception(f"Failed to get test id: {str(e)}")
   