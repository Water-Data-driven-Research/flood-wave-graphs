from itertools import product

import pandas as pd

from src.graph_building.interfaces.edge_interface import EdgeInterface
from src.graph_building.interfaces.vertex_data_interface import VertexDataInterface


class EdgeFinder:
    """
    This class is responsible for finding edges between vertices.
    """
    def __init__(self,
                 gauges: list,
                 beta: int
                 ):
        """
        Constructor.
        :param list gauges:
        :param int beta:
        """
        self.gauges = gauges
        self.beta = beta

        self.edge_interface = EdgeInterface()

    def run(self, vertex_interface: VertexDataInterface):
        """

        :param VertexDataInterface vertex_interface:
        """
        edges = dict()
        for upstream, downstream in zip(self.gauges[:-1], self.gauges[1:]):
            edges[f"{upstream}-{downstream}"] = self.find_edges(
                upstream_vertices=vertex_interface.vertices[upstream],
                downstream_vertices=vertex_interface.vertices[downstream]
            )

        self.edge_interface.edges = edges

    def find_edges(self,
                   upstream_vertices: dict,
                   downstream_vertices: dict
                   ) -> list:
        """

        :param dict upstream_vertices:
        :param dict downstream_vertices:
        :return list:
        """
        found_edges = list()

        upstream_dates = pd.to_datetime(
            list(upstream_vertices.keys()),
            format='ISO8601'
        )
        downstream_dates = pd.to_datetime(
            list(downstream_vertices.keys()),
            format='ISO8601'
        )

        for up_date in upstream_dates:
            cond = (downstream_dates >= up_date) & \
                   (downstream_dates <= up_date + pd.Timedelta(days=self.beta))

            next_dates = downstream_dates[cond]
            new_edges = list(
                product(
                    [up_date.strftime('%Y-%m-%d')],
                    [date.strftime('%Y-%m-%d') for date in next_dates]
                )
            )

            found_edges.extend(new_edges)

        return found_edges
