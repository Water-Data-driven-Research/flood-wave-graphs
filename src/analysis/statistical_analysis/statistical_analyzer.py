import networkx as nx
import pandas as pd

from src.analysis.statistical_analysis.stat_calculator import StatCalculator
from src.graph_building.interfaces.vertex_data_interface import VertexDataInterface
from src.graph_manipulation.flood_wave_filter import FloodWaveFilter
from src.graph_manipulation.fwg_filter import FWGFilter
from src.graph_manipulation.interfaces.flood_wave_interface import FloodWaveInterface


class StatisticalAnalyzer:
    """
    This class is responsible for the statistical analysis of graph (and flood wave) data.
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
        flood_waves = FloodWaveFilter.get_filtered_waves(
            extracted_graph=self.flood_wave_interface.extracted_graph,
            lower_station=lower_station,
            upper_station=upper_station,
            with_equivalence=with_equivalence
        )
        return StatCalculator.get_flood_wave_count(flood_waves)

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
        flood_waves = FloodWaveFilter.get_filtered_waves(
            extracted_graph=self.flood_wave_interface.extracted_graph,
            lower_station=lower_station,
            upper_station=upper_station,
            with_equivalence=with_equivalence
        )
        return StatCalculator.get_propagation_time_stat(flood_waves, statistic=statistic)

    def get_red_wave_count_at_station(self,
                                      flood_waves: list,
                                      target_station: float,
                                      check_whole_wave: bool = False
                                      ) -> dict:
        """
        Calculates the number of red waves that impacted the target station.
        A flood wave is considered red if it had a high water level at
        the target station (or throughout).
        Data is aggregated yearly and quarterly.
        :param list flood_waves: list of flood waves to analyze
        :param float target_station: the station to filter for
        :param bool check_whole_wave: True if we require all nodes in the wave to be red,
                                      False if we only consider the one at the target station
        :return dict: keys are time interval sizes, values are the respective data
        """
        red_waves = FloodWaveFilter.get_red_waves(
            flood_waves=flood_waves,
            vertex_interface=self.vertex_interface,
            target_station=str(target_station),
            check_whole_wave=check_whole_wave
        )
        return StatCalculator.get_flood_wave_count(red_waves)

    def get_red_wave_propagation_time_stat(self,
                                           flood_waves: list,
                                           target_station: float,
                                           statistic: str = 'mean',
                                           check_whole_wave: bool = False
                                           ) -> dict:
        """
        Calculates the chosen statistic for the propagation times of red waves
        that impacted the target station. A flood wave is considered red if it had
        a high water level at the target station (or throughout).
        Data is aggregated yearly and quarterly.
        :param list flood_waves: list of flood waves to analyze
        :param float target_station: the station to filter for
        :param str statistic: the statistic to calculate (mean, median, etc.)
        :param bool check_whole_wave: True if we require all nodes in the wave to be red,
                                      False if we only consider the one at the target station
        :return dict: keys are time interval sizes, values are the respective data
        """
        red_waves = FloodWaveFilter.get_red_waves(
            flood_waves=flood_waves,
            vertex_interface=self.vertex_interface,
            target_station=str(target_station),
            check_whole_wave=check_whole_wave
        )
        return StatCalculator.get_propagation_time_stat(red_waves, statistic=statistic)

    @staticmethod
    def get_slope_distribution(fwg: nx.DiGraph) -> dict:
        """
        Count the ratio of edges with positive/zero/negative slopes.
        :param nx.DiGraph fwg: the flood wave graph to analyze
        :return dict: ratios {'positive': x, 'zero': y, 'negative': z}
        """
        slopes = list()
        for u, v, data in fwg.edges(data=True):
            slopes.append(data.get('slope'))

        if not slopes:
            return {'positive': 0, 'zero': 0, 'negative': 0}

        total = len(slopes)
        return {
            'positive': sum(1 for s in slopes if s > 0) / total,
            'zero': sum(1 for s in slopes if s == 0) / total,
            'negative': sum(1 for s in slopes if s < 0) / total
        }

    @staticmethod
    def get_slope_error_ratios_between_stations(fwg: nx.DiGraph,
                                                lower_station: float,
                                                upper_station: float
                                                ) -> dict:
        """
        For a station pair, compute error ratios (zero/negative slope)
        yearly and quarterly.
        :param nx.DiGraph fwg: the flood wave graph to analyze
        :param float lower_station: the downstream station
        :param float upper_station: the upstream station
        :return dict: keys are time interval sizes, values are the respective data
        """
        filtered_graph = FWGFilter.filter_stations(
            fwg=fwg,
            lower_station=lower_station,
            upper_station=upper_station
        )

        records = list()
        for u, v, data in filtered_graph.edges(data=True):
            start_date = u[1]
            slope = data.get('slope')

            records.append({
                'date': pd.to_datetime(start_date),
                'slope': slope
            })

        df = pd.DataFrame(records).set_index('date')
        df['is_error'] = df['slope'] <= 0

        yearly = df.resample('YE')['is_error'].mean().to_frame(name='error ratio')
        yearly.index = yearly.index.to_period('Y')

        quarterly = df.resample('QE')['is_error'].mean().to_frame(name='error ratio')
        quarterly.index = quarterly.index.to_period('Q')

        return {'yearly': yearly, 'quarterly': quarterly}
