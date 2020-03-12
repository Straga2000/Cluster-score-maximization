from random import choice

# CONSTANTS
OCCUPIED_ZONE = 0
FREE_ZONE = 1
STANDARD_DIMENSION = (100, 100)


class Reader:

    def __init__(self):
        self.clusterMatrix = None

    def read(self, name):

        try:
            self.clusterMatrix = []

            with open(name) as file:

                line = [int(elem) for elem in file.readline().split()]

                while len(line) != 0:
                    self.clusterMatrix.append(line)
                    line = [int(elem) for elem in file.readline().split()]
        except:
            self.create_input(STANDARD_DIMENSION)

    def create_input(self, dimensions):

        width, height = dimensions
        self.clusterMatrix = []

        for i in range(width):
            line = []
            for j in range(height):
                value = choice([OCCUPIED_ZONE, FREE_ZONE])
                line.append(value)
            self.clusterMatrix.append(line)


    def print_input(self):
        for line in self.clusterMatrix:
            print(*line)

readObject = Reader()
readObject.read("input1.txt")
readObject.print_input()