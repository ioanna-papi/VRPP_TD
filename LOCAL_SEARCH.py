from VRP import *
from SolutionDrawer import *

class Solution:
    def __init__(self):
        self.profit = 0.0
        self.time = 0.0
        self.routes = []
        self.sequenceOfNodes = []
        
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

#class InsertionMove(object):        
    #def __init__(self):
        
    #def Initialize(self):
        
#class ProfitableSwapMove(object):        
    #def __init__(self):
        
    #def Initialize(self):
         

# Ερώτημα Β - Δημιουργία κατασκευαστικού αλγορίθμου που θα παράγει ολοκληρωμένη λύση        
class Solver:
    def __init__(self, m):
        self.allNodes = m.allNodes
        self.depot = m.allNodes[0]
        self.customers = m.customers
        self.distanceMatrix = m.matrix
        self.total_route_time = 0
        self.total_route_profit = 0
        self.sol = Solution()
        self.bestSolution = Solution()
        self.route = None
        
    def ApplyBestNodeMethod(self):
        for r in range(5):
            self.route = Route(self.allNodes[0],150)
            node = 0
            time_limit = 150
            self.route.sequenceOfNodes.append(self.allNodes[0])
            self.allNodes[0].isRouted = True
            total_time = 0
            total_profit = 0
            position = 0
            while time_limit >= 0:
                max1 = -100000000000
                flag = False
                for i in range(len(self.allNodes)):
                    if self.allNodes[i].isRouted == False:
                        flag = True
                        #if (self.allNodes[i].profit - (self.distanceMatrix[node][i] +  self.allNodes[i].service_time)) > max1:
                            #max1 = self.allNodes[i].profit - (self.distanceMatrix[node][i] +  self.allNodes[i].service_time)
                            #position = i
                        if (self.allNodes[i].profit - (self.distanceMatrix[node][i] +  self.allNodes[i].service_time) > max1 and (self.distanceMatrix[node][i] +  self.allNodes[i].service_time) < 25 ):
                            max1 = self.allNodes[i].profit - (self.distanceMatrix[node][i] +  self.allNodes[i].service_time)
                            position = i
                        
                if not flag:
                    break
                    
                elif (total_time + (self.distanceMatrix[node][position] +  self.allNodes[position].service_time) <= 150):
                    self.route.sequenceOfNodes.append(self.allNodes[position])
                    self.sol.sequenceOfNodes.append(self.allNodes[position])
                    self.allNodes[position].isRouted = True
                    a = self.allNodes[position]
                    total_profit += a.profit
                    total_time += (self.distanceMatrix[node][position] +  a.service_time)
                    time_limit -= (self.distanceMatrix[node][position] +  a.service_time)
                    node = position
                else:
                    break
                    
            self.route.profit += total_profit
            self.route.time += total_time
            self.route.time_limit -= total_time
            self.sol.routes.append(self.route)
            self.sol.profit += total_profit
            self.sol.time += total_time
        
        print(" ")
        f = open("AllRoutes_8180099.txt", "w+")
        counter = 1
        for i in range(len(self.sol.routes)):
            rt: Route = self.sol.routes[i]
            f.write("This is route: \n")
            print(" Route ", counter,"=", rt.sequenceOfNodes[0].ID, end=' ', )
            counter +=1
            for j in range(len(rt.sequenceOfNodes)):
                
                if (rt.sequenceOfNodes[j].ID != 0):
                    print(rt.sequenceOfNodes[j].ID, end=' ', )
                f.write("%d\n" % (rt.sequenceOfNodes[j].ID))
            f.write("\n")
            print(rt.sequenceOfNodes[0].ID, end=' ', )
            print("\n")
        solution = self.objective(self.sol)
        #print(" TOTAL PROFIT =", solution)
        f.write("This is the final objective: %d" % (solution))
        f.close()
        SolDrawer.draw('final_Solution_8180099', self.sol, self.allNodes)
        return (self.sol)

    # method that calculates the total profit of the solution given
    def objective(self, solution):
        total_profit = 0
        single_profit = []
        for i in range(len(solution.routes)):
            pr = 0
            rout: Route = solution.routes[i]
            for j in range(len(rout.sequenceOfNodes) - 1):
                index1 = rout.sequenceOfNodes[j]
                index2 = rout.sequenceOfNodes[j + 1]
                pr += index2.profit
            single_profit.append(pr)
            self.sol.routes[i].profit = pr
            total_profit += pr
        return total_profit
   
# Ερώτημα Γ - 4 Τελεστές τοπικής έρευνας (Relocation / Swap / Insertion / Profitable Swap)       
    def LocalSearch(self):
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        counter = 0
        rm = RelocationMove()
        sm = SwapMove()
        localSearchIterator = 0
        
        while terminationCondition is False:

            # SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)
            self.InitializeRm(rm)
            self.FindBestRelocationMove(rm)
            if rm.originRoutePosition is not None:
                if rm.moveCost < 0:
                    self.ApplyRelocationMove(rm)
                    counter += 1
                else:
                    terminationCondition = True

            self.TestSolution()

            if (self.sol.time < self.bestSolution.time):
                self.bestSolution = self.cloneSolution(self.sol)

            localSearchIterator = localSearchIterator + 1

        self.sol = self.bestSolution

        self.TestSolution()
        SolDrawer.draw('final_LS_8180099', self.sol, self.allNodes)

        f = open("LocalSearch8180099.txt", "w+")
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
        print(counter)

        return (self.sol)


    def cloneRoute(self, rt: Route):
        cloned = Route(self.allNodes[0], rt.time_limit)
        cloned.time = rt.time
        cloned.profit = rt.profit
        cloned.time_limit = rt.time_limit
        cloned.sequenceOfNodes = rt.sequenceOfNodes.copy()
        return cloned

    def cloneSolution(self, sol: Solution):
        cloned = Solution()
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            clonedRoute = self.cloneRoute(rt)
            cloned.routes.append(clonedRoute)
        cloned.time = self.sol.time
        cloned.profit = self.sol.profit
        return cloned

    # Relocation
    def FindBestRelocationMove(self, rm):
        for originRouteIndex in range(0, len(self.sol.routes)):
            rt1:Route = self.sol.routes[originRouteIndex]
            for targetRouteIndex in range (0, len(self.sol.routes)):
                rt2:Route = self.sol.routes[targetRouteIndex]
                for originNodeIndex in range (1, len(rt1.sequenceOfNodes) - 1):
                    for targetNodeIndex in range (0, len(rt2.sequenceOfNodes) - 1):

                        if originRouteIndex == targetRouteIndex and (targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue

                        A = rt1.sequenceOfNodes[originNodeIndex - 1]
                        B = rt1.sequenceOfNodes[originNodeIndex]
                        C = rt1.sequenceOfNodes[originNodeIndex + 1]

                        F = rt2.sequenceOfNodes[targetNodeIndex]
                        G = rt2.sequenceOfNodes[targetNodeIndex + 1]

                        costAdded = self.distanceMatrix[A.ID][C.ID] + self.customers[C.ID].service_time + self.distanceMatrix[F.ID][B.ID] + self.customers[B.ID].service_time + self.distanceMatrix[B.ID][G.ID] + self.customers[G.ID].service_time
                        costRemoved = self.distanceMatrix[A.ID][B.ID] + self.customers[B.ID].service_time + self.distanceMatrix[B.ID][C.ID] + self.customers[C.ID].service_time + self.distanceMatrix[F.ID][G.ID] + self.customers[G.ID].service_time

                        originRtCostChange = self.distanceMatrix[A.ID][C.ID] + self.customers[C.ID].service_time - self.distanceMatrix[A.ID][B.ID] - self.customers[B.ID].service_time - self.distanceMatrix[B.ID][C.ID] - self.customers[C.ID].service_time
                        targetRtCostChange = self.distanceMatrix[F.ID][B.ID] + self.customers[B.ID].service_time + self.distanceMatrix[B.ID][G.ID] + self.customers[G.ID].service_time - self.distanceMatrix[F.ID][G.ID] - self.customers[G.ID].service_time
                        
                        if rt1 != rt2:
                            rt1time = rt1.time + originRtCostChange
                            rt2time = rt2.time + targetRtCostChange
                            if rt1time <= 150:
                                continue
                            if rt2time <= 150:
                                continue
                         elif rt1 == rt2:
                            rtfull = rt1.time + originRtCostChange + targetRtCostChange
                            if rtfull <= 150:
                                continue
                                
                         moveCost = costAdded - costRemoved

                        if (moveCost < rm.moveCost) and abs(moveCost) > 0.0001:
                            self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm)

                        return rm.originRoutePosition
        
                
    def ApplyRelocationMove(self, rm: RelocationMove):
        oldCost = self.CalculateTotalCost(self.sol)

        originRt = self.sol.routes[rm.originRoutePosition]
        targetRt = self.sol.routes[rm.targetRoutePosition]

        B = originRt.sequenceOfNodes[rm.originNodePosition]

        if originRt == targetRt:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            if (rm.originNodePosition < rm.targetNodePosition):
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition, B)
            else:
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)

            originRt.time += rm.moveCost
        else:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)
            originRt.time += rm.costChangeOriginRt
            targetRt.time += rm.costChangeTargetRt
            originRt.profit -= B.profit
            targetRt.profit += B.profit

        self.sol.time += rm.moveCost    
        self.TestSolution()

        
    def StoreBestRelocationMove(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm:RelocationMove):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost

    def InitializeRm(self, rm):
        rm.Initialize()
    
    def CalculateTotalCost(self, sol):
        c = 0
        for i in range (0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range (0, len(rt.sequenceOfNodes) - 1):
                a = rt.sequenceOfNodes[j]
                b = rt.sequenceOfNodes[j + 1]
                c += self.distanceMatrix[a.ID][b.ID] + self.customers[b.ID].service_time
        return c

    
    def FindBestSwapMove(self, sm):
        for firstRouteIndex in range(0, len(self.sol.routes)):
            rt1:Route = self.sol.routes[firstRouteIndex]
            for secondRouteIndex in range (firstRouteIndex, len(self.sol.routes)):
                rt2:Route = self.sol.routes[secondRouteIndex]
                for firstNodeIndex in range (1, len(rt1.sequenceOfNodes) - 1):
                    startOfSecondNodeIndex = 1
                    if rt1 == rt2:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    for secondNodeIndex in range (startOfSecondNodeIndex, len(rt2.sequenceOfNodes) - 1):

                        a1 = rt1.sequenceOfNodes[firstNodeIndex - 1]
                        b1 = rt1.sequenceOfNodes[firstNodeIndex]
                        c1 = rt1.sequenceOfNodes[firstNodeIndex + 1]

                        a2 = rt2.sequenceOfNodes[secondNodeIndex - 1]
                        b2 = rt2.sequenceOfNodes[secondNodeIndex]
                        c2 = rt2.sequenceOfNodes[secondNodeIndex + 1]



                        moveCost = None
                        costChangeFirstRoute = None
                        costChangeSecondRoute = None

                        if rt1 == rt2:
                            if firstNodeIndex == secondNodeIndex - 1:
                                costRemoved = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][b2.ID] + self.distanceMatrix[b2.ID][c2.ID]
                                costAdded = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][b1.ID] + self.distanceMatrix[b1.ID][c2.ID]
                                moveCost = costAdded - costRemoved
                            else:

                                costRemoved1 = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][c1.ID]
                                costAdded1 = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][c1.ID]
                                costRemoved2 = self.distanceMatrix[a2.ID][b2.ID] + self.distanceMatrix[b2.ID][c2.ID]
                                costAdded2 = self.distanceMatrix[a2.ID][b1.ID] + self.distanceMatrix[b1.ID][c2.ID]
                                moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                        else:
                            if rt1.load - b1.demand + b2.demand > self.capacity:
                                continue
                            if rt2.load - b2.demand + b1.demand > self.capacity:
                                continue

                            costRemoved1 = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][c1.ID]
                            costAdded1 = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][c1.ID]
                            costRemoved2 = self.distanceMatrix[a2.ID][b2.ID] + self.distanceMatrix[b2.ID][c2.ID]
                            costAdded2 = self.distanceMatrix[a2.ID][b1.ID] + self.distanceMatrix[b1.ID][c2.ID]

                            costChangeFirstRoute = costAdded1 - costRemoved1
                            costChangeSecondRoute = costAdded2 - costRemoved2

                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                        if moveCost < sm.moveCost and abs(moveCost) > 0.0001:
                            self.StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm)

    
    
    
    
    
    
    
    
    def InitializeOperators(self, rm, sm, top):
        rm.Initialize()
        sm.Initialize()
        top.Initialize()

   
