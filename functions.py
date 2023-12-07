import numpy as np
import scipy.integrate as integrate
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt

def cost(player_type, current_cost, current_strategy, strategies1, strategies2, player, N):
    scalar = N / 10
    x1 = sum(strategies1 == 3) 
    x2 = sum(strategies2 == 3)
    y1 = int(N/2) - x1
    y2 = int(N/2) - x2
    z1 = sum(strategies1 == 2) 
    z2 = sum(strategies2 == 2)
    new_costs1 = []
    new_costs2 = []
    new_strat = 0
    if player_type == 1:
        if current_strategy == 1:
            cost2 = y1 + y2 + (z1 + 1) + z2
            cost3 = (x1 + 1) + x2 + 2*scalar
            if cost2 < current_cost:
                new_strat = 2
                z1 += 1
            if cost3 < current_cost:
                new_strat = 3
                x1 += 1
                y1 -= 1
            
        if current_strategy == 2:
            cost1 = y1 + y2 + 3*scalar
            cost3 = (x1 + 1) + x2 + 2*scalar
            if cost1 < current_cost:
                new_strat = 1
                z1 -= 1
            if cost3 < current_cost:
                new_strat = 3
                x1 += 1
                y1 -= 1
                z1 -= 1
        
        else:
            cost1 = y1 + 1 + y2 + 3*scalar
            cost2 = y1 + 1 + y2 + z1 + 1 + z2
            if cost1 < current_cost:
                new_strat = 1
                x1 -= 1
                y1 += 1
            if cost2 < current_cost:
                new_strat = 2
                x1 -= 1
                y1 += 1
                z1 += 1
        
        if new_strat:
            strategies1[player] = new_strat

    if player_type == 2:
        if current_strategy == 1:
            cost2 = y1 + y2 + 2*scalar + (z1 + 1) + z2
            cost3 = (x1 + 1) + x2
            if cost2 < current_cost:
                new_strat = 2
                z2 += 1
            if cost3 < current_cost:
                new_strat = 3
                x2 += 1
                y2 -= 1
            
        if current_strategy == 2:
            cost1 = y1 + y2 + 2*scalar + 3*scalar
            cost3 = (x1 + 1) + x2
            if cost1 < current_cost:
                new_strat = 1
                z2 -= 1
            if cost3 < current_cost:
                new_strat = 3
                x2 += 1
                y2 -= 1
                z2 -= 1
        
        else:
            cost1 = y1 + 1 + y2 + 2*scalar + 3*scalar
            cost2 = y1 + 1 + y2  + 2*scalar + z1 + 1 + z2
            if cost1 < current_cost:
                new_strat = 1
                x2 -= 1
                y2 += 1
            if cost2 < current_cost:
                new_strat = 2
                x2 -= 1
                y2 += 1
                z2 += 1

        if new_strat:
            strategies2[player] = new_strat
    if new_strat:
        player1_costs = [y1 + y2 + 3*scalar, y1 + y2 + z1 + z2, x1 + x2 + 2*scalar]
        player2_costs = [y1 + y2 + 2*scalar + 3*scalar, y1 + y2 + 2*scalar + z1 + z2, x1 + x2]

        for player1 in range(int(N/2)):
            new_costs1.append(player1_costs[strategies1[player1]-1])

        for player2 in range(int(N/2)):
            new_costs2.append(player2_costs[strategies2[player2]-1])

        return strategies1, strategies2, new_costs1, new_costs2
    else:
        return None


def congestion_equilibrium(N = 10, nsim = 100):
    equilibria = []
    count1_total = {"Path 1":0,"Path 2":0,"Path 3":0}
    count2_total = {"Path 1":0,"Path 2":0,"Path 3":0}
    found = 0
    equ_tracker = []
    for sim in range(nsim):
        strategies1 = np.random.randint(1,4,int(N/2))
        strategies2 = np.random.randint(1,4,int(N/2))

        current_costs1 = np.array([10000000000]*int(N/2))
        current_costs2 = np.array([10000000000]*int(N/2))

        player_moved = True
        iteration_count = 0
        while player_moved:
            player_moved = False
            for player1 in range(5):
                iteration_count += 1
                update1 = cost(1, current_costs1[player1], strategies1[player1], strategies1, strategies2, player1, N)
                if update1:
                    player_moved = True
                    strategies1, strategies2, current_costs1, current_costs2 = update1
            for player2 in range(5):
                iteration_count += 1
                update2 = cost(2, current_costs2[player2], strategies2[player2], strategies1, strategies2, player2, N)
                if update2:
                    player_moved = True
                    strategies1, strategies2, current_costs1, current_costs2 = update2
            if iteration_count > 10000: 
                print("No equilibria found")
                return None
        if player_moved == False:
            count1 = Counter(strategies1)
            count2 = Counter(strategies2)

            count1["Outlet 1"] = count1[1]
            del count1[1]
            count1["Outlet 2"] = count1[2]
            del count1[2]
            count1["Library Cafe"] = count1[3]
            del count1[3]
            count2["Outlet 1"] = count2[1]
            del count2[1]
            count2["Outlet 2"] = count2[2]
            del count2[2]
            count2["Library Cafe"] = count2[3]
            del count2[3]

            equ_tracker.append([count1["Outlet 1"], count1["Outlet 2"], count1["Library Cafe"]])
            equ_tracker.append([count2["Outlet 1"], count2["Outlet 2"], count2["Library Cafe"]])

            if (count1, count2) not in equilibria:
                # print("Equilibrium found!")
                found += 1
                equilibria.append((count1, count2))
                count1_total["Path 3"] += count1["Library Cafe"]
                count2_total["Path 3"] += count2["Library Cafe"]
                count1_total["Path 1"] += count1["Outlet 1"]
                count2_total["Path 1"] += count2["Outlet 1"]
                count1_total["Path 2"] += count1["Outlet 2"]
                count2_total["Path 2"] += count2["Outlet 2"]
    
    print("Number of equilibria found:", found)

    fig, axs = plt.subplots(4, 2, figsize=(17, 30))
    axs[0,0].tick_params(axis='both', which='major', labelsize=15)
    axs[0,0].bar([1,2,3], equ_tracker[-2], color="blue", tick_label=["Outlet 1", "Outlet 2", "Library Cafe"])
    axs[0,0].set_title(f"{N} Player Game: Type 1 Player Example", fontsize=20)
    axs[0,1].tick_params(axis='both', which='major', labelsize=15)
    axs[0,1].bar([1,2,3], equ_tracker[-1], color="red", tick_label=["Outlet 1", "Outlet 2", "Library Cafe"])
    axs[0,1].set_title(f"{N} Player Game: Type 2 Player Example", fontsize=20)

    axs[1,0].tick_params(axis='both', which='major', labelsize=15)
    axs[1,0].bar([1,2,3], equ_tracker[-4], color="blue", tick_label=["Outlet 1", "Outlet 2", "Library Cafe"])
    axs[1,0].set_title(f"{N} Player Game: Type 1 Player Example", fontsize=20)
    axs[1,1].tick_params(axis='both', which='major', labelsize=15)
    axs[1,1].bar([1,2,3], equ_tracker[-3], color="red", tick_label=["Outlet 1", "Outlet 2", "Library Cafe"])
    axs[1,1].set_title(f"{N} Player Game: Type 2 Player Example", fontsize=20)

    axs[2,0].tick_params(axis='both', which='major', labelsize=15)
    axs[2,0].bar([1,2,3], equ_tracker[-6], color="blue", tick_label=["Outlet 1", "Outlet 2", "Library Cafe"])
    axs[2,0].set_title(f"{N} Player Game: Type 1 Player Example", fontsize=20)
    axs[2,1].tick_params(axis='both', which='major', labelsize=15)
    axs[2,1].bar([1,2,3], equ_tracker[-5], color="red", tick_label=["Outlet 1", "Outlet 2", "Library Cafe"])
    axs[2,1].set_title(f"{N} Player Game: Type 2 Player Example", fontsize=20)

    axs[3,0].tick_params(axis='both', which='major', labelsize=15)
    axs[3,0].bar([1,2,3], [count1_total["Path 1"], count1_total["Path 2"], count1_total["Path 3"]], color="blue", tick_label=["Outlet 1", "Outlet 2", "Library Cafe"])
    axs[3,0].set_title("Type 1 Player Equilibria Combined", fontsize=20)
    axs[3,1].tick_params(axis='both', which='major', labelsize=15)
    axs[3,1].bar([1,2,3], [count2_total["Path 1"], count2_total["Path 2"], count2_total["Path 3"]], color="red", tick_label=["Outlet 1", "Outlet 2", "Library Cafe"])
    axs[3,1].set_title("Type 2 Player Equilibria Conbined", fontsize=20)


    # G1 = nx.DiGraph()
    # G1.add_edge(1,2,color='r',weight=count1_total["y"], label="y")
    # G1.add_edge(2,3,color='b',weight=count1_total["y"] - count1_total["z"], label="y-z")
    # G1.add_edge(3,2,color='g',weight=count1_total["z"], label="z")
    # G1.add_edge(1,3,color='g',weight=count1_total["x"], label="x")

    # pos=nx.spring_layout(G1,seed=7)
    # fig, ax = plt.subplots()
    # nx.draw_networkx_nodes(G1, pos, ax=ax)
    # nx.draw_networkx_labels(G1, pos, ax=ax)

    # curved_edges = list(G1.edges(2,3)) + list(G1.edges(3,2))
    # straight_edges = list(G1.edges(1,2)) + list(G1.edges(1,3))
    # # curved_weights = [G1[u] for u in enumerate(curved_edges)]
    # # straight_weights = [G1[u][v]['weight'] for u,v in straight_edges]
    # curved_weights = [count1_total["y"] - count1_total["z"], count1_total["z"]]
    # straight_weights = [count1_total["y"], count1_total["x"]]
    # nx.draw_networkx_edges(G1, pos, ax=ax, edgelist=straight_edges, width=straight_weights, arrows=False)

    # # pos=nx.spring_layout(G1,seed=5)
    # # colors = [G1[u][v]['color'] for u,v in edges]
    # # weights = [G1[u][v]['weight'] for u,v in edges]

    # # nx.draw(G1, pos, edge_color=colors, width=weights, connectionstyle=f'arc3, rad = {0.25}')
    # nx.draw_networkx_edges(G1, pos, ax=ax, edgelist=curved_edges, connectionstyle=f'arc3, rad = {0.25}', width=curved_weights)
    # # nx.draw_networkx_edge_labels(G1, pos, edge_labels=nx.get_edge_attributes(G1,'label'), font_size=15)
    # edge_labels = dict([((u, v,), f'{d["weight"]}\n\n{G1.edges[(v,u)]["weight"]}')
    #             for u, v, d in G1.edges(data=True) if pos[u][0] > pos[v][0]])
    # nx.draw_networkx_edge_labels(G1, pos, edge_labels=edge_labels, font_color='red')



    return equilibria
