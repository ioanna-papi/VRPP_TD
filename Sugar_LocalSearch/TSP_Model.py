import random
import math

class Model:

# instance variables
    def __init__(self):
        self.allNodes = []
        self.customers = []
        self.matrix = []

    def BuildModel(self):
        random.seed(1)
        depot = Node(0, 50, 50)
        self.allNodes.append(depot)

        totalCustomers = 100
        for i in range (0, totalCustomers):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            cust = Node(i + 1, x, y)
            self.allNodes.append(cust)
            self.customers.append(cust)

        rows = len(self.allNodes)
        self.matrix = [[0.0 for x in range(rows)] for y in range(rows)]

        for i in range(0, len(self.allNodes)):
            for j in range(0, len(self.allNodes)):
                a = self.allNodes[i]
                b = self.allNodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                self.matrix[i][j] = dist

    def BuildModelExamplePowerpoint(self):
        random.seed(1)
        depot = Node(0, -1, -1)
        self.allNodes.append(depot)

        totalCustomers = 6
        for i in range(0, totalCustomers):
            x = -1
            y = -1
            cust = Node(i + 1, x, y)
            self.allNodes.append(cust)
            self.customers.append(cust)

        rows = len(self.allNodes)
        self.matrix = []
        self.matrix.append([0, 22.52, 74.35, 49.82, 46.73, 31.17, 36.84])
        self.matrix.append([22.52, 0, 70.86, 44.88, 79.58, 66.99, 65.95])
        self.matrix.append([74.35, 70.86, 0, 32.48, 38.32, 42.61, 22.73])
        self.matrix.append([49.82, 44.88, 32.48, 0, 73.68, 58.2, 70.21])
        self.matrix.append([46.73, 79.58, 38.32, 73.68, 0, 54.39, 52.49])
        self.matrix.append([31.17, 66.99, 42.61, 58.2, 54.39, 0, 24.67])
        self.matrix.append([36.84, 65.95, 22.73, 70.21, 52.49, 24.67, 0])

class Node:
    def __init__(self, idd, xx, yy):
        self.x = xx
        self.y = yy
        self.ID = idd
        self.isRouted = False

