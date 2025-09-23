from grid import Grid
from charge import Charge
import numpy as np


class BCGenerator:
    def __init__(self, grid):
        self.grid = grid

    def getBoundaries(self):
        raise NotImplementedError("Subclass must implement this function!")


class ConstantBoundaries(BCGenerator):
    def __init__(self, grid, constant):
        super().__init__(grid)
        self.constant = constant

    def getBoundaries(self):
        # I think there is an error here; dx and dy are not taken into account!
        self.bc = self.grid.potential.copy()
        self.bc[0, :] = 2 * self.constant
        self.bc[-1, :] = 2 * self.constant
        self.bc[:, 0] = 2 * self.constant
        self.bc[:, -1] = 2 * self.constant
        self.bc[0, 0] = 4 * self.constant
        self.bc[0, -1] = 4 * self.constant
        self.bc[-1, 0] = 4 * self.constant
        self.bc[-1, -1] = self.constant
        return self.bc


class FreeSpaceboundaries(BCGenerator):
    def __init__(self, grid, charges):
        super().__init__(grid)
        self.charges = charges

    def getBoundaries(self):
        self.bc = self.grid.potential.copy()
        for i in range(self.grid.nx):
            for c in self.charges:
                r1 = np.sqrt((i * self.grid.dx - c.x) ** 2 + (c.y) ** 2)
                r2 = np.sqrt((i * self.grid.dx - c.x) ** 2 + (self.grid.Ly - c.y) ** 2)
                if c.sign == "+":
                    self.bc[i, 0] += np.log(r1) / self.grid.dy**2
                    self.bc[i, -1] += np.log(r2) / self.grid.dy**2
                if c.sign == "-":
                    self.bc[i, 0] -= np.log(r1) / self.grid.dy**2
                    self.bc[i, -1] -= np.log(r2) / self.grid.dy**2
        for i in range(self.grid.ny):
            for c in self.charges:
                r1 = np.sqrt((c.x) ** 2 + (i * self.grid.dy - c.y) ** 2)
                r2 = np.sqrt((c.x - self.grid.Lx) ** 2 + (i * self.grid.dy - c.y) ** 2)
                if c.sign == "+":
                    self.bc[0, i] += np.log(r1) / self.grid.dx**2
                    self.bc[-1, i] += np.log(r2) / self.grid.dx**2
                if c.sign == "-":
                    self.bc[0, i] -= np.log(r1) / self.grid.dx**2
                    self.bc[-1, i] -= np.log(r2) / self.grid.dx**2
        return self.bc / (2 * np.pi)
