import random
import matplotlib.pyplot as plt
import numpy as np
from utils import Point, pointsDistance


DATA_FOLDER = 'C:\\Users\\ejump\\travelling-salesman-problem\\data\\'
costMatrix = None
class Solution:
    points = None
    length = None
    fitness = None
    score = None

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


            alpha_cost = costMatrix[offspring_chromosone[-1]][selected_alpha]
            beta_cost = costMatrix[offspring_chromosone[-1]][selected_beta]

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



instance = None
population = None
plotter = None
fitness_history = []

def getInstanceFromFile(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

        for i in range(len(lines)):
            if lines[i].strip() == 'NODE_COORD_SECTION':
                points = []
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() == 'EOF':
                        break
                    line = lines[j].strip().split()
                    points.append([int(line[1]), int(line[2])])
                
                return {
                    'length': len(points),
                    'input': [Point(point[0], point[1]) for point in points]
                }
            
def randomInstance(length = -1):
    coords_max = 1000
    if length == -1:
        length = random.randint(10, 100)
    return {
        'length': length,
        'input': [Point(random.randint(1, coords_max), random.randint(1, coords_max)) for i in range(length)]
    }
            
def on_plot_close(event):
    exit()

def plot_fitness_history():
    x = [i for i in range(len(fitness_history))]
    plt.plot(x, fitness_history, 'r.:')

    plt.xlabel('Epoch')
    plt.ylabel('Fitness')
    
def plot(solution, epoch, circular, close=True):
    plt.subplot(3, 2, (1, 4))
    solution.plot(instance['input'], circular)
    plt.title('Epoch: ' + str(epoch) + ' Score: ' + str(int(fitness_history[-1])))
    plt.subplot(3, 2, (5, 6))
    plot_fitness_history()

    if close:
        plt.show(block=False)
        plt.pause(0.2)
        plt.clf()
    else:
        plt.show()

def fitnessFunction(value):
    value = 1 / np.exp(value)

    value = value * 1000
    value = int(value)
    value = value / 1000
    return min(0.999, max(0.001, value))

def mutatePopulation(population, mutation_rate):
    for i in range(len(population)):
        if random.random() < mutation_rate:
            population[i].mutate()

    return population

def pickMate(population):
    i = 0
    while True:
        if random.random() < population[i].getFitness():
            return population[i]
        i += 1
        i %= POPULATION_SIZE

def crossoverPopulation(population):
    while len(population) < POPULATION_SIZE:
        population.append(pickMate(population).crossover(pickMate(population)))

    return population

def selectPopulation(population, select_rate):
    new_population_size = max(int(POPULATION_SIZE * select_rate), 10)
    selected_population = []

    i = 0
    while len(selected_population) < new_population_size:
        if random.random() < population[i].getFitness():
            selected_population.append(population[i])
        i += 1
        i %= POPULATION_SIZE

    return selected_population
    
        

def computeFitness(population):
    population.sort(key=lambda x: x.getScore())
    max_score = population[-1].getScore()
    min_score = population[0].getScore()
    range_score = min(max_score - min_score, 1)

    for i in range(POPULATION_SIZE):
        value = ((population[i].getScore() - min_score) / range_score)
        population[i].setFitness(fitnessFunction(value))
            
    return population

EPOCHS = 300
POPULATION_SIZE = 5000
MUTATION_PROBABILITY = 0.1
SELECT_RATE = 0.6
TEMPERATURE_MAX = EPOCHS * 0.9

if __name__ == "__main__":
    fig = plt.figure(figsize=(12,6))
    fig.canvas.mpl_connect('close_event', on_plot_close)

    circular = True
    #instance = getInstanceFromFile(DATA_FOLDER + 'xqf131.tsp')
    instance = randomInstance(30)
    costMatrix = np.array(
        [[pointsDistance(instance['input'][i], instance['input'][j]) for j in range(instance['length'])] for i in range(instance['length'])]
    )
    population = [Solution(instance['length'], instance['input']) for i in range(POPULATION_SIZE)]

 
    temperature = TEMPERATURE_MAX
    
    for i in range(EPOCHS):
        select_rate = SELECT_RATE * (( TEMPERATURE_MAX - temperature) / TEMPERATURE_MAX) + 0.01
        mutation_rate = MUTATION_PROBABILITY + (1 - MUTATION_PROBABILITY) * (temperature / TEMPERATURE_MAX)
        for j in range(POPULATION_SIZE):
            population[j].setScore(population[j].getTotalDistance(instance['input'], circular))

        population = computeFitness(population)
        population.sort(key=lambda x: x.getScore())
        fitness_history.append(population[0].getScore())

        print('Epoch: ', i, 
              ' Select rate: ', "{:.2f}".format(select_rate) , 
              ' Mutation rate: ', "{:.2f}".format(mutation_rate), 
              ' Temperature: ', str(int(temperature)),
              ' Diversity: ', "{:.2f}".format(population[-1].getScore() / population[0].getScore()),
              ' Score: ', int(fitness_history[-1])
        )
        plot(population[0], i, circular)
        
        population = selectPopulation(population, select_rate)
        population = crossoverPopulation(population)
        population = mutatePopulation(population, mutation_rate)
        if temperature > 0:
            temperature -= 1
        
    plot(population[0], EPOCHS, circular, close=False)

