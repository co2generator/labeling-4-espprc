# **********************************************************
# * Author        : CO2MAKER
# * Email         : 429401330@qq.com
# * Create time   : 2023/1/16 9:41 AM
# * Filename      : Graph
# * Description   :
# **********************************************************
from src.util.ORException import NotEqual


class Graph:

    """Class for defined directed or undirected graph.

    Note that, the passed edge dict is required to be, e.g.

    edge_list = {
        node_id_1: [edge_1, ..., edge_m],
        node_id_2: [edge_n, ..., edge_k]
    }

    Typical usage example:

    graph = Graph(node_list_, edge_list_)
    graph.outgoing_edge_sort()

    """

    def __init__(self, node_list: list, edge_dict: dict):
        self.node_list = node_list
        self.edge_dict = edge_dict    # key: node id, value: edge list
        self.original_cost_map = {}
        self.revised_cost_map = {}

        # check if the number of nodes are equal, otherwise raise NotEqual exception
        if len(node_list) != len(edge_dict):
            raise NotEqual(
                f"The input node list has {len(node_list)} nodes, while edge list has {len(edge_dict)} nodes."
            )

        self.node_num = len(node_list)
        self._init_original_cost_map()

    def _init_original_cost_map(self):
        """Initialize cost map."""
        for i in range(self.node_num):
            for edge in self.edge_dict[i]:
                self.original_cost_map[edge.from_, edge.to_] = edge.revised_cost

    def get_original_cost(self, shortest_path: list) -> float:
        """Get original cost."""
        cur, cost = shortest_path[0], 0
        for next_ in range(1, len(shortest_path)):
            cost += self.original_cost_map[cur, shortest_path[next_]]
            cur = shortest_path[next_]
        return cost

    def outgoing_edge_sort(self):
        """Sort the outgoing edge for every node.

        Note that, sometimes this method can speed up the solution process of ESPPRC. However, since
        the sorting can be time consuming, sometimes it also san reduce the efficiency.

        """
        for node_index in range(self.node_num):
            self.edge_dict[node_index].sort()

    def revise_dist_map(self, branch_arc: tuple, branch_value: int):
        """Revise distance map when branching."""
        from_, to_ = branch_arc[0], branch_arc[1]
        if branch_value == 0:
            # Remove the branch arc from edge list
            for edge in self.edge_dict[from_]:
                if edge.to_ == to_:
                    self.edge_dict[from_].remove(edge)
        else:
            # Remove all the arcs between from_ and to_ node of branch arc except the branch arc
            for edge in self.edge_dict[from_]:
                if edge.to_ != to_:
                    self.edge_dict[from_].remove(edge)

    def revise_cost_map(self, dual_val: list):
        """Revise cost map when perform Column Generation."""
        for key in self.original_cost_map.keys():
            from_ = key[0]
            self.revised_cost_map[key] = self.original_cost_map[key] - dual_val[from_]

