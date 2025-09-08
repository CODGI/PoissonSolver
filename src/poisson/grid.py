import numpy as np


class Grid:
    def __init__(self, Lx, Ly, dx, dy, includeEnd=True):
        if dx <= 0 or dy <= 0:
            raise ValueError("dx and dy must be positive")
        if Lx <= 0 or Ly <= 0:
            raise ValueError("Lx and Ly must be positive")

        self.Lx, self.Ly = float(Lx), float(Ly)
        self.dx, self.dy = float(dx), float(dy)
        self.includeEnd = includeEnd

        if includeEnd:
            self.nx = int(np.floor(self.Lx / self.dx)) + 1
            self.ny = int(np.floor(self.Ly / self.dy)) + 1
            self.x = np.linspace(0.0, self.Lx, self.nx)
            self.y = np.linspace(0.0, self.Ly, self.ny)
        else:
            self.nx = int(np.floor(self.Lx / self.dx))
            self.ny = int(np.floor(self.Ly / self.dy))
            self.x = np.arange(0.0, self.nx) * dx
            self.y = np.arange(0.0, self.ny) * dy

        self.potential = np.zeros((self.nx, self.ny), dtype=float)

    def initGrid(self):
        self.potential = np.empty((round(self.Lx / self.dx), round(self.Ly / self.dy)))
        print(self.potential.shape)

    def __str__(self):
        return (
            f"This grid has lengths of Lx = {self.Lx}, Ly = {self.Ly} \n"
            f"and resolutions dx = {self.dx}, dy={self.dy}.\n"
            f"Shape = ({self.nx},{self.ny})"
        )
