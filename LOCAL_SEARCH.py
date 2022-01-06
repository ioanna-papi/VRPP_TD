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
   
# Ερώτημα Γ - Τελεστές τοπικής έρευνας        

    def LocalSearch(self, operator):
        self.bestSolution = self.cloneSolution(self.sol)
        self.TestSolution()
        terminationCondition = False
        localSearchIterator = 1

        rm = RelocationMove()
        sm = SwapMove()
        #im = InsertionMove()
        #psm = ProfitableSwapMove()

        while terminationCondition is False:
            rm.Initialize()
            sm.Initialize()
            #im.Initialize()
            #psm.Initialize()

            SolDrawer.draw(str(localSearchIterator), self.sol, self.allNodes)

            # Relocations
            if operator == 0:
                self.FindBestRelocationMove(rm)
                if rm.positionOfRelocated is not None:
                    if rm.moveCost < 0:
                        self.ApplyRelocationMove(rm)
                    else:
                        terminationCondition = True
            # Swaps
            elif operator == 1:
                self.FindBestSwapMove(sm)
                if sm.positionOfFirst is not None:
                    if sm.moveCost < 0:
                        self.ApplySwapMove(sm)
                    else:
                        terminationCondition = True
            
            
            # Insertions
            elif operator == 2:
                #self.FindBestInsertionMove(im)
                if im.positionOfFirst is not None:
                    if im.moveCost < 0:
                        self.ApplySwapMove(im)
                    else:
                        terminationCondition = True    
                
                
            # Profitable Swaps
            elif operator == 3:
                #self.FindBestInsertionMove(psm)
                if psm.positionOfFirst is not None:
                    if psm.moveCost < 0:
                        self.ApplySwapMove(psm)
                    else:
                        terminationCondition = True 
                
                
            self.TestSolution()

            if (self.sol.time < self.bestSolution.time):
                self.bestSolution = self.cloneSolution(self.sol)

            localSearchIterator = localSearchIterator + 1

        self.sol = self.bestSolution
    
    def cloneRoute(self, rt: Route):
        cloned = Route(self.allNodes[0], rt.time_limit)
        cloned.time = rt.time
        cloned.profit = rt.profit
        cloned.time_limit = rt.time_limit
        cloned.sequenceOfNodes = rt.sequenceOfNodes.copy()
        return cloned
    
    def cloneSolution(self, sol: Solution):
        cloned = Solution()
        cloned.sequenceOfNodes = self.sol.sequenceOfNodes.copy()
        cloned.time = self.sol.time
        return cloned

    def FindBestRelocationMove(self, rm):

        for relIndex in range(1, len(self.sol.sequenceOfNodes) - 1):
            A:Node = self.sol.sequenceOfNodes[relIndex - 1]
            B = self.sol.sequenceOfNodes[relIndex]
            C = self.sol.sequenceOfNodes[relIndex + 1]

            for afterIndex in range(0, len(self.sol.sequenceOfNodes) - 1):

                if afterIndex != relIndex and afterIndex != relIndex - 1:

                    F = self.sol.sequenceOfNodes[afterIndex]
                    G = self.sol.sequenceOfNodes[afterIndex + 1]

                    costRemoved1 = self.distanceMatrix[A.ID][B.ID] + self.customers[B.ID].service_time + self.distanceMatrix[B.ID][C.ID] + self.customers[C.ID].service_time
                    costRemoved2 = self.distanceMatrix[F.ID][G.ID] + self.customers[G.ID].service_time

                    costAdded1 = self.distanceMatrix[A.ID][C.ID] + self.customers[C.ID].service_time
                    costAdded2 = self.distanceMatrix[F.ID][B.ID] + self.customers[B.ID].service_time + self.distanceMatrix[B.ID][G.ID] + self.customers[G.ID].service_time

                    moveCost = costAdded1 + costAdded2 - costRemoved1 - costRemoved2

                    if moveCost < rm.moveCost:
                        rm.moveCost = moveCost
                        rm.positionOfRelocated = relIndex
                        rm.positionToBeInserted = afterIndex

    def FindBestSwapMove(self, sm):
        for firstIndex in range(1, len(self.sol.sequenceOfNodes) - 1):
            A = self.sol.sequenceOfNodes[firstIndex - 1]
            B = self.sol.sequenceOfNodes[firstIndex]
            C = self.sol.sequenceOfNodes[firstIndex + 1]

            for secondIndex in range (firstIndex + 1, len(self.sol.sequenceOfNodes) -1):
                D = self.sol.sequenceOfNodes[secondIndex - 1]
                E = self.sol.sequenceOfNodes[secondIndex]
                F = self.sol.sequenceOfNodes[secondIndex + 1]

                if (secondIndex == firstIndex + 1):
                    costRemoved = self.distanceMatrix[A.ID][B.ID] + self.customers[B.ID].service_time + self.distanceMatrix[B.ID][C.ID] + self.customers[C.ID].service_time + self.distanceMatrix[C.ID][F.ID] + self.customers[F.ID].service_time
                    costAdded = self.distanceMatrix[A.ID][C.ID] + self.customers[C.ID].service_time + self.distanceMatrix[C.ID][B.ID] + self.customers[B.ID].service_time + self.distanceMatrix[B.ID][F.ID] + self.customers[F.ID].service_time
                else:
                    costRemoved1 = self.distanceMatrix[A.ID][B.ID] + self.customers[B.ID].service_time + self.distanceMatrix[B.ID][C.ID] + self.customers[C.ID].service_time
                    costAdded1 = self.distanceMatrix[A.ID][E.ID] + self.customers[E.ID].service_time + self.distanceMatrix[E.ID][C.ID] + self.customers[C.ID].service_time
                    costRemoved2 = self.distanceMatrix[D.ID][E.ID] + self.customers[E.ID].service_time + self.distanceMatrix[E.ID][F.ID] + self.customers[F.ID].service_time
                    costAdded2 = self.distanceMatrix[D.ID][B.ID] + self.customers[B.ID].service_time + self.distanceMatrix[B.ID][F.ID] + self.customers[F.ID].service_time
                    costAdded = costAdded1 + costAdded2
                    costRemoved = costRemoved1 + costRemoved2

                moveCost = costAdded - costRemoved

                if moveCost < sm.moveCost:
                    sm.moveCost = moveCost
                    sm.positionOfFirst = firstIndex
                    sm.positionOfSecond = secondIndex

    def ApplyRelocationMove(self, rm):
        relocatedNode = self.sol.sequenceOfNodes[rm.positionOfRelocated]
        #self.sol.sequenceOfNodes:list.remove(relocatedNode)
        del self.sol.sequenceOfNodes[rm.positionOfRelocated]

        if rm.positionToBeInserted < rm.positionOfRelocated:
            self.sol.sequenceOfNodes.insert(rm.positionToBeInserted + 1, relocatedNode)
        else:
            self.sol.sequenceOfNodes.insert(rm.positionToBeInserted, relocatedNode)

        self.sol.time = self.sol.time + rm.moveCost


    def ApplySwapMove(self, sm):
        firstNode = self.sol.sequenceOfNodes[sm.positionOfFirst]
        secondNode = self.sol.sequenceOfNodes[sm.positionOfSecond]
        self.sol.sequenceOfNodes[sm.positionOfFirst] = secondNode
        self.sol.sequenceOfNodes[sm.positionOfSecond] = firstNode

        self.sol.time = self.sol.time + sm.moveCost

    def ReportSolution(self, sol):
        for i in range(0, len(sol.sequenceOfNodes)):
            print(sol.sequenceOfNodes[i].ID, end=' ')
        print(sol.time)

   
    def TestSolution(self):
        tc = 0
        for i in range (0, len(self.sol.sequenceOfNodes) - 1):
            A: Node = self.sol.sequenceOfNodes[i]
            B: Node = self.sol.sequenceOfNodes[i + 1]
            tc += self.distanceMatrix[A.ID][B.ID] + self.customers[B.ID].service_time

        if abs (self.sol.time - tc) > 0.0001:
            print('Problem!!!')

    def BuildExampleSolution(self):
        self.sol = Solution()
        self.sol.sequenceOfNodes.append(self.allNodes[0])
        self.sol.sequenceOfNodes.append(self.allNodes[3])
        self.sol.sequenceOfNodes.append(self.allNodes[6])
        self.sol.sequenceOfNodes.append(self.allNodes[2])
        self.sol.sequenceOfNodes.append(self.allNodes[5])
        self.sol.sequenceOfNodes.append(self.allNodes[1])
        self.sol.sequenceOfNodes.append(self.allNodes[4])
        self.sol.sequenceOfNodes.append(self.allNodes[0])

        self.sol.time = 0.0
        for i in range (0, len(self.sol.sequenceOfNodes) - 1):
            n1 = self.sol.sequenceOfNodes[i]
            n2 = self.sol.sequenceOfNodes[i + 1]
            self.sol.time += self.distanceMatrix[n1.ID][n2.ID] + self.customers[n2.ID]

     










