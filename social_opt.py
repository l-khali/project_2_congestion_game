import math
import numpy as np

def avg_cost(strat, N):
    # scaling factor
    k = N/5

    # compute total cost
    total = 2*strat[0]**2 - (2*N-k)*strat[0] + strat[1]**2 - 3*k*strat[1] + 2*strat[2]**2 - (2*N-5*k)*strat[2] + strat[3]**2 - 3*k*strat[3] + 2*N*(N+k)
    # return average cost
    return total/(2*N)

def split_social_opt(N):
    # scaling factor
    k = N/5

    # social optimum values for each variable
    y1 = (2*N-k)/4
    z1 = 3*k/2
    x1 = N-y1

    y2 = (2*N-5*k)/4
    z2 = 3*k/2
    x2 = N-y2

    # average cost per player under social optimum
    avg_cost = N+k - 1/N*((2*N-k)**2/16+(2*N-5*k)**2/16+9*k**2/4)

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
    avg_costs = []
    for o in atom_opts:
        avg_costs.append(avg_cost(o, N))
    
    # find smallest cost
    ind = np.argmin(avg_costs)
    
    return atom_opts[ind], avg_costs[ind]
    