P = [[1,2,3],[4,5],[6]]

def get_target(P, target):
    for sl in P:
        if target in sl:
            return sl
    return False

print(get_target(P, 7))