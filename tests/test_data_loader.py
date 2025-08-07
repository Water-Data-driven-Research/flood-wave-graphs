import pandas as pd
import pytest

from src.data.data_downloader import DataDownloader
from src.data.data_loader import DataLoader


@pytest.fixture
def data_loader() -> DataLoader:
    downloader = DataDownloader(
        folder_link="https://drive.google.com/drive/folders/11ZydzGGaMeTih5mG-A-Pm0A2fKafun9W?usp=sharing"
    )

    loader = DataLoader(data_downloader=downloader)
    return loader


def test_measurement_data(data_loader: DataLoader):
    df = data_loader.measurement_data

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (52595, 23)


def test_meta_data(data_loader: DataLoader):
    df = data_loader.meta_data

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (22, 4)


def test_level_groups(data_loader: DataLoader):
    level_groups = data_loader.level_groups

    assert isinstance(level_groups, dict)
    assert len(level_groups) == 22


def test_null_points(data_loader: DataLoader):
    null_points = data_loader.null_points

    assert isinstance(null_points, dict)
    assert len(null_points) == 22


def test_station_lifetimes(data_loader: DataLoader):
    station_lifetimes = data_loader.station_lifetimes

    assert isinstance(station_lifetimes, dict)
    assert len(station_lifetimes) == 22
