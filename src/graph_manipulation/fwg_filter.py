import json
import os

import networkx as nx


class FWGFilter:
    """
    Class for filtering the flood wave graph.
    """
    CONFIG_PATH = os.path.join(
        os.path.dirname(__file__), 'config', 'filter_config.json'
    )
    _config = None

    @classmethod
    def load_config(cls) -> dict:
        """
        Loads the filter configuration JSON.
        :return dict: configuration values
        """
        if cls._config is None:
            with open(cls.CONFIG_PATH) as f:
                return json.load(f)
        return cls._config

    @classmethod
    def filter_date_range(cls,
                          fwg: nx.DiGraph,
                          start_date: str = None,
                          end_date: str = None
                          ) -> nx.DiGraph:
        """
        Filters the flood wave graph by date range.
        :param nx.DiGraph fwg: the flood wave graph
        :param str start_date: the start date
        :param str end_date: the end date
        :return nx.DiGraph: the filtered flood wave graph
        """
        config = cls.load_config()

        if start_date is None:
            start_date = config['start_date']
        if end_date is None:
            end_date = config['end_date']

        if start_date == config['start_date'] and end_date == config['end_date']:
            return fwg

        final_nodes = [
            node for node in fwg.nodes
            if start_date <= node[1] <= end_date
        ]

        return nx.DiGraph(fwg.subgraph(nodes=final_nodes))

    @classmethod
    def filter_stations(cls,
                        fwg: nx.DiGraph,
                        lower_station: float = None,
                        upper_station: float = None
                        ) -> nx.DiGraph:
        """
        Filters the flood wave graph between two stations.
        :param nx.DiGraph fwg: the flood wave graph
        :param float lower_station: the downstream station (river kilometer)
        :param float upper_station: the upstream station (river kilometer)
        :return nx.DiGraph: the filtered flood wave graph
        """
        config = cls.load_config()

        if lower_station is None:
            lower_station = config['lower_station']
        if upper_station is None:
            upper_station = config['upper_station']

        if lower_station == config['lower_station'] and upper_station == config['upper_station']:
            return fwg

        if upper_station < lower_station:
            raise ValueError('Upper station must be upstream from the lower station')

        final_nodes = [
            node for node in fwg.nodes
            if lower_station <= float(node[0]) <= upper_station
        ]

        return nx.DiGraph(fwg.subgraph(nodes=final_nodes))
