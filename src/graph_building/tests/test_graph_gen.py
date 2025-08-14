import pandas as pd
import pytest

from src.data.interfaces.data_interface import DataInterface
from src.graph_building.graph_data_generator import GraphDataGenerator

mock_data = {
    '5.0': [1, 2, 3, 4, 5, 6, 7, 8, 7, 6],
    '4.0': [1, 2, 3, 4, 5, 4, 3, 4, 3, 2],
    '3.0': [1, 2, 3, 3, 3, 4, 5, 6, 6, 6],
    '2.0': [1, 2, 3, 4, 4, 4, 3, 3, 2, 1],
    '1.0': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
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
    data={'river_km': list(map(float, mock_data.keys()))}
)

mock_info = {
    gauge: {
        'life_interval': {
            'start': dates[0],
            'end': dates[-1]
        },
        'null_point': 10,
        'level_group': 6
    }
    for gauge in mock_data.keys()
}


@pytest.fixture
def data_interface() -> DataInterface:
    data = {
        'time_series': mock_measurements,
        'meta': mock_meta,
        'gauges': mock_data.keys(),
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
    vertex_interface = graph_data_generator.delta_peak_finder.vertex_interface

    expected_peaks = {
        '5.0': {
            '2020.01.08': {
                'value': 18,
                'color': 'red'
            }
        },
        '4.0': {
            '2020-01-05': {
                'value': 15,
                'color': 'yellow'
            }
        },
        '3.0': {
            '2020-01-03': {
                'value': 13,
                'color': 'yellow'
            },
            '2020.01.08': {
                'value': 16,
                'color': 'red'
            }
        },
        '2.0': {
            '2020-01-04': {
                'value': 14,
                'color': 'yellow'
            }
        },
        '1.0': {}
    }

    for gauge in mock_data.keys():
        assert vertex_interface.vertices[gauge] == expected_peaks[gauge]
