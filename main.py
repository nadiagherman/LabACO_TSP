import networkx as nx
import tsplib95 as tsp
import numpy as np

from aco import Aco


def readFileHard(filename):
    network = {}
    tsp_file = tsp.load_problem(filename)
    g = tsp_file.get_graph()
    nrCities = len(g.nodes())
    network['nrCities'] = nrCities
    matrix = nx.to_numpy_matrix(g)
    network['min'] = np.amin(matrix)
    network['max'] = np.amax(matrix)
    graph = []
    for i in range(nrCities):
        graph.append([])
        for j in range(nrCities):
            value = matrix.item((i, j))
            if value == 0:
                value += 1
            graph[i].append(value)
    print(nrCities)
    print(graph)
    network['mat'] = graph
    return network


def main():

    net = readFileHard("date_in2.txt")
    print(str(net['min']) + " " + str(net['max']))

    problParams = {'distMat': net['mat'], 'nrNodes': net['nrCities'], 'alpha': 0.9, 'beta': 2.1, 'min': net['min'], 'max': net['max']}
    acoParams = {'antCount': 40, 'nrGen': 200, 'pheromoneConstant': 100.0, 'pheromoneEvaporationCoeff': 0.4}

    aco = Aco(0, acoParams, problParams)
    solution, best_distance, all_bests = aco.mainmethod()

    print('solution = ' + str(solution) + " with distance = " + str(best_distance))


main()