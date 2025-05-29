import cyperf
import pandas as pd
from cyperf.api.sessions_api import SessionsApi
from cyperf.api.statistics_api import StatisticsApi

class CyperfStatistics:
    """
    Handles statistics collection and visualization for CyPerf test runs.
    """
    def __init__(self, client: cyperf.ApiClient):
        """
        Initializes the CyperfStatistics class with a CyPerf API client.

        Args:
            client (cyperf.ApiClient): The CyPerf API client instance.
        """
        self.client = client
        self.session_client = SessionsApi(self.client)

    def collect_test_run_stats(
        self,
        session_id: str = None,
        stats_name: str = None,
        time_from: int = None,
        time_to: int = None
    ) -> dict:
        """
        Collects test run statistics for a given session.

        Args:
            session_id (str, optional): The ID of the session to collect stats for. Defaults to None.
            stats_name (str, optional): The name of the statistic to collect. Defaults to None.
            time_from (int, optional): The start time for stats collection. Defaults to None.
            time_to (int, optional): The end time for stats collection. Defaults to None.

        Returns:
            dict: A dictionary containing the processed statistics.
        """
        test = self.session_client.get_session_test(session_id=session_id)
        test_id = [a[1] for a in test if a[0] == 'test_id'][0]
        stats_api = StatisticsApi(self.client)
        stats = stats_api.get_result_stats(test_id)
        if time_from:
            if time_to > time_from:
                stats = [stats_api.get_result_stat_by_id(test_id, stat.name, var_from=time_from, to=time_to) for stat in stats]
            else:
                stats = [stats_api.get_result_stat_by_id(test_id, stat.name, var_from=time_from) for stat in stats]
        else:
            stats_final = []
            for stat in stats:
                try:
                    b = stats_api.get_result_stat_by_id(test_id, stat.name)
                    stats_final.append(b)
                except cyperf.ApiException as e:
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

    def view_stats(
        self,
        processed_stats: dict,
        stat_name: str = None
    ) -> pd.DataFrame:
        """
        Visualizes the selected stat as a time series using pandas and prints available columns.

        Args:
            processed_stats (dict): The processed stats dictionary (as returned by collect_test_run_stats).
            stat_name (str, optional): The stat name to visualize (e.g., 'client-application-connection-rate'). Defaults to None.

        Returns:
            pd.DataFrame: The last 50 records of the selected stat as a DataFrame.
        """
        if stat_name not in list(processed_stats.keys()):
            raise ValueError(f"Stats name {stat_name} not found in available stats")
        stats_dict = processed_stats[stat_name]
        df = pd.DataFrame.from_dict(stats_dict, orient='index')
        for col in df.columns:
            df[col] = df[col].apply(lambda x: x[0] if isinstance(x, list) and len(x) == 1 else x)
        columns_to_show = [col for col in df.columns if col != 'filter']
        print("\nAvailable columns:")
        for col in columns_to_show:
            print(f"- {col}")
        if 'filter' in df.columns:
            df = df.drop(columns=['filter'])
        return df.tail(50) 