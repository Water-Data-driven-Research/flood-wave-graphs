import networkx as nx


class FloodWaveInterface:
    """
    Stores flood waves found in FloodWaveExtractor.
    """
    def __init__(self, data: dict = None):
        """
        Constructor.
        :param dict data: Dictionary: the keys represent the data structures.
        The expected keys are:
        - 'flood_waves'
        - 'extracted_graph'
        """
        self.flood_waves = list()
        self.extracted_graph = nx.DiGraph()

        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)
