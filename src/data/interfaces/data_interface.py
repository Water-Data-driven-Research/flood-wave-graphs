import pandas as pd


class DataInterface:
    """
    Class for storing data created in DataHandler.
    """
    def __init__(self, data: dict = None):
        """
        Constructor.
        :param dict data: Dictionary: the keys represent the data structures.
        The expected keys are:
        - 'time_series'
        - 'meta'
        - 'gauges'
        - 'station_info'
        """
        self.time_series = pd.DataFrame()
        self.meta = pd.DataFrame()
        self.gauges = list()
        self.station_info = dict()

        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)
