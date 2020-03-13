from random import choice

# CONSTANTS
OCCUPIED_ZONE = 1
FREE_ZONE = 0

WIDTH = 256
STANDARD_DIMENSION = (WIDTH, WIDTH)
START_ID_VALUE = 2

STANDARD_LIST_SPLITTER = -1
STANDARD_DICT_SPLITTER = -2
STANDARD_NUMBER_SPLITTER = -3

#GLOBAL VARIABLES
FILLING_COUNTER = 0
CLUSTER_ID = 0


class Reader:

    def __init__(self):
        self.clusterMatrix = None

    # read cluster matrix from file or generate one
    def read(self, name):
        global OCCUPIED_ZONE, FREE_ZONE

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

    # create cluster matrix
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

    # get cluster's size and start position with id
    def get_cluster_properties(self, id):
        return self.associativeLengthMap[id - START_ID_VALUE]

    # get cluster's id
    def get_cluster_matrix_value(self, i, j):
        return self.clusterMatrix[i][j]

    # return cluster to fit the input size
    def find_cluster_with_size(self, size):

        for elem in self.associativeLengthMap:
            if size <= elem[0]:
                return elem

        return -1, -1, -1

    # verify if a position exists and if it contains a specific element(comp)
    def matrix_verify(self, i, j, comp=FREE_ZONE):

        try:

            if i < 0 or j < 0:
                return False

            return self.clusterMatrix[i][j] == comp
        except:
            return False

    # mark clusters with id
    def matrix_iterate(self):

        for i in range(self.width):
            for j in range(self.height):
                if self.clusterMatrix[i][j] == FREE_ZONE:
                    self.associativeLengthMap.append((self.mark_cluster(i, j), i, j))
                    self.currentId += 1

    # fill cluster with input data
    def fill_cluster(self, i, j, information, length):

        #print(i, j)

        if length >= len(information):
            return 0
        elif CLUSTER_ID == self.clusterMatrix[i][j]:
            self.clusterMatrix[i][j] = information[length]
        else:
            return 0

        if self.matrix_verify(i + 1, j, CLUSTER_ID):
            length += self.fill_cluster(i + 1, j, information, length + 1)

        if self.matrix_verify(i - 1, j, CLUSTER_ID):
            length += self.fill_cluster(i - 1, j, information, length + 1)

        if self.matrix_verify(i, j + 1, CLUSTER_ID):
            length += self.fill_cluster(i, j + 1, information, length + 1)

        if self.matrix_verify(i, j - 1, CLUSTER_ID):
            length += self.fill_cluster(i, j - 1, information, length + 1)

        return 1

    # fill cluster with id
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

    # update matrix with message
    def update_cluster_matrix(self, message):
        global CLUSTER_ID

        size, positionX, positionY = self.find_cluster_with_size(len(message))
        if positionY == -1 and positionX == -1:
            print("No cluster with this dimension")
        else:
            CLUSTER_ID = self.get_cluster_matrix_value(positionX, positionY)
            self.fill_cluster(positionX, positionY, message, 0)
            CLUSTER_ID = 0

        return positionX, positionY, message

    def print_matrix(self):
        for line in self.clusterMatrix:
            print(*line)
        print()


class Encoder:
    def __init__(self):
        self.message = ""

    def get_package(self, information):
        self.message = self.get_input(information)
        return self.message

    def encode(self):
        pass

    # transform any structure into string
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
message = encoderObject.get_package(dictionary)

print(*recognizerObject.update_cluster_matrix(message))
print()

recognizerObject.print_matrix()