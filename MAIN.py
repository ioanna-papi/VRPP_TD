from SOLVER import *

# 1ο Ερώτημα
m = Model()
m.BuildModel()

# 2ο Ερώτημα
s = Solver(m)
solution = s.ApplyBestNodeMethod()
print(" TOTAL PROFIT =", s.objective(solution))


