import json
import os

import pandas as pd

from src.data.data_downloader import DataDownloader


class DataLoader:
    """
    This class is for loading all necessary data.
    """
    def __init__(self, data_downloader: DataDownloader):
        """
        Constructor.
        :param DataDownloader data_downloader: a DataDownloader instance
        """
        self.data_folder_path = data_downloader.data_folder_path

        self.level_groups = dict()
        self.measurement_data = pd.DataFrame()
        self.meta_data = pd.DataFrame()
        self.null_points = dict()
        self.station_lifetimes = dict()

        self.load_data()

    def load_data(self) -> None:
        """
        Reads downloaded data, and saves them in member variables.
        """
        level_groups_file_name = 'level_groups.json'
        measurement_file_name = 'measurement_data.csv'
        meta_file_name = 'meta_data.csv'
        null_points_file_name = 'null_points.json'
        station_lifetimes_file_name = 'station_lifetimes.json'

        with open(
                os.path.join(self.data_folder_path, level_groups_file_name)
        ) as level_groups_file:
            self.level_groups = json.load(level_groups_file)

        self.measurement_data = pd.read_csv(
            os.path.join(self.data_folder_path, measurement_file_name),
            index_col=0,
            sep=','
        )

        self.meta_data = pd.read_csv(
            os.path.join(self.data_folder_path, meta_file_name),
            index_col=0,
            sep=';'
        )

        with open(
                os.path.join(self.data_folder_path, null_points_file_name)
        ) as null_points_file:
            self.null_points = json.load(null_points_file)

        with open(
                os.path.join(self.data_folder_path, station_lifetimes_file_name)
        ) as station_lifetimes_file:
            self.station_lifetimes = json.load(station_lifetimes_file)
