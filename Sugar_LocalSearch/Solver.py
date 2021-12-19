from TSP_Model import *
from SolutionDrawer import *

class Solution:
    def __init__(self):
        self.cost = 0.0
        self.sequenceOfNodes = []


class RelocationMove(object):
    def __init__(self):
        self.positionOfRelocated = None
        self.positionToBeInserted = None
        self.moveCost = None

    def Initialize(self):
        self.moveCost = 10 ** 9
        self.positionOfRelocated = None
        self.positionToBeInserted = None


class SwapMove(object):
    def __init__(self):
        self.positionOfFirst = None
        self.positionOfSecond = None
        self.moveCost = None
    def Initialize(self):
        self.moveCost = 10 ** 9
        self.positionOfFirst = None
        self.positionOfSecond = None


class TwoOptMove(object):
    def __init__(self):
        self.positionOfFirst = None
        self.positionOfSecond = None
        self.moveCost = None
    def Initialize(self):
        self.moveCost = 10 ** 9
        self.positionOfFirst = None
        self.positionOfSecond = None


class Solver:
    def __init__(self, m):
        self.allNodes = m.allNodes
        self.customers = m.customers
        self.depot = m.allNodes[0]
        self.distanceMatrix = m.matrix
        self.sol = None
        self.bestSolution = None

    def solve(self):
        self.SetRoutedFlagToFalseForAllCustomers()
        self.ApplyNearestNeighborMethod()
        self.ReportSolution(self.sol)
        self.LocalSearch(2)
        self.ReportSolution(self.sol)
        return self.sol

    def solveExample(self):
        self.BuildExampleSolution()
        self.ReportSolution(self.sol)
        self.LocalSearch(1)
        self.ReportSolution(self.sol)
        return self.sol


    def SetRoutedFlagToFalseForAllCustomers(self):
        for i in range(0, len(self.customers)):
            self.customers[i].isRouted = False

    def ApplyNearestNeighborMethod(self):
        self.sol = Solution()
        self.sol.sequenceOfNodes.append(self.depot)

        for i in range(0, len(self.customers)):
            indexOfTheNextCustomer = -1
            minimumInsertionCost = 1000000
            lastIndexInSolution = len(self.sol.sequenceOfNodes) - 1
            lastNodeInTheCurrentSequence = self.sol.sequenceOfNodes[lastIndexInSolution]

            for j in range(0, len(self.customers)):
                candidate = self.customers[j]

                if candidate.isRouted == True:
                    continue

                trialCost = self.distanceMatrix[lastNodeInTheCurrentSequence.ID][candidate.ID]

                if (trialCost < minimumInsertionCost):
                    indexOfTheNextCustomer = j
                    minimumInsertionCost = trialCost

            insertedCustomer = self.customers[indexOfTheNextCustomer]
            self.sol.sequenceOfNodes.append(insertedCustomer)
            self.sol.cost += self.distanceMatrix[lastNodeInTheCurrentSequence.ID][insertedCustomer.ID]
            insertedCustomer.isRouted = True

        lastNodeInTheCurrentSequence = self.sol.sequenceOfNodes[-1]
        self.sol.sequenceOfNodes.append(self.depot)
        self.sol.cost += self.distanceMatrix[lastNodeInTheCurrentSequence.ID][self.depot.ID]

        SolDrawer.draw('NN-', self.sol, self.allNodes)

    def LocalSearch(self, operator):
        self.bestSolution = self.cloneSolution(self.sol)
        self.TestSolution()
        terminationCondition = False
        localSearchIterator = 1

        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()

        while terminationCondition is False:
            rm.Initialize()
            sm.Initialize()
            top.Initialize()

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
            #TwoOpt
            elif operator == 2:
                self.FindBestTwoOptMove(top)
                if top.positionOfFirst is not None:
                    if top.moveCost < 0:
                        self.ApplyTwoOptMove(top)
                    else:
                        terminationCondition = True

            self.TestSolution()

            if (self.sol.cost < self.bestSolution.cost):
                self.bestSolution = self.cloneSolution(self.sol)

            localSearchIterator = localSearchIterator + 1

        self.sol = self.bestSolution

    def cloneSolution(self, sol: Solution):
        cloned = Solution()
        cloned.sequenceOfNodes = self.sol.sequenceOfNodes.copy()
        cloned.cost = self.sol.cost
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

                    costRemoved1 = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][C.ID]
                    costRemoved2 = self.distanceMatrix[F.ID][G.ID]

                    costAdded1 = self.distanceMatrix[A.ID][C.ID]
                    costAdded2 = self.distanceMatrix[F.ID][B.ID] + self.distanceMatrix[B.ID][G.ID]

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
                    costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][C.ID] + self.distanceMatrix[C.ID][F.ID]
                    costAdded = self.distanceMatrix[A.ID][C.ID] + self.distanceMatrix[C.ID][B.ID] + self.distanceMatrix[B.ID][F.ID]
                else:
                    costRemoved1 = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][C.ID]
                    costAdded1 = self.distanceMatrix[A.ID][E.ID] + self.distanceMatrix[E.ID][C.ID]
                    costRemoved2 = self.distanceMatrix[D.ID][E.ID] + self.distanceMatrix[E.ID][F.ID]
                    costAdded2 = self.distanceMatrix[D.ID][B.ID] + self.distanceMatrix[B.ID][F.ID]
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

        self.sol.cost = self.sol.cost + rm.moveCost


    def ApplySwapMove(self, sm):
        firstNode = self.sol.sequenceOfNodes[sm.positionOfFirst]
        secondNode = self.sol.sequenceOfNodes[sm.positionOfSecond]
        self.sol.sequenceOfNodes[sm.positionOfFirst] = secondNode
        self.sol.sequenceOfNodes[sm.positionOfSecond] = firstNode

        self.sol.cost = self.sol.cost + sm.moveCost

    def ReportSolution(self, sol):
        for i in range(0, len(sol.sequenceOfNodes)):
            print(sol.sequenceOfNodes[i].ID, end=' ')
        print(sol.cost)

    def FindBestTwoOptMove(self, top):
        for firstIndex in range(0, len(self.sol.sequenceOfNodes) - 1):
            A:Node = self.sol.sequenceOfNodes[firstIndex]
            B:Node = self.sol.sequenceOfNodes[firstIndex + 1]

            for secondIndex in range (firstIndex + 2, len(self.sol.sequenceOfNodes) - 1):
                K:Node = self.sol.sequenceOfNodes[secondIndex]
                L: Node = self.sol.sequenceOfNodes[secondIndex + 1]

                if firstIndex == 0 and secondIndex == len(self.sol.sequenceOfNodes) - 2:
                    continue

                costAdded = self.distanceMatrix[A.ID][K.ID] + self.distanceMatrix[B.ID][L.ID]
                costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[K.ID][L.ID]

                moveCost = costAdded - costRemoved

                if moveCost < top.moveCost:
                    top.moveCost = moveCost
                    top.positionOfFirst = firstIndex
                    top.positionOfSecond = secondIndex

    def ApplyTwoOptMove(self, top):
        #mylist[::-1] creates a copy and reverses it
        modifiedSequence = []
        i = 0
        while i <= top.positionOfFirst:
            modifiedSequence.append(self.sol.sequenceOfNodes[i])
            i = i + 1
        i = top.positionOfSecond
        while i > top.positionOfFirst:
            modifiedSequence.append(self.sol.sequenceOfNodes[i])
            i = i - 1
        i = top.positionOfSecond + 1
        while i < len(self.sol.sequenceOfNodes):
            modifiedSequence.append(self.sol.sequenceOfNodes[i])
            i = i + 1

        self.sol.sequenceOfNodes = modifiedSequence

        #could also use this more complex syntax
        #self.sol.sequenceOfNodes[top.positionOfFirst: top.positionOfSecond + 1] = reversed(self.sol.sequenceOfNodes[top.positionOfFirst: top.positionOfSecond + 1])

        self.sol.cost = self.sol.cost + top.moveCost

    def TestSolution(self):
        tc = 0
        for i in range (0, len(self.sol.sequenceOfNodes) - 1):
            A: Node = self.sol.sequenceOfNodes[i]
            B: Node = self.sol.sequenceOfNodes[i + 1]
            tc += self.distanceMatrix[A.ID][B.ID]

        if abs (self.sol.cost - tc) > 0.0001:
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

        self.sol.cost = 0
        for i in range (0, len(self.sol.sequenceOfNodes) - 1):
            n1 = self.sol.sequenceOfNodes[i]
            n2 = self.sol.sequenceOfNodes[i + 1]
            self.sol.cost += self.distanceMatrix[n1.ID][n2.ID]

        a = 0







