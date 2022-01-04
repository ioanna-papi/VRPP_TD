from SOLVER import *

m = Model()
m.BuildModel()
s = Solver(m)
print("Best Node")
#sol = s.solve()
solution = s.ApplyBestNodeMethod()
print(s.ObjectiveFunction(solution))
print()
