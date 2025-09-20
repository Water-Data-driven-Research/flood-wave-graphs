import pandas as pd

from src.graph_building.interfaces.vertex_data_interface import VertexDataInterface
from src.graph_manipulation.flood_wave_extractor import FloodWaveExtractor
from src.graph_manipulation.fwg_filter import FWGFilter
from src.graph_manipulation.interfaces.flood_wave_interface import FloodWaveInterface


class StatisticalAnalyzer:
    """
    This class calculates and stores data in appropriate format.
    """
    def __init__(self, flood_wave_interface: FloodWaveInterface, vertex_interface: VertexDataInterface):
        """
        Constructor.
        :param FloodWaveInterface flood_wave_interface: interface containing all
                                                        flood waves from the whole graph
        :param VertexDataInterface vertex_interface: interface containing vertex data
        """
        self.flood_wave_interface = flood_wave_interface
        self.vertex_interface = vertex_interface

    def get_flood_wave_count(self,
                             lower_station: float,
                             upper_station: float
                             ) -> dict:
        """
        Calculates the number of flood waves between two stations,
        yearly and quarterly.
        :param float lower_station: the downstream station (river km)
        :param float upper_station: the upstream station (river km)
        :return dict: keys are time interval sizes, values are the respective data
        """
        flood_waves = self.get_filtered_waves(
            lower_station=lower_station,
            upper_station=upper_station
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

    def get_propagation_times(self,
                              lower_station: float,
                              upper_station: float,
                              statistic: str = 'mean'
                              ) -> dict:
        """
        Calculates selected statistic of wave propagation times
        between two stations, yearly and quarterly.
        :param float lower_station: the downstream station (river km)
        :param float upper_station: the upstream station (river km)
        :param str statistic: the statistic to calculate
        :return dict: keys are time interval sizes, values are the respective data
        """
        flood_waves = self.get_filtered_waves(
            lower_station=lower_station,
            upper_station=upper_station
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

        match statistic:
            case 'mean':
                yearly = df.resample('YE').mean()
                quarterly = df.resample('QE').mean()
            case 'median':
                yearly = df.resample('YE').median()
                quarterly = df.resample('QE').median()
            case _:
                raise ValueError('Invalid statistic')

        yearly.index = yearly.index.to_period('Y')
        quarterly.index = quarterly.index.to_period('Q')

        return {'yearly': yearly, 'quarterly': quarterly}

    def get_filtered_waves(self,
                           lower_station: float,
                           upper_station: float
                           ) -> list:
        """
        Finds flood waves between two stations.
        :param float lower_station: the downstream station (river km)
        :param float upper_station: the upstream station (river km)
        :return list: list of filtered waves
        """
        whole_graph = self.flood_wave_interface.extracted_graph
        graph_section = FWGFilter.filter_stations(
            fwg=whole_graph,
            lower_station=lower_station,
            upper_station=upper_station
        )

        extractor = FloodWaveExtractor(fwg=graph_section)
        flood_waves = extractor(with_equivalence=True).flood_waves

        return flood_waves
