import networkx as nx

from src.analysis.statistical_analysis.stat_calculator import StatCalculator
from src.graph_manipulation.flood_wave_filter import FloodWaveFilter


class FloodWaveAnalyzer:
    """
    This class is responsible for the general statistical analysis of flood waves.
    """
    @staticmethod
    def get_flood_wave_count_between_stations(extracted_graph: nx.DiGraph,
                                              lower_station: float = None,
                                              upper_station: float = None,
                                              with_equivalence: bool = True
                                              ) -> dict:
        """
        Calculates the number of flood waves between two stations,
        yearly and quarterly.
        :param nx.DiGraph extracted_graph: graph object containing flood waves
        :param float lower_station: the downstream station (river km)
        :param float upper_station: the upstream station (river km)
        :param bool with_equivalence: whether to apply equivalence on paths
        :return dict: keys are time interval sizes, values are the respective data
        """
        flood_waves = FloodWaveFilter.get_filtered_waves(
            extracted_graph=extracted_graph,
            lower_station=lower_station,
            upper_station=upper_station,
            with_equivalence=with_equivalence
        )
        return StatCalculator.get_flood_wave_count(flood_waves)

    @staticmethod
    def get_propagation_time_stat_between_stations(extracted_graph: nx.DiGraph,
                                                   lower_station: float = None,
                                                   upper_station: float = None,
                                                   statistic: str = 'mean',
                                                   with_equivalence: bool = True
                                                   ) -> dict:
        """
        Calculates selected statistic of wave propagation times
        between two stations, yearly and quarterly.
        :param nx.DiGraph extracted_graph: graph object containing flood waves
        :param float lower_station: the downstream station (river km)
        :param float upper_station: the upstream station (river km)
        :param str statistic: the statistic to calculate
        :param bool with_equivalence: whether to apply equivalence on paths
        :return dict: keys are time interval sizes, values are the respective data
        """
        flood_waves = FloodWaveFilter.get_filtered_waves(
            extracted_graph=extracted_graph,
            lower_station=lower_station,
            upper_station=upper_station,
            with_equivalence=with_equivalence
        )
        return StatCalculator.get_propagation_time_stat(flood_waves, statistic=statistic)
