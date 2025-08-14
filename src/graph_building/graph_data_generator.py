import pandas as pd

from src.data.interfaces.data_interface import DataInterface
from src.graph_building.interfaces.vertex_data_interface import VertexDataInterface


class GraphDataGenerator:
    """
    This class finds all vertices and edges of the FWG.
    """
    def __init__(self,
                 data_interface: DataInterface,
                 beta: int,
                 delta: int = 2
                 ):
        """
        Constructor.
        :param DataInterface data_interface: the DataInterface instance containing required data
        :param int beta: the number of days allowed after a vertex for continuation
        :param int delta: the number of days that a record is required to be greater
                          than the records before, and to be greater or equal to after
                          to be considered a peak
        """
        self.data_interface = data_interface
        self.beta = beta
        self.delta = delta

        self.vertex_interface = VertexDataInterface()

    def run(self):
        """
        Finds all vertices per gauge and connects them with edges.
        """
        gauges = self.data_interface.gauges

        vertices = dict()
        for gauge in gauges:
            vertices[str(gauge)] = self.find_vertices(gauge=str(gauge))

        river_kms = self.data_interface.meta['river_km'].tolist()

        data = {
            'vertices': vertices,
            'river_kms': river_kms
        }

        self.vertex_interface = VertexDataInterface(data=data)

    def find_vertices(self, gauge: str) -> dict:
        """
        We find the potential vertices for a gauge, then return them as dictionaries
        in a dictionary: {'date': {'value': null-corrected water level value, 'color': color}}.
        :param str gauge: the current gauge
        :return dict: dictionary of potential vertices
        """
        station_info = self.data_interface.station_info

        start_date = station_info[gauge]['life_interval']['start']
        end_date = station_info[gauge]['life_interval']['end']

        series = self.data_interface.time_series[gauge].loc[start_date:end_date]

        peak_series = self.get_peaks(series=series)

        null_point = station_info[gauge]['null_point']
        level_group = station_info[gauge]['level_group']

        peak_data = {
            date: {
                'value': round(value + null_point, 2),
                'color': 'yellow' if value < level_group else 'red'
            }
            for date, value in peak_series.items()
        }

        return peak_data

    def get_peaks(self, series: pd.Series) -> pd.Series:
        """
        We find the delta-peaks, and return the filtered series.
        :param pd.Series series: the original time series
        :return pd.Series: found delta-peaks
        """
        before_max = series.rolling(
            window=self.delta,
            min_periods=self.delta
        ).max().shift(periods=1)

        after_max = series[::-1].rolling(
            window=self.delta,
            min_periods=self.delta
        ).max().shift(periods=1)[::-1]

        cond_before = series > before_max
        cond_after = series >= after_max

        is_peak = cond_before & cond_after

        return series[is_peak]
