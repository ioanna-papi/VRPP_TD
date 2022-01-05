from VRP import *
from SolutionDrawer import *

class Solution:
    def __init__(self):
        self.profit = 0.0
        self.time = 0.0
        self.routes = []

class CustomerInsertion(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.profit = -(10 ** 9)
        self.time = 10 ** 9
        
class CustomerInsertionAllPositions(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.insertionPosition = None
        self.profit = -(10 ** 9)
        self.time = 10 ** 9
        
        
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
        self.customers = m.customers
        self.distanceMatrix = m.matrix
        self.total_route_time = 0
        self.total_route_profit = 0
        self.sol = None
        self.bestSolution = None  
        
    def solve(self):
        self.ApplyBestNodeMethod()
        self.ReportSolution(self.sol)
        return self.sol

    def CalculateProfit(self, sol):
        profit = 0
        for i in range(0, len(sol.routes)):
            for j in range(0, len(sol.routes[i].sequenceOfNodes) - 1):
                profit += self.allNodes[sol.routes[i].sequenceOfNodes[j].ID].profit
        return profit

    def GetLastOpenRoute(self):
        if len(self.sol.routes) == 0:
            return None
        else:
            return self.sol.routes[-1]

    def IdentifyBestInsertion(self, bestInsertion, rt):
        for i in range(0, len(self.customers)):
            candidateCust: Node = self.customers[i]
            if candidateCust.isRouted is False:
                if rt.time_limit >= 0:
                    lastNode = rt.sequenceOfNodes[-1]
                    total_time = self.distanceMatrix[lastNode.ID][candidateCust.ID] + candidateCust.service_time
                    cprofit = candidateCust.profit
                    if rt.time_limit - total_time >= 0:
                        if (cprofit - total_time) > (bestInsertion.profit - bestInsertion.time):
                            bestInsertion.customer = candidateCust
                            bestInsertion.route = rt
                            bestInsertion.profit = cprofit
                            bestInsertion.time = total_time

                            
    def ApplyCustomerInsertion(self, insertion):
        insCustomer = insertion.customer
        rt = insertion.route
        rt.sequenceOfNodes.append(insCustomer)
        beforeInserted = rt.sequenceOfNodes[-2]
        distAdded = self.distanceMatrix[beforeInserted.ID][insCustomer.ID]
        rt.time += (distAdded + insCustomer.service_time)
        rt.profit += insCustomer.profit
        self.sol.profit += insCustomer.profit
        self.sol.time += (distAdded + insCustomer.service_time)
        rt.time_limit -= (distAdded + insCustomer.service_time)
        insCustomer.isRouted = True

    def ReportSolution(self, sol):
        print(self.sol.profit)
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range(0, len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].ID, end=' ')
            print("")

    def TestSolution(self):
        totalSolTime = 0
        for r in range(0, len(self.sol.routes)):
            rt: Route = self.sol.routes[r]
            rtTime = 0
            for n in range(0, len(rt.sequenceOfNodes) - 1):
                A = rt.sequenceOfNodes[n]
                B = rt.sequenceOfNodes[n + 1]
                rtTime += (self.distanceMatrix[A.ID][B.ID] + self.customers[B.ID].service_time)
               
            if abs(rtTime - rt.time) > 0.0001:
                print('Route Cost problem')
            totalSolTime += rt.time
        if abs(totalSolTime - self.sol.time) > 0.0001:
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
            lastRoute: Route = self.GetLastOpenRoute()
            if lastRoute is not None:
                self.IdentifyBestInsertion(bestInsertion, lastRoute)
            if (bestInsertion.customer is not None):
                self.ApplyCustomerInsertion(bestInsertion)
                insertions += 1
            else:
                if lastRoute is not None and len(lastRoute.sequenceOfNodes) == 1:
                    modelIsFeasible = False
                    break
                else:
                    rt = Route(self.depot, 150)
                    self.sol.routes.append(rt)
        if (modelIsFeasible == False):
            print('FeasibilityIssue')
        
        
    
