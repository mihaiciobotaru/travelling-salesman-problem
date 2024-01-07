import random
import matplotlib.pyplot as plt
from utils import Point, pointsDistance

class Solution:
    points = None
    length = None

    def __init__(self, arg):
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
        a = random.randint(0, self.length - 1)
        b = random.randint(0, self.length - 1)

        if a > b:
            a, b = b, a

        child = Solution(self.length)

        child.points = self.points[a:b]

        for i in range(self.length):
            if other.points[i] not in child.points:
                child.points.append(other.points[i])

        return child
    
    def getTotalDistance(self, pointsPositions, circular = False):
        distance = 0

        for i in range(self.length) if circular else range(self.length - 1):
            distance += pointsDistance(pointsPositions[self.points[i]], pointsPositions[self.points[(i + 1) % self.length]])

        return distance
    
    def plot(self, pointsPositions):
        x = [pointsPositions[self.points[i]].x for i in range(self.length)]
        y = [pointsPositions[self.points[i]].y for i in range(self.length)]
        plt.xlabel('x')
        plt.ylabel('y')
        plt.plot(x, y, 'ro-')

