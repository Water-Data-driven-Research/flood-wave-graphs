import os

import gdown

from src import ROOT_DIR


class DataDownloaderBase:
    """
    Base class for downloading data from Google Drive.
    Handles initialization and generic download functionality.
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

    def download_data(self):
        """
        Downloads all data from Google Drive.
        """
        gdown.download_folder(url=self.folder_link, output=self.data_folder_path)
