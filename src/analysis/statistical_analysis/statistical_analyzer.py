import pandas as pd

from src.graph_manipulation.flood_wave_extractor import FloodWaveExtractor
from src.graph_manipulation.fwg_filter import FWGFilter
from src.graph_manipulation.interfaces.flood_wave_interface import FloodWaveInterface


class StatisticalAnalyzer:
    """
    This class calculates and stores data in appropriate format.
    """
    def __init__(self, flood_wave_interface: FloodWaveInterface):
        """
        Constructor.
        :param FloodWaveInterface flood_wave_interface: interface containing all
                                                        flood waves from the whole graph
        """
        self.flood_wave_interface = flood_wave_interface

    def get_flood_wave_count(self,
                             lower_station: float,
                             upper_station: float,
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
        flood_waves = self.get_filtered_waves(
            lower_station=lower_station,
            upper_station=upper_station,
            with_equivalence=with_equivalence
        )
        wave_dates = [wave[0][1] for wave in flood_waves]

        df = pd.DataFrame({
            'date': pd.to_datetime(wave_dates),
            'count': 1
        }).set_index('date')

        yearly = df.resample('YE').sum()
        yearly.index = yearly.index.to_period('Y')

        quarterly = df.resample('QE').sum()
        quarterly.index = quarterly.index.to_period('Q')

        return {'yearly': yearly, 'quarterly': quarterly}

    def get_propagation_time_stat(self,
                                  lower_station: float,
                                  upper_station: float,
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
        flood_waves = self.get_filtered_waves(
            lower_station=lower_station,
            upper_station=upper_station,
            with_equivalence=with_equivalence
        )

        propagation_times = list()
        start_dates = list()
        for wave in flood_waves:
            start_date = pd.to_datetime(wave[0][1])
            end_date = pd.to_datetime(wave[-1][1])
            start_dates.append(start_date)
            propagation_times.append((end_date - start_date).days)

        df = pd.DataFrame({
            'date': start_dates,
            'propagation_time': propagation_times
        }).set_index('date')

        try:
            yearly = getattr(df.resample('YE'), statistic)()
            quarterly = getattr(df.resample('QE'), statistic)()
        except AttributeError:
            raise ValueError('Invalid statistic')

        yearly.index = yearly.index.to_period('Y')
        quarterly.index = quarterly.index.to_period('Q')

        return {'yearly': yearly, 'quarterly': quarterly}

    def get_filtered_waves(self,
                           lower_station: float,
                           upper_station: float,
                           with_equivalence: bool = True
                           ) -> list:
        """
        Finds flood waves between two stations.
        :param float lower_station: the downstream station (river km)
        :param float upper_station: the upstream station (river km)
        :param bool with_equivalence: whether to apply equivalence on paths
        :return list: list of filtered waves
        """
        whole_graph = self.flood_wave_interface.extracted_graph
        graph_section = FWGFilter.filter_stations(
            fwg=whole_graph,
            lower_station=lower_station,
            upper_station=upper_station
        )

        extractor = FloodWaveExtractor(fwg=graph_section)
        flood_waves = extractor(with_equivalence=with_equivalence).flood_waves

        return flood_waves
