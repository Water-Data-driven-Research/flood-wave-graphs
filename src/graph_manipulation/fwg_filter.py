import networkx as nx


class FWGFilter:
    """
    Class for filtering the flood wave graph.
    """
    @staticmethod
    def filter_date_range(fwg: nx.DiGraph,
                          start_date: str = '1876-01-01',
                          end_date: str = '2019-12-31'
                          ) -> nx.DiGraph:
        """
        Filters the flood wave graph by date range.
        :param nx.DiGraph fwg: the flood wave graph
        :param str start_date: the start date
        :param str end_date: the end date
        :return nx.DiGraph: the filtered flood wave graph
        """
        if start_date == '1876-01-01' and end_date == '2019-12-31':
            return fwg

        final_nodes = [
            node for node in fwg.nodes
            if start_date <= node[1] <= end_date
        ]

        return nx.DiGraph(fwg.subgraph(nodes=final_nodes))

    @staticmethod
    def filter_stations(fwg: nx.DiGraph,
                        lower_station: float = 9.8,
                        upper_station: float = 744.3
                        ) -> nx.DiGraph:
        """
        Filters the flood wave graph between two stations.
        :param nx.DiGraph fwg: the flood wave graph
        :param float lower_station: the downstream station (river kilometer)
        :param float upper_station: the upstream station (river kilometer)
        :return nx.DiGraph: the filtered flood wave graph
        """
        if lower_station == 9.8 and upper_station == 744.3:
            return fwg

        if upper_station < lower_station:
            raise ValueError('Upper station must be upstream from the lower station')

        final_nodes = [
            node for node in fwg.nodes
            if lower_station <= float(node[0]) <= upper_station
        ]

        return nx.DiGraph(fwg.subgraph(nodes=final_nodes))
