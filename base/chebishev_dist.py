import numpy as np
def chebishev_roots(n, bounds):
    a,b = bounds
    grid = []
    print(int(n))
    if n == 1: 
        return np.array([(a+b/2)])
    for i in range(1,int(n)):
        node = (a+b)/2 + (b-a)/2*np.cos((2*i-1)/(2*n) * np.pi)
        grid.append(node)
    return np.array(grid)