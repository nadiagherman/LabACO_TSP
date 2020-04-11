import math
import random


class Particle:

    def __init__(self, initial, available, pheromoneMatrix, problParams=None, firstIteration=False):
        self.problParams = problParams
        self.initial = initial
        self.available = list(available)
        self.repres = []
        self.distance = 0.0
        self.current = initial
        self.pheromoneMatrix = pheromoneMatrix
        self.firstIteration = firstIteration
        self._update_particle(initial)
        self.isFinished = False

    def getRepres(self):
        if self.isFinished:
            return self.repres
        else:
            return None

    def getDistance(self):
        if self.isFinished:
            return self.distance
        else:
            return None

    def _update_particle(self, node):
        self.repres.append(node)
        self.available.remove(node)

        # if we visited every city from the graph
        if len(self.available) == 0:
            self.distance += float(self.problParams['distMat'][self.repres[-1]][self.repres[0]])
            self.repres.append(self.repres[0])

    def findpath(self):
        while self.available:
            nextOne = self._pick()
            self._addpath(self.current, nextOne)
        self.isFinished = True

    def _addpath(self, start, end):

        self._update_particle(end)
        self.distance += float(self.problParams['distMat'][start][end])
        self.current = end

    def _pick(self):
        # if it's the first iteration (there are no pheromones), we pick a random next location
        if self.firstIteration:
            return random.choice(self.available)

        quality = {}
        sum = 0.0

        # p[i,j] = (1/distance)^beta * (pheromone)^alpha

        for possible_next in self.available:
            pheromone_amount = float(self.pheromoneMatrix[self.current][possible_next])
            distance = float(self.problParams['distMat'][self.current][possible_next])

            fitness = math.pow((1 / distance), self.problParams['beta'])
            quality[possible_next] = math.pow(pheromone_amount, self.problParams['alpha']) * fitness
            sum += quality[possible_next]

        random_q = random.random()
        probability_sum = 0.0
        probability_index = 0
        for possible_next in quality:
            roulette_value = (quality[possible_next] / sum)
            if random_q <= roulette_value + probability_sum:
                return possible_next
            probability_sum += roulette_value
