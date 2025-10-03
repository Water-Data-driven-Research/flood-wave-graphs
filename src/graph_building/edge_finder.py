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
        :param list gauges: list of stations
        :param int beta: the number of days allowed after a vertex for continuation
        """
        self.gauges = gauges
        self.beta = beta

        self.edge_interface: EdgeInterface = None

    def run(self, vertex_interface: VertexDataInterface):
        """
        We take neighboring gauges and find all edges going between them.
        :param VertexDataInterface vertex_interface: interface with vertices
        """
        edges = dict()
        for upstream, downstream in zip(self.gauges[:-1], self.gauges[1:]):
            edges[(upstream, downstream)] = self.find_edges(
                upstream=upstream,
                downstream=downstream,
                vertices=vertex_interface.vertices
            )

        self.edge_interface = EdgeInterface(edges=edges)

    def find_edges(self,
                   upstream: str,
                   downstream: str,
                   vertices: dict
                   ) -> list:
        """
        We find the edges between two stations.
        :param str upstream: the start station
        :param str downstream: the end station
        :param dict vertices: potential vertices of the graph
        :return list: found edges
        """
        upstream_vertices = vertices[upstream]
        downstream_vertices = vertices[downstream]

        upstream_dates = pd.to_datetime(
            list(upstream_vertices.keys()),
            format='ISO8601'
        )
        downstream_dates = pd.to_datetime(
            list(downstream_vertices.keys()),
            format='ISO8601'
        )

        found_edges = list()
        for up_date in upstream_dates:
            cond = (downstream_dates >= up_date) & \
                   (downstream_dates <= up_date + pd.Timedelta(days=self.beta))
            down_dates = downstream_dates[cond]
            for down_date in down_dates:
                up_date = up_date.strftime('%Y-%m-%d')
                down_date = down_date.strftime('%Y-%m-%d')

                up_level = upstream_vertices[up_date]['value']
                down_level = downstream_vertices[down_date]['value']
                distance = float(downstream) - float(upstream)
                slope = (down_level - up_level) / distance

                found_edges.append(
                    ((up_date, down_date), slope)
                )

        return found_edges
