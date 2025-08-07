import json
import os
import tempfile
import unittest

import pandas as pd

from src.data.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.data_loader = DataLoader.__new__(DataLoader)
        self.data_loader.data_folder_path = self.tmpdir.name

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_load_json(self):
        test_dict = {'a': 1, 'b': 2, 'c': 3}

        json_path = os.path.join(self.tmpdir.name, 'test.json')
        with open(json_path, 'w') as f:
            json.dump(test_dict, f)

        result = self.data_loader.load_json('test.json')
        self.assertEqual(result, test_dict)

    def test_load_csv(self):
        test_df = pd.DataFrame(
            {'col1': [1, 2], 'col2': [3, 4]},
            index=['row1', 'row2']
        )

        csv_path = os.path.join(self.tmpdir.name, 'test.csv')
        test_df.to_csv(csv_path, sep=',')

        result = self.data_loader.load_csv('test.csv', sep=',')
        pd.testing.assert_frame_equal(result, test_df)


if __name__ == '__main__':
    unittest.main()
