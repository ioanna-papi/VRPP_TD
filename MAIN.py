from SOLVER import *

# 1st task
m = Model()
m.BuildModel()

# 2nd task
s = Solver(m)
solution = s.ApplyBestNodeMethod()
print(" TOTAL PROFIT =", s.objective(solution))


