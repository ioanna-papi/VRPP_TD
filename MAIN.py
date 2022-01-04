from VRP import *
from SOLVER import *

m = Model()
m.BuildModel()
s = Solver(m)
