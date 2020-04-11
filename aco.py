from random import randint

from chromozome import Particle


class Aco:
    def __init__(self, start=None, acoParams=None, problParams=None):
        self.problParams = problParams
        self.acoParams = acoParams
        if start is None:
            self.start = 0
        self.pheromoneMatrix = self._initMatrix(self.problParams['nrNodes'], 1.0)
        self.pheromoneMatrixForUpdate = self._initMatrix(self.problParams['nrNodes'])
        self.FirstPass = True
        self.ants = self._initialization()
        self.shortestDistance = None
        self.shortestPath = None
        self.bestAnt = None

    def _initMatrix(self, size, value=0.0):
        mat = []
        for _ in range(size):  # foreach row
            mat.append([float(value) for _ in range(size)])
        return mat

    # DYNAMIC GRAPH

    def dynamic(self):
        change = randint(0, 10)
        if change in range(0, 7):
            # update an edge
            distance = randint(self.problParams['min'] + 1, self.problParams['max'])
            pos1 = randint(0, self.problParams['nrNodes'] // 2)
            pos2 = randint(self.problParams['nrNodes'] // 2 + 1, self.problParams['nrNodes'] - 1)

            print(str(pos1) + "-" + str(pos2) + "\n" + "initial distance: " + str(self.problParams['distMat'][pos1][pos2]))
            self.problParams['distMat'][pos1][pos2] = distance
            print("after change :" + str(self.problParams['distMat'][pos1][pos2]) + "\n")

        if change in range(8, 10):
            pos1 = randint(0, self.problParams['nrNodes'] // 2)
            pos2 = randint(self.problParams['nrNodes'] // 2 + 1, self.problParams['nrNodes'] - 1)
            # delete an edge
            self.problParams['distMat'][pos1][pos2] = 9999999
            self.pheromoneMatrix[pos1][pos2] = 1.0
            print("edge deleted : " + str(pos1) + "-" + str(pos2))

    def _initialization(self):

        self.dynamic()
        if self.FirstPass:
            return [Particle(randint(0, self.problParams['nrNodes'] - 1),
                             [x for x in range(0, self.problParams['nrNodes'])], self.pheromoneMatrix, self.problParams,
                             True) for _ in
                    range(self.acoParams['antCount'])]
        for ant in self.ants:
            ant.__init__(randint(0, self.problParams['nrNodes'] - 1),
                         [x for x in range(0, self.problParams['nrNodes'])], self.pheromoneMatrix, self.problParams)

    def _updatePheromoneMatrix(self):
        for node1 in range(len(self.pheromoneMatrix)):
            for node2 in range(len(self.pheromoneMatrix)):
                # update pheromone -> t[i,j] = (1 - p) * t[i,j] + (delta)t[i,j]
                self.pheromoneMatrix[node1][node2] = (1 - self.acoParams['pheromoneEvaporationCoeff']) * \
                                                     self.pheromoneMatrix[node1][node2]

                self.pheromoneMatrix[node1][node2] += self.pheromoneMatrixForUpdate[node1][node2]

    def _fillPheromoneMatrixForUpdate(self, ant):
        repres = ant.getRepres()
        for i in range(len(repres) - 1):
            # find the pheromone over the route of the ant
            currentPheromoneValue = float(self.pheromoneMatrixForUpdate[repres[i]][repres[i + 1]])

            # update the pheromone along that section of the route

            # (delta)t[i,j] = Q / L[i,j]
            # Q - a pheromone constant
            # L[i,j] - distance between node i and j
            newPheromoneValue = (self.acoParams['pheromoneConstant'] / ant.getDistance())

            self.pheromoneMatrixForUpdate[repres[i]][repres[i + 1]] = currentPheromoneValue + newPheromoneValue
            self.pheromoneMatrixForUpdate[repres[i + 1]][repres[i]] = currentPheromoneValue + newPheromoneValue

    def mainmethod(self):
        bestParticles = []
        bestParticlesFitness = []
        for generation in range(0, self.acoParams['nrGen']):
            for ant in self.ants:
                ant.findpath()

            for ant in self.ants:

                if self.shortestDistance is None and self.shortestPath is None and self.bestAnt is None:
                    self.shortestDistance = ant.getDistance()
                    self.shortestPath = ant.getRepres()
                    self.bestAnt = ant

                if self.shortestDistance > ant.getDistance():
                    self.shortestDistance = ant.getDistance()
                    self.shortestPath = ant.getRepres()
                    self.bestAnt = ant

                self._fillPheromoneMatrixForUpdate(ant)

            print("best particle in generation " + str(generation) + " is x =" + str(self.shortestPath) + '\n' + "with f(x) "
                                                                                                          "= " + str(
                self.shortestDistance))
            bestParticlesFitness.append(self.shortestDistance)
            bestParticles.append(self.shortestPath)

            # self._fillPheromoneMatrixForUpdate(self.bestAnt)

            self._updatePheromoneMatrix()

            if self.FirstPass:
                self.FirstPass = None

            self._initialization()

            self.pheromoneMatrixForUpdate = self._initMatrix(self.problParams['nrNodes'], 0.0)

        return self.shortestPath, self.shortestDistance, bestParticlesFitness
