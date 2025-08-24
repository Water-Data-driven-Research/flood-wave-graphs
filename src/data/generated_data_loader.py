import os
import pickle

import networkx as nx


class GeneratedDataLoader:
    """
    Class for writing and reading pickle files.
    """
    @staticmethod
    def save_pickle(folder_path: str,
                    file_name: str,
                    graph: nx.DiGraph
                    ):
        """
        Method for saving a graph into a pickle file.
        :param str folder_path: path of the data folder
        :param str file_name: name of the file
        :param nx.DiGraph graph: a directed graph
        """
        os.makedirs(
            os.path.join(folder_path, 'generated'),
            exist_ok=True
        )

        with open(os.path.join(
                folder_path, 'generated', f'{file_name}.pkl'
        ), 'wb') as f:
            pickle.dump(graph, f)
