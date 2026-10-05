import networkx as nx

from src.graph_manipulation.interfaces.flood_wave_interface import (
    FloodWaveInterface
)


class ReducedFWGCreator:
    """
    This class constructs a reduced flood wave graph between given boundary
    stations, whose nodes are delta peaks, and whose edges are those flood
    waves that made it all the way between two neighboring boundary stations.
    """
    def __init__(self, flood_wave_if: FloodWaveInterface, stations: list):
        """
        Constructor.
        :param FloodWaveInterface flood_wave_if: contains the flood waves to
               be mapped
        :param list stations: the boundary stations between river sections
        """
        self.flood_waves = flood_wave_if.flood_waves
        self.stations = sorted(stations, reverse=True)

    def run(self) -> nx.DiGraph:
        """
        Run function, creates a flood map (only containing those flood waves
        that went all the way from one boundary station to another).
        :return nx.DiGraph: the created flood map
        """
        reduced_fwg = nx.DiGraph()
        edges = self.find_edges()

        reduced_fwg.add_edges_from(ebunch_to_add=edges)
        return reduced_fwg

    def find_edges(self) -> list:
        """
        Finds all the flood waves that went from one boundary station to
        another.
        :return list: the flood waves to be plotted
        """
        edges = []

        for start, end in zip(self.stations[:-1], self.stations[1:]):
            found_edges = []
            for fw in self.flood_waves:
                station_list = [station for station, date in fw]
                if str(start) in station_list and str(end) in station_list:
                    start_node = fw[station_list.index(str(start))]
                    end_node = fw[station_list.index(str(end))]
                    found_edges.append([start_node, end_node])
            edges.extend(found_edges)

        return edges
