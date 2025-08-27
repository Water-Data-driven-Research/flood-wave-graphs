class EdgeInterface:
    """
    Class for storing edges used in the creation of the FWG.
    """
    def __init__(self, edges: dict = None):
        """
        Constructor.
        :param dict edges: the potential edges of the flood wave graph
        """
        self.edges = edges
