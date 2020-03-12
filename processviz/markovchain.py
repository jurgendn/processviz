"""
Thư viện này viết ra phục vụ cho môn học `Các mô hình ngẫu nhiên và ứng dụng`
Sử dụng các thư viện `networkx, pandas, numpy, matplotlib`
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
import pandas as pd


class MarkovChain:

    """
    Constructor function: Generate blank instance
    Có 2 cách để xích:
        - Nhập từ file csv:
            Sử dụng from_file
        - Nhập từ bàn phím:
            Sử dụng from_stdin
    """

    def __init__(self):
        self.data = None
        self.state = None
        self.struct = None

    def from_stdin(self, state=None, data=None, pi=None):
        if state == None or data == None:
            return "Nothing is given"
        else:
            self.P = data
            self.pi = pi
            self.data = self.P
            self.state = state
            self.struct = self._generate_struct()

    def from_file(self, path='input.csv'):
        data = pd.read_csv(path)
        matrix = pd.DataFrame(data)
        data = matrix.values.tolist()
        self.pi = data[0]
        self.state = matrix.columns
        self.P = data[1:]
        self.data = self.P
        self.struct = self._generate_struct()

    """
    Sinh ra cấu trúc của đồ thị
    Cấu trúc của đồ thị hiện tại như sau:
    ['đỉnh 1', 'đỉnh 2', '{'label':label}']
    """

    def _generate_struct(self):
        struct = []
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                struct.append([self.state[i], self.state[j],
                               {'label': self.data[i][j]}])
        return struct

    """
    Sinh ma trận xác suất chuyển trạng thái của quá trình
    """

    def _get_nth_matrix_state(self, n):
        self.data = np.matrix.round(np.linalg.matrix_power(self.P, n), 3)
        self.struct = self._generate_struct()

    """
    Sinh đồ thị, đồ thị được lưu vào thư mục img
    """

    def _get_state_vector(self, n):
        self._get_nth_matrix_state(n)
        self.state_vector = np.matmul(self.pi, self.data)

    def _get_state_track(self, n):
        state = np.empty(shape=(len(self.pi), 1))
        state = state.tolist()
        steps = []
        for i in range(n):
            steps.append(i+1)
            self._get_state_vector(i)
            for j in range(len(self.pi)):
                state[j].append(self.state_vector[j])
        return state, steps

    


    def generate_state_graph(self, n):
        if self.pi == None:
            return "Not found origin state"
        else:
            state, steps = self._get_state_track(n)        
            legend = self.state
            for i in range(len(self.pi)):
                plt.plot(steps, state[i][1:])
            plt.legend(legend, loc = 'best')
            plt.title("Distribution state vector through time")
            plt.xlabel("Steps")
            plt.ylabel("Probability")
            plt.savefig('img/state_vector.svg', format='svg', dpi=1200)
            plt.show()

    def generate_graph(self, n=1):
        if self.state is None:
            return "Graph is empty. \n Nothing to show"
        else:
            self._get_nth_matrix_state(n)
            self = nx.drawing.nx_agraph.to_agraph(nx.DiGraph(self.struct))
            self.layout('dot')
            self.node_attr.update(color='red', height=0.5,
                                  width=0.5, fontname="Calibri", fontsize=10)
            self.edge_attr.update(color='blue', fontsize=8,
                                  fontname="Calibri", rotate=True)
            self.draw('img/Graph.eps')
            img = imread('img/Graph.eps')
            plt.axis("off")
            plt.imshow(img)