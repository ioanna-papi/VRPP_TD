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
                
                for i in range(len(self.allNodes)):
                    if self.allNodes[i].isRouted == False:
                        
                        if (self.allNodes[i].profit - (self.distanceMatrix[node][i] +  self.allNodes[i].service_time)) > max1:
                            max1 = self.allNodes[i].profit - (self.distanceMatrix[node][i] +  self.allNodes[i].service_time)
                            position = i
                    
                if (total_route_time + (self.distanceMatrix[node][position] +  self.allNodes[position].service_time) <= 150):
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
                  
        f = open("BestNode8180099.txt", "w+")
        for i in range(len(self.sol.routes)):
            rt: Route = self.sol.routes[i]
            f.write("This is route: \n")
            for j in range(len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].ID, end=' ', )
                f.write("%d\n" % (rt.sequenceOfNodes[j].ID))
            f.write("\n")
            print("\n")
        solution = self.objective(self.sol)
        f.write("This is the final objective: %d" % (solution))
        f.close()
        SolDrawer.draw('BestNode8180099', self.sol, self.allNodes)
        return (self.sol)                  
            
        ## method that calculates the total time of the solution given
        def objective(self, solution):
        total_time = 0
        single_time = []
        for i in range(len(solution.routes)):
            time = 0
            rout: Route = solution.routes[i]
            for j in range(len(rout.sequenceOfNodes) - 1):
                index1 = rout.sequenceOfNodes[j]
                index2 = rout.sequenceOfNodes[j + 1]
                time += (self.allNodes[index2.ID].service_time + self.distanceMatrix[index1.ID][index2.ID])
            single_time.append(time)
            self.sol.routes[i].distance = time
            total_time += time
        return total_time   
            
            
        
