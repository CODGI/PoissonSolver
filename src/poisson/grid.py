import numpy as np


class grid:
    def __init__(self, Lx, Ly, dx, dy):
        self.Lx = Lx
        self.Ly = Ly
        self.dx = dx
        self.dy = dy
        self.initGrid()

    def initGrid(self):
        self.potential = np.empty((round(self.Lx / self.dx), round(self.Ly / self.dy)))
        print(self.potential.shape)

    def __str__(self):
        return f"This grid has lengths of Lx = {self.Lx}, Ly = {self.Ly} and resolutions dx = {self.dx}, dy={self.dy}."


g = grid(10, 10, 1, 1)
print(g)
