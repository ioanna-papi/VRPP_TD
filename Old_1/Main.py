from Vrp_model import *
from Solver import *

#1st question
m1 = Model()
m1.BuildModel()

#3nd question
s1 = Solver(m1)
sol = s1.solve()

#2nd question
dist = s1.CalculateDistance(s1.sol)
print("Total distance: ", dist)

#4th question
s1.LocalSearch()
s1.ReportSolution(s1.sol)
print("Total routes (after local search): ", len(s1.sol.routes))

#5th question
s1.VND()
s1.ReportSolution(s1.sol)

