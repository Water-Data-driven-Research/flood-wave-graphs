import pandas as pd

from src.data.data_loader import DataLoader
from src.data.interfaces.data_interface import DataInterface


class DataHandler:
    """
    This class preprocesses the data for use.
    """
    def __init__(self, data_loader: DataLoader):
        """
        Constructor. We create the following data structures:
        - time_series: Pandas DataFrame containing all water level time series data.
        The indices are dates and the column names are station regional numbers.
        - meta: Pandas DataFrame containing regional numbers, station names and kilometers.
        - gauges: List of gauges (regional numbers).
        - station_info: Dictionary: keys are regional numbers, values are dictionaries like
        {'life_interval': {'start': '1876-01-01', 'end': '2019-12-31'}, 'null_point': 73.7, 'level_group': 570}
        (for Szeged)
        :param DataLoader data_loader: a DataLoader instance
        """
        self.data_if = DataInterface()

        self.run(data_loader=data_loader)

    def run(self, data_loader: DataLoader):
        """
        Run function. Gets all data structures described in the constructor.
        :param DataLoader data_loader: a DataLoader instance
        """
        gauges = list(map(str, data_loader.meta_data.index.tolist()))

        time_series = data_loader.measurement_data
        time_series.index = pd.to_datetime(time_series.index, format='ISO8601')
        time_series.index = time_series.index.strftime('%Y-%m-%d')

        data = {
            'time_series': time_series,
            'meta': data_loader.meta_data,
            'gauges': gauges,
            'station_info': self.get_station_info(
                data_loader=data_loader,
                gauges=gauges
            )
        }

        self.data_if = DataInterface(data=data)

    @staticmethod
    def get_null_corrected_series(null_point: float,
                                  series: pd.Series) -> pd.Series:
        """
        Returns the series with values that are null-corrected, that is, values
        that are measured not relative to the gauge but in absolute sea level
        (in meters above the Baltic Sea).
        :param float null_point: gauge height above the Baltic Sea
        :param pd.Series series: the series to null-correct (values in cm)
        :return pd.Series: the null-corrected series (sea level in meters)
        """
        null_corrected_series = series / 100 + null_point
        return null_corrected_series.round(decimals=2)

    @staticmethod
    def get_station_info(data_loader: DataLoader, gauges: list) -> dict:
        """
        We create a dictionary by combining dictionaries.
        :param DataLoader data_loader: a DataLoader instance
        :param list gauges: list of gauges (regional numbers)
        :return dict: dictionary of relevant station information
        """
        station_info = dict()

        for gauge in gauges:
            station_info[gauge] = {
                "life_interval": data_loader.station_lifetimes.get(gauge),
                "null_point": data_loader.null_points.get(gauge),
                "level_group": data_loader.level_groups.get(gauge)
            }

        return station_info
