import networkx as nx

from src.graph_manipulation.interfaces.flood_wave_interface import (
    FloodWaveInterface
)


class FloodMapCreator:
    """
    This class constructs a simplified (weighted) graph between given stations.
    """
    def __init__(self, flood_wave_if: FloodWaveInterface, stations: list):
        """
        Constructor.
        :param FloodWaveInterface flood_wave_if: contains the flood waves to
               be mapped.
        :param list stations: the boundary stations between river sections
        """
        self.floods_waves = flood_wave_if.flood_waves
        self.stations = stations

    def run(self) -> nx.DiGraph:
        """
        Run function, creates a flood map (only containing those flood waves
        that went all the way from one boundary station to another).
        :return nx.DiGraph: the created flood map
        """
        flood_map = nx.DiGraph()
        edges = self.find_edges()

        flood_map.add_edges_from(ebunch_to_add=edges)
        return flood_map

    def find_edges(self) -> list:
        """
        Finds all the flood waves that went from one boundary station to
        another.
        :return list: the flood waves to be plotted
        """
        edges = []

        for start, end in zip(self.stations[:-1], self.stations[1:]):
            found_edges = [[fw[0], fw[-1]] for fw in self.floods_waves
                           if fw[0][0] == str(start) and fw[-1][0] == str(end)]
            edges.extend(found_edges)

        return edges
