import networkx as nx


class FWGFilter:
    """
    Class for filtering the flood wave graph.
    """
    @staticmethod
    def filter_date_range(fwg: nx.DiGraph,
                          start_date: str,
                          end_date: str
                          ) -> nx.DiGraph:
        """
        Filters the flood wave graph by date range.
        :param nx.DiGraph fwg: the flood wave graph
        :param str start_date: the start date
        :param str end_date: the end date
        :return nx.DiGraph: the filtered flood wave graph
        """
        final_nodes = [
            node for node in fwg.nodes
            if start_date <= node[1] <= end_date
        ]

        return nx.DiGraph(fwg.subgraph(nodes=final_nodes))

    @staticmethod
    def filter_stations(fwg: nx.DiGraph,
                        first_station: float,
                        second_station: float
                        ) -> nx.DiGraph:
        """
        Filters the flood wave graph between two stations.
        :param nx.DiGraph fwg: the flood wave graph
        :param float first_station: the first station (river kilometer)
        :param float second_station: the second station (river kilometer)
        :return nx.DiGraph: the filtered flood wave graph
        """
        lower_station = min(
            first_station,
            second_station
        )
        upper_station = max(
            first_station,
            second_station
        )

        final_nodes = [
            node for node in fwg.nodes
            if lower_station <= float(node[0]) <= upper_station
        ]

        return nx.DiGraph(fwg.subgraph(nodes=final_nodes))
