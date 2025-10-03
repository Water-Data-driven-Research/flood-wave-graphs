import networkx as nx

from src.graph_building.interfaces.vertex_data_interface import VertexDataInterface
from src.graph_manipulation.flood_wave_extractor import FloodWaveExtractor
from src.graph_manipulation.fwg_filter import FWGFilter


class FloodWaveFilter:
    """
    Class used to prepare flood waves for analysis.
    """
    @staticmethod
    def get_filtered_waves(extracted_graph: nx.DiGraph,
                           lower_station: float = None,
                           upper_station: float = None,
                           with_equivalence: bool = True
                           ) -> list:
        """
        Finds flood waves between two stations.
        :param nx.DiGraph extracted_graph: graph object containing waves
        :param float lower_station: the downstream station (river km)
        :param float upper_station: the upstream station (river km)
        :param bool with_equivalence: whether to apply equivalence on paths
        :return list: list of filtered waves
        """
        graph_section = FWGFilter.filter_stations(
            fwg=extracted_graph,
            lower_station=lower_station,
            upper_station=upper_station
        )

        extractor = FloodWaveExtractor(fwg=graph_section)
        flood_waves = extractor(with_equivalence=with_equivalence).flood_waves

        return flood_waves

    @staticmethod
    def get_red_waves(flood_waves: list,
                      vertex_interface: VertexDataInterface,
                      target_station: str,
                      is_full_wave_considered: bool = False
                      ) -> list:
        """
        We find all flood waves that pass through the target station while
        having high water levels either at the target station or throughout.
        :param list flood_waves: the flood waves to analyze
        :param VertexDataInterface vertex_interface: interface containing necessary
                                                     vertex data (colors)
        :param str target_station: the station to filter for
        :param bool is_full_wave_considered: True if we require all nodes in the wave to be red,
                                             False if we only consider the one at the target station
        :return list: all high water level (red) waves at the target station
        """
        vertices = vertex_interface.vertices

        if is_full_wave_considered:
            return [
                wave for wave in flood_waves
                if any(station == target_station for station, _ in wave) and
                all(vertices[station][date]['color'] == 'red'
                    for station, date in wave)
            ]
        else:
            return [
                wave for wave in flood_waves
                if any(station == target_station and
                       vertices[station][date]['color'] == 'red'
                       for station, date in wave)
            ]
