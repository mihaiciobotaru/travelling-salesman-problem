from instance import Instance, getInstanceFromFile
from plot import Plotter
from genetic_algorithm import GeneticAlgortihm 

def main():
    GA = GeneticAlgortihm(instance = getInstanceFromFile("C:\\Users\\ejump\\travelling-salesman-problem\\data\\xqf131.tsp"))
    GA.run()


if __name__ == "__main__":
    main()
