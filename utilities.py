from random import choice

# CONSTANTS
OCCUPIED_ZONE = 1
FREE_ZONE = 0

WIDTH = 50
STANDARD_DIMENSION = (WIDTH, WIDTH)
START_ID_VALUE = 2

STANDARD_LIST_SPLITTER = -1
STANDARD_DICT_SPLITTER = -2
STANDARD_NUMBER_SPLITTER = -3


class Reader:

    def __init__(self):
        self.clusterMatrix = None

    def read(self, name):

        try:
            self.clusterMatrix = []

            with open(name) as file:

                line = [int(elem) for elem in file.readline().split()]

                OCCUPIED_ZONE = line[0]
                FREE_ZONE = line[1]

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
                value = choice([OCCUPIED_ZONE, OCCUPIED_ZONE, FREE_ZONE])
                line.append(value)
            self.clusterMatrix.append(line)

    def print_input(self):
        for line in self.clusterMatrix:
            print(*line)
        print()

    def get_matrix(self):
        return self.clusterMatrix

class Recognizer:

    def __init__(self, matrixObject):
        self.clusterMatrix = matrixObject
        self.width = len(self.clusterMatrix)
        self.height = len(self.clusterMatrix[0])
        self.currentId = START_ID_VALUE
        self.associativeLengthMap = []

    def get_cluster_properties(self, id):
        return self.associativeLengthMap[id - START_ID_VALUE]

    def find_cluster_with_size(self, size):
        for elem in self.associativeLengthMap:
            if size == elem[0]:
                return elem

    def matrix_verify(self, i, j):

        try:

            if i < 0 or j < 0:
                return False

            return self.clusterMatrix[i][j] == FREE_ZONE
        except:
            return False

    def matrix_iterate(self):

        for i in range(self.width):
            for j in range(self.height):
                if self.clusterMatrix[i][j] == FREE_ZONE:
                    self.associativeLengthMap.append((self.mark_cluster(i, j), i, j))
                    self.currentId += 1

    def fill_cluster(self, information):
        pass

    def mark_cluster(self, i, j):

        self.clusterMatrix[i][j] = self.currentId
        length = 1

        if self.matrix_verify(i + 1, j):
            length += self.mark_cluster(i + 1, j)

        if self.matrix_verify(i - 1, j):
            length += self.mark_cluster(i - 1, j)

        if self.matrix_verify(i, j + 1):
            length += self.mark_cluster(i, j + 1)

        if self.matrix_verify(i, j - 1):
            length += self.mark_cluster(i, j - 1)

        return length

    def print_matrix(self):
        for line in self.clusterMatrix:
            print(*line)
        print()


class Encoder:
    def __init__(self):
        self.message = ""

    def get_package(self, information):
        self.message = self.get_input(information)

    def encode(self):
        pass

    def get_input(self, information):
        t = type(information)
        result = []

        if t is int or t is float:
            result.append(STANDARD_NUMBER_SPLITTER)
            result.extend(self.get_input(str(information)))

        if t is str:
            result = list(information)

        elif t is list or t is tuple:

            for elem in information:

                result.append(STANDARD_LIST_SPLITTER)
                result.extend(self.get_input(elem))

        elif t is dict:

            for key in information:

                result.append(STANDARD_DICT_SPLITTER)
                result.extend(self.get_input(key))
                result.append(STANDARD_DICT_SPLITTER)
                result.extend(self.get_input(information[key]))

        return result


# MAIN
readObject = Reader()
readObject.read("input1.txt")
readObject.print_input()

recognizerObject = Recognizer(readObject.get_matrix())
recognizerObject.matrix_iterate()
recognizerObject.print_matrix()
#print(recognizerObject.get_cluster_properties(15))
dictionary = {'ana': [1.60000023, 3.7, 4.5], 'are': [2.3, 1.0, 3], 'pere': [3, 4, 2]}
encoderObject = Encoder()
print(encoderObject.get_input(dictionary))
