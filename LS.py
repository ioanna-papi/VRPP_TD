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
        self.moveCost = None
        
    def Initialize(self):
        self.customer = None
        self.route = None
        self.insertionPosition = None
        self.profit = -(10 ** 9)
        self.time = 10 ** 9
        self.moveCost = 10 ** 9
        
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
        
class ProfitableSwapMove(object):
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
         

# Ερώτημα Β - Δημιουργία κατασκευαστικού αλγορίθμου που θα παράγει ολοκληρωμένη λύση  

class Solver2:
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
        self.searchTrajectory = []
        
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
        total_time = 0
        single_time = []
        for i in range(len(solution.routes)):
            pr = 0
            t = 0
            rout: Route = solution.routes[i]
            for j in range(len(rout.sequenceOfNodes) - 1):
                index1 = rout.sequenceOfNodes[j]
                index2 = rout.sequenceOfNodes[j + 1]
                pr += index2.profit
                t += (self.distanceMatrix[index1.ID][index2.ID] + self.allNodes[index2.ID].service_time)
            single_profit.append(pr)
            single_time.append(t)
            self.sol.routes[i].profit = pr
            self.sol.routes[i].time = t
            total_time += t
            total_profit += pr
        return total_profit
   
# Ερώτημα Γ - Τελεστές τοπικής έρευνας (Relocation / Swap / Insertion / Profitable Swap)       

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
                        
                        if (rt1.sequenceOfNodes[originNodeIndex] == rt1.sequenceOfNodes[-1]):
                            C = rt1.sequenceOfNodes[originNodeIndex]
                        else:
                            C = rt1.sequenceOfNodes[originNodeIndex + 1]

                        F = rt2.sequenceOfNodes[targetNodeIndex]
                        
                        if (rt2.sequenceOfNodes[targetNodeIndex] == rt2.sequenceOfNodes[-1]):
                            G = rt2.sequenceOfNodes[targetNodeIndex]
                        else:
                            G = rt2.sequenceOfNodes[targetNodeIndex + 1]

                        #costAdded = self.distanceMatrix[A.ID][C.ID] + self.allNodes[C.ID].service_time + self.distanceMatrix[F.ID][B.ID] + self.allNodes[B.ID].service_time + self.distanceMatrix[B.ID][G.ID] + self.allNodes[G.ID].service_time
                        #costRemoved = self.distanceMatrix[A.ID][B.ID] + self.allNodes[B.ID].service_time + self.distanceMatrix[B.ID][C.ID] + self.allNodes[C.ID].service_time + self.distanceMatrix[F.ID][G.ID] + self.allNodes[G.ID].service_time

                        #originRtCostChange = self.distanceMatrix[A.ID][C.ID] + self.allNodes[C.ID].service_time - self.distanceMatrix[A.ID][B.ID] - self.allNodes[B.ID].service_time - self.distanceMatrix[B.ID][C.ID] - self.allNodes[C.ID].service_time
                        #targetRtCostChange = self.distanceMatrix[F.ID][B.ID] + self.allNodes[B.ID].service_time + self.distanceMatrix[B.ID][G.ID] + self.allNodes[G.ID].service_time - self.distanceMatrix[F.ID][G.ID] - self.allNodes[G.ID].service_time
                        
                        if (rt1.sequenceOfNodes[originNodeIndex] == rt1.sequenceOfNodes[-1]):
                            if (rt2.sequenceOfNodes[targetNodeIndex] == rt2.sequenceOfNodes[-1]):
                                costAdded = self.distanceMatrix[F.ID][B.ID] + self.allNodes[B.ID].service_time
                                costRemoved = self.distanceMatrix[A.ID][B.ID] + self.allNodes[B.ID].service_time
                                originRtCostChange = - self.distanceMatrix[A.ID][B.ID] - self.allNodes[B.ID].service_time
                                targetRtCostChange = self.distanceMatrix[F.ID][B.ID] + self.allNodes[B.ID].service_time
                                
                            else:
                                costAdded = self.distanceMatrix[F.ID][B.ID] + self.allNodes[B.ID].service_time + self.distanceMatrix[B.ID][G.ID] + self.allNodes[G.ID].service_time
                                costRemoved = self.distanceMatrix[A.ID][B.ID] + self.allNodes[B.ID].service_time + self.distanceMatrix[F.ID][G.ID] + self.allNodes[G.ID].service_time
                                originRtCostChange = - self.distanceMatrix[A.ID][B.ID] - self.allNodes[B.ID].service_time
                                targetRtCostChange = self.distanceMatrix[F.ID][B.ID] + self.allNodes[B.ID].service_time + self.distanceMatrix[B.ID][G.ID] + self.allNodes[G.ID].service_time - self.distanceMatrix[F.ID][G.ID] - self.allNodes[G.ID].service_time
                   
                        elif (rt2.sequenceOfNodes[targetNodeIndex] == rt2.sequenceOfNodes[-1]):
                            costAdded = self.distanceMatrix[A.ID][C.ID] + self.allNodes[C.ID].service_time + self.distanceMatrix[F.ID][B.ID] + self.allNodes[B.ID].service_time
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + self.allNodes[B.ID].service_time + self.distanceMatrix[B.ID][C.ID] + self.allNodes[C.ID].service_time
                            originRtCostChange = self.distanceMatrix[A.ID][C.ID] + self.allNodes[C.ID].service_time - self.distanceMatrix[A.ID][B.ID] - self.allNodes[B.ID].service_time - self.distanceMatrix[B.ID][C.ID] - self.allNodes[C.ID].service_time
                            targetRtCostChange = self.distanceMatrix[F.ID][B.ID] + self.allNodes[B.ID].service_time

                        else:
                            costAdded = self.distanceMatrix[A.ID][C.ID] + self.allNodes[C.ID].service_time + self.distanceMatrix[F.ID][B.ID] + self.allNodes[B.ID].service_time + self.distanceMatrix[B.ID][G.ID] + self.allNodes[G.ID].service_time
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + self.allNodes[B.ID].service_time + self.distanceMatrix[B.ID][C.ID] + self.allNodes[C.ID].service_time + self.distanceMatrix[F.ID][G.ID] + self.allNodes[G.ID].service_time

                            originRtCostChange = self.distanceMatrix[A.ID][C.ID] + self.allNodes[C.ID].service_time - self.distanceMatrix[A.ID][B.ID] - self.allNodes[B.ID].service_time - self.distanceMatrix[B.ID][C.ID] - self.allNodes[C.ID].service_time
                            targetRtCostChange = self.distanceMatrix[F.ID][B.ID] + self.allNodes[B.ID].service_time + self.distanceMatrix[B.ID][G.ID] + self.allNodes[G.ID].service_time - self.distanceMatrix[F.ID][G.ID] - self.allNodes[G.ID].service_time
                    
                        if rt1 != rt2:
                            rt1time = rt1.time + originRtCostChange
                            rt2time = rt2.time + targetRtCostChange
                            if rt1time > 150:
                                continue
                            if rt2time > 150:
                                continue 
                        elif (rt1 == rt2):
                            rtfull = rt1.time + originRtCostChange + targetRtCostChange
                            if rtfull > 150:
                                continue
            
                        moveCost = costAdded - costRemoved

                        if (moveCost < rm.moveCost) and abs(moveCost) > 0.0001:
                            self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm)

                        return rm.originRoutePosition
        
                
    def ApplyRelocationMove(self, rm: RelocationMove):
        oldCost = self.CalculateTotalCost(self.sol)

        originRt = self.bestSolution.routes[rm.originRoutePosition]
        targetRt = self.bestSolution.routes[rm.targetRoutePosition]

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
                c += (self.distanceMatrix[a.ID][b.ID] + self.allNodes[b.ID].service_time)
        return c
    
    def ReportSolution(self, sol):
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range (0, len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].ID, end=' ')
            print(rt.time)
        print (self.sol.time)
        
        
    def ReportSolution(self, sol):
        print(self.sol.dist)
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range(0, len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].id, end=' ')
            print("")
    
    
    
    
    def TestSolution(self):
        totalSolCost = 0
        for r in range (0, len(self.sol.routes)):
            rt: Route = self.sol.routes[r]
            rtTime = 0
            rtProfit = 0
            for n in range (0 , len(rt.sequenceOfNodes) - 1):
                A = rt.sequenceOfNodes[n]
                B = rt.sequenceOfNodes[n + 1]
                rtTime += (self.distanceMatrix[A.ID][B.ID] + self.allNodes[B.ID].service_time)
                rtProfit += A.profit
            if abs(rtTime - rt.time) > 0.0001:
                print ('Route Cost problem')
                
            totalSolCost += rt.time
            
        if abs(totalSolCost - self.sol.time) > 0.0001:
            print('Solution Cost problem')
            
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
    
    def ModifySolution(self):
        for route in self.sol.routes:
            route.sequenceOfNodes.append(Node(101, 0, 0, 50, 50))
        list = []
        for i in range(0, len(self.allNodes)):
            self.distanceMatrix[i].append(0)
            list.append(0)
        self.distanceMatrix.append(list)   
        
    def InitializeOperators(self, rm):
        rm.Initialize()
    
    
    
    def LocalSearch(self):
        self.bestSolution = self.cloneSolution(self.sol)
        self.ModifySolution()
        terminationCondition = False
        rm = RelocationMove()
        count = 0
        while terminationCondition is False:
            count += 1
            rm.Initialize()
            self.FindBestRelocationMove(rm)
            if rm.originRoutePosition is not None:
                if rm.moveCost < 0:
                    self.ApplyRelocationMove(rm)
                else:
                    terminationCondition = True
            if (self.sol.moveCost < self.bestSolution.moveCost):
                self.CalculateRoutes()
                self.bestSolution = self.cloneSolution(self.sol)
        for rt in self.bestSolution.routes:
            rt.sequenceOfNodes = rt.sequenceOfNodes[:-1]
        for rt in self.sol.routes:
            rt.sequenceOfNodes = rt.sequenceOfNodes[:-1]
        print("Termination after ", count, "loops.")
    
    
    
    
    
    
    
    
    
    
    
    
       
# Ερώτημα Δ - Κατασκευή VND Αλγορίθμου που θα καλεί τους 4 τελεστές 

    def VND(self):
        self.bestSolution = self.cloneSolution(self.sol)
        VNDIterator = 0
        kmax = 2
        rm = RelocationMove()
        k = 0
        draw = True

        while k <= kmax:
            self.InitializeOperators(rm)
            if k == 1:
                self.FindBestRelocationMove(rm)
                if rm.originRoutePosition is not None and rm.moveCost < 0:
                    self.ApplyRelocationMove(rm)
                    if draw:
                        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                    VNDIterator = VNDIterator + 1
                    self.searchTrajectory.append(self.sol.time)
                    k = 0
                else:
                    k += 1
            
            if (self.sol.time < self.bestSolution.time):
                self.bestSolution = self.cloneSolution(self.sol)

        SolDrawer.draw('final_vnd', self.bestSolution, self.allNodes)
        SolDrawer.drawTrajectory(self.searchTrajectory)
        
        
    def ApplyMove(self, moveStructure):
        if isinstance(moveStructure, RelocationMove):
            self.ApplyRelocationMove(moveStructure)
       
