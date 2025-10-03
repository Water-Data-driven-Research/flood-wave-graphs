import pandas as pd
import pytest

from src.data.interfaces.data_interface import DataInterface
from src.graph_building.graph_builder import GraphBuilder

mock_data = {
    '5.0': [1, 2, 3, 4, 5, 6, 7, 8, 7, 6],
    '4.0': [1, 2, 3, 4, 5, 4, 3, 4, 3, 2],
    '3.0': [1, 2, 3, 3, 3, 4, 5, 6, 6, 6],
    '2.0': [1, 2, 3, 4, 4, 4, 3, 3, 2, 1],
    '1.0': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
}
dates = [
    '2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05',
    '2020-01-06', '2020-01-07', '2020-01-08', '2020-01-09', '2020-01-10'
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
        'gauges': list(mock_data.keys()),
        'station_info': mock_info
    }

    return DataInterface(data=data)


@pytest.mark.parametrize('delta, expected_peaks', [
    (2, {
        '5.0': {
            '2020-01-08': {'value': 18, 'color': 'red'}
        },
        '4.0': {
            '2020-01-05': {'value': 15, 'color': 'yellow'}
        },
        '3.0': {
            '2020-01-03': {'value': 13, 'color': 'yellow'},
            '2020-01-08': {'value': 16, 'color': 'red'}
        },
        '2.0': {
            '2020-01-04': {'value': 14, 'color': 'yellow'}
        },
        '1.0': {}
    }),
    (3, {
        '5.0': {},
        '4.0': {
            '2020-01-05': {'value': 15, 'color': 'yellow'}
        },
        '3.0': {},
        '2.0': {
            '2020-01-04': {'value': 14, 'color': 'yellow'}
        },
        '1.0': {}
    })
])
def test_delta_peak_detection(data_interface: DataInterface,
                              delta: int,
                              expected_peaks: dict
                              ):
    data_gen = GraphBuilder(
        data_interface=data_interface,
        delta=delta
    )
    data_gen.run()

    vertex_interface = data_gen.delta_peak_finder.vertex_interface

    for gauge in data_interface.gauges:
        assert vertex_interface.vertices[gauge] == expected_peaks[gauge]


@pytest.mark.parametrize('beta, expected_edges, expected_graph_data', [
    (2, {
        ('5.0', '4.0'): [],
        ('4.0', '3.0'): [],
        ('3.0', '2.0'): [
            ('2020-01-03', '2020-01-04')
        ],
        ('2.0', '1.0'): []
    }, [
        (('3.0', '2020-01-03'), ('2.0', '2020-01-04'))
    ]),
    (3, {
        ('5.0', '4.0'): [],
        ('4.0', '3.0'): [
            ('2020-01-05', '2020-01-08')
        ],
        ('3.0', '2.0'): [
            ('2020-01-03', '2020-01-04')
        ],
        ('2.0', '1.0'): []
    }, [
        (('4.0', '2020-01-05'), ('3.0', '2020-01-08')),
        (('3.0', '2020-01-03'), ('2.0', '2020-01-04'))
    ])
])
def test_edge_finding(data_interface: DataInterface,
                      beta: int,
                      expected_edges: dict,
                      expected_graph_data: list
                      ):
    data_gen = GraphBuilder(
        data_interface=data_interface,
        beta=beta
    )
    data_gen.run()

    edge_interface = data_gen.edge_finder.edge_interface

    gauges = data_interface.gauges
    for upstream, downstream in zip(gauges[:-1], gauges[1:]):
        gauge_pair = (upstream, downstream)
        assert edge_interface.edges[gauge_pair] == expected_edges[gauge_pair]

    fwg = data_gen.fwg_interface.fwg
    assert list(fwg.edges) == expected_graph_data
