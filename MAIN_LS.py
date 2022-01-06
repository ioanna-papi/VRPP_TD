from LOCAL_SEARCH import *

# 1ο Ερώτημα
m = Model()
m.BuildModel()

# 2ο Ερώτημα
s = Solver(m)
solution = s.ApplyBestNodeMethod()
print(" TOTAL PROFIT =", s.objective(solution))

print("Local Search")
solution2 = s.LocalSearch(1)
print(s.objective(solution2))
print()
