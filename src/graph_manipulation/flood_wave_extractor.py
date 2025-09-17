from itertools import product

import networkx as nx
import numpy as np

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

    def __call__(self, with_equivalence: bool) -> FloodWaveInterface:
        """
        Produces both a list of waves (node lists) for statistics,
        and a graph object for visualization.
        :param bool with_equivalence: whether to apply equivalence on paths
        :return FloodWaveInterface: interface with extracted flood waves
        """
        flood_waves = self.get_flood_waves(with_equivalence=with_equivalence)

        data = {
            'flood_waves': flood_waves,
            'extracted_graph': self.build_wave_graph(flood_waves=flood_waves)
        }

        return FloodWaveInterface(data=data)

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

            if with_equivalence:
                flood_waves = self.find_waves_with_equivalence(
                    possible_pairs=possible_pairs
                )
            else:
                flood_waves = self.find_waves(
                    possible_pairs=possible_pairs
                )

        return flood_waves

    def get_possible_pairs(self, nodes: list) -> list:
        """
        We find potential start and end nodes to form paths.
        :param list nodes: nodes in the component
        :return list: possible (start node, end node) pairs
        """
        in_deg_pairs = list(self.fwg.in_degree(nodes))
        out_deg_pairs = list(self.fwg.out_degree(nodes))

        in_nodes, in_values = zip(*in_deg_pairs)
        out_nodes, out_values = zip(*out_deg_pairs)

        in_nodes = np.array(in_nodes)
        in_values = np.array(in_values)
        out_nodes = np.array(out_nodes)
        out_values = np.array(out_values)

        possible_start_nodes = in_nodes[in_values == 0].tolist()
        possible_end_nodes = out_nodes[out_values == 0].tolist()

        return list(product(possible_start_nodes, possible_end_nodes))

    def find_waves_with_equivalence(self, possible_pairs: list) -> list:
        """
        We find waves with equivalence.
        :param list possible_pairs: possible (start node, end node) pairs
        :return list: found waves
        """
        waves = list()
        for start, end in possible_pairs:
            try:
                wave = nx.shortest_path(
                    G=self.fwg,
                    source=start,
                    target=end
                )
                waves.append(wave)
            except nx.NetworkXNoPath:
                continue

        return waves

    def find_waves(self, possible_pairs: list) -> list:
        """
        We find all waves between start and end nodes.
        :param list possible_pairs: possible (start node, end node) pairs
        :return list: found waves
        """
        waves = list()
        for start, end in possible_pairs:
            try:
                for wave in nx.all_shortest_paths(G=self.fwg, source=start, target=end):
                    waves.append(wave)
            except nx.NetworkXNoPath:
                continue

        return waves

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
