import numpy as np
from matplotlib import pyplot as plt, patches as pth
from PIL import Image


class TwoTierSolver(object):
    def __init__(self) -> None:
        None

    def F(self, x: dict, norm=1) -> np.array:
        f = np.zeros(43)
        f[0] = 2000 - x["p"]          # p = 2000 Pa
        f[1] = 0 - x["Ax"]            # Ax = 0
        f[2] = 0.95 * 2 - x["Ay"]     # Ay = 0.95 * 2
        f[3] = 0.30 * 2 - x["Bx"]     # Bx = 0.30 * 2
        f[4] = 0.65 * 2 - x["By"]     # By = 0.65 * 2
        f[5] = 0 - x["xTop"]          # xTop = 0
        f[6] = 0.65 * 2 - x["yTop"]   # yTop = 0.65 * 2
        f[7] = 0 - x["xBot"]          # xBot = 0
        f[8] = 0.22 * 2 - x["yBot"]   # yBot = 0.22 * 2
        f[9] = 0.30 * 2 - x["rt"]     # rt = 0.30 * 2
        f[10] = 0.19 * 2 - x["rb"]    # rb = 0.19 * 2

        f[11] = 12000 * 2 - x["pt0"]  # pt0 = 12000 * 2
        f[12] = 4000 * 2 - x["pb0"]   # pb0 = 4000 * 2
        f[13] = 2.753364902 - x["phiNd1"]  # phiNd1 = 2.753364902
        f[14] = 1.182568575 - x["phiNd2"]  # phiNd2 = 1.182568575
        f[15] = 0.776455503 - x["phiNd3"]  # phiNd3 = 0.776455030
        f[16] = 5.001905970 - x["phiNd4"] - x["phiNd5"]  # phiNd4 + phiNd5 = 5.001905970
        f[17] = 3*np.pi/2 - x["alpha5"]  # alpha5 = 3/2 * pi
        f[18] = x["x5"] - x["x4"]  # x5 = x4
        f[19] = 3*np.pi/2 - x["phi4"] - x["alpha4"]  # alpha4 = 3/2 * pi - phi4

        f[20] = x["r1"] * x["phi1"] - x["rt"] * x["phiNd1"]
        f[21] = x["r2"] * x["phi2"] - x["rt"] * x["phiNd2"]
        f[22] = x["r3"] * x["phi3"] - x["rt"] * x["phiNd3"]
        f[23] = x["r4"] * x["phi4"] + x["r5"] * x["phi5"] - x["rb"]*(x["phiNd4"] + x["phiNd5"])

        f[24] = x["r1"] * np.cos(x["alpha1"]) + x["x1"] - x["Ax"]
        f[25] = x["r1"] * np.sin(x["alpha1"]) + x["y1"] - x["Ay"]
        f[26] = x["r2"] * np.cos(x["phi2"] + x["alpha2"]) + x["x2"] - x["Bx"]
        f[27] = x["r2"] * np.sin(x["phi2"] + x["alpha2"]) + x["y2"] - x["By"]

        f[28] = x["r3"] * np.cos(x["alpha3"] + x["phi3"]) + x["x3"] - x["r2"]*np.cos(x["alpha2"]) - x["x2"]
        f[29] = x["r3"] * np.sin(x["alpha3"] + x["phi3"]) + x["y3"] - x["r2"]*np.sin(x["alpha2"]) - x["y2"]
        f[30] = x["r3"] * np.cos(x["alpha3"] + x["phi3"]) + x["x3"] - x["r5"]*np.cos(x["alpha5"] + x["phi5"]) - x["x5"]
        f[31] = x["r3"] * np.sin(x["alpha3"] + x["phi3"]) + x["y3"] - x["r5"]*np.sin(x["alpha5"] + x["phi5"]) - x["y5"]

        f[32] = x["r1"] * np.cos(x["alpha1"] + x["phi1"]) + x["x1"] - x["r3"]*np.cos(x["alpha3"]) - x["x3"]
        f[33] = x["r1"] * np.sin(x["alpha1"] + x["phi1"]) + x["y1"] - x["r3"]*np.sin(x["alpha3"]) - x["y3"]
        f[34] = x["r1"] * np.cos(x["alpha1"] + x["phi1"]) + x["x1"] - x["r4"]*np.cos(x["alpha4"]) - x["x4"]
        f[35] = x["r1"] * np.sin(x["alpha1"] + x["phi1"]) + x["y1"] - x["r4"]*np.sin(x["alpha4"]) - x["y4"]

        f[36] = x["x4"] - x["x5"]
        f[37] = x["y4"] - x["r4"] - x["y5"] + x["r5"]

        f[38] = x["pt"]*x["r1"]*np.sin(x["alpha1"] + x["phi1"]) - (x["pt"] - x["pb"])*x["r3"]*np.sin(x["alpha3"]) - x["pb"]*x["r4"]*np.sin(x["alpha4"])
        f[39] = x["pt"]*x["r1"]*np.cos(x["alpha1"] + x["phi1"]) - (x["pt"] - x["pb"])*x["r3"]*np.cos(x["alpha3"]) - x["pb"]*x["r4"]*np.cos(x["alpha4"])

        f[40] = (x["pt"] - x["p"])*x["r2"]*np.sin(x["alpha2"]) - (x["pt"] - x["pb"])*x["r3"]*np.sin(x["alpha3"] + x["phi3"]) - (x["pb"] - x["p"])*x["r5"]*np.cos(x["alpha5"] + x["phi5"])
        f[41] = (x["pt"] - x["p"])*x["r2"]*np.cos(x["alpha2"]) - (x["pt"] - x["pb"])*x["r3"]*np.cos(x["alpha3"] + x["phi3"]) - (x["pb"] - x["p"])*x["r5"]*np.cos(x["alpha5"] + x["phi5"])

        f[42] = x["pb"]*x["r4"] - (x["pb"] - x["p"])*x["r5"]
        return np.linalg.norm(f, norm)

    def findSolution(self, vector, norm=2):
        eps = 1e-6
        omi = 1e-6
        for i in range(1, 5000):
            gradient = {parameter: 0 for parameter in vector}
            for parameter in vector:
                epsvector = vector.copy()
                epsvector[parameter] += eps
                gradient[parameter] = (self.F(epsvector, norm) - self.F(vector, norm))/eps

            for parameter in vector:
                vector[parameter] = vector[parameter] - omi * gradient[parameter]
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
            (self.parameters["Ax"], self.parameters["Bx"]),
            (self.parameters["Ay"], self.parameters["By"]),
            color="black"
        )

        # Convert to GIF format
        fig.savefig("saved_parameters/temp.png")
        im = Image.open("saved_parameters/temp.png")
        if rotate:
            im = im.rotate(180)
        im.save("saved_parameters/temp.gif")



    def calculate_overpressure(self, n):
        ...


solver = TwoTierSolver()
vector = {
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
    "phiNd4": 0.5,
    "phiNd5": 0.5,

    "x1": 1,
    "x2": 1,
    "x3": 1,
    "x4": 1,
    "x5": 1,

    "y1": 1,
    "y2": 1,
    "y3": 1,
    "y4": 1,
    "y5": 1,

    "alpha1": 0.5,
    "alpha2": 0.5,
    "alpha3": 0.5,
    "alpha4": 0.5,
    "alpha5": 3*np.pi/2,

    "phi1": 0.5,
    "phi2": 0.5,
    "phi3": 0.5,
    "phi4": 0.5,
    "phi5": 0.5,

    "r1": 2,
    "r2": 2,
    "r3": 2,
    "r4": 2,
    "r5": 2,

    "pt": 1,
    "pb": 1,
}
print(solver.findSolution(vector))
