import numpy as np
from matplotlib import pyplot as plt, patches as pth
from PIL import Image
import back


class TwoTierSolver(object):
    def __init__(self, constants: dict) -> None:
        self.constants = constants

    def F(self, x: dict, norm=1, return_f=False) -> np.array:
        f = np.zeros(43)
        f[0] = x["r1"]*x["phi1"] - self.constants["rt"]*self.constants["phiNd1"]
        f[1] = x["r2"]*x["phi2"] - self.constants["rt"]*self.constants["phiNd2"]
        f[2] = x["r3"]*x["phi3"] - self.constants["rt"]*self.constants["phiNd3"]
        f[3] = x["r4"]*x["phi4"] + x["r5"]*x["phi5"] - self.constants["rb"]*(x["phiNd4"] + x["phiNd5"])

        f[4] = x["r1"]*np.cos(x["alpha1"]) + x["x1"] - self.constants["Ax"]
        f[5] = x["r1"]*np.sin(x["alpha1"]) + x["y1"] - self.constants["Ay"]

        f[6] = x["r2"]*np.cos(x["phi2"] + x["alpha2"]) + x["x2"] - self.constants["Bx"]
        f[7] = x["r2"]*np.sin(x["phi2"] + x["alpha2"]) + x["y2"] - self.constants["By"]

        f[8] = x["r3"]*np.cos(x["alpha3"] + x["phi3"]) + x["x3"] - x["r2"]*np.cos(x["alpha2"]) - x["x2"]
        f[9] = x["r3"]*np.sin(x["alpha3"] + x["phi3"]) + x["y3"] - x["r2"]*np.sin(x["alpha2"]) - x["y2"]
        f[10] = x["r3"]*np.cos(x["alpha3"] + x["phi3"]) + x["x3"] - x["r5"]*np.cos(self.constants["alpha5"] + x["phi5"]) - x["x5"]
        f[11] = x["r3"]*np.sin(x["alpha3"] + x["phi3"]) + x["y3"] - x["r5"]*np.sin(self.constants["alpha5"] + x["phi5"]) - x["y5"]

        f[12] = x["r1"]*np.cos(x["alpha1"] + x["phi1"]) + x["x1"] - x["r3"]*np.cos(x["alpha3"]) - x["x3"]
        f[13] = x["r1"]*np.sin(x["alpha1"] + x["phi1"]) + x["y1"] - x["r3"]*np.sin(x["alpha3"]) - x["y3"]
        f[14] = x["r1"]*np.cos(x["alpha1"] + x["phi1"]) + x["x1"] - x["r4"]*np.cos(x["alpha4"]) - x["x4"]
        f[15] = x["r1"]*np.sin(x["alpha1"] + x["phi1"]) + x["y1"] - x["r4"]*np.sin(x["alpha4"]) - x["y4"]

        f[16] = x["x4"] - x["x5"]
        f[17] = -x["r4"] + x["y5"] + x["r5"] - x["y5"]

        f[18] = x["pt"]*x["r1"]*np.sin(x["alpha1"] + x["phi1"]) - (x["pt"] - x["pb"])*x["r3"]*np.sin(x["alpha3"]) - x["pb"]*x["r4"]*np.sin(x["alpha4"])
        f[19] = -x["pt"]*x["r1"]*np.cos(x["alpha1"] + x["phi1"]) + (x["pt"] - x["pb"])*x["r3"]*np.cos(x["alpha3"]) + x["pb"]*x["r4"]*np.cos(x["alpha4"])
        f[20] = -(x["pt"] - self.constants["p"])*x["r2"]*np.sin(x["alpha2"]) + (x["pt"] - x["pb"])*x["r3"]*np.sin(x["alpha3"] + x["phi3"]) + (x["pt"] - self.constants["p"])*x["r5"]*np.sin(self.constants["alpha5"] + x["phi5"])
        f[21] = (x["pt"] - self.constants["p"])*x["r2"]*np.cos(x["alpha2"]) - (x["pt"] - x["pb"])*x["r3"]*np.cos(x["alpha3"] + x["phi3"]) - (x["pt"] - self.constants["p"])*x["r5"]*np.cos(self.constants["alpha5"] + x["phi5"])
        # f[18] = self.constants["pt"] * x["r1"] * np.sin(x["alpha1"] + x["phi1"]) - (
        #             self.constants["pt"] - self.constants["pb"]) * x["r3"] * np.sin(x["alpha3"]) - self.constants[
        #             "pb"] * x["r4"] * np.sin(x["alpha4"])
        # f[19] = -self.constants["pt"] * x["r1"] * np.cos(x["alpha1"] + x["phi1"]) + (
        #             self.constants["pt"] - self.constants["pb"]) * x["r3"] * np.cos(x["alpha3"]) + self.constants[
        #             "pb"] * x["r4"] * np.cos(x["alpha4"])
        # f[20] = -(self.constants["pt"] - self.constants["p"]) * x["r2"] * np.sin(x["alpha2"]) + (
        #             self.constants["pt"] - self.constants["pb"]) * x["r3"] * np.sin(x["alpha3"] + x["phi3"]) + (
        #                     self.constants["pt"] - self.constants["p"]) * x["r5"] * np.sin(
        #     self.constants["alpha5"] + x["phi5"])
        # f[21] = (self.constants["pt"] - self.constants["p"]) * x["r2"] * np.cos(x["alpha2"]) - (
        #             self.constants["pt"] - self.constants["pb"]) * x["r3"] * np.cos(x["alpha3"] + x["phi3"]) - (
        #                     self.constants["pt"] - self.constants["p"]) * x["r5"] * np.cos(
        #     self.constants["alpha5"] + x["phi5"])

        f[22] = x["pb"]*x["r4"] - (x["pb"] - self.constants["p"])*x["r5"]
        f[23] = x["alpha4"] - 3*np.pi/2 + x["phi4"]
        f[24] = self.constants["alpha5"] - 3*np.pi/2


        # f[0] = 5.001905970 - x["phiNd4"] - x["phiNd5"]
        # f[1] = 3*np.pi/2 - x["phi4"] - x["alpha4"]
        # f[2] = x["r1"] * x["phi1"] - self.constants["rt"] * self.constants["phiNd1"]
        # f[3] = x["r2"] * x["phi2"] - self.constants["rt"] * self.constants["phiNd2"]
        # f[4] = x["r3"] * x["phi3"] - self.constants["rt"] * self.constants["phiNd3"]
        # f[5] = x["r4"] * x["phi4"] + x["r5"] * x["phi5"] - self.constants["rb"]*(x["phiNd4"] + x["phiNd5"])
        # f[6] = x["r1"] * np.cos(x["alpha1"]) + x["x1"] - self.constants["Ax"]
        # f[7] = x["r1"] * np.sin(x["alpha1"]) + x["y1"] - self.constants["Ay"]
        # f[8] = x["r2"] * np.cos(x["phi2"] + x["alpha2"]) + x["x2"] - self.constants["Bx"]
        # f[9] = x["r2"] * np.sin(x["phi2"] + x["alpha2"]) + x["y2"] - self.constants["By"]
        # f[10] = x["r3"] * np.cos(x["alpha3"] + x["phi3"]) + x["x3"] - x["r2"]*np.cos(x["alpha2"]) - x["x2"]
        # f[11] = x["r3"] * np.sin(x["alpha3"] + x["phi3"]) + x["y3"] - x["r2"]*np.sin(x["alpha2"]) - x["y2"]
        # f[12] = x["r3"] * np.cos(x["alpha3"] + x["phi3"]) + x["x3"] - x["r5"]*np.cos(self.constants["alpha5"] + x["phi5"]) - x["x5"]
        # f[13] = x["r3"] * np.sin(x["alpha3"] + x["phi3"]) + x["y3"] - x["r5"]*np.sin(self.constants["alpha5"] + x["phi5"]) - x["y5"]
        # f[14] = x["r1"] * np.cos(x["alpha1"] + x["phi1"]) + x["x1"] - x["r3"]*np.cos(x["alpha3"]) - x["x3"]
        # f[15] = x["r1"] * np.sin(x["alpha1"] + x["phi1"]) + x["y1"] - x["r3"]*np.sin(x["alpha3"]) - x["y3"]
        # f[16] = x["r1"] * np.cos(x["alpha1"] + x["phi1"]) + x["x1"] - x["r4"]*np.cos(x["alpha4"]) - x["x4"]
        # f[17] = x["r1"] * np.sin(x["alpha1"] + x["phi1"]) + x["y1"] - x["r4"]*np.sin(x["alpha4"]) - x["y4"]
        # f[18] = x["x4"] - x["x5"]
        # f[19] = x["y4"] - x["r4"] - x["y5"] + x["r5"]
        # f[20] = x["pt"]*x["r1"]*np.sin(x["alpha1"] + x["phi1"]) - (x["pt"] - x["pb"])*x["r3"]*np.sin(x["alpha3"]) - x["pb"]*x["r4"]*np.sin(x["alpha4"])
        # f[21] = x["pt"]*x["r1"]*np.cos(x["alpha1"] + x["phi1"]) - (x["pt"] - x["pb"])*x["r3"]*np.cos(x["alpha3"]) - x["pb"]*x["r4"]*np.cos(x["alpha4"])
        # f[22] = (x["pt"] - self.constants["p"])*x["r2"]*np.sin(x["alpha2"]) - (x["pt"] - x["pb"])*x["r3"]*np.sin(x["alpha3"] + x["phi3"]) - (x["pb"] - self.constants["p"])*x["r5"]*np.sin(self.constants["alpha5"] + x["phi5"])
        # f[23] = (x["pt"] - self.constants["p"])*x["r2"]*np.cos(x["alpha2"]) - (x["pt"] - x["pb"])*x["r3"]*np.cos(x["alpha3"] + x["phi3"]) - (x["pb"] - self.constants["p"])*x["r5"]*np.cos(self.constants["alpha5"] + x["phi5"])
        # f[24] = x["pb"]*x["r4"] - (x["pb"] - self.constants["p"])*x["r5"]

        for i in range(len(f)):
            f[i] = f[i] * f[i]

        if return_f:
            return np.linalg.norm(f, norm), f
        return np.linalg.norm(f, norm)

    def findSolution(self, vector, norm=2):
        for i in range(1, 5000):
            gradient = {parameter: 0 for parameter in vector}
            for parameter in vector:
                epsvector = vector.copy()
                epsvector[parameter] += back.EPS
                gradient[parameter] = (self.F(epsvector, norm) - self.F(vector, norm))/back.EPS

            for parameter in vector:
                vector[parameter] = vector[parameter] - back.OMI * gradient[parameter]

            print(self.F(vector, norm))
        return vector


    def makeAnimation(self, vector):
        ...

    def makePlot(self, vector, rotate=False):
        # init PLT
        fig, axs = plt.subplots(figsize=(5, 5))
        axs.grid(linestyle='--')
        axs.set_aspect('equal')

        # Line AB
        axs.plot(
            (constants["Ax"], constants["Bx"]),
            (constants["Ay"], constants["By"]),
            color="black"
        )

        arcad = pth.Arc(
            xy=(vector["x1"], vector["y1"]),
            width=vector["r1"] * 2,
            height=vector["r1"] * 2,
            angle=(180 - vector["alpha1"]) * 180 / np.pi,
            theta1=(180 - vector["alpha1"]) * 180 / np.pi,
            theta2=(vector["phi1"] - (180 - vector["alpha1"])) * 180 / np.pi,

        )
        axs.add_patch(arcad)
        arccb = pth.Arc(
            xy=(vector["x2"], vector["y2"]),
            width=vector["r2"] * 2,
            height=vector["r2"] * 2,
            angle=(180 - vector["alpha2"]) * 180 / np.pi,
            theta1=(180 - vector["alpha2"]) * 180 / np.pi,
            theta2=(vector["phi2"] - (180 - vector["alpha2"])) * 180 / np.pi,

        )
        axs.add_patch(arccb)
        arcdc = pth.Arc(
            xy=(vector["x3"], vector["y3"]),
            width=vector["r3"] * 2,
            height=vector["r3"] * 2,
            angle=(180 - vector["alpha3"]) * 180 / np.pi,
            theta1=(180 - vector["alpha3"]) * 180 / np.pi,
            theta2=(vector["phi3"] - (180 - vector["alpha3"])) * 180 / np.pi,

        )
        axs.add_patch(arcdc)
        arcde = pth.Arc(
            xy=(vector["x4"], vector["y4"]),
            width=vector["r4"] * 2,
            height=vector["r4"] * 2,
            angle=(-45 - vector["alpha4"]) * 180 / np.pi,
            theta1=(180 - vector["alpha4"]) * 180 / np.pi,
            theta2=(vector["phi4"] - (180 - vector["alpha4"])) * 180 / np.pi,

        )
        axs.add_patch(arcde)
        arcec = pth.Arc(
            xy=(vector["x5"], vector["y5"]),
            width=vector["r5"] * 2,
            height=vector["r5"] * 2,
            angle=(-45 - constants["alpha5"]) * 180 / np.pi,
            theta1=(180 - constants["alpha5"]) * 180 / np.pi,
            theta2=(vector["phi5"] - (180 - constants["alpha5"])) * 180 / np.pi,

        )
        axs.add_patch(arcec)

        plt.show()

        # Convert to GIF format
        fig.savefig("saved_parameters/temp.png")
        im = Image.open("saved_parameters/temp.png")
        if rotate:
            im = im.rotate(180)
        im.save("saved_parameters/temp.gif")


    def calculate_overpressure(self, n):
        ...


constants = {
    "p": 2000,
    "Ax": 0,
    "Ay": 1.9,
    "Bx": 0.6,
    "By": 1.3,
    "xTop": 0,
    "yTop": 1.3,
    "xBot": 0,
    "yBot": 0.44,
    "rt": 0.6,
    "rb": 0.38,
    "pt0": 24000,
    "pb0": 8000,
    "phiNd1": 2.753364902,
    "phiNd2": 1.182568575,
    "phiNd3": 0.776455503,
    "alpha5": 3*np.pi/2,
}
vector = {
    "phiNd4": 0.5,
    "phiNd5": 0.5,
    "x1": constants["xTop"],
    "x2": constants["xTop"],
    "x3": constants["xTop"],
    "x4": constants["xBot"],
    "x5": constants["xBot"],
    "y1": constants["yTop"],
    "y2": constants["yTop"],
    "y3": constants["yTop"],
    "y4": constants["yBot"],
    "y5": constants["yBot"],
    "alpha1": 0.5,
    "alpha2": 0.5,
    "alpha3": 0.5,
    "alpha4": 0.5,
    "phi1": 0.5,
    "phi2": 0.5,
    "phi3": 0.5,
    "phi4": 0.5,
    "phi5": 0.5,
    "r1": constants["rt"],
    "r2": constants["rt"],
    "r3": constants["rt"],
    "r4": constants["rb"],
    "r5": constants["rb"],
    "pt": 1,
    "pb": 1,
}
solver = TwoTierSolver(constants=constants)
vector = solver.findSolution(vector=vector)
print(solver.F(vector), vector)

TwoTierSolver(constants=constants).makePlot(vector)