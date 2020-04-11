import numpy as np


def get_absoring_state(state, P):
    return [state[i] for i in range(len(state)) if P[i][i] == 1]


def get_transient_state(state, P):
    return [state[i] for i in range(len(state)) if P[i][i] != 1]


def get_index(state, target_list):
    return [list(state).index(i) for i in target_list]


def get_transient_matrix(state, P):
    abr_state = get_absoring_state(state, P)
    idx = get_index(state, abr_state)
    P = np.delete(P, idx, 0)
    P = np.delete(P, idx, 1)
    return P


def get_mean_time_transient(state, P):
    return(np.linalg.inv(np.subtract(np.identity(len(get_transient_matrix(state, P))), get_transient_matrix(state, P))))


def get_mean_time_absoring(state, P):
    matrix = get_transient_matrix(state, P)
    step = np.ones(shape=(len(matrix), 1))
    return np.linalg.solve(np.subtract(np.identity(len(matrix)), matrix), step)
