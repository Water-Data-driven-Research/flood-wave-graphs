class VertexDataInterface:
    """
    Class for storing data created in GraphDataGenerator and used in analysis.
    """
    def __init__(self, data: dict = None):
        """
        Constructor.
        :param dict data: Dictionary: the keys represent the data structures.
        The expected keys are:
        - 'vertices'
        - 'river_kms'
        """
        self.vertices = dict()
        self.river_kms = list()

        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)
