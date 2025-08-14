import pandas as pd
import pytest

from src.data.interfaces.data_interface import DataInterface
from src.graph_building.graph_data_generator import GraphDataGenerator

mock_data = {
    "3.0": [1, 1, 8, 8, 8, None, None, 8, 8, 8],
    "2.0": [None, None, 5, 1, 1, 5, 1, 1, None, None],
    "1.0": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
}
dates = [
    '2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05',
    '2020.01.06', '2020.01.07', '2020.01.08', '2020.01.09', '2020.01.10'
]

mock_measurements = pd.DataFrame(
    data=mock_data,
    index=dates
)

mock_meta = pd.DataFrame(
    data={'river_km': [1.0, 2.0, 3.0]}
)

mock_info = {
    '3.0': {
        'life_interval': {
            'start': dates[0],
            'end': dates[-1]
        },
        'null_point': 10,
        'level_group': 8
    },
    '2.0': {
        'life_interval': {
            'start': dates[2],
            'end': dates[-3]
        },
        'null_point': 10,
        'level_group': 8
    },
    '1.0': {
        'life_interval': {
            'start': dates[0],
            'end': dates[-1]
        },
        'null_point': 10,
        'level_group': 8
    }
}


@pytest.fixture
def data_interface() -> DataInterface:
    data = {
        'time_series': mock_measurements,
        'meta': mock_meta,
        'gauges': [3.0, 2.0, 1.0],
        'station_info': mock_info
    }

    return DataInterface(data=data)


@pytest.fixture
def graph_data_generator(data_interface: DataInterface) -> GraphDataGenerator:
    data_gen = GraphDataGenerator(
        data_interface=data_interface,
        beta=2,
        delta=2
    )
    data_gen.run()

    return data_gen


def test_delta_peak_detection(graph_data_generator: GraphDataGenerator):
    vertex_interface = graph_data_generator.vertex_interface

    expected_peaks = {
        '3.0': {
            '2020-01-03': {
                'value': 18,
                'color': 'red'
            }
        },
        '2.0': {
            '2020.01.06': {
                'value': 15,
                'color': 'yellow'
            }
        },
        '1.0': {}
    }

    assert vertex_interface.vertices['1.0'] == expected_peaks['1.0']
    assert vertex_interface.vertices['2.0'] == expected_peaks['2.0']
    assert vertex_interface.vertices['3.0'] == expected_peaks['3.0']
