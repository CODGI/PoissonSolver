from grid import Grid


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
