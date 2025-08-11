import pandas as pd

from src.data.interfaces.data_interface import DataInterface
from src.graph_building.interfaces.graph_data_interface import GraphDataInterface
from src.graph_building.interfaces.vertex_data_interface import VertexDataInterface


class GraphDataGenerator:
    """
    This class finds all vertices and edges of the FWG.
    """
    def __init__(self,
                 data_interface: DataInterface,
                 beta: int,
                 delta: int = 2,
                 start_date: str = '1876-01-01',
                 end_date: str = '2019-12-31'
                 ):
        """
        Constructor.
        :param DataInterface data_interface: the DataInterface instance containing required data
        :param int beta: the number of days allowed after a vertex for continuation
        :param int delta: the number of days that a record is required to be greater
                          than the records before, and to be greater or equal to after
                          to be considered a peak
        :param str start_date: the beginning date of our analysis
        :param str end_date: the end date of our analysis
        """
        self.data_interface = data_interface

        self.beta = beta
        self.delta = delta
        self.start_date = start_date
        self.end_date = end_date

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

    def find_vertices(self, gauge: str) -> list:
        """
        We find the potential vertices for a gauge, then return them
        in the form: (date, null-corrected water level value, color).
        :param str gauge: the current gauge
        :return list: list of the potential vertices
        """
        station_info = self.data_interface.station_info
        start_date, end_date = self.find_time_interval(
            start_dates=(
                station_info[gauge]['life_interval']['start'],
                self.start_date
            ),
            end_dates=(
                station_info[gauge]['life_interval']['end'],
                self.end_date
            )
        )

        series = self.data_interface.time_series.loc[start_date:end_date, gauge]

        before_max = series.rolling(
            window=self.delta + 1,
            min_periods=self.delta + 1
        ).max().shift(1)

        after_max = series[::-1].rolling(
            window=self.delta + 1,
            min_periods=self.delta + 1
        ).max().shift(1)[::-1]

        cond_before = series > before_max
        cond_after = series >= after_max

        is_peak = cond_before & cond_after

        null_point = station_info[gauge]['null_point']
        level_group = station_info[gauge]['level_group']

        peak_data = [
            [
                date,
                round(value + null_point, 2),
                'yellow' if value < level_group else 'red'
            ]
            for date, value in series[is_peak].items()
        ]

        return peak_data

    @staticmethod
    def find_time_interval(start_dates: tuple,
                           end_dates: tuple
                           ) -> tuple:
        """
        Helper function for finding the intersection of time intervals.
        :param tuple start_dates: tuple of start dates
        :param tuple end_dates: tuple of end dates
        :return tuple: final start and end dates
        """
        start_date = max(
            pd.to_datetime(date) for date in start_dates
        ).strftime('%Y-%m-%d')

        end_date = min(
            pd.to_datetime(date) for date in end_dates
        ).strftime('%Y-%m-%d')

        return start_date, end_date
