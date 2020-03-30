def convert_to_adjacency(state, P):
    adjagecy_vector = {i: [] for i in state}
    for i in range(len(P)):
        for j in range(len(P)):
            if P[i][j] != 0:
                adjagecy_vector[state[i]].append(state[j])
    return adjagecy_vector


def BFS(state, P, source=None, target=None):
    vector = convert_to_adjacency(state, P)
    visit_status = {i: False for i in state}
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