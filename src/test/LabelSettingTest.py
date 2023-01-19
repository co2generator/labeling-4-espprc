# **********************************************************
# * Author        : CO2MAKER
# * Email         : 429401330@qq.com
# * Create time   : 2023/1/18 12:37 PM
# * Filename      : LabelSettingTest
# * Description   :
# **********************************************************
import json
import math
from time import time
from random import randint, random

from src.graph.Graph import Graph
from src.graph.GraphNode import GraphNode
from src.graph.GraphEdge import GraphEdge
from src.labeling.LabelSetting import LabelSetting


class LabelSettingTest:

    """Class for testing label setting algorithm on the Solomon Benchmark. """

    def __init__(self, inst_file_path: str, node_num: int):
        with open(inst_file_path, 'r') as f:
            self.solomon_inst = json.load(f)

        self.node_num = node_num

        # initialize node list
        self.node_list = []
        for i in range(self.node_num):
            x_coord = self.solomon_inst['all_customers'][f'{i}']['x_coord']
            y_coord = self.solomon_inst['all_customers'][f'{i}']['y_coord']
            demand = self.solomon_inst['all_customers'][f'{i}']['demand']
            ready_time = self.solomon_inst['all_customers'][f'{i}']['ready_time']
            due_time = self.solomon_inst['all_customers'][f'{i}']['due_time']
            service_time = self.solomon_inst['all_customers'][f'{i}']['service_time']
            self.node_list.append(
                GraphNode(
                    i,
                    x_coord,
                    y_coord,
                    demand,
                    ready_time,
                    due_time,
                    service_time
                )
            )
        # initialize edge dict
        self.edge_dict = {}
        for i in range(self.node_num - 1):
            temp = []
            for j in range(1, self.node_num):
                if i != j:
                    x_1, x_2 = self.node_list[i].x_coord, self.node_list[j].x_coord
                    y_1, y_2 = self.node_list[i].y_coord, self.node_list[j].y_coord
                    euclidean_distance = self._cal_euclidean_distance(x_1, x_2, y_1, y_2)
                    cost = randint(1, 5) * euclidean_distance
                    routing_time = 15 * euclidean_distance
                    temp.append(
                        GraphEdge(
                            i,
                            j,
                            cost,
                            routing_time
                        )
                    )
            self.edge_dict[i] = temp
        self.edge_dict[self.node_num - 1] = []

        self.graph = Graph(self.node_list, self.edge_dict)
        self.label_setting = LabelSetting(self.graph)

    @staticmethod
    def _cal_euclidean_distance(x_1: int, x_2: int, y_1: int, y_2: int) -> int:
        """Calculate euclidean distance.

        Note that, the distance value is floored to integer.
        """
        return int(math.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2))

    def run(self):
        # randomly generate dual value
        dual_val = [100 * random() for _ in range(self.node_num)]
        # dual_val = [0 for _ in range(self.node_num)]
        start_ = time()
        self.label_setting.solve(dual_val)
        end_ = time()

        print(f'Label setting algorithm terminated. {end_ - start_ :.2f} seconds elapsed.')
        print('-' * 100)
        print(f'The reduced cost = {self.label_setting.reduced_cost}')
        print('The shortest path:')
        print(self.label_setting.shortest_path)
