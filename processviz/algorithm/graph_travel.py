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
            if s == target:
                return step
            if visit_status[s] == False:
                queue.append(s)
    return 0


def get_communicating_class(state, P):
    connected_component = [[]]
    status = {i: False for i in state}
    while True:
        counter = 0
        for i in state:
            for j in state:
                if (BFS(state, P, i, j) and BFS(state, P, j, i)):
                    if status[i] == False:
                        connected_component[counter].append(i)
                        status[i] = True
                    if status[j] == False:
                        connected_component[counter].append(j)
                        status[j] = True
            connected_component.append([])
            counter += 1
        if i == state[len(state) - 1] and j == state[len(state) - 1]:
            break
    connected_component = list(filter(None, connected_component))
    return connected_component


def get_containing_class(s, P, state):
    communicating_class = get_communicating_class(s, P)
    for cl in communicating_class:
        if state in cl:
            return cl
    return False


def is_recurrent(s, P, state):
    containing_class = get_containing_class(s, P, state)
    state_vector = convert_to_adjacency(s, P)
    union = set([])
    for i in containing_class:
        union = union.union(set(state_vector[i]))
    return True if union == set(containing_class) else False
