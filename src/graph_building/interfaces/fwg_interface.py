import networkx as nx


class FWGInterface:
    """
    Class used to store the FWG.
    """
    def __init__(self, fwg: nx.DiGraph = None):
        """
        Constructor.
        :param nx.DiGraph fwg: the generated flood wave graph
        """
        self.fwg = fwg
