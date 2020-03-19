from random import choice
from PIL import Image

# CONSTANTS
OCCUPIED_ZONE = 1
FREE_ZONE = 0

WIDTH = 256
STANDARD_DIMENSION = (WIDTH, WIDTH)
START_ID_VALUE = 2

STANDARD_LIST_SPLITTER = -1
STANDARD_DICT_SPLITTER = -2
STANDARD_NUMBER_SPLITTER = -3

STANDARD_UNUSED_SPACE = 64

#GLOBAL VARIABLES
FILLING_COUNTER = 0
CLUSTER_ID = 0


class Reader:

    def __init__(self):
        self.clusterMatrix = None

    def read_matrix_cluster(self, name):
        pass

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
            self.create_input()

    # create cluster matrix
    def create_input(self, dimensions=STANDARD_DIMENSION):

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

        minimal = STANDARD_UNUSED_SPACE
        index = -1
        for i in range(len(self.associativeLengthMap)):
            #print(minimal, index)
            value = self.associativeLengthMap[i][0] - size

            if value == 0:
                return self.associativeLengthMap[i]
            elif 0 < value < minimal:
                minimal = self.associativeLengthMap[i][0] - size
                index = i

        if index == -1:
            return -1, -1, -1
        else:
            return self.associativeLengthMap[index]

    # verify if a position exists and if it contains a specific element(comp)
    def matrix_verify(self, i, j, comp= FREE_ZONE):

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

        if length >= len(information):
            return 0
        elif self.clusterMatrix[i][j] == CLUSTER_ID:
            self.clusterMatrix[i][j] = information[length]

        if self.matrix_verify(i + 1, j, CLUSTER_ID):
            length += self.fill_cluster(i + 1, j, information, length + 1)
        elif self.matrix_verify(i - 1, j, CLUSTER_ID):
            length += self.fill_cluster(i - 1, j, information, length + 1)
        elif self.matrix_verify(i, j + 1, CLUSTER_ID):
            length += self.fill_cluster(i, j + 1, information, length + 1)
        elif self.matrix_verify(i, j - 1, CLUSTER_ID):
            length += self.fill_cluster(i, j - 1, information, length + 1)

        return 1

    # fill cluster with id
    def mark_cluster(self, i, j, marker = None):

        if marker is None:
            self.clusterMatrix[i][j] = self.currentId
        else:
            self.clusterMatrix[i][j] = marker
        length = 1

        if self.matrix_verify(i + 1, j) and length < WIDTH:
            length += self.mark_cluster(i + 1, j)
        elif self.matrix_verify(i - 1, j) and length < WIDTH:
            length += self.mark_cluster(i - 1, j)
        elif self.matrix_verify(i, j + 1) and length < WIDTH:
            length += self.mark_cluster(i, j + 1)
        elif self.matrix_verify(i, j - 1) and length < WIDTH:
            length += self.mark_cluster(i, j - 1)

        return length

    """""
    def search_for_id(self, i, j, searchId):

        if searchId == self.clusterMatrix[i][j]:
            return i, j

        if self.matrix_verify(i + 1, j):
            self.search_for_id(i + 1, j, searchId)
        elif self.matrix_verify(i - 1, j):
            self.search_for_id(i - 1, j, searchId)
        elif self.matrix_verify(i, j + 1):
            self.search_for_id(i, j + 1, searchId)
        elif self.matrix_verify(i, j - 1):
            self.search_for_id(i, j - 1, searchId)

        return 0, 0
    """""

    # update matrix with message
    def update_cluster_matrix(self, message):
        global CLUSTER_ID

        size, positionX, positionY = self.find_cluster_with_size(len(message))

        print(size - len(message))

        if positionY == -1 and positionX == -1:
            print("No cluster with this dimension")
            CLUSTER_ID = 0
        else:
            CLUSTER_ID = self.get_cluster_matrix_value(positionX, positionY)
            self.fill_cluster(positionX, positionY, message, 0)

            """"
            if size - len(message) != 0:
                print(size - len(message))
                positionX, positionY = self.search_for_id(positionX, positionY, CLUSTER_ID)
                self.mark_cluster(positionX, positionY)
                self.currentId += 1
            """
        return CLUSTER_ID, positionX, positionY, message

    def enlarge_cluster_matrix(self):
        for i in range(self.width - 1):
            for j in range(self.height - 1):
                if self.clusterMatrix[i][j] == OCCUPIED_ZONE and self.clusterMatrix[i][j + 1] == OCCUPIED_ZONE:
                    if self.clusterMatrix[i + 1][j + 1] == OCCUPIED_ZONE or self.clusterMatrix[i + 1][j] == OCCUPIED_ZONE:
                        # print("Am resetat elementul:", i, j)
                        self.clusterMatrix[i][j] = FREE_ZONE

    def print_matrix(self):
        for line in self.clusterMatrix:
            print(*line)
        print()


class Encoder:
    def __init__(self):
        self.message = ""

    def get_package(self, information, messType = "encripted"):
        self.message = self.get_input(information, messType)
        return self.message

    # create an encoder function for the message
    def encode(self):
        pass

    # transform any structure into string
    def get_input(self, information, messType = "encrypted"):

        if messType == "encrypted":
            t = type(information)
            result = []

            if t is int or t is float:
                result.append(STANDARD_NUMBER_SPLITTER)
                result.extend(self.get_input(str(information)))

            if t is str:
                result.extend(list(information))

            if t is list or t is tuple:

                for elem in information:

                    result.append(STANDARD_LIST_SPLITTER)
                    result.extend(self.get_input(elem))

            if t is dict:

                for key in information:

                    result.append(STANDARD_DICT_SPLITTER)
                    result.extend(self.get_input(key))
                    result.append(STANDARD_DICT_SPLITTER)
                    result.extend(self.get_input(information[key]))

            return result

        if messType == "clear":
            return [ord(x) for x in information]

class MemoryUnlocker:
    def __init__(self, clusterMatrix):
        self.clusterMatrix = clusterMatrix

    def decrypt_key(self, key):
        return key

    def get_key_property(self, key):
        pass

class Writer:
    def __init__(self):
        self.image = Image.new("RGBA", (WIDTH//4, WIDTH//4), "black")
        self.pixels = self.image.load()
        self.clusterMatrix = None

    def get_cluster_matrix(self,clusterMatrix):
        self.clusterMatrix = clusterMatrix

    def get_current_position(self):
        for i in range(WIDTH):
            for j in range(WIDTH):
                yield i,j

    def write_cluster_matrix(self):

        pos = self.get_current_position()
        m = self.clusterMatrix

        for i in range(WIDTH//4):
            for j in range(WIDTH//4):

                pos1 = next(pos)
                r = m[pos1[0]][pos1[1]]
                pos1 = next(pos)
                g = m[pos1[0]][pos1[1]]
                pos1 = next(pos)
                b = m[pos1[0]][pos1[1]]
                pos1 = next(pos)
                a = m[pos1[0]][pos1[1]]

                #print(r, g, b, a)
                self.pixels[i, j] = (r, g, b, a)

    def show_cluster_matrix(self):
        self.image.show()

# MAIN
readObject = Reader()
readObject.read("input1.txt")
#readObject.print_input()

recognizerObject = Recognizer(readObject.get_matrix())

#recognizerObject.print_matrix()

recognizerObject.enlarge_cluster_matrix()
#recognizerObject.print_matrix()

recognizerObject.matrix_iterate()
#recognizerObject.print_matrix()

#recognizerObject.print_matrix()
#print(recognizerObject.get_cluster_properties(15))
dictionary = {'ana': [1.60000023, 3.7, 4.5], 'are': [2.3, 1.0, 3], 'pere': [3, 4, 2]}
objectList = [1, 2, 3, 4]
name = "there a lot of things to live for, but not this one."
encoderObject = Encoder()
message = encoderObject.get_package(name, "clear")
# broken get_input function, needs to be redone
obj = recognizerObject.update_cluster_matrix(message)
recognizerObject.print_matrix()
print(obj)

writer = Writer()
writer.get_cluster_matrix(recognizerObject.clusterMatrix)
writer.write_cluster_matrix()
writer.show_cluster_matrix()