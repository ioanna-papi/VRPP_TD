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
    

    # Swap
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
                            
                            if rt1.time > 150:
                                continue
                            if firstNodeIndex == secondNodeIndex - 1:
                                costRemoved = self.distanceMatrix[a1.ID][b1.ID] + self.allNodes[b1.ID].service_time + self.distanceMatrix[b1.ID][b2.ID] + self.allNodes[b2.ID].service_time + self.distanceMatrix[b2.ID][c2.ID] + self.allNodes[c2.ID].service_time
                                costAdded = self.distanceMatrix[a1.ID][b2.ID] + self.allNodes[b2.ID].service_time + self.distanceMatrix[b2.ID][b1.ID] + self.allNodes[b1.ID].service_time + self.distanceMatrix[b1.ID][c2.ID] + self.allNodes[c2.ID].service_time
                                moveCost = costAdded - costRemoved
                                if (rt1.time + moveCost) > 150:
                                    continue   
                                
                            else:

                                costRemoved1 = self.distanceMatrix[a1.ID][b1.ID] + self.allNodes[b1.ID].service_time + self.distanceMatrix[b1.ID][c1.ID] + self.allNodes[c1.ID].service_time
                                costAdded1 = self.distanceMatrix[a1.ID][b2.ID] + self.allNodes[b2.ID].service_time + self.distanceMatrix[b2.ID][c1.ID] + self.allNodes[c1.ID].service_time
                                costRemoved2 = self.distanceMatrix[a2.ID][b2.ID] + self.allNodes[b2.ID].service_time + self.distanceMatrix[b2.ID][c2.ID] + self.allNodes[c2.ID].service_time
                                costAdded2 = self.distanceMatrix[a2.ID][b1.ID] + self.allNodes[b1.ID].service_time + self.distanceMatrix[b1.ID][c2.ID] + self.allNodes[c2.ID].service_time
                                
                                costChangeFRoute = costAdded1 - costRemoved1
                                costChangeSRoute = costAdded2 - costRemoved2
                                rttime1 = rt1.time + costChangeFRoute
                                rttime2 = rt2.time + costChangeSRoute
                                if rttime1 > 150:
                                    continue
                                if rttime2 > 150:
                                    continue
                                    
                                moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                                 
                         
                        else:
                            costRemoved1 = self.distanceMatrix[a1.ID][b1.ID] + self.allNodes[b1.ID].service_time + self.distanceMatrix[b1.ID][c1.ID] + self.allNodes[c1.ID].service_time
                            costAdded1 = self.distanceMatrix[a1.ID][b2.ID] + self.allNodes[b2.ID].service_time + self.distanceMatrix[b2.ID][c1.ID] + self.allNodes[c1.ID].service_time
                            costRemoved2 = self.distanceMatrix[a2.ID][b2.ID] + self.allNodes[b2.ID].service_time + self.distanceMatrix[b2.ID][c2.ID] + self.allNodes[c2.ID].service_time
                            costAdded2 = self.distanceMatrix[a2.ID][b1.ID] + self.allNodes[b1.ID].service_time + self.distanceMatrix[b1.ID][c2.ID] + self.allNodes[c2.ID].service_time

                            costChangeFirstRoute = costAdded1 - costRemoved1
                            costChangeSecondRoute = costAdded2 - costRemoved2
                            rttime1 = rt1.time + costChangeFirstRoute
                            rttime2 = rt2.time + costChangeSecondRoute
                            if rttime1 > 150:
                                continue
                            if rttime2 > 150:
                                continue

                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                            
                        if moveCost < sm.moveCost and abs(moveCost) > 0.0001:
                            self.StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm)
    
    def ApplySwapMove(self, sm):
       oldCost = self.CalculateTotalCost(self.sol)
       rt1 = self.sol.routes[sm.positionOfFirstRoute]
       rt2 = self.sol.routes[sm.positionOfSecondRoute]
       b1 = rt1.sequenceOfNodes[sm.positionOfFirstNode]
       b2 = rt2.sequenceOfNodes[sm.positionOfSecondNode]
       rt1.sequenceOfNodes[sm.positionOfFirstNode] = b2
       rt2.sequenceOfNodes[sm.positionOfSecondNode] = b1

       if (rt1 == rt2):
           rt1.time += sm.moveCost
       else:
           rt1.time += sm.costChangeFirstRt
           rt2.time += sm.costChangeSecondRt
           rt1.profit = rt1.profit - b1.profit + b2.profit
           rt2.profit = rt2.profit + b1.profit - b2.profit

       self.sol.time += sm.moveCost
       self.TestSolution()
  
    def StoreBestSwapMove(self, firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm):
        sm.positionOfFirstRoute = firstRouteIndex
        sm.positionOfSecondRoute = secondRouteIndex
        sm.positionOfFirstNode = firstNodeIndex
        sm.positionOfSecondNode = secondNodeIndex
        sm.costChangeFirstRt = costChangeFirstRoute
        sm.costChangeSecondRt = costChangeSecondRoute
        sm.moveCost = moveCost
      
    def InitializeSm(self, sm):
        sm.Initialize()
    
    # Insertion
    def FindBestInsertionAllPositions(self, im):
        for firstInd in range(0, len(self.sol.routes)):
            rt1:Route = self.sol.routes[firstInd]
            for i in range(0, len(self.customers)):
                candidateCust: Node = self.customers[i]
                if candidateCust.isRouted is False:
                    if (rt1.time + self.distanceMatrix[firstInd][candidateCust.ID] + allNodes[candidateCust.ID].service_time) <= 150:
                        lastNodePresentInTheRoute = rt.sequenceOfNodes[-2]
                        for j in range(0, len(rt1.sequenceOfNodes) - 1):
                            A = rt1.sequenceOfNodes[j]
                            B = rt1.sequenceOfNodes[j + 1] 
                            costAdded = self.distanceMatrix[A.ID][candidateCust.ID] + allNodes[candidateCust.ID].service_time + self.distanceMatrix[candidateCust.ID][B.ID] + allNodes[B.ID].service_time
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + allNodes[B.ID].service_time
                            moveCost = costAdded - costRemoved

                            if moveCost < im.time and abs(moveCost) > 0.0001:
                                im.customer = candidateCust
                                im.route = rt
                                im.time = moveCost
                                im.profit = candidateCust.profit
                                im.insertionPosition = j
        
        
    def ApplyCustomerInsertionAllPositions(self, im):
        insCustomer = im.customer
        rt = im.route
        # before the second depot occurrence
        insIndex = im.insertionPosition
        rt.sequenceOfNodes.insert(insIndex + 1, insCustomer)
        rt.time += im.time
        self.sol.time += im.time
        rt.profit += insCustomer.profit
        self.sol.profit += insCustomer.profit
        insCustomer.isRouted = True
    
    
    def InitializeIm(self, im):
        im.Initialize()
    
    # Profitable Swap
    def FindBestProfitableSwapMove(self, psm):
        for firstRouteIndex in range(0, len(self.sol.routes)):
            rt1:Route = self.sol.routes[firstRouteIndex]
            for secondRouteIndex in range (firstRouteIndex, len(self.sol.routes)):
                rt2:Route = self.sol.routes[secondRouteIndex]
                for firstNodeIndex in range (1, len(rt1.sequenceOfNodes) - 1):
                     
                    for secondNodeIndex in range (0, len(self.customers)):
                        cust: Node = self.customers[secondNodeIndex]
                        if cust.isRouted is False:

                            a1 = rt1.sequenceOfNodes[firstNodeIndex - 1]
                            b1 = rt1.sequenceOfNodes[firstNodeIndex]
                            c1 = rt1.sequenceOfNodes[firstNodeIndex + 1]

                            a2 = self.allNodes[cust.ID - 1]
                            b2 = self.allNodes[cust.ID]
                            c2 = self.allNodes[cust.ID + 1]

                            moveCost = None
                            costChangeFirstRoute = None
                            costChangeSecondRoute = None

                            moveCost = None
                            costChangeFirstRoute = None
                            costChangeSecondRoute = None

                            if rt1 == rt2:
                            
                                if rt1.time > 150:
                                    continue
                                if firstNodeIndex == secondNodeIndex - 1:
                                    costRemoved = self.distanceMatrix[a1.ID][b1.ID] + self.allNodes[b1.ID].service_time + self.distanceMatrix[b1.ID][b2.ID] + self.allNodes[b2.ID].service_time + self.distanceMatrix[b2.ID][c2.ID] + self.allNodes[c2.ID].service_time
                                    costAdded = self.distanceMatrix[a1.ID][b2.ID] + self.allNodes[b2.ID].service_time + self.distanceMatrix[b2.ID][b1.ID] + self.allNodes[b1.ID].service_time + self.distanceMatrix[b1.ID][c2.ID] + self.allNodes[c2.ID].service_time
                                    moveCost = costAdded - costRemoved
                                    if (rt1.time + moveCost) > 150:
                                        continue   
                                
                                else:

                                    costRemoved1 = self.distanceMatrix[a1.ID][b1.ID] + self.allNodes[b1.ID].service_time + self.distanceMatrix[b1.ID][c1.ID] + self.allNodes[c1.ID].service_time
                                    costAdded1 = self.distanceMatrix[a1.ID][b2.ID] + self.allNodes[b2.ID].service_time + self.distanceMatrix[b2.ID][c1.ID] + self.allNodes[c1.ID].service_time
                                    costRemoved2 = self.distanceMatrix[a2.ID][b2.ID] + self.allNodes[b2.ID].service_time + self.distanceMatrix[b2.ID][c2.ID] + self.allNodes[c2.ID].service_time
                                    costAdded2 = self.distanceMatrix[a2.ID][b1.ID] + self.allNodes[b1.ID].service_time + self.distanceMatrix[b1.ID][c2.ID] + self.allNodes[c2.ID].service_time
                                
                                    costChangeFRoute = costAdded1 - costRemoved1
                                    costChangeSRoute = costAdded2 - costRemoved2
                                    rttime1 = rt1.time + costChangeFRoute
                                    rttime2 = rt2.time + costChangeSRoute
                                    if rttime1 > 150:
                                        continue
                                    if rttime2 > 150:
                                        continue
                                    
                                    moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                                 
                         
                            else:
                                costRemoved1 = self.distanceMatrix[a1.ID][b1.ID] + self.allNodes[b1.ID].service_time + self.distanceMatrix[b1.ID][c1.ID] + self.allNodes[c1.ID].service_time
                                costAdded1 = self.distanceMatrix[a1.ID][b2.ID] + self.allNodes[b2.ID].service_time + self.distanceMatrix[b2.ID][c1.ID] + self.allNodes[c1.ID].service_time
                                costRemoved2 = self.distanceMatrix[a2.ID][b2.ID] + self.allNodes[b2.ID].service_time + self.distanceMatrix[b2.ID][c2.ID] + self.allNodes[c2.ID].service_time
                                costAdded2 = self.distanceMatrix[a2.ID][b1.ID] + self.allNodes[b1.ID].service_time + self.distanceMatrix[b1.ID][c2.ID] + self.allNodes[c2.ID].service_time

                                costChangeFirstRoute = costAdded1 - costRemoved1
                                costChangeSecondRoute = costAdded2 - costRemoved2
                                rttime1 = rt1.time + costChangeFirstRoute
                                rttime2 = rt2.time + costChangeSecondRoute
                                if rttime1 > 150:
                                    continue
                                if rttime2 > 150:
                                    continue

                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                            if moveCost < sm.moveCost and abs(moveCost) > 0.0001:
                                self.StoreBestProfitableSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, psm)
    
    
    def ApplyProfitableSwapMove(self, psm):
       oldCost = self.CalculateTotalCost(self.sol)
       rt1 = self.sol.routes[psm.positionOfFirstRoute]
       rt2 = self.sol.routes[psm.positionOfSecondRoute]
       b1 = rt1.sequenceOfNodes[psm.positionOfFirstNode]
       b2 = self.allNodes[psm.positionOfSecondNode]
       rt1.sequenceOfNodes[psm.positionOfFirstNode] = b2
       self.allNodes[psm.positionOfSecondNode] = b1

       if (rt1 == rt2):
           rt1.time += psm.moveCost
       else:
           rt1.time += psm.costChangeFirstRt
           rt2.time += psm.costChangeSecondRt
           rt1.profit = rt1.profit - b1.profit + b2.profit
           rt2.profit = rt2.profit + b1.profit - b2.profit

       self.sol.time += psm.moveCost
       self.TestSolution()
        
    def StoreBestProfitableSwapMove(self, firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, psm):
        psm.positionOfFirstRoute = firstRouteIndex
        psm.positionOfSecondRoute = secondRouteIndex
        psm.positionOfFirstNode = firstNodeIndex
        psm.positionOfSecondNode = secondNodeIndex
        psm.costChangeFirstRt = costChangeFirstRoute
        psm.costChangeSecondRt = costChangeSecondRoute
        psm.moveCost = moveCost  
        
    def InitializePsm(self, psm):
        psm.Initialize()
    
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
        
    def InitializeOperators(self, rm, sm, im, psm):
        rm.Initialize()
        sm.Initialize()
        im.Initialize()
        psm.Initialize()
        
       
# Ερώτημα Δ - Κατασκευή VND Αλγορίθμου που θα καλεί τους 4 τελεστές 

    def VND(self):
        self.bestSolution = self.cloneSolution(self.sol)
        VNDIterator = 0
        kmax = 2
        rm = RelocationMove()
        sm = SwapMove()
        im = CustomerInsertionAllPositions()
        psm = ProfitableSwapMove()
        k = 0
        draw = True

        while k <= kmax:
            self.InitializeOperators(rm, sm, im, psm)
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
            elif k == 2:
                self.FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None and sm.moveCost < 0:
                    self.ApplySwapMove(sm)
                    if draw:
                        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                    VNDIterator = VNDIterator + 1
                    self.searchTrajectory.append(self.sol.time)
                    k = 0
                else:
                    k += 1
            elif k == 3:
                self.FindBestInsertionAllPositions(im)
                if im.insertionPosition is not None and im.moveCost < 0:
                    self.ApplyCustomerInsertionAllPositions(im)
                    if draw:
                        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                    VNDIterator = VNDIterator + 1
                    self.searchTrajectory.append(self.sol.time)
                    k = 0
                else:
                    k += 1
            elif k == 0:
                self.FindBestProfitableSwapMove(psm)
                if psm.positionOfFirstRoute is not None and psm.moveCost < 0:
                    self.ApplyProfitableSwapMove(psm)
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
        elif isinstance(moveStructure, SwapMove):
            self.ApplySwapMove(moveStructure)
        elif isinstance(moveStructure, CustomerInsertion):
            self.ApplyCustomerInsertionAllPositions(moveStructure)
        elif isinstance(moveStructure, ProfitableSwapMove):
            self.ApplyProfitableSwapMove(moveStructure)  
       

    
            

   
