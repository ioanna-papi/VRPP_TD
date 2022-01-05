from VRP import *
from SolutionDrawer import *

class Solution:
    def __init__(self):
        self.profit = 0.0
        self.cost = 0.0
        self.routes = []

class CustomerInsertion(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.profit = -(10 ** 9)
        self.dist = 10 ** 9
        self.cost = 10 ** 9
        
class CustomerInsertionAllPositions(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.insertionPosition = None
        self.profit = -(10 ** 9)
        self.dist = 10 ** 9
        self.cost = 10 ** 9
        
class RelocationMove(object):
    def __init__(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.distChangeOriginRt = None
        self.distChangeTargetRt = None
        self.timeChangeOriginRt = None
        self.timeChangeTargetRt = None
        self.moveCost = None

    def Initialize(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.distChangeOriginRt = None
        self.distChangeTargetRt = None
        self.timeChangeOriginRt = None
        self.timeChangeTargetRt = None
        self.moveCost = 10 ** 9

class SwapMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.distChangeFirstRt = None
        self.distChangeSecondRt = None
        self.time1 = None
        self.time2 = None
        self.moveCost = None

    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.distChangeFirstRt = None
        self.distChangeSecondRt = None
        self.time1 = None
        self.time2 = None
        self.moveCost = 10 ** 9

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
        self.depot = m.allNodes[0]
        self.distanceMatrix = m.matrix
        self.total_route_time = 0
        self.total_route_profit = 0
        self.sol = None
        self.bestSolution = None  
        
    def solve(self):
        self.ApplyBestNodeMethod()
        self.ReportSolution(self.sol)
        return self.sol

    def CalculateDistance(self, sol):
        distance = 0
        for i in range(0, len(sol.routes)):
            for j in range(0, len(sol.routes[i].sequenceOfNodes) - 1):
                distance = distance + self.distanceMatrix[sol.routes[i].sequenceOfNodes[j].id][
                    sol.routes[i].sequenceOfNodes[j + 1].id]
        return distance

    def GetLastOpenRoute(self):
        if len(self.sol.routes) == 0:
            return None
        else:
            return self.sol.routes[-1]

    def IdentifyBestInsertion(self, bestInsertion, rt):
        for i in range(0, len(self.customers)):
            candidateCust: Node = self.customers[i]
            if candidateCust.isRouted is False:
                if rt.load + candidateCust.demand <= rt.capacity:
                    lastNodePresentInTheRoute = rt.sequenceOfNodes[-1]
                    trialDist = self.distanceMatrix[lastNodePresentInTheRoute.id][candidateCust.id]
                    if rt.time + candidateCust.service_time + (trialDist / 35) <= 3.5:
                        if trialDist < bestInsertion.dist:
                            bestInsertion.customer = candidateCust
                            bestInsertion.route = rt
                            bestInsertion.dist = trialDist

    def ApplyCustomerInsertion(self, insertion):
        insCustomer = insertion.customer
        rt = insertion.route
        rt.sequenceOfNodes.append(insCustomer)
        beforeInserted = rt.sequenceOfNodes[-2]
        distAdded = self.distanceMatrix[beforeInserted.id][insCustomer.id]
        rt.dist += distAdded
        self.sol.dist += distAdded
        rt.load += insCustomer.demand
        rt.time += distAdded / 35 + insCustomer.service_time
        insCustomer.isRouted = True

    def ReportSolution(self, sol):
        print(self.sol.dist)
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range(0, len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].id, end=' ')
            print("")

    def TestSolution(self):
        totalSolDist = 0
        for r in range(0, len(self.sol.routes)):
            rt: Route = self.sol.routes[r]
            rtDist = 0
            rtLoad = 0
            for n in range(0, len(rt.sequenceOfNodes) - 1):
                A = rt.sequenceOfNodes[n]
                B = rt.sequenceOfNodes[n + 1]
                rtDist += self.distanceMatrix[A.id][B.id]
                rtLoad += A.demand
            rtLoad += B.demand
            if abs(rtDist - rt.dist) > 0.0001:
                print('Route Cost problem')
            if rtLoad != rt.load:
                print('Route Load problem')
            totalSolDist += rt.dist
        if abs(totalSolDist - self.sol.dist) > 0.0001:
            print('Solution Cost problem')

    def CalculateRoutes(self):
        for rt in self.sol.routes:
            if rt.dist <= 0:
                self.sol.routes.remove(rt)

    def ApplyBestNodeMethod(self):
        modelIsFeasible = True
        self.sol = Solution()
        insertions = 0
        while (insertions < len(self.customers)):
            bestInsertion = CustomerInsertion()
            lastOpenRoute: Route = self.GetLastOpenRoute()
            if lastOpenRoute is not None:
                self.IdentifyBestInsertion(bestInsertion, lastOpenRoute)
            if (bestInsertion.customer is not None):
                self.ApplyCustomerInsertion(bestInsertion)
                insertions += 1
            else:
                if lastOpenRoute is not None and len(lastOpenRoute.sequenceOfNodes) == 1:
                    modelIsFeasible = False
                    break
                else:
                    if len(self.sol.routes) < 15:
                        rt = Route(self.depot, 1500)
                    else:
                        rt = Route(self.depot, 1200)
                    self.sol.routes.append(rt)
        if (modelIsFeasible == False):
            print('FeasibilityIssue')
        
        
    
