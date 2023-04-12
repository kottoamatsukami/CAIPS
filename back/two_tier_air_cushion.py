import numpy as np
from matplotlib import pyplot as plt, patches as pth
from PIL import Image


class TwoTierSolver(object):
    def __init__(self, parameters) -> None:
        self.history = []
        self.p_history = {}
        self.parameters = parameters

    def F(self, x: dict, n: int) -> np.array:
        f = np.zeros(14)
        # In point A
        f[0] = x["r1"]*np.cos(x["alpha1"]) + x["x1"] - self.parameters["Ax"]
        f[1] = x["r1"]*np.sin(x["alpha1"]) + x["y1"] - self.parameters["Ay"]
        # In point B
        f[2] = x["r2"]*np.cos(x["phi2"] + x["alpha2"]) + x["x2"] - self.parameters["Bx"]
        f[3] = x["r2"]*np.sin(x["phi2"] + x["alpha2"]) + x["y2"] - self.parameters["By"]
        # In point C
        f[4] = x["r3"]*np.cos(x["alpha3"] + x["phi3"]) + x["x3"] - x["r2"]*np.cos(x["alpha2"]) - x["x2"]
        f[5] = x["r3"]*np.sin(x["alpha3"] + x["phi3"]) + x["y3"] - x["r2"]*np.sin(x["alpha2"]) - x["y2"]
        f[6] = x["r3"]*np.cos(x["alpha3"] + x["phi3"]) + x["x3"] - x["r5"]*np.cos(x["alpha5"] + x["phi5"]) - x["x5"]
        f[7] = x["r3"]*np.sin(x["alpha3"] + x["phi3"]) + x["y3"] - x["r5"]*np.sin(x["alpha5"] + x["phi5"]) - x["y5"]
        # In point D
        f[8] = x["r1"]*np.cos(x["alpha1"] + x["phi1"]) + x["x1"] - x["r3"]*np.cos(x["alpha3"]) - x["x3"]
        f[9] = x["r1"]*np.sin(x["alpha1"] + x["phi1"]) + x["y1"] - x["r3"]*np.sin(x["alpha3"]) - x["y3"]
        f[10] = x["r1"]*np.cos(x["alpha1"] + x["phi1"]) + x["x1"] - x["r4"]*np.cos(x["alpha4"]) - x["x4"]
        f[11] = x["r1"]*np.sin(x["alpha1"] + x["phi1"]) + x["y1"] - x["r4"]*np.sin(x["alpha4"]) - x["y4"]
        # In point E
        f[12] = x["x4"] - x["x5"]
        f[13] = x["y4"] - x["r4"] + x["r5"] - x["y5"]

        # Calculating Overpressure
        return f

    def findSolution(self, vector):
        # vector = {
        # 0: Ax, 1: Ay, 2: Bx, 3: By,
        # 4: xTop, 5: yTop, 6: xBot,
        # 7: yBot, 8: rt, 9: rb,
        # 10: pt0, 11: pb0, 12: pac,
        # 13: alpha5 = 3*pi/2,
        # 14: x5 = x4,
        # 15: alpha4 = 3*Pi/2 - phi4
        # }

        # solution = {
        #  0: r1, 1: alpha1, 2: x1, 3: y1,
        #  4: r2, 5: alpha2, 6: x2, 7: y2,
        #  8: phi2,
        #  9: r3, 10: alpha3, 11: x3, 12: y3,
        #
        # }
        ...

    def makeAnimation(self, vector):
        ...

    def makePlot(self, vector):
        # init PLT
        fig, axs = plt.subplots(figsize=(5, 5))
        axs.grid(linestyle='--')
        axs.set_aspect('equal')

        # Line AB
        axs.plot(
            (self.parameters["Ax"], self.parameters["Bx"]),
            (self.parameters["Ay"], self.parameters["By"]),
            color="black"
        )

        # Convert to GIF format
        fig.savefig("saved_parameters/temp.png")
        im = Image.open("saved_parameters/temp.png")
        im.save("saved_parameters/temp.gif")



    def calculate_overpressure(self, n):
        ...