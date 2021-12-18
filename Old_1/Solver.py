from Vrp_model import *

class Solution:
    def __init__(self):
        self.dist = 0.0
        self.routes = []

class CustomerInsertion(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.dist = 10 ** 9

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
        self.customers = m.customers
        self.depot = m.allNodes[0]
        self.distanceMatrix = m.matrix
        self.sol = None

    def solve(self):
        self.ApplyNearestNeighborMethod()
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

    def ApplyNearestNeighborMethod(self):
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

# Local search

    def cloneRoute(self, rt: Route, i):
        if i < 15:
            cloned = Route(self.depot, 1500)
        else:
            cloned = Route(self.depot, 1200)
        cloned.dist = rt.dist
        cloned.load = rt.load
        cloned.time = rt.time
        cloned.sequenceOfNodes = rt.sequenceOfNodes.copy()
        return cloned

    def cloneSolution(self, sol: Solution):
        cloned = Solution()
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            clonedRoute = self.cloneRoute(rt, i)
            cloned.routes.append(clonedRoute)
        cloned.dist = self.sol.dist
        return cloned

    def StoreBestRelocationMove(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost,
                                originRtDistChange, targetRtDistChange, t, o, rm: RelocationMove):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.distChangeOriginRt = originRtDistChange
        rm.distChangeTargetRt = targetRtDistChange
        rm.timeChangeOriginRt = o
        rm.timeChangeTargetRt = t
        rm.moveCost = moveCost

    def FindBestRelocationMove(self, rm):
        for originRouteIndex in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[originRouteIndex]
            for targetRouteIndex in range(0, len(self.sol.routes)):
                rt2: Route = self.sol.routes[targetRouteIndex]
                for originNodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                    for targetNodeIndex in range(0, len(rt2.sequenceOfNodes) - 1):
                        if originRouteIndex == targetRouteIndex and (
                                targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue
                        A = rt1.sequenceOfNodes[originNodeIndex - 1]
                        B = rt1.sequenceOfNodes[originNodeIndex]
                        C = rt1.sequenceOfNodes[originNodeIndex + 1]
                        F = rt2.sequenceOfNodes[targetNodeIndex]
                        G = rt2.sequenceOfNodes[targetNodeIndex + 1]
                        if rt1 != rt2:
                            if rt2.load + B.demand > rt2.capacity:
                                continue
                        if (rt2.time - (self.distanceMatrix[F.id][G.id] / 35) + (self.distanceMatrix[F.id][B.id] / 35) + (self.distanceMatrix[B.id][G.id] / 35 + B.service_time) > 3.5):
                            continue
                        t = rt2.time - (self.distanceMatrix[F.id][G.id] / 35) + (
                                    self.distanceMatrix[F.id][B.id] / 35) + (
                                        self.distanceMatrix[B.id][G.id] / 35 + B.service_time)
                        o = rt1.time - self.distanceMatrix[A.id][B.id] / 35 - self.distanceMatrix[B.id][
                            C.id] / 35 + self.distanceMatrix[A.id][C.id] / 35 - B.service_time
                        distAdded = self.distanceMatrix[A.id][C.id] + self.distanceMatrix[F.id][B.id] + \
                                    self.distanceMatrix[B.id][G.id]
                        distRemoved = self.distanceMatrix[A.id][B.id] + self.distanceMatrix[B.id][C.id] + \
                                      self.distanceMatrix[F.id][G.id]
                        originRtDistChange = self.distanceMatrix[A.id][C.id] - self.distanceMatrix[A.id][B.id] - \
                                             self.distanceMatrix[B.id][C.id]
                        targetRtDistChange = self.distanceMatrix[F.id][B.id] + self.distanceMatrix[B.id][G.id] - \
                                             self.distanceMatrix[F.id][G.id]
                        moveCost = distAdded - distRemoved
                        if (moveCost < rm.moveCost) and abs(moveCost) > 0.0001:
                            self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex,
                                                         targetNodeIndex, moveCost, originRtDistChange,
                                                         targetRtDistChange, t, o, rm)

    def ApplyRelocationMove(self, rm: RelocationMove):
        originRt = self.sol.routes[rm.originRoutePosition]
        targetRt = self.sol.routes[rm.targetRoutePosition]
        B = originRt.sequenceOfNodes[rm.originNodePosition]
        if originRt == targetRt:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            if rm.originNodePosition < rm.targetNodePosition:
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition, B)
            else:
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)
            originRt.dist += rm.moveCost
        else:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)
            originRt.dist += rm.distChangeOriginRt
            if (originRt.dist < 0):
                originRt.dist = 0
            targetRt.dist += rm.distChangeTargetRt
            if (targetRt.dist < 0):
                targetRt.dist = 0
            originRt.load -= B.demand
            targetRt.load += B.demand
        originRt.time = rm.timeChangeOriginRt
        targetRt.time = rm.timeChangeTargetRt
        self.sol.dist += rm.moveCost
        self.TestSolution()

    def ModifySolution(self):
        for route in self.sol.routes:
            route.sequenceOfNodes.append(Node(101, 0, 0, 50, 50))
        list = []
        for i in range(0, len(self.allNodes)):
            self.distanceMatrix[i].append(0)
            list.append(0)
        self.distanceMatrix.append(list)

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
            if (self.sol.dist < self.bestSolution.dist):
                self.CalculateRoutes()
                self.bestSolution = self.cloneSolution(self.sol)
        for rt in self.bestSolution.routes:
            rt.sequenceOfNodes = rt.sequenceOfNodes[:-1]
        for rt in self.sol.routes:
            rt.sequenceOfNodes = rt.sequenceOfNodes[:-1]
        print("Termination after ", count, "loops.")

# VND
    def FindBestSwapMove(self, sm):
        for firstRouteIndex in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[firstRouteIndex]
            for secondRouteIndex in range(firstRouteIndex, len(self.sol.routes)):
                rt2: Route = self.sol.routes[secondRouteIndex]
                for firstNodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                    startOfSecondNodeIndex = 1
                    if rt1 == rt2:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    for secondNodeIndex in range(startOfSecondNodeIndex, len(rt2.sequenceOfNodes) - 1):
                        a1 = rt1.sequenceOfNodes[firstNodeIndex - 1]
                        b1 = rt1.sequenceOfNodes[firstNodeIndex]
                        c1 = rt1.sequenceOfNodes[firstNodeIndex + 1]
                        a2 = rt2.sequenceOfNodes[secondNodeIndex - 1]
                        b2 = rt2.sequenceOfNodes[secondNodeIndex]
                        c2 = rt2.sequenceOfNodes[secondNodeIndex + 1]
                        if rt1 == rt2:
                            if firstNodeIndex == secondNodeIndex - 1:
                                distRemoved = self.distanceMatrix[a1.id][b1.id] + self.distanceMatrix[b1.id][b2.id] + \
                                              self.distanceMatrix[b2.id][c2.id]
                                distAdded = self.distanceMatrix[a1.id][b2.id] + self.distanceMatrix[b2.id][b1.id] + \
                                            self.distanceMatrix[b1.id][c2.id]
                                moveCost = distAdded - distRemoved
                                if (rt2.time + moveCost / 35) > 3.5:
                                    continue
                                time1 = rt1.time - distRemoved / 35 + distAdded / 35
                                time2 = rt1.time - distRemoved / 35 + distAdded / 35
                            else:
                                distRemoved1 = self.distanceMatrix[a1.id][b1.id] + self.distanceMatrix[b1.id][c1.id]
                                distAdded1 = self.distanceMatrix[a1.id][b2.id] + self.distanceMatrix[b2.id][c1.id]
                                distRemoved2 = self.distanceMatrix[a2.id][b2.id] + self.distanceMatrix[b2.id][c2.id]
                                distAdded2 = self.distanceMatrix[a2.id][b1.id] + self.distanceMatrix[b1.id][c2.id]
                                moveCost = distAdded1 + distAdded2 - (distRemoved1 + distRemoved2)
                                if (rt2.time + moveCost / 35) > 3.5:
                                    continue
                                time1 = rt1.time - distRemoved1 / 35 + distAdded1 / 35
                                time2 = rt1.time - distRemoved2 / 35 + distAdded2 / 35
                            distChangeFirstRoute = moveCost
                            distChangeSecondRoute = moveCost
                        else:
                            if rt1.load - b1.demand + b2.demand > rt1.capacity:
                                continue
                            if rt2.load - b2.demand + b1.demand > rt2.capacity:
                                continue
                            distRemoved1 = self.distanceMatrix[a1.id][b1.id] + self.distanceMatrix[b1.id][c1.id]
                            distAdded1 = self.distanceMatrix[a1.id][b2.id] + self.distanceMatrix[b2.id][c1.id]
                            distRemoved2 = self.distanceMatrix[a2.id][b2.id] + self.distanceMatrix[b2.id][c2.id]
                            distAdded2 = self.distanceMatrix[a2.id][b1.id] + self.distanceMatrix[b1.id][c2.id]
                            if ((rt2.time - distRemoved2 / 35 + distAdded2 / 35) or (
                                    rt1.time - distRemoved1 / 35 + distAdded1 / 35)) > 3.5:
                                continue
                            time1 = rt1.time - distRemoved1 / 35 + distAdded1 / 35
                            time2 = rt1.time - distRemoved2 / 35 + distAdded2 / 35
                            distChangeFirstRoute = distAdded1 - distRemoved1
                            distChangeSecondRoute = distAdded2 - distRemoved2

                            moveCost = distAdded1 + distAdded2 - (distRemoved1 + distRemoved2)
                        if moveCost < sm.moveCost and abs(moveCost) > 0.0001:
                            self.StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex,
                                                   moveCost, distChangeFirstRoute, distChangeSecondRoute, time1, time2,
                                                   sm)

    def StoreBestSwapMove(self, firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost,
                          distChangeFirstRoute, distChangeSecondRoute, time1, time2, sm):
        sm.positionOfFirstRoute = firstRouteIndex
        sm.positionOfSecondRoute = secondRouteIndex
        sm.positionOfFirstNode = firstNodeIndex
        sm.positionOfSecondNode = secondNodeIndex
        sm.distChangeFirstRt = distChangeFirstRoute
        sm.distChangeSecondRt = distChangeSecondRoute
        sm.time1 = time1
        sm.time2 = time2
        sm.moveCost = moveCost

    def ApplySwapMove(self, sm):
        oldDist = self.CalculateDistance(self.sol)
        rt1 = self.sol.routes[sm.positionOfFirstRoute]
        rt2 = self.sol.routes[sm.positionOfSecondRoute]
        b1 = rt1.sequenceOfNodes[sm.positionOfFirstNode]
        b2 = rt2.sequenceOfNodes[sm.positionOfSecondNode]
        rt1.sequenceOfNodes[sm.positionOfFirstNode] = b2
        rt2.sequenceOfNodes[sm.positionOfSecondNode] = b1
        if (rt1 == rt2):
            rt1.dist += sm.moveCost
            rt1.time = sm.time1
        else:
            rt1.dist += sm.distChangeFirstRt
            rt2.dist += sm.distChangeSecondRt
            rt1.load = rt1.load - b1.demand + b2.demand
            rt2.load = rt2.load + b1.demand - b2.demand
            rt1.time = sm.time1
            rt2.time = sm.time2
        self.sol.dist += sm.moveCost
        self.TestSolution()

    def FindBestTwoOptMove(self, top):
        for rtInd1 in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[rtInd1]
            for rtInd2 in range(rtInd1, len(self.sol.routes)):
                rt2: Route = self.sol.routes[rtInd2]
                for nodeInd1 in range(0, len(rt1.sequenceOfNodes) - 1):
                    start2 = 0
                    if (rt1 == rt2):
                        start2 = nodeInd1 + 2
                    for nodeInd2 in range(start2, len(rt2.sequenceOfNodes) - 1):
                        moveCost = 10 ** 9
                        A = rt1.sequenceOfNodes[nodeInd1]
                        B = rt1.sequenceOfNodes[nodeInd1 + 1]
                        K = rt2.sequenceOfNodes[nodeInd2]
                        L = rt2.sequenceOfNodes[nodeInd2 + 1]
                        if rt1 == rt2:
                            distAdded = self.distanceMatrix[A.id][K.id] + self.distanceMatrix[B.id][L.id]
                            distRemoved = self.distanceMatrix[A.id][B.id] + self.distanceMatrix[K.id][L.id]
                            moveCost = distAdded - distRemoved
                            if rt1.time - (moveCost / 35) > 3.5:
                                continue
                        else:
                            if nodeInd1 == 0 and nodeInd2 == 0:
                                continue
                            if self.CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):
                                continue
                            distAdded = self.distanceMatrix[A.id][L.id] + self.distanceMatrix[B.id][K.id]
                            distRemoved = self.distanceMatrix[A.id][B.id] + self.distanceMatrix[K.id][L.id]
                            if (rt1.time - self.distanceMatrix[A.id][B.id] / 35 + self.distanceMatrix[A.id][
                                L.id]) > 3.5 or (
                                    rt2.time - self.distanceMatrix[K.id][L.id] / 35 + self.distanceMatrix[B.id][
                                K.id]) > 3.5:
                                continue
                            moveCost = distAdded - distRemoved
                        if moveCost < top.moveCost and abs(moveCost) > 0.0001:
                            self.StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top)

    def StoreBestTwoOptMove(self, rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top):
        top.positionOfFirstRoute = rtInd1
        top.positionOfSecondRoute = rtInd2
        top.positionOfFirstNode = nodeInd1
        top.positionOfSecondNode = nodeInd2
        top.moveCost = moveCost

    def ApplyTwoOptMove(self, top):
        rt1: Route = self.sol.routes[top.positionOfFirstRoute]
        rt2: Route = self.sol.routes[top.positionOfSecondRoute]
        if rt1 == rt2:
            reversedSegment = reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
            rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegment
            rt1.dist += top.moveCost
        else:
            relocatedSegmentOfRt1 = rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]
            relocatedSegmentOfRt2 = rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]
            del rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]
            del rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]
            rt1.sequenceOfNodes.extend(relocatedSegmentOfRt2)
            rt2.sequenceOfNodes.extend(relocatedSegmentOfRt1)
            self.UpdateRouteCostLoadTime(rt1)
            self.UpdateRouteCostLoadTime(rt2)
        self.sol.dist += top.moveCost
        self.TestSolution()

    def UpdateRouteCostLoadTime(self, rt: Route):
        tc = 0
        tl = 0
        tt = 0
        for i in range(0, len(rt.sequenceOfNodes) - 1):
            A = rt.sequenceOfNodes[i]
            B = rt.sequenceOfNodes[i + 1]
            tc += self.distanceMatrix[A.id][B.id]
            tl += A.demand
            tt += tc / 35 + A.service_time
        rt.load = tl
        rt.dist = tc
        rt.time = tt

    def CapacityIsViolated(self, rt1, nodeInd1, rt2, nodeInd2):
        rt1FirstSegmentLoad = 0
        for i in range(0, nodeInd1 + 1):
            n = rt1.sequenceOfNodes[i]
            rt1FirstSegmentLoad += n.demand
        rt1SecondSegmentLoad = rt1.load - rt1FirstSegmentLoad
        rt2FirstSegmentLoad = 0
        for i in range(0, nodeInd2 + 1):
            n = rt2.sequenceOfNodes[i]
            rt2FirstSegmentLoad += n.demand
        rt2SecondSegmentLoad = rt2.load - rt2FirstSegmentLoad
        if (rt1FirstSegmentLoad + rt2SecondSegmentLoad > rt1.capacity):
            return True
        if (rt2FirstSegmentLoad + rt1SecondSegmentLoad > rt2.capacity):
            return True

    def InitializeOperators(self, rm, sm, top):
        rm.Initialize()
        sm.Initialize()
        top.Initialize()

    def VND(self):
        self.bestSolution = self.cloneSolution(self.sol)
        self.ModifySolution()
        VNDIterator = 0
        kmax = 2
        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()
        k = 0
        count = 0
        while k <= kmax:
            self.InitializeOperators(rm, sm, top)
            if k == 1:
                self.FindBestRelocationMove(rm)
                if rm.originRoutePosition is not None and rm.moveCost < 0:
                    self.ApplyRelocationMove(rm)
                    VNDIterator = VNDIterator + 1
                    k = 0
                else:
                    k += 1
            elif k == 2:
                self.FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None and sm.moveCost < 0:
                    self.ApplySwapMove(sm)
                    VNDIterator = VNDIterator + 1
                    k = 0
                else:
                    k += 1
            elif k == 0:
                self.FindBestTwoOptMove(top)
                if top.positionOfFirstRoute is not None and top.moveCost < 0:
                    self.ApplyTwoOptMove(top)
                    VNDIterator = VNDIterator + 1
                    k = 0
                else:
                    k += 1
            count += 1

        if (self.sol.dist < self.bestSolution.dist):
            self.CalculateRoutes()
            self.bestSolution = self.cloneSolution(self.sol)
        for rt in self.bestSolution.routes:
            rt.sequenceOfNodes = rt.sequenceOfNodes[:-1]
        for rt in self.sol.routes:
            rt.sequenceOfNodes = rt.sequenceOfNodes[:-1]