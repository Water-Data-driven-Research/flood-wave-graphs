from itertools import product

import networkx as nx

from src.graph_manipulation.interfaces.flood_wave_interface import FloodWaveInterface


class FloodWaveExtractor:
    """
    This class finds all flood waves in the FWG.
    """
    def __init__(self, fwg: nx.DiGraph):
        """
        Constructor.
        :param nx.DiGraph fwg: the graph to extract flood waves from
        """
        self.fwg = fwg

        self.flood_wave_interface = FloodWaveInterface()

    def __call__(self, with_equivalence: bool):
        """
        Produces both a list of waves (node lists) for statistics,
        and a graph object for visualization.
        :param bool with_equivalence: whether to apply equivalence on paths
        """
        flood_waves = self.get_flood_waves(with_equivalence=with_equivalence)

        data = {
            'flood_waves': flood_waves,
            'extracted_graph': self.build_wave_graph(flood_waves=flood_waves)
        }
        self.flood_wave_interface = FloodWaveInterface(data=data)

    def get_flood_waves(self, with_equivalence: bool) -> list:
        """
        Extracts flood waves from the FWG.
        :param bool with_equivalence: whether to apply equivalence on paths
        :return list: found flood waves
        """
        components = sorted(map(
            sorted,
            list(nx.weakly_connected_components(self.fwg))
        ))

        flood_waves = list()
        for component in components:
            nodes = list(component)
            possible_pairs = self.get_possible_pairs(nodes=nodes)

            for start, end in possible_pairs:
                try:
                    if with_equivalence:
                        wave = nx.shortest_path(
                            G=self.fwg,
                            source=start,
                            target=end
                        )
                        flood_waves.append(wave)
                    else:
                        for wave in nx.all_shortest_paths(self.fwg, source=start, target=end):
                            flood_waves.append(wave)
                except nx.NetworkXNoPath:
                    continue

        return flood_waves

    def get_possible_pairs(self, nodes: list) -> list:
        """
        We find potential start and end nodes to form paths.
        :param list nodes: nodes in the component
        :return list: possible (start node, end node) pairs
        """
        possible_start_nodes = [n for n in nodes if self.fwg.in_degree(n) == 0]
        possible_end_nodes = [n for n in nodes if self.fwg.out_degree(n) == 0]

        return list(product(possible_start_nodes, possible_end_nodes))

    @staticmethod
    def build_wave_graph(flood_waves: list) -> nx.DiGraph:
        """
        Build a graph object from the extracted waves.
        :param list flood_waves: extracted waves
        """
        extracted_graph = nx.DiGraph()
        for wave in flood_waves:
            nx.add_path(
                G_to_add_to=extracted_graph,
                nodes_for_path=wave
            )

        return extracted_graph
