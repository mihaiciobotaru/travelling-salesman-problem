import random


class Solution:
    points = None

    def __init__(self, arg):
        if isinstance(arg, int):
            self.points = [i for i in range(arg)]
            random.shuffle(self.points)
        elif isinstance(arg, list):
            self.points = arg


    def mutate(self):
        a = random.randint(0, len(self.points) - 1)
        b = random.randint(0, len(self.points) - 1)

        self.points[a], self.points[b] = self.points[b], self.points[a]

    def crossover(self, other):
        a = random.randint(0, len(self.points) - 1)
        b = random.randint(0, len(self.points) - 1)

        if a > b:
            a, b = b, a

        child = Solution(len(self.points))

        child.points = self.points[a:b]

        for i in range(len(other.points)):
            if other.points[i] not in child.points:
                child.points.append(other.points[i])

        return child