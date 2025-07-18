import os

import gdown

from src import ROOT_DIR


class DataDownloader:
    """
    This class is for downloading the data from Google Drive.
    """
    def __init__(self, folder_link: str, data_folder_path: str = None):
        """
        Constructor.
        :param str folder_link: the link to the folder in Google Drive
        :param str data_folder_path: the desired path of the data folder
        """
        self.folder_link = folder_link
        self.data_folder_path = data_folder_path

        if self.data_folder_path is None:
            self.data_folder_path = os.path.join(ROOT_DIR, 'data')

        if not self.do_all_files_exist():
            self.download_data()

    def download_data(self) -> None:
        """
        Downloads all data from Google Drive.
        """
        gdown.download_folder(url=self.folder_link, output=self.data_folder_path)

    def do_all_files_exist(self) -> bool:
        """
        This function checks if all files are present in the data folder.
        :return: True if all files exist, False if at least one does not
        """
        files = (
            'level_groups.json',
            'measurement_data.csv',
            'meta_data.csv',
            'null_points.json',
            'station_lifetimes.json'
        )

        for file in files:
            if not os.path.exists(os.path.join(self.data_folder_path, file)):
                return False

        return True
