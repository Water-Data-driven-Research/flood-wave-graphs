from src.data.interfaces.data_interface import DataInterface
from src.graph_building.delta_peak_finder import DeltaPeakFinder
from src.graph_building.edge_finder import EdgeFinder


class GraphBuilder:
    """
    This class builds the FWG.
    """
    def __init__(self,
                 data_interface: DataInterface,
                 beta: int = 2,
                 delta: int = 2
                 ):
        """
        Constructor.
        :param DataInterface data_interface: the DataInterface instance containing required data
        :param int beta: the number of days allowed after a vertex for continuation
        :param int delta: the number of days that a record is required to be greater
                          than the records before, and to be greater or equal to after
                          to be considered a peak
        """
        self.data_interface = data_interface
        self.beta = beta
        self.delta = delta

        self.delta_peak_finder = DeltaPeakFinder(
            data_interface=self.data_interface,
            delta=self.delta
        )
        self.edge_finder = EdgeFinder(
            gauges=self.data_interface.gauges,
            beta=self.beta
        )

    def run(self):
        """
        Runs the operations for building the graph.
        """
        self.delta_peak_finder.run()
        self.edge_finder.run(vertex_interface=self.delta_peak_finder.vertex_interface)
