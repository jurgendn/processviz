def _gcd(a, b):
    if a == 0:
        return b
    return _gcd(b%a, int(b/a))

def gcd(arr):
    t = arr[0]
    for i in range(len(arr)):
        t = _gcd(t, arr[i])
    return t 