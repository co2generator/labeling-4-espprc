# **********************************************************
# * Author        : CO2MAKER
# * Email         : 429401330@qq.com
# * Create time   : 2023/1/16 10:32 AM
# * Filename      : GraphEdge
# * Description   :
# **********************************************************
class GraphEdge:

    """Class for edge on the defined directed or undirected graph.

    Typical usage:

    from_, to_ = 1, 2
    cost, revised_cost = 100, -50
    routing_time = 20
    edge = GraphEdge(from_, to_, cost, revised_cost, routing_time)

    """

    def __init__(self,
                 from_: int,
                 to_: int,
                 revised_cost: float,
                 routing_time: int
                 ):
        self.from_ = from_
        self.to_ = to_
        self.revised_cost = revised_cost
        self.routing_time = routing_time

    def __lt__(self, other):
        return self.revised_cost < other.revised_cost

    def __eq__(self, other):
        if self.from_ != other.from_:
            return False
        if self.to_ != other.to_:
            return False
        return True

    def __str__(self):
        return f'({self.from_}, {self.to_})'
