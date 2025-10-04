from src.analysis.statistical_analysis.flood_wave_analyzer import FloodWaveAnalyzer
from src.analysis.statistical_analysis.high_water_level_analyzer import HighWaterLevelAnalyzer
from src.graph_building.interfaces.vertex_data_interface import VertexDataInterface
from src.graph_manipulation.interfaces.flood_wave_interface import FloodWaveInterface


class StatisticalAnalyzer:
    """
    This class calculates and stores data in appropriate format.
    """
    def __init__(self,
                 flood_wave_interface: FloodWaveInterface,
                 vertex_interface: VertexDataInterface
                 ):
        """
        Constructor.
        :param FloodWaveInterface flood_wave_interface: interface containing all
                                                        flood waves from the whole graph
        :param VertexDataInterface vertex_interface: interface containing vertex data
        """
        self.flood_wave_interface = flood_wave_interface
        self.vertex_interface = vertex_interface

    def get_flood_wave_count_between_stations(self,
                                              lower_station: float = None,
                                              upper_station: float = None,
                                              with_equivalence: bool = True
                                              ) -> dict:
        """
        Calculates the number of flood waves between two stations,
        yearly and quarterly.
        :param float lower_station: the downstream station (river km)
        :param float upper_station: the upstream station (river km)
        :param bool with_equivalence: whether to apply equivalence on paths
        :return dict: keys are time interval sizes, values are the respective data
        """
        return FloodWaveAnalyzer.get_flood_wave_count_between_stations(
            extracted_graph=self.flood_wave_interface.extracted_graph,
            lower_station=lower_station,
            upper_station=upper_station,
            with_equivalence=with_equivalence
        )

    def get_propagation_time_stat_between_stations(self,
                                                   lower_station: float = None,
                                                   upper_station: float = None,
                                                   statistic: str = 'mean',
                                                   with_equivalence: bool = True
                                                   ) -> dict:
        """
        Calculates selected statistic of wave propagation times
        between two stations, yearly and quarterly.
        :param float lower_station: the downstream station (river km)
        :param float upper_station: the upstream station (river km)
        :param str statistic: the statistic to calculate
        :param bool with_equivalence: whether to apply equivalence on paths
        :return dict: keys are time interval sizes, values are the respective data
        """
        return FloodWaveAnalyzer.get_propagation_time_stat_between_stations(
            extracted_graph=self.flood_wave_interface.extracted_graph,
            lower_station=lower_station,
            upper_station=upper_station,
            statistic=statistic,
            with_equivalence=with_equivalence
        )

    def get_red_wave_count_at_station(self,
                                      flood_waves: list,
                                      target_station: float,
                                      is_full_wave_considered: bool = False
                                      ) -> dict:
        """
        Calculates the number of red waves that impacted the target station.
        A flood wave is considered red if it had a high water level at
        the target station (or throughout).
        Data is aggregated yearly and quarterly.
        :param list flood_waves: list of flood waves to analyze
        :param float target_station: the station to filter for
        :param bool is_full_wave_considered: True if we require all nodes in the wave to be red,
                                             False if we only consider the one at the target station
        :return dict: keys are time interval sizes, values are the respective data
        """
        return HighWaterLevelAnalyzer.get_red_wave_count_at_station(
            flood_waves=flood_waves,
            vertex_interface=self.vertex_interface,
            target_station=target_station,
            is_full_wave_considered=is_full_wave_considered
        )

    def get_red_wave_propagation_time_stat(self,
                                           flood_waves: list,
                                           target_station: float,
                                           statistic: str = 'mean',
                                           is_full_wave_considered: bool = False
                                           ) -> dict:
        """
        Calculates the chosen statistic for the propagation times of red waves
        that impacted the target station. A flood wave is considered red if it had
        a high water level at the target station (or throughout).
        Data is aggregated yearly and quarterly.
        :param list flood_waves: list of flood waves to analyze
        :param float target_station: the station to filter for
        :param str statistic: the statistic to calculate (mean, median, etc.)
        :param bool is_full_wave_considered: True if we require all nodes in the wave to be red,
                                             False if we only consider the one at the target station
        :return dict: keys are time interval sizes, values are the respective data
        """
        return HighWaterLevelAnalyzer.get_red_wave_propagation_time_stat(
            flood_waves=flood_waves,
            vertex_interface=self.vertex_interface,
            target_station=target_station,
            statistic=statistic,
            is_full_wave_considered=is_full_wave_considered
        )
