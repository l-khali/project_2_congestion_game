import math
import numpy as np
from scipy.optimize import minimize

def avg_cost(strat, N):
    # scaling factor
    k = N/5

    y1, z1, y2, z2 = strat
    # compute total cost
    total = 2*y1**2 + 4*y1*y2 + 2*y2**2 + z1**2 + 2*z1*z2 + z2**2 + (k-4*N)*y1 + (5*k-4*N)*y2 - 3*k*(z1+z2) + 4*N**2 + 2*N*k
    # return average cost
    return total/(2*N)

def split_social_opt(N):
    # scaling factor
    k = N/5

    def cost(a):
        w1, z1, w2, z2 = a
        return avg_cost([w1+z1, z1, w2+z2, z2], N)
    
    opt = minimize(cost, [0,0,0,0], bounds = ((0,N),(0,N),(0,N),(0,N)))

    w1, z1, w2, z2 = opt.x

    return [w1+z1, z1, w2+z2, w2]

def atom_social_opt(N):
    # splittable social optimum
    y1, z1, y2, z2 = split_social_opt(N)

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
    ind = np.where(avg_costs==min(np.array(avg_costs)))[0]

    return list(set([tuple(o)for o in np.array(atom_opts)[ind]]))
    