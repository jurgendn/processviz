def gcd_two_num(a, b):
    if a == 0:
        return b
    return gcd_two_num(b % a, a)


def gcd_list(arr):
    if len(arr) == 0:
        return 0
    if (len(arr) == 1):
        return arr[0]
    t = arr[0]
    for i in range(len(arr)):
        t = gcd_two_num(t, arr[i])
    return t
