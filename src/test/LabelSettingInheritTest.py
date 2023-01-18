# **********************************************************
# * Author        : CO2MAKER
# * Email         : 429401330@qq.com
# * Create time   : 2023/1/18 7:33 PM
# * Filename      : LabelSettingInheritTest
# * Description   :
# **********************************************************
from src.graph.Graph import Graph
from src.graph.GraphEdge import GraphEdge
from src.labeling.LabelSetting import LabelSetting, Label


class LabelSettingInheritTest(LabelSetting):

    def __init__(self, graph: Graph):
        super().__init__(graph)

    # Override solve method
    def solve(self, dual_val: list):
        pass

    # Override label extension
    def label_extension(self, cur_label: Label, out_edge: GraphEdge):
        # we can customize label extension method here, e.g. add robust routing time
        pass

    # Override dominance
    def dominance(self, label_2_compare: Label):
        # we can add more specific dominance rule here, e.g. add lower bound
        pass



