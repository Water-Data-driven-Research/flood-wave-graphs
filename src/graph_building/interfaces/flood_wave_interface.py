class FloodWaveInterface:
    """
    Stores flood waves found in FloodWaveExtractor.
    """
    def __init__(self, flood_waves: list):
        """
        Constructor.
        :param list flood_waves: found flood waves
        """
        self.flood_waves = flood_waves
