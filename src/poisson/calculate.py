from poisson.charge import Charge
from poisson.grid import Grid
import numpy as np
from bc_generators import ConstantBoundaries, FreeSpaceboundaries
from scipy import sparse
from plotter import Plotter


class Calculation:
    def __init__(self, g, epsilon=1):
        self.grid = g
        self.charges = []
        self.epsilon = epsilon

    def addCharge(self, c):
        self.charges.append(c)

    def getCharges(self):
        return self.charges

    def addCharges(self, positions, signs):
        if len(positions) == 0 or len(signs) == 0:
            raise ValueError("Neitehr positions nor charges can be empty")
        if len(positions) != len(signs):
            raise ValueError("Must have same size.")
        for (x, y), s in zip(positions, signs):
            c = Charge(x + self.grid.dx / 10, y + self.grid.dy / 10, s)
            self.addCharge(c)

    def buildRho(self):
        self.rho = np.zeros((self.grid.nx, self.grid.ny))
        for c in self.charges:
            if (self.grid.dx < c.x < self.grid.Lx) and (
                self.grid.dy < c.y < self.grid.Ly
            ):
                nx = int(np.floor(c.x / self.grid.dx))
                ny = int(np.floor(c.y / self.grid.dy))
                if c.sign == "+":
                    self.rho[nx, ny] = 1
                else:
                    self.rho[nx, ny] = -1
            else:
                continue
        self.rho_vec = self.rho.flatten() / self.epsilon

    def addBC(self, bc):
        self.bc = bc.flatten()

    def buildMatrix(self):
        mainDiag = (
            -2
            * ((1 / self.grid.dx) ** 2 + (1 / self.grid.dy) ** 2)
            * np.ones((self.grid.nx * self.grid.ny))
        )
        xDiag = (1 / self.grid.dx) ** 2 * np.ones((self.grid.nx * self.grid.ny) - 1)
        xDiag[self.grid.nx - 1 :: self.grid.nx] = 0
        yDiag = (1 / self.grid.dy) ** 2 * np.ones(
            (self.grid.nx * self.grid.ny) - self.grid.nx
        )
        self.M = sparse.diags(
            [mainDiag, xDiag, xDiag, yDiag, yDiag],
            [0, 1, -1, self.grid.nx, -self.grid.nx],
        )

    def solve(self):
        x = sparse.linalg.spsolve(self.M, self.rho_vec - self.bc)
        return x.reshape((self.grid.nx, self.grid.ny))


Lx, Ly, dx, dy = 1, 1, 0.01, 0.01
g = Grid(Lx, Ly, dx, dy)
calc = Calculation(g)
calc.addCharges([(0.5, 0.4), (0.5, 0.5), (0.6, 0.5)], ["-", "+", "-"])
# calc.addCharges([(0.5, 0.5)], ["+"])
calc.buildRho()
bc = ConstantBoundaries(g, 0).getBoundaries()
# bc2 = FreeSpaceboundaries(g, calc.charges).getBoundaries()
calc.addBC(bc)
calc.buildMatrix()
phi = calc.solve()
p = Plotter(g, phi)
p.plot()
