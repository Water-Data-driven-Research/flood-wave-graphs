import networkx as nx
import numpy as np
import pandas as pd

from src.graph_manipulation.fwg_filter import FWGFilter


class SlopeAnalyzer:
    """
    This class is responsible for the analysis of slope values.
    """
    def __init__(self, fwg: nx.DiGraph):
        """
        Constructor.
        :param nx.DiGraph fwg: the flood wave graph to analyze
        """
        self.fwg = fwg

    def get_slope_distribution(self) -> dict:
        """
        Count the ratio of edges with positive/zero/negative slopes.
        :return dict: ratios {'positive': x, 'zero': y, 'negative': z}
        """
        slopes = [data.get('slope') for _, _, data in self.fwg.edges(data=True)]
        if not slopes:
            return {'positive': 0.0, 'zero': 0.0, 'negative': 0.0}

        df = pd.DataFrame({'slope': slopes})
        df['category'] = np.select(
            condlist=[df['slope'] > 0, df['slope'] == 0, df['slope'] < 0],
            choicelist=['positive', 'zero', 'negative'],
            default='unknown'
        )

        dist = df.groupby('category')\
            .size()\
            .div(len(df))\
            .reindex(index=['positive', 'zero', 'negative'], fill_value=0.0)\
            .to_dict()

        return dist

    def get_slope_error_ratios_between_stations(self,
                                                lower_station: float = None,
                                                upper_station: float = None
                                                ) -> dict:
        """
        For a station pair, compute error ratios (zero/negative slopes).
        Data is aggregated yearly and quarterly.
        :param float lower_station: the downstream station
        :param float upper_station: the upstream station
        :return dict: keys are frequencies, values are the respective data
        """
        filtered_graph = FWGFilter.filter_stations(
            fwg=self.fwg,
            lower_station=lower_station,
            upper_station=upper_station
        )

        edges_data = [
            (pd.to_datetime(u[1]), data.get('slope'))
            for u, v, data in filtered_graph.edges(data=True)
        ]
        if not edges_data:
            empty = pd.DataFrame(columns=['error ratio'])
            return {'yearly': empty, 'quarterly': empty}

        df = pd.DataFrame(data=edges_data, columns=['date', 'slope']).set_index('date')
        df['is_error'] = df['slope'] <= 0

        yearly = df.resample('YE')['is_error'].mean().to_frame(name='error ratio')
        yearly.index = yearly.index.to_period('Y')

        quarterly = df.resample('QE')['is_error'].mean().to_frame(name='error ratio')
        quarterly.index = quarterly.index.to_period('Q')

        return {'yearly': yearly, 'quarterly': quarterly}
