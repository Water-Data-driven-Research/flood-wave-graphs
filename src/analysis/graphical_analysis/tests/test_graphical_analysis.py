import networkx as nx
import pytest

from src.analysis.graphical_analysis.flood_map_creator import FloodMapCreator
from src.graph_manipulation.interfaces.flood_wave_interface import (
    FloodWaveInterface
)


@pytest.fixture
def mock_flood_waves() -> list:
    """
    A potential list of flood waves on the river.
    :return list: the potential list of flood waves
    """
    flood_waves = [
        [('13.0', '1989-12-23'), ('11.0', '1989-12-24'), ('9.0', '1989-12-26'),
         ('6.0', '1989-12-27'), ('4.0', '1989-12-28'), ('2.0', '1989-12-30'),
         ('1.0', '1989-12-31')],
        [('13.0', '1990-01-10'), ('11.0', '1990-01-11'), ('9.0', '1990-01-13'),
         ('6.0', '1990-01-14')],
        [('6.0', '1990-02-15'), ('4.0', '1990-02-17'), ('2.0', '1990-02-19'),
         ('1.0', '1990-02-20')],
        [('4.0', '1990-03-20'), ('2.0', '1990-03-21'), ('1.0', '1990-03-22')]
    ]

    return flood_waves


@pytest.fixture
def mock_data(mock_flood_waves: list) -> dict:
    """
    Creates the mock data to make a flood map.
    :return dict: the data to make the flood map
    """
    mock_data: dict = {'flood_waves': mock_flood_waves,
                       'extracted_graph': nx.DiGraph()}
    return mock_data


@pytest.fixture
def mock_flood_wave_if(mock_data: dict) -> FloodWaveInterface:
    """
    Creates a flood wave interface which contains the data for flood map
    creation.
    :param dict mock_data: the data to store in the flood wave interface
    :return FloodWaveInterface: the flood wave interface
    """
    flood_wave_if = FloodWaveInterface(data=mock_data)
    return flood_wave_if


@pytest.fixture
def mock_stations() -> list:
    """
    The list of boundary mock_stations between which we look for flood waves.
    :return list: the list of mock_stations
    """
    stations = [13.0, 6.0, 1.0]
    return stations


@pytest.fixture
def flood_map(mock_flood_wave_if: FloodWaveInterface,
              mock_stations: list) -> nx.DiGraph:
    """
    A flood map which we will run tests on.
    :param FloodWaveInterface mock_flood_wave_if: contains the flood waves to
           be mapped
    :param list mock_stations: the boundary mock_stations between river sections
    :return nx.DiGraph: the flood map
    """
    flood_map_creator = FloodMapCreator(flood_wave_if=mock_flood_wave_if,
                                        stations=mock_stations)
    flood_map = flood_map_creator.run()
    return flood_map


@pytest.mark.parametrize('expected_edges', [
    [(('13.0', '1990-01-10'), ('6.0', '1990-01-14')),
     (('6.0', '1990-02-15'), ('1.0', '1990-02-20'))]
])
def test_flood_map_edges(flood_map: nx.DiGraph, expected_edges: list):
    """
    Tests whether the flood map has the correct edges or not.
    :param nx.DiGraph flood_map: the created flood map
    :param list expected_edges: the expected correct list of edges
    """
    assert sorted(list(flood_map.edges())) == sorted(expected_edges)
