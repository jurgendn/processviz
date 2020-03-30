"""
Thư viện này viết ra phục vụ cho môn học `Các mô hình ngẫu nhiên và ứng dụng`
Sử dụng các thư viện `networkx, pandas, numpy, matplotlib`
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
import pandas as pd

import processviz.algorithm.graph_travel as gt


def _gcd(a, b):
    if a == 0:
        return b
    return _gcd(b % a, a)


def gcd(arr):
    if len(arr) == 0:
        return 0
    if (len(arr) == 1):
        return arr[0]
    t = arr[0]
    for i in range(len(arr)):
        t = _gcd(t, arr[i])
    return t


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
            self.struct = self.__generate_struct__()

    def from_file(self, path='input.csv'):
        data = pd.read_csv(path)
        matrix = pd.DataFrame(data)
        data = matrix.values.tolist()
        self.pi = data[0]
        self.state = matrix.columns
        self.P = data[1:]
        self.data = self.P
        self.struct = self.__generate_struct__()

    """
    Sinh ra cấu trúc của đồ thị
    Cấu trúc của đồ thị hiện tại như sau:
    ['đỉnh 1', 'đỉnh 2', '{'label':label}']
    """

    def __generate_struct__(self):
        struct = []
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if self.data[i][j] > 0:
                    struct.append([self.state[i], self.state[j],
                                   {'label': self.data[i][j]}])
        return struct

    """
    Sinh ma trận xác suất chuyển trạng thái của quá trình
    """

    def matrix_at(self, n):
        self.data = np.matrix.round(np.linalg.matrix_power(self.P, n), 3)
        self.struct = self.__generate_struct__()

    """
    Sinh đồ thị, đồ thị được lưu vào thư mục img
    """

    def __get_state_vector__(self, n):
        self.matrix_at(n)
        self.state_vector = np.matmul(self.pi, self.data)

    def __get_state_track__(self, n):
        state = np.empty(shape=(len(self.pi), 1))
        state = state.tolist()
        steps = []
        for i in range(n):
            steps.append(i+1)
            self.__get_state_vector__(i)
            state.append(self.state_vector)
        state = np.transpose(state)
        return state.tolist(), steps

    def generate_state_graph(self, n):
        if self.pi == None:
            return "Not found origin state"
        else:
            state, steps = self.__get_state_track__(n)
            legend = self.state
            for i in range(len(self.pi)):
                plt.plot(steps, state[i][1:])
            plt.legend(legend, loc='best')
            plt.title("Distribution state vector through time")
            plt.xlabel("Steps")
            plt.ylabel("Probability")
            plt.savefig('img/state_vector.svg', format='svg', dpi=1200)
            plt.show()

    def generate_graph(self, n=1):
        if self.state is None:
            return "Graph is empty. \n Nothing to show"
        else:
            self.matrix_at(n)
            self = nx.drawing.nx_agraph.to_agraph(nx.DiGraph(self.struct))
            self.layout('dot')
            self.node_attr.update(color='red', height=0.5,
                                  width=0.5, fontname="Calibri", fontsize=10)
            self.edge_attr.update(color='blue', fontsize=8,
                                  fontname="Calibri", rotate=True)
            self.draw('img/Graph.svg')
            self.draw('img/Graph.png')
            img = imread('img/Graph.png')
            plt.axis("off")
            plt.imshow(img)

    def has_path(self, source, target):
        if gt.BFS(self.state, self.P, source=source, target=target) > 0:
            return True
        return False

    def is_connected(self, state1, state2):
        if self.has_path(state1, state2) and self.has_path(state2, state1):
            return True
        return False

    def is_regular(self):
        # Check is irreducible
        component = self.classify_state()
        if len(component) > 1:
            return False
        tmp = self.get_period(self.state[0])
        if tmp == 1:
            return True
        return False

    def is_irreducible(self):
        if len(self.classify_state()) > 1:
            return False
        return True
    # ----------------------------------------------------------
    #   Get period of a state
    # ----------------------------------------------------------

    def classify_state(self):
        connected_component = [[]]
        status = {i: False for i in self.state}
        while True:
            counter = 0
            for i in self.state:
                for j in self.state:
                    if (self.is_connected(i, j) and self.is_connected(j, i)):
                        if status[i] == False:
                            connected_component[counter].append(i)
                            status[i] = True
                        if status[j] == False:
                            connected_component[counter].append(j)
                            status[j] = True
                connected_component.append([])
                counter += 1
            if i == self.state[len(self.state) - 1] and j == self.state[len(self.state) - 1]:
                break
        connected_component = list(filter(None, connected_component))
        return connected_component
    
    def get_period(self, target):
        component = self.classify_state()
        for sl in component:
            if target in sl:
                break
        t = []
        if target not in sl:
            return 0
        else:
            for i in sl:
                t.append(gt.BFS(self.state, self.P, i, i))
            return gcd(t)

    # ----------------------------------------------------
    #   Get steady state
    # ----------------------------------------------------

    def get_steady_state(self):
        A = np.transpose(self.P)
        A = np.subtract(A, np.identity(len(A)))
        A = np.ndarray.tolist(A)
        A.append(np.ndarray.tolist(np.ones(len(A))))
        b = np.ndarray.tolist(np.transpose(np.zeros(len(A))))
        b[len(b)-1] = 1
        # Calc
        return np.matmul(np.linalg.inv(np.matmul(np.transpose(A), A)), np.matmul(np.transpose(A), b))

    # ----------------------------------------------------
    #   Get mean time spent
    # ----------------------------------------------------

    def __get_index__(self, state_set):
        idx_list = []
        tmp = list(self.state)
        try:
            for state in state_set:
                idx_list.append(tmp.index(state))
            del tmp
            return idx_list
        except:
            return "State is not in the state set"

    def __get_absoring_state__(self):
        abr_state = []
        for i in range((len(self.state))):
            if self.P[i][i] == 1:
                abr_state.append(self.state[i])
        return abr_state

    def __get_mean_state_list__(self, state_set):
        tmp = list(self.state)
        tmp = [state for state in tmp if state not in state_set]
        return tmp

    def __get_mean_time_absoring__(self):
        try:
            idx_list = self.__get_index__(self.__get_absoring_state__())
            state_list = self.__get_mean_state_list__(target_set)
            P = self.data
            P = np.delete(P, idx_list, 0)
            P = np.delete(P, idx_list, 1)
            P = np.transpose(P)
            I = np.identity(len(P))
            A = np.subtract(I, P)
            b = np.transpose(np.ones(len(P)))
            x = np.round(np.linalg.solve(A, b), 2)
            del idx_list, P, I, A, b
            mean_time = {"Mean time spent " +
                         state: x_val for (state, x_val) in zip(state_list, x)}
            return mean_time
        except:
            return "Check your state or matrix"

    def __get_mean_time_transient__(self, source=None, target=None):
        idx_list = self.__get_index__(self.__get_absoring_state__())
        P = self.data
        P = np.delete(P, idx_list, 0)
        P = np.delete(P, idx_list, 1)
        P = np.transpose(P)
        I = np.identity(len(P))
        A = np.subtract(I, P)
        A = A.tolist()
        if source == None or target == None:
            return A
