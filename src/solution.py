import random
import matplotlib.pyplot as plt
from utils import pointsDistance



class Solution:
    points = None
    length = None
    fitness = None
    score = None

    costMatrix = None

    def __init__(self, arg, points = None):
        if isinstance(arg, int):
            self.points = [i for i in range(arg)]
            random.shuffle(self.points)
            self.length = arg
        elif isinstance(arg, list):
            self.points = arg
            self.length = len(arg)

    def mutate(self):
        a = random.randint(0, self.length - 1)
        b = random.randint(0, self.length - 1)

        self.points[a], self.points[b] = self.points[b], self.points[a]

    def crossover(self, other):
        return self.scxCrossover(other)
        

    def scxCrossover(self, other):
        offspring_chromosone = [1]

        while len(offspring_chromosone) < self.length:
            i = 0
            selected_alpha = None
            while i < self.length:
                if self.points[i] not in offspring_chromosone:
                    selected_alpha = self.points[i]
                    break
                i += 1

            i = 0
            selected_beta = None
            while i < other.length:
                if other.points[i] not in offspring_chromosone:
                    selected_beta = other.points[i]
                    break
                i += 1


            alpha_cost = Solution.costMatrix[offspring_chromosone[-1]][selected_alpha]
            beta_cost = Solution.costMatrix[offspring_chromosone[-1]][selected_beta]

            if alpha_cost < beta_cost:
                offspring_chromosone.append(selected_alpha)
            else:
                offspring_chromosone.append(selected_beta)

        solution = Solution(offspring_chromosone)
        return solution

    
    def getTotalDistance(self, pointsPositions, circular = False):
        distance = 0

        for i in range(self.length) if circular else range(self.length - 1):
            distance += pointsDistance(pointsPositions[self.points[i]], pointsPositions[self.points[(i + 1) % self.length]])

        return distance
    
    def plot(self, pointsPositions, circular = False):
        x = [pointsPositions[self.points[i]].x for i in range(self.length)]
        y = [pointsPositions[self.points[i]].y for i in range(self.length)]

        if circular:
            x.append(x[0])
            y.append(y[0])

        plt.xlabel('x')
        plt.ylabel('y')
        plt.plot(x, y, 'ro-')
    
     


    def setScore(self, score):
        self.score = score

    def getScore(self):
        return self.score

    def setFitness(self, fitness):
        self.fitness = fitness

    def getFitness(self):
        return self.fitness

