import networkx as nx

from src.analysis.statistical_analysis.stat_calculator import StatCalculator
from src.graph_manipulation.flood_wave_filter import FloodWaveFilter


class FloodWaveAnalyzer:
    """
    This class is responsible for the analysis of flood waves between two stations.
    """
    def __init__(self,
                 extracted_graph: nx.DiGraph,
                 lower_station: float = None,
                 upper_station: float = None,
                 with_equivalence: bool = True
                 ):
        """
        Constructor.
        :param nx.DiGraph extracted_graph: graph object containing flood waves
        :param float lower_station: the downstream station (river km)
        :param float upper_station: the upstream station (river km)
        :param bool with_equivalence: whether to apply equivalence on paths
        """
        self.extracted_graph = extracted_graph
        self.lower_station = lower_station
        self.upper_station = upper_station
        self.with_equivalence = with_equivalence

    def get_flood_wave_count(self) -> dict:
        """
        Calculates the number of flood waves between the two stations.
        Data is aggregated yearly and quarterly.
        :return dict: keys are frequencies, values are the respective data
        """
        flood_waves = FloodWaveFilter.get_filtered_waves(
            extracted_graph=self.extracted_graph,
            lower_station=self.lower_station,
            upper_station=self.upper_station,
            with_equivalence=self.with_equivalence
        )
        return StatCalculator.get_flood_wave_count(
            flood_waves=flood_waves
        )

    def get_propagation_time_stat(self, statistic: str = 'mean') -> dict:
        """
        Calculates the selected statistic of flood wave
        propagation times between the two stations.
        Data is aggregated yearly and quarterly.
        :param str statistic: the statistic to calculate
        :return dict: keys are frequencies, values are the respective data
        """
        flood_waves = FloodWaveFilter.get_filtered_waves(
            extracted_graph=self.extracted_graph,
            lower_station=self.lower_station,
            upper_station=self.upper_station,
            with_equivalence=self.with_equivalence
        )
        return StatCalculator.get_propagation_time_stat(
            flood_waves=flood_waves,
            statistic=statistic
        )
