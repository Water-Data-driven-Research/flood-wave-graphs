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

        self.file_name_dict = {
            'level_groups_file_name': 'level_groups.json',
            'measurement_file_name': 'measurement_data.csv',
            'meta_file_name': 'meta_data.csv',
            'null_points_file_name': 'null_points.json',
            'station_lifetimes_file_name': 'station_lifetimes.json'
        }

        self.level_groups = dict()
        self.measurement_data = pd.DataFrame()
        self.meta_data = pd.DataFrame()
        self.null_points = dict()
        self.station_lifetimes = dict()

        self.load_data()

    def load_data(self):
        """
        Reads downloaded data, and saves them in member variables.
        """
        self.level_groups = self.load_json(
            file_name=self.file_name_dict['level_groups_file_name']
        )

        self.measurement_data = self.load_csv(
            file_name=self.file_name_dict['measurement_file_name'],
            sep=','
        )

        self.meta_data = self.load_csv(
            file_name=self.file_name_dict['meta_file_name'],
            sep=';'
        )

        self.null_points = self.load_json(
            file_name=self.file_name_dict['null_points_file_name']
        )

        self.station_lifetimes = self.load_json(
            file_name=self.file_name_dict['station_lifetimes_file_name']
        )

    def load_json(self, file_name: str) -> dict:
        """
        We load the JSON file into a dictionary.
        :param str file_name: the name of the JSON file
        :return dict: the JSON file as a dictionary
        """
        with open(
            os.path.join(self.data_folder_path, file_name)
        ) as json_file:
            return json.load(json_file)

    def load_csv(self, file_name: str, sep: str) -> pd.DataFrame:
        """
        We load the CSV file into a pandas DataFrame.
        :param str file_name: the name of the CSV file
        :param str sep: the used seperator character
        :return pd.DataFrame: the CSV file as a pandas DataFrame
        """
        return pd.read_csv(
            os.path.join(self.data_folder_path, file_name),
            sep=sep,
            index_col=0
        )
