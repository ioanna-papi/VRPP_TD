from VRP import *

class Solution:
    def __init__(self):
        self.profit = 0
        self.cost = 0
        self.routes = []

class CustomerInsertion(object):
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
        self.SetRoutedFlagToFalseForAllCustomers()
        self.MinimumInsertions()
        self.ReportSolution(self.sol)
        return self.sol

    def SetRoutedFlagToFalseForAllCustomers(self):
        for i in range(0, len(self.customers)):
            self.customers[i].isRouted = False

                
    def IdentifyMaxProfitInsertion(self, best_insertion):
        for i in range(0, len(self.customers)):
            candidateCust: Node = self.customers[i]
            if candidateCust.isRouted is False:
                for rt in self.sol.routes:
                    if rt.time_limit >= 0:
                        for j in range(0, len(rt.sequenceOfNodes) - 1):
                            A = rt.sequenceOfNodes[j]
                            B = rt.sequenceOfNodes[j + 1]
                            costAdded = self.distanceMatrix[A.ID][candidateCust.ID] + self.distanceMatrix[candidateCust.ID][
                                B.ID] + self.allNodes[candidateCust.ID].service_time + self.allNodes[B.ID].service_time
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + self.allNodes[B.ID].service_time
                            trialCost = costAdded - costRemoved
                            marginalProfit = self.allNodes[candidateCust.ID].profit - trialCost
                            if marginalProfit > best_insertion.cost:
                                best_insertion.customer = candidateCust
                                best_insertion.route = rt
                                best_insertion.insertionPosition = j
                                best_insertion.cost = trialCost
                                best_insertion.profit = marginalProfit
                    else:
                        continue
                
    def MinimumInsertions(self):
        model_is_feasible = True
        self.sol = Solution()
        insertions = 0

        while insertions < len(self.allNodes):
            best_insertion = CustomerInsertionAllPositions()
            self.IdentifyMaxProfitInsertion(best_insertion)

            if best_insertion.customer is not None:
                self.ApplyCustomerInsertionAllPositions(best_insertion)
                insertions += 1
            else:
                print('FeasibilityIssue')
                model_is_feasible = False
                break

        if model_is_feasible:
            self.TestSolution()

    def ReportSolution(self, sol):
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range (0, len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].ID, end=' ')
            print(rt.profit)
        SolDrawer.draw('MinIns', self.sol, self.allNodes)
        print(self.sol.profit)

    def GetLastOpenRoute(self):
        if len(self.sol.routes) == 0:
            return None
        else:
            return self.sol.routes[-1]

    def CalculateTotalProfit(self, sol):
        pr = 0
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range(0, len(rt.sequenceOfNodes) - 1):
                a = rt.sequenceOfNodes[j]
                b = rt.sequenceOfNodes[j + 1]
                pr += self.allNodes[b.ID].profit
        return pr

    def UpdateRouteCostAndProfit(self, rt: Route):
        c = 0
        p = 0
        for i in range(0, len(rt.sequenceOfNodes) - 1):
            A = rt.sequenceOfNodes[i]
            B = rt.sequenceOfNodes[i+1]
            c += self.distanceMatrix[A.ID][B.ID] + self.allNodes[B.ID].service_time
            p += self.allNodes[B.ID].profit
        rt.profit = p
        rt.time = c

    def TestSolution(self):
        totalSolCost = 0
        for r in range (0, len(self.sol.routes)):
            rt: Route = self.sol.routes[r]
            rtCost = 0
            for n in range (0 , len(rt.sequenceOfNodes) - 1):
                A = rt.sequenceOfNodes[n]
                B = rt.sequenceOfNodes[n + 1]
                rtCost += (self.distanceMatrix[A.ID][B.ID] + self.allNodes[B.ID].service_time)
            if (rt.time > 150)
                print ('Route Cost problem')
                
            if abs(rtCost - rt.time) > 0.0001:
                print ('Route Cost problem')

            totalSolCost += rt.time

        if abs(totalSolCost - self.sol.cost) > 0.0001:
            print('Solution Cost problem')

    def IdentifyBestInsertionAllPositions(self, best_insertion, rt):
        for i in range(0, len(self.customers)):
            candidateCust: Node = self.customers[i]
            if candidateCust.isRouted is False:
                for rt in self.sol.routes:
                    if rt.time_limit >= 0:
                        for j in range(0, len(rt.sequenceOfNodes) - 1):
                            A = rt.sequenceOfNodes[j]
                            B = rt.sequenceOfNodes[j + 1]
                            costAdded = self.distanceMatrix[A.ID][candidateCust.ID] + self.distanceMatrix[candidateCust.ID][
                                B.ID] + self.allNodes[candidateCust.ID].service_time + self.allNodes[B.ID].service_time
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + self.allNodes[B.ID].service_time
                            trialCost = costAdded - costRemoved
                            marginalProfit = self.allNodes[candidateCust.ID].profit - trialCost
                            if marginalProfit > best_insertion.cost:
                                best_insertion.customer = candidateCust
                                best_insertion.route = rt
                                best_insertion.insertionPosition = j
                                best_insertion.profit = marginalProfit
                                best_insertion.cost = trialCost
                   

    def ApplyCustomerInsertionAllPositions(self, insertion):
        insCustomer = insertion.customer
        rt = insertion.route
        insIndex = insertion.insertionPosition
        rt.sequenceOfNodes.insert(insIndex + 1, insCustomer)
        rt.profit += insertion.profit
        rt.time += insertion.cost
        rt.time_limit -= insertion.cost
        self.sol.profit += insertion.profit
        self.sol.cost += insertion.cost
        insCustomer.isRouted = True
