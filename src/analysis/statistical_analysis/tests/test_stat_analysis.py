import networkx as nx
import pytest

import pandas as pd

from src.analysis.statistical_analysis.statistical_analyzer import StatisticalAnalyzer
from src.graph_building.interfaces.vertex_data_interface import VertexDataInterface
from src.graph_manipulation.interfaces.flood_wave_interface import FloodWaveInterface


@pytest.fixture
def mock_vertex_interface() -> VertexDataInterface:
    interface = VertexDataInterface()
    interface.vertices = {
        '1.0': {
            '2000-01-01': {'value': 8, 'color': 'red'},
            '2000-06-01': {'value': 6, 'color': 'yellow'}
        },
        '2.0': {
            '2000-01-01': {'value': 6, 'color': 'yellow'},
            '2000-01-02': {'value': 6, 'color': 'yellow'},
            '2000-01-03': {'value': 2, 'color': 'yellow'},
            '2000-01-04': {'value': 10, 'color': 'red'},
            '2000-06-02': {'value': 6, 'color': 'yellow'},
            '2000-06-03': {'value': 10, 'color': 'red'}
        }
    }
    return interface


@pytest.fixture
def mock_flood_wave_interface() -> FloodWaveInterface:
    flood_waves = [
        [('1.0', '2000-01-01'), ('2.0', '2000-01-01')],
        [('1.0', '2000-01-01'), ('2.0', '2000-01-02')],
        [('1.0', '2000-01-01'), ('2.0', '2000-01-03')],
        [('1.0', '2000-01-01'), ('2.0', '2000-01-04')],
        [('1.0', '2000-06-01'), ('2.0', '2000-06-02')],
        [('1.0', '2000-06-01'), ('2.0', '2000-06-03')],
    ]
    extracted_graph = nx.DiGraph()
    edges = [((wave[0][0], wave[0][1]), (wave[1][0], wave[1][1])) for wave in flood_waves]
    extracted_graph.add_edges_from(edges)

    data = {
        'flood_waves': flood_waves,
        'extracted_graph': extracted_graph
    }
    return FloodWaveInterface(data=data)


@pytest.fixture
def stat_analyzer(mock_vertex_interface: VertexDataInterface,
                  mock_flood_wave_interface: FloodWaveInterface
                  ) -> StatisticalAnalyzer:
    return StatisticalAnalyzer(
        vertex_interface=mock_vertex_interface,
        flood_wave_interface=mock_flood_wave_interface
    )


def test_flood_wave_analyzer(stat_analyzer: StatisticalAnalyzer):
    flood_wave_analyzer = stat_analyzer.get_flood_wave_analyzer(
        lower_station=1.0,
        upper_station=2.0,
        with_equivalence=True
    )

    flood_wave_count = flood_wave_analyzer.get_flood_wave_count()

    yearly_data = pd.DataFrame({
        'date': pd.to_datetime('2000-01').to_period('Y'),
        'flood wave count': [6]
    }).set_index('date')
    quarterly_data = pd.DataFrame({
        'date': pd.to_datetime(['2000-01', '2000-06']).to_period('Q'),
        'flood wave count': [4, 2]
    }).set_index('date')

    expected_f_w_count = {
        'yearly': yearly_data,
        'quarterly': quarterly_data
    }

    pd.testing.assert_frame_equal(
        flood_wave_count['yearly'],
        expected_f_w_count['yearly']
    )
    pd.testing.assert_frame_equal(
        flood_wave_count['quarterly'],
        expected_f_w_count['quarterly']
    )

    prop_time_stat = flood_wave_analyzer.get_propagation_time_stat(
        statistic='mean'
    )

    yearly_data = pd.DataFrame({
        'date': pd.to_datetime('2000-01').to_period('Y'),
        'mean propagation time': [1.5]
    }).set_index('date')
    quarterly_data = pd.DataFrame({
        'date': pd.to_datetime(['2000-01', '2000-06']).to_period('Q'),
        'mean propagation time': [1.5, 1.5]
    }).set_index('date')

    expected_prop_stat = {
        'yearly': yearly_data,
        'quarterly': quarterly_data
    }

    pd.testing.assert_frame_equal(
        prop_time_stat['yearly'],
        expected_prop_stat['yearly']
    )
    pd.testing.assert_frame_equal(
        prop_time_stat['quarterly'],
        expected_prop_stat['quarterly']
    )


@pytest.mark.parametrize('is_full_wave_considered, expected_f_w_count, expected_prop_stat', [
    (False, {
        'yearly': pd.DataFrame({
            'date': pd.to_datetime('2000-01').to_period('Y'),
            'flood wave count': [4]
        }).set_index('date'),
        'quarterly': pd.DataFrame({
            'date': pd.to_datetime(['2000-01']).to_period('Q'),
            'flood wave count': [4]
        }).set_index('date')
    }, {
        'yearly': pd.DataFrame({
            'date': pd.to_datetime('2000-01').to_period('Y'),
            'mean propagation time': [1.5]
        }).set_index('date'),
        'quarterly': pd.DataFrame({
            'date': pd.to_datetime(['2000-01']).to_period('Q'),
            'mean propagation time': [1.5]
        }).set_index('date')
    }),
    (True, {
        'yearly': pd.DataFrame({
            'date': pd.to_datetime('2000-01').to_period('Y'),
            'flood wave count': [1]
        }).set_index('date'),
        'quarterly': pd.DataFrame({
            'date': pd.to_datetime(['2000-01']).to_period('Q'),
            'flood wave count': [1]
        }).set_index('date')
    }, {
        'yearly': pd.DataFrame({
            'date': pd.to_datetime('2000-01').to_period('Y'),
            'mean propagation time': [3.0]
        }).set_index('date'),
        'quarterly': pd.DataFrame({
            'date': pd.to_datetime(['2000-01']).to_period('Q'),
            'mean propagation time': [3.0]
        }).set_index('date')
    })
])
def test_high_water_level_analyzer(stat_analyzer: StatisticalAnalyzer,
                                   is_full_wave_considered: bool,
                                   expected_f_w_count: dict,
                                   expected_prop_stat: dict
                                   ):
    red_analyzer = stat_analyzer.get_high_water_level_analyzer(
        flood_waves=stat_analyzer.flood_wave_interface.flood_waves,
        target_station=1.0,
        is_full_wave_considered=is_full_wave_considered
    )

    red_wave_count = red_analyzer.get_red_wave_count_at_station()

    pd.testing.assert_frame_equal(
        red_wave_count['yearly'],
        expected_f_w_count['yearly']
    )
    pd.testing.assert_frame_equal(
        red_wave_count['quarterly'],
        expected_f_w_count['quarterly']
    )

    red_wave_prop_stat = red_analyzer.get_red_wave_propagation_time_stat(
        statistic='mean'
    )

    pd.testing.assert_frame_equal(
        red_wave_prop_stat['yearly'],
        expected_prop_stat['yearly']
    )
    pd.testing.assert_frame_equal(
        red_wave_prop_stat['quarterly'],
        expected_prop_stat['quarterly']
    )
