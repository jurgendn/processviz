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
import processviz.algorithm.mean_time as mt
import processviz.algorithm.side_algo as sa


class MarkovChain:
    def __init__(self):
        pass

    '''
    Initialize data of Markov chain:
        From stdin:
            Provide state space, transition matrix, initial vector(optional)
        From file:
            Import from a csv file.
            Please include path to file
    '''

    def from_stdin(self, state=None, data=None, pi=None):
        if state == None or data == None:
            return "Nothing is given"
        else:
            self.P = data
            self.pi = pi
            self.state = state

    def from_file(self, path='input.csv'):
        data = pd.read_csv(path)
        matrix = pd.DataFrame(data)
        data = matrix.values.tolist()
        self.pi = data[0]
        self.state = matrix.columns
        self.P = data[1:]

    '''
    Generate graph structure:
    Structure is provided by a list with each element has form:
    [state1, state2, 'label':value]
    '''

    def __generate_struct__(self, n):
        matrix = self.matrix_at(n)
        struct = []
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                if matrix[i][j] > 0:
                    struct.append([self.state[i], self.state[j],
                                   {'label': matrix[i][j]}])
        del matrix
        return struct

    """
    Generate transition matrix, state vector at specific step
    """

    def matrix_at(self, n=1):
        return np.matrix.round(np.linalg.matrix_power(self.P, n), 3)

    def state_vector_at(self, n=1):
        return list(np.matmul(self.pi, self.matrix_at(n)))

    '''
    Generate state distribution graph and transition graph through time
        __get_state_through_time__:
            get each state distribution at time
        generate_state_graph:
            plot graph from given figures
        generate_graph:
            create a graph
    '''

    def __get_state_through_time__(self, n):
        state = [[i] for i in self.pi]
        steps = []
        for i in range(n):
            steps.append(i+1)
            state.append(self.state_vector_at(i))
        state = (np.transpose(state[len(self.P):])).tolist()
        return state, steps

    def generate_state_graph(self, n):
        if self.pi == None:
            return "Not found origin state"
        else:
            state, steps = self.__get_state_through_time__(n)
            legend = self.state
            for i in range(len(self.pi)):
                plt.plot(steps, state[i])
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
            self = nx.drawing.nx_agraph.to_agraph(
                nx.DiGraph(self.__generate_struct__(n)))
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

    # This part is use for further properties of Markov chain

    def has_path(self, source, target):
        '''
        Check if a state can reach another state.
        Use BFS to travel through graph
        For more detail, go to graph_travel in algorithm
        '''
        return True if gt.BFS(self.state, self.P, source=source, target=target) > 0 else False

    def is_connected(self, state1, state2):
        '''
        Check if two state is connected
        '''
        return True if self.has_path(state1, state2) and self.has_path(state2, state1) else False

    def is_regular(self):
        # Check is irreducible
        component = self.classify_state()
        if len(component) > 1:
            return False
        tmp = self.get_period(self.state[0])
        return True if tmp == 1 else False

    def is_irreducible(self):
        '''
        Return True if Matrix is reducible
        False if not
        '''
        return True if len(self.classify_state()) > 1 else False

    def classify_state(self):
        '''
        Classify matrix into closed set of state
        use BFS
        '''
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
        '''
        Return period of a state
        '''
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
            return sa.gcd_list(t)

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
    '''
    get_mean_time(source, target, type):
        if type == 'absoring':
            return expected time to reach absoring state
        if type == 'transient':
            case1: source and target are given:
                return expected time to reach target from source
            case2: at least source or target is not provided:
                return matrix
        if type is not provided correctly, return "Invalid"
    '''

    def get_mean_time(self, source=None, target=None, type='transient'):
        try:
            state = mt.get_transient_state(self.state, self.P)
            matrix = mt.get_mean_time_transient(self.state, self.P)
            if type == 'absoring':
                return state, mt.get_mean_time_absoring(self.state, self.P)
            elif type == 'transient':
                if source == None or target == None:
                    return state, matrix
                else:
                    return state, matrix[state.index(source)][state.index(target)]
        except:
            return "Invalid"
