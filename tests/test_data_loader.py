import json
import os
import tempfile

import pandas as pd
import pytest

from src.data.data_loader import DataLoader


@pytest.fixture
def tmp_data_loader():
    tmpdir = tempfile.TemporaryDirectory()

    data_loader = DataLoader.__new__(DataLoader)
    data_loader.data_folder_path = tmpdir.name

    yield data_loader, tmpdir.name

    tmpdir.cleanup()


def test_load_json(tmp_data_loader):
    data_loader, tmpdir = tmp_data_loader
    test_dict = {'a': 1, 'b': 2, 'c': 3}

    json_path = os.path.join(tmpdir, 'test.json')
    with open(json_path, 'w') as f:
        json.dump(test_dict, f)

    result = data_loader.load_json('test.json')
    assert result == test_dict


def test_load_csv(tmp_data_loader):
    data_loader, tmpdir = tmp_data_loader
    test_df = pd.DataFrame(
        {'col1': [1, 2], 'col2': [3, 4]},
        index=['row1', 'row2']
    )

    csv_path = os.path.join(tmpdir, 'test.csv')
    test_df.to_csv(csv_path, sep=',')

    result = data_loader.load_csv('test.csv', sep=',')
    pd.testing.assert_frame_equal(result, test_df)
