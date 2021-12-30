from VRP import *

class Solution:
    def __init__(self):
        self.profit = 0
        self.routes = []
        
class RelocationMove(object):
    def __init__(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = None

    def Initialize(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = 10 ** 9

        
class SwapMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = None
    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = 10 ** 9


class CustomerInsertion(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.cost = 10 ** 9

class CustomerInsertionAllPositions(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.insertionPosition = None
        self.cost = 10 ** 9

class TwoOptMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = None
    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = 10 ** 9

class Solver:
    
    def __init__(self, m):
        self.allNodes = m.allNodes
        self.customers = m.customers
        self.depot = m.allNodes[0]
        self.distanceMatrix = m.matrix
        self.total_route_time = m.total_route_time
        self.sol = None
        self.bestSolution = None
        
     def ApplyBestNodeMethod(self):
        
        for r in range(5):
            total_route_time = Route(0)
            total_route_profit[r] = 0
               
            node = 0
            self.route.sequenceOfNodes.append(self.allNodes[0])
            self.allNodes[0].isRouted = True
            total_time = 0
            position = 0
            
            while total_route_time <= 150:
                max1 = -10000000
                flag = False
                
                for i in range(len(self.allNodes)):
                    if self.allNodes[i].isRouted == False:
                        flag = True
                        if (self.allNodes[i].profit - (self.distanceMatrix[node][i] +  self.allNodes[i].service_time)) > max1:
                            max1 = self.allNodes[i].profit - (self.distanceMatrix[node][i] +  self.allNodes[i].service_time)
                            position = i
                if not flag:
                    break
                    
                elif (total_route_time + (self.distanceMatrix[node][position] +  self.allNodes[position].service_time) <= 150):
                    self.route.sequenceOfNodes.append(self.allNodes[position])
                    self.allNodes[position].isRouted = True
                    a = self.allNodes[position]
                    
                    total_route_time += (self.distanceMatrix[node][position] +  self.allNodes[position].service_time)
                    total_route_profit[r] += self.allNodes[position].profit
                    node = position
                else:
                    break 
                    
                
                self.route.time = total_route_time
                self.sol.routes.append(self.route)
                self.sol.profit += total_route_profit[r]
                  
                            
            
            
            
            
        
