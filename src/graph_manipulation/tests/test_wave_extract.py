import networkx as nx
import pytest

from src.graph_manipulation.flood_wave_extractor import FloodWaveExtractor


@pytest.fixture
def mock_graph() -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_edges_from([
        (('A', '1'), ('B', '2')),
        (('B', '2'), ('D', '4')),
        (('A', '1'), ('C', '3')),
        (('C', '3'), ('D', '4'))
    ])
    return graph


@pytest.mark.parametrize('with_equivalence, expected_waves', [
    (
        False,
        [
            [('A', '1'), ('B', '2'), ('D', '4')],
            [('A', '1'), ('C', '3'), ('D', '4')]
        ]
    ),
    (
        True,
        [
            [('A', '1'), ('B', '2'), ('D', '4')]
        ]
    )
])
def test_wave_extraction(mock_graph: nx.DiGraph,
                         with_equivalence: bool,
                         expected_waves: list
                         ):
    extractor = FloodWaveExtractor(fwg=mock_graph)
    flood_wave_interface = extractor(with_equivalence=with_equivalence)

    waves = flood_wave_interface.flood_waves

    waves_sorted = sorted(waves)
    expected_sorted = sorted(expected_waves)

    assert waves_sorted == expected_sorted

    extracted_graph = flood_wave_interface.extracted_graph

    expected_graph = nx.DiGraph()
    for wave in expected_waves:
        nx.add_path(
            G_to_add_to=expected_graph,
            nodes_for_path=wave
        )

    assert nx.is_isomorphic(extracted_graph, expected_graph)
