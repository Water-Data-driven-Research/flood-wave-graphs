from src.analysis.statistical_analysis.stat_calculator import StatCalculator
from src.graph_building.interfaces.vertex_data_interface import VertexDataInterface
from src.graph_manipulation.flood_wave_filter import FloodWaveFilter


class HighWaterLevelAnalyzer:
    """
    This class gets statistics of high water level (red) flood waves.
    """
    @staticmethod
    def get_red_wave_count_at_station(flood_waves: list,
                                      vertex_interface: VertexDataInterface,
                                      target_station: float,
                                      is_full_wave_considered: bool = False
                                      ) -> dict:
        """
        Calculates the number of red waves that impacted the target station.
        A flood wave is considered red if it had a high water level at
        the target station (or throughout).
        Data is aggregated yearly and quarterly.
        :param list flood_waves: list of flood waves to analyze
        :param VertexDataInterface vertex_interface: interface containing necessary
                                                     vertex data (colors)
        :param float target_station: the station to filter for
        :param bool is_full_wave_considered: True if we require all nodes in the wave to be red,
                                             False if we only consider the one at the target station
        :return dict: keys are time interval sizes, values are the respective data
        """
        red_waves = FloodWaveFilter.get_red_waves(
            flood_waves=flood_waves,
            vertex_interface=vertex_interface,
            target_station=str(target_station),
            is_full_wave_considered=is_full_wave_considered
        )
        return StatCalculator.get_flood_wave_count(red_waves)

    @staticmethod
    def get_red_wave_propagation_time_stat(flood_waves: list,
                                           vertex_interface: VertexDataInterface,
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
        :param VertexDataInterface vertex_interface: interface containing necessary
                                                     vertex data (colors)
        :param float target_station: the station to filter for
        :param str statistic: the statistic to calculate (mean, median, etc.)
        :param bool is_full_wave_considered: True if we require all nodes in the wave to be red,
                                             False if we only consider the one at the target station
        :return dict: keys are time interval sizes, values are the respective data
        """
        red_waves = FloodWaveFilter.get_red_waves(
            flood_waves=flood_waves,
            vertex_interface=vertex_interface,
            target_station=str(target_station),
            is_full_wave_considered=is_full_wave_considered
        )
        return StatCalculator.get_propagation_time_stat(red_waves, statistic=statistic)
