from SOLVER import *

m = Model()
m.BuildModel()
s = Solver(m)
sol = s.solve()

print()
