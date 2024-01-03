from solution import Solution

class Point:
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        assert isinstance(other, Point)
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

def assertListOfPoints(input):
    assert isinstance(input, list)
    for point in input:
        assert isinstance(point, list)
        assert len(point) == 2
        assert isinstance(point[0], int)
        assert isinstance(point[1], int)

class Instance:
    input = None
    output = None
    length = None

    def __init__(self, input, output = 0):
        assertListOfPoints(input)
        assert isinstance(output, int)

        points = []

        for point in input:
            points.append(Point(point[0], point[1]))

        self.input = points
        self.output = output
        self.length = len(points)

    def getSolutionDistance(self, solution: Solution):
        distance = 0
        for i in range(self.length):
            distance += self.input[solution.points[i]].distance(self.input[solution.points[(i + 1) % self.length]])

        return distance


def getInstanceFromFile(file_path):
    # Find row with string `NODE_COORD_SECTION`
    # from that string downards are coords of points, read until string `EOF`
    # coords are like n x y where n is number of point and x, y are coordinates

    
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
                return Instance(points)






    
    

    