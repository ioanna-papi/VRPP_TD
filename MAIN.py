from SOLVER import *

m = Model()
m.BuildModel()
s = Solver(m)
print("Best Node")
solution = s.ApplyBestNodeMethod()
#print(s.objective(solution))
print()
