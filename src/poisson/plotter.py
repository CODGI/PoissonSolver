import matplotlib.pyplot as plt
import numpy as np
from generateEfields import fieldCalculator
from grid import Grid


class Plotter:
    def __init__(self, grid, phi):
        self.dx, self.dy, self.Lx, self.Ly = grid.dx, grid.dy, grid.Lx, grid.Ly
        self.grid = grid
        self.phi = phi

    def plotSomething(self, field, title, labelOfColorBar):
        plt.figure()
        plt.imshow(field.transpose(), extent=[0, self.Lx, 0, self.Ly])
        plt.title(title)
        plt.colorbar(label=labelOfColorBar)
        plt.savefig(title + ".png", dpi=300, bbox_inches="tight")
        plt.clf()

    def plot(self):
        calculator = fieldCalculator(self.phi, self.dx, self.dy, self.grid)
        Ex = calculator.calc_Ex()
        Ey = calculator.calc_Ey()
        self.plotSomething(self.phi, "Potential", "")
        self.plotSomething(Ex, "Ex", "")
        self.plotSomething(Ey, "Ey", "")
        E = np.sqrt(np.abs(Ex) ** 2 + np.abs(Ey) ** 2)
        self.plotSomething(E, "abs(E)", "")
