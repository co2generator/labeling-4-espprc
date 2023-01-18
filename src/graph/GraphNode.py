# **********************************************************
# * Author        : CO2MAKER
# * Email         : 429401330@qq.com
# * Create time   : 2023/1/16 9:42 AM
# * Filename      : GraphNode
# * Description   :
# **********************************************************
class GraphNode:

    """Class for node on the defined directed or undirected graph.

    Typical usage example:

    node = GraphNode()
    print(node)
    """

    def __init__(self,
                 id_: int,
                 x_coord: int,
                 y_coord: int,
                 demand: int,
                 earliest_time: int,
                 latest_time: int,
                 service_time: int
                 ):
        self.id = id_
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.demand = demand
        self.earliest_time = earliest_time    # release time
        self.latest_time = latest_time        # due time
        self.service_time = service_time
