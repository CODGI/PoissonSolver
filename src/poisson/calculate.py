from poisson.charge import Charge
from poisson.grid import Grid
import numpy as np
from scipy import sparse
import matplotlib.pyplot as plt


class Calculation:
    def __init__(self, g, epsilon=1):
        self.grid = g
        self.charges = []
        self.epsilon = epsilon

    def addCharge(self, c):
        self.charges.append(c)

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
        """ """
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


g = Grid(1, 1, 0.01, 0.01)
calc = Calculation(g)
c = Charge(0.5, 0.4, "-")
c2 = Charge(0.5, 0.5, "+")
c3 = Charge(0.5, 0.6, "-")
calc.addCharge(c)
calc.addCharge(c2)
calc.addCharge(c3)
calc.buildRho()
calc.addBC(np.zeros((101, 101)))
calc.buildMatrix()
phi = calc.solve()
plt.imshow(phi, cmap="viridis")
plt.colorbar(label="Potential")
plt.savefig("field_plot.png", dpi=300, bbox_inches="tight")
