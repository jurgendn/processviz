def _get_index(self, state_set):
    idx_list = []
    for state in state_set:
        idx_list.append(self.state.index(state))
    return idx_list


def get_mean_time(self, target_set):
    idx_list = self._get_index(target_set)
    P = self.data
    P = np.delete(P, idx_list, 0)
    P = np.delete(P, idx_list, 1)
    I = np.identity(len(P))
    A = np.subtract(I, P)
    b = np.transpose(np.ones(len(P)))
    x = np.linalg.solve(A, b)
    return x
