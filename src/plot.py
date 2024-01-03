import matplotlib.pyplot as plt
import matplotlib as mpl
from instance import Point

class Plotter:
    def __init__(self):


        pass

    def drawGraph(self, vertices: list, edges: list):
        
        x = []
        y = []
        for vertex in vertices:
            x.append(vertex.x)
            y.append(vertex.y)

        plt.plot(x, y, 'ro')

        # edges is the list of points that are connected
        # edges = [ 0, 3 , 2 ,1 ,5, 4]

        # vertice is a lsit of Points

        for i in range(len(edges)):
            if i == len(edges) - 1:
                plt.plot([vertices[edges[i]].x, vertices[edges[0]].x], [vertices[edges[i]].y, vertices[edges[0]].y], 'k-')
            else:
                plt.plot([vertices[edges[i]].x, vertices[edges[i + 1]].x], [vertices[edges[i]].y, vertices[edges[i + 1]].y], 'k-')

        plt.show(block=False)
        plt.pause(0.2)
        plt.clf()