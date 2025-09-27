import os
import pickle

import networkx as nx

from src.graph_building.interfaces.vertex_data_interface import VertexDataInterface


class GeneratedDataLoader:
    """
    Class for writing and reading pickle files.
    """
    @staticmethod
    def save_pickle(folder_path: str,
                    file_name: str,
                    graph: nx.DiGraph,
                    vertex_interface: VertexDataInterface
                    ):
        """
        Method for saving a graph into a pickle file.
        :param str folder_path: path of the data folder
        :param str file_name: name of the file
        :param nx.DiGraph graph: a directed graph
        :param VertexDataInterface vertex_interface: interface containing vertex data
                                                     necessary for analysis
        """
        os.makedirs(
            os.path.join(folder_path, 'generated'),
            exist_ok=True
        )

        data = {
            'graph': graph,
            'vertex_interface': vertex_interface
        }

        with open(os.path.join(
                folder_path, 'generated', f'{file_name}.pkl'
        ), 'wb') as f:
            pickle.dump(data, f)

    @staticmethod
    def read_pickle(folder_path: str,
                    file_name: str,
                    ) -> dict:
        """
        Method for loading a graph from a pickle file.
        :param str folder_path: path of the target folder
        :param str file_name: name of the file
        :return dict: the loaded graph and vertex data
        """
        with open(os.path.join(
                folder_path, f'{file_name}.pkl'
        ), 'rb') as f:
            data = pickle.load(f)

        return data
