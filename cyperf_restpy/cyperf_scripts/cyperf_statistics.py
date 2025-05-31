"""CyPerf statistics collection and visualization utilities."""

import cyperf
import pandas as pd
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.statistics_api import StatisticsApi
from typing import Optional, Dict, Any, List, Union

class CyperfStatistics:
    """Handles statistics collection and visualization for CyPerf test runs."""
    def __init__(self, client: cyperf.ApiClient) -> None:
        """Initializes the CyperfStatistics class with a CyPerf API client."""
        self.client = client
        self.session_client = SessionsApi(self.client)

    def collect_test_run_stats(
        self,
        session_id: Optional[str] = None,
        stats_name: Optional[str] = None,
        time_from: Optional[int] = None,
        time_to: Optional[int] = None
    ) -> Union[Dict[str, Any], Exception]:
        """Collects test run statistics for a given session."""
        try:
            test = self.session_client.get_session_test(session_id=session_id)
            test_id = [a[1] for a in test if a[0] == 'test_id'][0]
            stats_api = StatisticsApi(self.client)
            stats = stats_api.get_result_stats(test_id)
            if time_from:
                if time_to and time_to > time_from:
                    stats = [stats_api.get_result_stat_by_id(test_id, stat.name, var_from=time_from, to=time_to) for stat in stats]
                else:
                    stats = [stats_api.get_result_stat_by_id(test_id, stat.name, var_from=time_from) for stat in stats]
            else:
                stats_final = []
                for stat in stats:
                    try:
                        b = stats_api.get_result_stat_by_id(test_id, stat.name)
                        stats_final.append(b)
                    except cyperf.ApiException:
                        continue
            processed_stats = {}
            for stat in stats_final:
                if stat.snapshots:
                    processed_stats[stat.name] = {}
                    for snapshot in stat.snapshots:
                        time_stamp = snapshot.timestamp
                        processed_stats[stat.name][time_stamp] = []
                        d = {}
                        for idx, stat_name in enumerate(stat.columns):
                            d[stat_name] = [val[idx].actual_instance for val in snapshot.values]
                        processed_stats[stat.name][time_stamp] = d
            return processed_stats
        except Exception as e:
            return Exception(f"Failed to collect test run stats: {str(e)}")

    def view_stats(
        self,
        session_id: Optional[str] = None,
        processed_stats: Optional[Dict[str, Any]] = None,
        stat_name: Optional[str] = None
    ) -> Union[pd.DataFrame, Exception]:
        """Visualizes the selected stat as a time series using pandas and prints available columns."""
        try:
            if not processed_stats:
                processed_stats = self.collect_test_run_stats(session_id=session_id, stats_name=stat_name)
                if isinstance(processed_stats, Exception):
                    return processed_stats
            if stat_name not in list(processed_stats.keys()):
                raise ValueError(f"Stats name {stat_name} not found in available stats")
            stats_dict = processed_stats[stat_name]
            df = pd.DataFrame.from_dict(stats_dict, orient='index')
            for col in df.columns:
                df[col] = df[col].apply(lambda x: x[0] if isinstance(x, list) and len(x) == 1 else x)
            columns_to_show = [col for col in df.columns if col != 'filter']
            if 'filter' in df.columns:
                df = df.drop(columns=['filter'])
            return df.tail(50)
        except Exception as e:
            return Exception(f"Failed to view stats: {str(e)}")

    def show_available_stats(self, session_id: Optional[str] = None) -> Union[List[str], Exception]:
        """Shows all available stats for a given session."""
        try:
            collected_stats = self.collect_test_run_stats(session_id=session_id)
            if isinstance(collected_stats, Exception):
                return collected_stats
            return list(collected_stats.keys())
        except Exception as e:
            return Exception(f"Failed to show available stats: {str(e)}")


