from Solver import *

m = Model()
m.BuildModel()

s = Solver(m)
solution = s.ApplyBestNodeMethod()
print(" TOTAL PROFIT =", s.objective(solution))


