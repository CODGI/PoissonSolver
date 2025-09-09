from poisson.grid import Grid
from poisson.charge import Charge
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

    def addBC(self, b):
        """
        Boundary conditions are implemented as arrays of size 2*Nx+2*Ny+4 and go clockwise from the edge (0,Ly) around the domain.
        At the moment the bc just default to 0.
        TODO: Maybe check continuity of bc=
        """
        if b.shape == (2 * (self.grid.nx + self.grid.ny) + 4,):
            self.b = b
        else:
            raise ValueError("Boundary conditions don't match domain!")
        self.bc = np.zeros(self.grid.nx * self.grid.ny)
        """
        # arounddd top
        self.bc[: self.grid.nx] += b[1 : self.grid.nx + 1] / (
            self.grid.dy**2
        )  # Top row
        self.bc[:: self.grid.nx] += b[-1 : -1 - self.grid.ny] / (
            self.grid.dx**2
        )  # left column
        self.bc[self.grid.nx - 1 :: self.grid.nx] += b[
            self.grid.nx + 2 : self.grid.nx + 2 + self.grid.ny
        ] / (
            self.grid.dx**2
        )  # right column
        self.bc[self.grid.ny * (self.grid.nx - 1) :: -1] += b[
            self.grid.nx + self.grid.ny + 3 : 2 * self.grid.nx + self.grid.ny + 3
        ] / (
            self.grid.dy**2
        )  # bottom row
        print(self.bc)
            """

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
        self.M = (
            sparse.diags(mainDiag, 0)
            + sparse.diags(xDiag, 1)
            + sparse.diags(xDiag, -1)
            + sparse.diags(yDiag, self.grid.nx)
            + sparse.diags(yDiag, -self.grid.nx)
        )

    def solve(self):
        x = sparse.linalg.spsolve(self.M, self.rho_vec)
        return x.reshape((self.grid.nx, self.grid.ny))


g = Grid(10, 10, 0.1, 0.1)
calc = Calculation(g)
c = Charge(4, 4, "+")
c2 = Charge(8, 8, "+")
calc.addCharge(c)
calc.addCharge(c2)
calc.buildRho()
b = np.zeros(2 * (101 + 101) + 4)
calc.addBC(b)
calc.buildMatrix()
phi = calc.solve()
# plt.imsave("phi.png", phi, cmap="viridis")
plt.imshow(phi, cmap="viridis")
plt.colorbar(label="Potential")
plt.savefig("field_plot.png", dpi=300, bbox_inches="tight")
