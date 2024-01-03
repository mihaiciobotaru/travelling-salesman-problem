import random
from instance import Instance
from solution import Solution
from plot import Plotter

class GeneticAlgortihm:

    EPOCHS = 1000
    POPULATION_SIZE = 1000
    MUTATION_PROBABILITY = 0.1
    CROSSOVER_PROBABILITY = 0.0

    instance = None
    population = None
    plotter = None

    def __init__(self, instance: Instance):
        self.instance = instance
        self.population = [Solution(instance.length) for i in range(self.POPULATION_SIZE)]
        self.plotter = Plotter()

    def run(self):
        for i in range(self.EPOCHS):
            self.population.sort(key=lambda solution: self.instance.getSolutionDistance(solution))

            if i % 10 == 0:
                print('Epoch: ', i, ' Fitness: ', self.instance.getSolutionDistance(self.population[0]))
                self.plotter.drawGraph(self.instance.input, self.population[0].points)

            new_population = []

            for j in range(int(self.POPULATION_SIZE / 2)):
                if random.random() < self.CROSSOVER_PROBABILITY:
                    child = self.population[j].crossover(self.population[random.randint(0, len(self.population) - 1)])
                else:
                    child = self.population[j]

                if random.random() < self.MUTATION_PROBABILITY:
                    child.mutate()

                new_population.append(child)

            self.population = new_population

        self.population.sort(key=lambda solution: self.instance.getSolutionDistance(solution))

        return self.population[0]