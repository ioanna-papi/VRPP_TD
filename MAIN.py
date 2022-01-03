from VRP import *
from SOLVER import *

m = Model()
m.BuildModel()
s = Solver(m)
print("Best Neighbor")
solution = s.ApplyBestNodeMethod()
print(s.objective(solution))
print()
# print("Local Search")
# solution2 = s.LocalSearch()
# print(s.objective(solution2))
# print()
#print("VND")
#solution_vnd = s.VND()
#print(s.objective(solution_vnd))
