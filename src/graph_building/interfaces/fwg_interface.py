import networkx as nx


class FWGInterface:
    """
    Class used to store the FWG.
    """
    def __init__(self):
        """
        Constructor. The only member variable is the graph instance.
        """
        self.fwg = nx.DiGraph()
