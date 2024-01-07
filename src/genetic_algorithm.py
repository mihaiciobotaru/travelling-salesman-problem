import random
import matplotlib.pyplot as plt
from solution import Solution
from utils import Point

DATA_FOLDER = 'C:\\Users\\ejump\\travelling-salesman-problem\\data\\'
EPOCHS = 100
POPULATION_SIZE = 1000
MUTATION_PROBABILITY = 0.1
CROSSOVER_PROBABILITY = 0.0

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
            
def on_plot_close(event):
    exit()

def plot_fitness_history():
    x = [i for i in range(len(fitness_history))]
    plt.plot(x, fitness_history, 'r.:')

    plt.xlabel('Epoch')
    plt.ylabel('Fitness')
    
def plot(solution, epoch, close=True):
    plt.subplot(3, 2, (1, 4))
    solution.plot(instance['input'])
    plt.title('Epoch: ' + str(epoch) + ' Fitness: ' + str( "{:.2f}".format(fitness_history[-1])))
    plt.subplot(3, 2, (5, 6))
    plot_fitness_history()

    if close:
        plt.show(block=False)
        plt.pause(0.2)
        plt.clf()
    else:
        plt.show()




if __name__ == "__main__":
    fig = plt.figure(figsize=(12,6))
    fig.canvas.mpl_connect('close_event', on_plot_close)


    instance = getInstanceFromFile(DATA_FOLDER + 'xqf131.tsp')
    population = [Solution(instance['length']) for i in range(POPULATION_SIZE)]

    for i in range(EPOCHS):
        population.sort(key=lambda x: x.getTotalDistance(instance['input']), reverse=True)
        fitness = population[0].getTotalDistance(instance['input'])
        fitness_history.append(fitness)

        if i % 10 == 0:
            print('Epoch: ', i, ' Fitness: ', fitness)
            plot(population[0], i)

        new_population = []

        for j in range(POPULATION_SIZE):
            if random.random() < CROSSOVER_PROBABILITY:
                new_population.append(population[j].crossover(population[j + 1]))
            else:
                new_population.append(population[j])

        for j in range(POPULATION_SIZE):
            if random.random() < MUTATION_PROBABILITY:
                new_population[j].mutate()

        population = new_population

    population.sort(key=lambda x: x.getTotalDistance(instance['input']), reverse=True)
    print('Epoch: ', EPOCHS, ' Fitness: ', fitness_history[-1])

    # dont close the plot window
    plot(population[0], EPOCHS, close=False)

