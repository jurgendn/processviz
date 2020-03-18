def BFS(src):
    vector = self.convert_to_adjagecy()
    visit_status = {i: False for i in self.state}
    queue = []
    queue.append(source)
    while queue != []:
        current_state = queue[0]
        visit_status[current_state] = True
        queue.pop(0)
        for s in vector[current_state]:
            if visit_status[s] == False:
                queue.append(s)
        if target in queue or visit_status[target] == True:
            return True
    return False
