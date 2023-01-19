# **********************************************************
# * Author        : CO2MAKER
# * Email         : 429401330@qq.com
# * Create time   : 2023/1/16 9:41 AM
# * Filename      : LabelSetting
# **********************************************************
from queue import PriorityQueue
from copy import deepcopy
from src.graph.Graph import Graph
from src.graph.GraphEdge import GraphEdge


class Label:

    """Class for label in the labeling-4-espprc algorithm.

    This is an python implementation of label setting algorithm proposed by Boland et al. in

    Boland, N., Dethridge, J., & Dumitrescu, I. (2006). Accelerated label setting algorithms
    for the elementary resource constrained shortest path problem. Operations Research Letters, 34(1), 58-68.

    And an outstanding java implementation of this algorithm has been developed by Xiong W. Q., which can
    be found at,

    https://github.com/xiongwq16/exact-algorithm/blob/master/src/vrptw/algorithm/subproblem/labelalgorithm/SpptwccViaLabelSetting.java

    """

    def __init__(self,
                 graph_node_id: int,
                 revised_cost: float,
                 routing_time: float,
                 demand: float,
                 pre_label=None):
        self.graph_node_id = graph_node_id
        self.revised_cost = revised_cost
        self.routing_time = routing_time
        self.demand = demand
        self.pre_label = pre_label
        self.is_node_reachable = []
        self.reachable_nodes_num = 0

    def dominate(self, other, flag=False) -> bool:
        """Check whether can dominate other label.

        Note that, if the node is sink node, then it is only need compare the cost.

        Args:
            other: other label
            flag: whether it is sink node or not

        Returns: whether the label can dominate the other label.

        """
        # If it is sink node
        if flag:
            return self.revised_cost < other.revised_cost
        # Otherwise:
        if (self.demand > other.demand) or (self.revised_cost > other.revised_cost) or (self.routing_time > other.routing_time):
            return False
        # If reachable nodes is smaller than other label, then it cannot dominate other.
        if self.reachable_nodes_num < other.reachable_nodes_num:
            return False
        # If there exists unreachable nodes that other label can reach, then it cannot dominate other.
        for i in range(len(self.is_node_reachable)):
            if (not self.is_node_reachable[i]) and other.is_node_reachable[i]:
                return False

        return True

    def get_visited_nodes(self) -> list:
        """Get visited nodes."""
        node_list = []
        cur_label = self
        while cur_label is not None:
            node_list.append(cur_label.graph_node_id)
            cur_label = cur_label.pre_label
        # reverse visited nodes
        node_list.reverse()
        return node_list

    def update_reachable_nodes(self, reachable_nodes: list):
        """Update reachable node set."""
        self.is_node_reachable = reachable_nodes[:]
        for item in reachable_nodes:
            if item:
                self.reachable_nodes_num += 1

    def __eq__(self, other):
        if self.graph_node_id != other.graph_node_id:
            return False
        if self.demand != other.demand:
            return False
        if self.routing_time != other.routing_time:
            return False
        cur_label_1, cur_label_2 = self, other
        while cur_label_1.pre_label is not None:
            if cur_label_2 is None:
                return False
            if cur_label_1.graph_node_id != cur_label_2.graph_node_id:
                return False
            cur_label_1 = cur_label_1.pre_label
            cur_label_2 = cur_label_2.pre_label

        if cur_label_2.pre_label is not None:
            return False

        return True

    def __lt__(self, other):
        if self.revised_cost < other.revised_cost:
            return True
        if self.revised_cost >= other.revised_cost:
            return False
        if self.routing_time < other.routing_time:
            return True
        if self.routing_time >= other.routing_time:
            return False
        if self.demand < other.demand:
            return True
        if self.demand >= other.demand:
            return False


class LabelSetting:

    """Class for general label setting algorithm.

    Typical usage example:

    ls = LabelSetting(graph_)
    ls.solve()

    """

    def __init__(self, graph: Graph, branch_arc=None, branch_value=None, capacity=100):
        self.graph = deepcopy(graph)
        self.capacity = capacity
        if branch_arc is not None:
            self.graph.revise_dist_map(branch_arc, branch_value)

        self._unprocessed_labels = PriorityQueue()
        self._label_dict = {i: [] for i in range(self.graph.node_num)}    # label list for every nodes
        # Solution info
        self.reduced_cost = 0
        self.shortest_path = []
        self.original_cost = 0

    def solve(self, dual_val: list):
        """Solve a elementary shortest path problem via labeling-4-espprc approach."""
        # Note that, we should reset properties first
        self.reset()
        # Revise cost map
        self.graph.revise_cost_map(dual_val)
        # Start from source node
        init_label = Label(0, 0, 0, 0)
        reachable_nodes = self._cal_reachable_nodes([True for _ in range(self.graph.node_num)], init_label)
        init_label.update_reachable_nodes(reachable_nodes)
        self._label_dict[0].append(init_label)
        self._unprocessed_labels.put_nowait(init_label)

        while not self._unprocessed_labels.empty():
            # Get lexico-graphically minimal label and remove it from queue
            cur_label = self._unprocessed_labels.get_nowait()
            cur_graph_node_id = cur_label.graph_node_id
            # Extension and Dominance
            for edge in self.graph.edge_dict[cur_graph_node_id]:
                self.label_extension(cur_label, edge)

        # Get optimal shortest path
        self.reduced_cost = self._label_dict[self.graph.node_num - 1][0].revised_cost
        self.shortest_path = self._label_dict[self.graph.node_num - 1][0].get_visited_nodes()
        self.original_cost = self.graph.get_original_cost(self.shortest_path)

    def label_extension(self, cur_label: Label, out_edge: GraphEdge):
        """Extend label to reachable nodes."""
        cur_node_id, next_node_id = cur_label.graph_node_id, out_edge.to_

        if not cur_label.is_node_reachable[next_node_id]:
            return

        demand = cur_label.demand + self.graph.node_list[next_node_id].demand

        routing_time = cur_label.routing_time + self.graph.node_list[next_node_id].service_time + out_edge.routing_time

        if routing_time < self.graph.node_list[next_node_id].earliest_time:
            routing_time = self.graph.node_list[next_node_id].earliest_time

        revised_cost = cur_label.revised_cost + self.graph.revised_cost_map[cur_node_id, next_node_id]
        new_label = Label(next_node_id, revised_cost, routing_time, demand, pre_label=cur_label)
        new_label.update_reachable_nodes(self._cal_reachable_nodes(cur_label.is_node_reachable, new_label))

        # Use dominance rule to check whether can be dominated by other labels
        self.dominance(new_label)

    def _cal_reachable_nodes(self, pre_label_reachable_nodes: list, new_label: Label) -> list:
        """Calculate reachable nodes set."""
        next_node_id = new_label.graph_node_id
        # Cal reachable nodes set
        # Note that, since the routing time and demand are non-decreasing,
        # the unreachable nodes of last label must be unreachable for the
        # current node.
        reachable_nodes = pre_label_reachable_nodes[:]
        # set the current node as unreachable
        reachable_nodes[next_node_id] = False
        # Check the reachable node of last label whether still reachable.
        for edge in self.graph.edge_dict[next_node_id]:
            to_ = edge.to_
            if not reachable_nodes[to_]:
                continue
            demand = new_label.demand + self.graph.node_list[to_].demand
            if demand > self.capacity:
                reachable_nodes[to_] = False
            routing_time = new_label.routing_time + self.graph.node_list[to_].service_time + edge.routing_time
            if routing_time > self.graph.node_list[to_].latest_time:
                reachable_nodes[to_] = False

        return reachable_nodes

    def dominance(self, label_2_compare: Label):
        """Use basic dominance rule."""
        cur_node_id = label_2_compare.graph_node_id
        processed_labels = self._label_dict[cur_node_id]

        is_possible_dominated_by_next_label = True
        dominance_flag = True if (cur_node_id == self.graph.node_num - 1) else False

        # compare with all the processed labels
        temp, is_dominated = [], False
        for item in processed_labels:
            if label_2_compare.dominate(item, dominance_flag):
                # skip if they are equal
                if is_possible_dominated_by_next_label and label_2_compare == item:
                    return
                # if the current label can dominate one label, then the other label in the processed labels list
                # can not dominate the current label
                is_possible_dominated_by_next_label = False
            else:
                temp.append(item)

            if is_possible_dominated_by_next_label and item.dominate(label_2_compare, dominance_flag):
                is_dominated = True
                break

        if not is_dominated:
            temp.append(label_2_compare)
            if cur_node_id != self.graph.node_num - 1:
                self._unprocessed_labels.put_nowait(label_2_compare)

        self._label_dict[cur_node_id] = temp

    def reset(self):
        # reset properties
        self.reduced_cost = 0
        self.shortest_path = []
        self._label_dict = {i: [] for i in range(self.graph.node_num)}
        self._unprocessed_labels = PriorityQueue()


