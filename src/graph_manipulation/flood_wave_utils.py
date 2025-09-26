import networkx as nx

from src.graph_manipulation.flood_wave_extractor import FloodWaveExtractor
from src.graph_manipulation.fwg_filter import FWGFilter


class FloodWaveUtils:
    """
    Class used to prepare flood waves for analysis.
    """
    @staticmethod
    def get_filtered_waves(extracted_graph: nx.DiGraph,
                           lower_station: float,
                           upper_station: float,
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
