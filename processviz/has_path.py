def convert_to_adjagecy(state, P):
    adjagecy_vector = {i:[] for i in state}
    for i in range(len(P)):
        for j in range(len(P)):
            if P[i][j] != 0:
                adjagecy_vector[state[i]].append(state[j])
    return adjagecy_vector


def is_connected(state, P, source, target):
    vector = convert_to_adjagecy(state, P)
    visit_status = {i: False for i in state}
    queue = []
    queue.append(source)
    while queue != []:
        current_state = queue[0]
        visit_status[current_state] = True
        queue.pop(0)
        for s in vector[current_state]:
            if visit_status[s] == False:
                queue.append(s)
        if target in queue:
            return True
    return False