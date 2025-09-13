from itertools import product

import networkx as nx

from src.graph_building.interfaces.fwg_interface import FWGInterface
from src.graph_manipulation.interfaces.flood_wave_interface import FloodWaveInterface


class FloodWaveExtractor:
    """
    This class finds all flood waves in the FWG.
    """
    def __init__(self,
                 fwg_interface: FWGInterface,
                 ):
        """
        Constructor.
        :param FWGInterface fwg_interface: interface containing the graph
        """
        self.fwg = fwg_interface.fwg

        self.flood_wave_interface: FloodWaveInterface = None

    def __call__(self, with_equivalence: bool):
        """
        Triggers flood wave extraction.
        :param bool with_equivalence: whether to apply equivalence on paths
        """
        flood_waves = self.get_flood_waves(with_equivalence=with_equivalence)
        self.flood_wave_interface = FloodWaveInterface(flood_waves=flood_waves)

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
                    else:
                        wave = nx.all_shortest_paths(
                            G=self.fwg,
                            source=start,
                            target=end
                        )

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
        possible_start_nodes = list()
        possible_end_nodes = list()
        for node in nodes:
            in_degree = self.fwg.in_degree(node)
            out_degree = self.fwg.out_degree(node)

            if in_degree == 0:
                possible_start_nodes.append(node)
            if out_degree == 0:
                possible_end_nodes.append(node)

        possible_pairs = list(product(possible_start_nodes, possible_end_nodes))

        return possible_pairs
