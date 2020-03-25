"""
Thư viện này viết ra phục vụ cho môn học `Các mô hình ngẫu nhiên và ứng dụng`
Sử dụng các thư viện `networkx, pandas, numpy, matplotlib`
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
import pandas as pd


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
                if self.data[i][j] > 0:
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
            self._get_nth_matrix_state(n)
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

    def convert_to_adjagecy(self):
        adjagecy_vector = {i: [] for i in self.state}
        for i in range(len(self.P)):
            for j in range(len(self.P)):
                if self.P[i][j] != 0:
                    adjagecy_vector[self.state[i]].append(self.state[j])
        return adjagecy_vector

    def is_connected(self, source, target):
        vector = self.convert_to_adjagecy()
        visit_status = {i: False for i in self.state}
        queue = []
        queue.append(source)
        while queue != []:
            current_state = queue[0]
            visit_status[current_state] = True
            queue.pop(0)
            for s in vector[current_state]:
                if target == s:
                    return True
                if visit_status[s] == False:
                    queue.append(s)
        return False

    # This part is unused -> comment for later use
    # ------------------------------------------
    # def has_selfloop(self):
    #     for i in range(len(self.P)):
    #         if self.P[i][i] != 0:
    #             return True
    #     return False

    # def rank_test(self):
    #     P = np.subtract(self.P, np.identity(len(self.P)))
    #     if np.linalg.matrix_rank(P) == len(self.P):
    #         return True
    #     return False

    # -------------------------------------------

    def is_regular(self):
        # Check is irreducible
        component = self.get_connected_component()
        if len(component) > 1:
            return False
        tmp = self.get_period(self.state[0])
        if tmp == 1:
            return True
        return False

    # ----------------------------------------------------------
    #   Get period of a state
    # ----------------------------------------------------------

    def cycle_length(self, source):
        vector = self.convert_to_adjagecy()
        visit_status = {i: False for i in self.state}
        step = 0
        queue = [source]
        while queue != []:
            current_state = queue[0]
            visit_status[current_state] = True
            queue.pop(0)
            step += 1
            for s in vector[current_state]:
                if s == source:
                    return step
                if visit_status[s] == False:
                    queue.append(s)
        return step

    def get_connected_component(self):
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
        component = self.get_connected_component()
        for sl in component:
            if target in sl:
                break
        t = []
        if target not in sl:
            return 0
        else:
            for i in sl:
                t.append(self.cycle_length(i))
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

    def _get_index(self, state_set):
        idx_list = []
        tmp = list(self.state)
        try:
            for state in state_set:
                idx_list.append(tmp.index(state))
            del tmp
        except:
            return "State is not in the state set"
        return idx_list

    def _get_mean_state_list(self, state_set):
        tmp = list(self.state)
        tmp = [state for state in tmp if tmp not in state_set]
        return tmp

    def get_mean_time(self, target_set):
        try:
            idx_list = self._get_index(target_set)
            state_list = self._get_mean_state_list(target_set)
            P = self.data
            P = np.delete(P, idx_list, 0)
            P = np.delete(P, idx_list, 1)
            I = np.identity(len(P))
            A = np.subtract(I, P)
            b = np.transpose(np.ones(len(P)))
            x = np.round(np.matmul(np.linalg.inv(A), b), 2)
            del idx_list, P, I, A, b
            mean_time = {"Mean time spent of " +
                         state: x_val for (state, x_val) in zip(state_list, x)}
            return mean_time
        except:
            return "Check your state or matrix"
