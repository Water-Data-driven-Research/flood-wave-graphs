import pandas as pd

from src.data.interfaces.data_interface import DataInterface
from src.graph_building.interfaces.vertex_data_interface import VertexDataInterface


class DeltaPeakFinder:
    """
    This class is responsible for finding delta-peaks.
    """
    def __init__(self,
                 data_interface: DataInterface = None,
                 delta: int = None
                 ):
        """
        Constructor.
        :param DataInterface data_interface: the DataInterface instance containing required data
        :param int delta: the number of days that a record is required to be greater
                          than the records before, and to be greater or equal to after
                          to be considered a peak
        """
        self.data_interface = data_interface
        self.delta = delta

        self.vertex_interface = VertexDataInterface()

    def run(self):
        """
        Finds and stores delta-peaks alongside gauge distances.
        """
        gauges = self.data_interface.gauges

        vertices = dict()
        for gauge in gauges:
            series = self.get_series(gauge=gauge)
            peak_series = self.get_peak_series(series=series)

            vertices[gauge] = self.get_peak_data(
                gauge=gauge,
                peak_series=peak_series
            )

        river_kms = self.data_interface.meta['river_km'].tolist()

        data = {
            'vertices': vertices,
            'river_kms': river_kms
        }

        self.vertex_interface = VertexDataInterface(data=data)

    def get_series(self, gauge: str) -> pd.Series:
        """
        We filter for the measurements when the station was active.
        :param str gauge: the current gauge
        :return pd.Series: the existing measurements
        """
        station_info = self.data_interface.station_info

        start_date = station_info[gauge]['life_interval']['start']
        end_date = station_info[gauge]['life_interval']['end']

        series = self.data_interface.time_series[gauge].loc[start_date:end_date]

        return series

    def get_peak_series(self, series: pd.Series) -> pd.Series:
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

    def get_peak_data(self, gauge: str, peak_series: pd.Series) -> dict:
        """
        We construct the following dictionary for each peak:
        {'date': {'value': null-corrected water level value, 'color': color}}.
        :param str gauge: the current gauge
        :param pd.Series peak_series: the series of peaks
        :return dict: dictionary of peak data
        """
        station_info = self.data_interface.station_info

        null_point = station_info[gauge]['null_point']
        level_group = station_info[gauge]['level_group']

        null_corrected_series = peak_series.apply(
            lambda value: round(value + null_point, 2)
        )
        color_values = peak_series.apply(
            lambda value: 'yellow' if value < level_group else 'red'
        )

        peak_data = {
            date: {
                'value': value,
                'color': color_values[date]
            }
            for date, value in null_corrected_series.items()
        }

        return peak_data
