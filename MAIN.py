from SOLVER import *

m = Model()
m.BuildModel()
s = Solver(m)
#sol = s.solve()

solution = s.ApplyBestNodeMethod()
print(" TOTAL PROFIT =", s.objective(solution))
print()
