import random
import math

class Model:
    def __init__(self):
        self.allNodes = []
        self.customers = []
        self.matrix = []

    def BuildModel(self):
        all_nodes = []
        d = Node(0, 50, 50, 0, 0)
        all_nodes.append(d)
        # my birthday = 03/11/2000
        birthday = 3112000
        random.seed(birthday)
        total_route_time = 0
        for i in range(0, 200):
            xx = random.randint(0, 100)
            yy = random.randint(0, 100)
            service_time = random.randint(5, 10)
            profit = random.randint(5, 20)
            cust = Node(i + 1, xx, yy, service_time, profit)
            all_nodes.append(cust)
            self.customers.append(cust)
               
        self.allNodes = all_nodes
        rows = len(self.allNodes)
        self.matrix = [[0.0 for x in range(rows)] for y in range(rows)]
        self.dist = [[0.0 for x in range(rows)] for y in range(rows)]
        self.time = [[0.0 for x in range(rows)] for y in range(rows)]

        for i in range(0, len(self.allNodes)):
            for j in range(0, len(self.allNodes)):
                a = self.allNodes[i]
                b = self.allNodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                self.matrix[i][j] = dist

class Node:
    def __init__(self, idd, xx, yy, service_time, profit):
        self.x = xx
        self.y = yy
        self.ID = idd
        self.service_time = service_time
        self.profit = profit
        self.isRouted = False

class Route:
    def __init__(self, dp, time_limit):
        self.sequenceOfNodes = []
        self.sequenceOfNodes.append(dp)
        self.time_limit = time_limit
        self.time = 0
        self.profit = 0
      
    
