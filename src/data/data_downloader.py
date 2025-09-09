import os

from src import ROOT_DIR
from src.data.data_downloader_base import DataDownloaderBase


class DataDownloader(DataDownloaderBase):
    """
    This class is for downloading the input data from Google Drive.
    """
    def __init__(self, folder_link: str):
        """
        Constructor.
        :param str folder_link: the link to the folder in Google Drive
        """
        super().__init__(
            folder_link=folder_link,
            data_folder_path=os.path.join(ROOT_DIR, 'data')
        )

        self.download_input_data()

    def download_input_data(self):
        """
        Ensures all required input data is available locally.
        Downloads the data if not all files exist.
        """
        if not self.do_all_files_exist():
            self.download_data()

    def do_all_files_exist(self) -> bool:
        """
        This function checks if all files are present in the data folder.
        :return bool: True if all files exist, False if at least one does not
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
