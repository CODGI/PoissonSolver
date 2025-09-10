import numpy as np
from poisson.grid import Grid


class calculateFields:
    def __init(self, phi, dx, dy, grid):
        self.dx, self.dy = dx, dy
        self.grid = grid
        self.phi = phi

    def calc_Ex(self):
        Ex = np.zeros((self.grid.nx, self.grid.ny))
        Ex[1:-1, :] = (self.phi[2:, :] - self.phi[:-2, :]) / (2 * self.grid.dx)
        Ex[0, :] = (self.phi[1, :] - self.phi[0, :]) / (self.grid.dx)
        Ex[-1, :] = (self.phi[-1, :] - self.phi[-2, :]) / (self.grid.dx)
        return Ex

    def calc_Ey(self):
        Ey = np.zeros((self.grid.nx, self.grid.ny))
        Ey[:, 1:-1] = (self.phi[:, 2:] - self.phi[:, :-2]) / (2 * self.grid.dy)
        Ey[:, 0] = (self.phi[:, 1] - self.phi[:, 0]) / (self.grid.dy)
        Ey[:, -1] = (self.phi[:, -1] - self.phi[:, -2]) / (self.grid.dy)
        return Ey
