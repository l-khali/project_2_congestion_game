import math
import numpy as np

def split_social_opt(N):
    # social optimum values for each variable
    y1 = (2*N-1)/4
    z1 = 3/2
    x1 = N-y1

    y2 = (2*N-5)/4
    z2 = 3/2
    x2 = N-y2

    # average cost per player under social optimum
    avg_cost = N+1 - 1/N*((2*N-1)**2/16+(2*N-5)**2/16+9/4)

    return y1, z1, x1, y2, z2, x2, avg_cost

def atom_social_opt(N):
    # splittable social optimum
    y1, z1, _, y2, z2, _, _ = split_social_opt(N)

    split_opt = [y1, z1, y2, z2]

    # either round up or round down each value
    strats = []
    for o in split_opt:
        strats.append([math.floor(o), math.ceil(o)])

    # every permutation of either rounding up or down
    atom_opts = [[y1, z1, y2, z2] for y1 in strats[0] for z1 in strats[1] for y2 in strats[2] for z2 in strats[3]]

    # compute cost for every strategy permutation
    costs = []
    for o in atom_opts:
        costs.append(2*o[0]**2 - (2*N-1)*o[0] + o[1]**2 - 3*o[1] + 2*o[2]**2 - (2*N-5)*o[2] + o[3]**2 - 3*o[3] + 2*N*(N+1))
    
    # find smallest cost
    ind = np.argmin(costs)
    
    return atom_opts[ind], costs[ind]/(2*N)
    