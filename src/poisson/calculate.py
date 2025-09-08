from poisson.grid import Grid
from poisson.charge import Charge
import numpy as np


class Calculation:
    def __init__(self, g, epsilon=1):
        self.grid = g
        self.charges = []
        self.epsilon = epsilon

    def addCharge(self, c):
        self.charges.append(c)

    def buildChargeSite(self):
        self.rho = np.zeros((self.grid.nx, self.grid.ny))
        for c in self.charges:
            pass


g = Grid(10, 10, 1, 1)
calc = Calculation(g)
calc.buildChargeSite()
