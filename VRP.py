import random
import math

class Model:

    def __init__(self):
        self.allNodes = []
        self.customers = []
        self.matrix = []

    def BuildModel(self):
        allNodes = []
        d = Node(0, 50, 50, 0, 0)
        allNodes.append(d)
        birthday = 3112000
        random.seed(birthday)
        for i in range(0, 200):
            xx = random.randint(0, 100)
            yy = random.randint(0, 100)
            service_time = random.randint(5, 10)
            profit = random.randint(5, 20)
            cust = Node(i + 1, xx, yy, service_time, profit)
            allNodes.append(cust)
