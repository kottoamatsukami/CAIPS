from turtle import circle

import numpy as np
from matplotlib import pyplot as plt, patches as pth
from collections import namedtuple
from PIL import Image
from back import __init__ as init

# In point E
X5_0 = 0.0
Y5_0 = 0.0

class TwoTierSolver(object):
    def __init__(self, parameters) -> None:
        self.history = []
        self.p_history = {}
        self.parameters = parameters

    global X5_0, Y5_0
    @staticmethod
    def getCentres(p1: tuple, p2: tuple, r: float):
        if r == 0:
            raise ValueError("Radius of zero")
        if p1 == p2:
            raise ValueError("Coincident points")
        dx, dy = p1[0] - p2[0], p1[1] - p2[1]
        # Distance between points
        q = np.sqrt(dx**2 + dy**2)
        if q > 2.0*r:
            raise ValueError("Separation of point > diameter")
        x3, y3 = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        # Distance along the mirror line
        d = np.sqrt(r**2 + (q / 2)**2)

        c1 = [(x3 - d*dy/q),
              y3 + d*dx/q]
        # c2 = [x3 + d*dy/q,
        #       y3 - d*dx/q]
        return c1#, c2

    @staticmethod
    def getIntersections(cent1: dict, cent2: dict, r1: float, r2: float) -> dict:
        d = np.sqrt((cent2["x"] - cent1["x"])**2 + (cent2["y"] - cent1["y"])**2)

        if d > r1 + r2:
            return None
        if d < abs(r1 - r2):
            return None
        if d == 0 and r1 == r2:
            return None
        else:
            a = (r1**2 - r2**2 + d**2) / (2*d)
            h = np.sqrt(r1**2 - a**2)
            x2 = cent1["x"] + a*(cent2["x"] - cent1["x"]) / d
            y2 = cent1["y"] + a*(cent2["y"] - cent1["y"]) / d
            x3 = x2 + h*(cent2["y"] - cent1["y"]) / d
            y3 = y2 - h*(cent2["x"] - cent1["x"]) / d

            x4 = x2 - h*(cent2["y"] - cent1["y"]) / d
            y4 = y2 + h*(cent2["x"] - cent1["x"]) / d

            return {"x3": x3, "y3": y3, "x4": x4, "y4": y4}

    def formInitialVector(self, parameters: dict) -> dict:
        # ---------------------------------------
        # parameters = {
        # 0: Ax, 1: Ay, 2: Bx, 3: By,
        # 4: xt, 5: yt, 6: xb, 7: yb,
        # 8: rt, 9: rb, 10: pt0, 11: pb0,
        # 12: alpha5, 13: alpha4
        #
        # }
        # ---------------------------------------
        intersects = self.getIntersections({"x": parameters["xt"], "y": parameters["yt"]},
                                          {"x": parameters["xb"], "y": parameters["yb"]},
                                          parameters["rt"], parameters["rb"])
        vector = {}
        vector["x1"] = self.parameters["Ax"]
        vector["y1"] = self.parameters["Ay"]
        vector["x2"] = self.parameters["Bx"]
        vector["y2"] = self.parameters["By"]
        vector["x3"] = intersects["x3"]
        vector["y3"] = intersects["y3"]
        vector["x4"] = intersects["x4"]
        vector["y4"] = intersects["y4"]
        # vector["x5"] = # X5_0 or? vector["x4"]
        # vector["y5"] = # Y5_0 or? ...

        vector["r1"] = vector["r2"] = vector["r3"] = parameters["rt"]
        vector["r4"] = vector["r5"] = parameters["rb"]

        vector["phi1"] = init.PHI1ND
        vector["phi2"] = init.PHI2ND
        vector["phi3"] = init.PHI3ND
        # vector["phi4"] =
        # vector["phi5"] =

        vector["alpha1"] = np.pi - np.arccos(abs(parameters["xt"] - self.parameters["Ax"]) / vector["rt"])
        vector["alpha2"] = np.pi - np.arccos(abs(parameters["xt"] - self.parameters["Bx"]) / vector["rt"])
        vector["alpha3"] = np.pi - np.arccos(abs(parameters["xt"] - intersects["x3"]) / vector["rt"])
        # vector["alpha4"] = # np.pi - np.arccos(abs(parameters["xb"] - intersects["x4"]) / parameters["rb"]) or? vector["phi4"]
        vector["alpha5"] = 3*np.pi / 2
        # vector[0]

        # vector = {
        # 0: x1, 1: y1, 2: r1, 3: phi1, 4: alpha1,
        # 5: x2, 6: y2, 7: r2, 8: phi2, 9: alpha2,
        # 10: x3, 11: y3, 12: r3, 13: phi3, 14: alpha3,
        # 15: x4, 16: y4, 17: r4, 18: phi4, 19: alpha4,
        # 20: x5, 21: y5, 22: r5, 23: phi5, 24: alpha5 = parameters["alpha5"]

    def F(self, x: dict, n: int) -> np.array:
        f = np.zeros(19)
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
        # In point D
        f[14] = init.PRESSURE_TOP*x["r1"]*np.sin(x["alpha1"] + x["phi1"]) - (init.PRESSURE_TOP-init.PRESSURE_BOT)*x["r3"]*np.sin(x["alpha3"]) \
                - init.PRESSURE_BOT*x["r4"]*np.sin(x["alpha4"])
        f[15] = -init.PRESSURE_TOP*x["r1"]*np.cos(x["alpha1"] + x["phi1"]) + (init.PRESSURE_TOP-init.PRESSURE_BOT)*x["r3"]*np.cos(x["alpha3"]) \
                + init.PRESSURE_BOT*x["r4"]*np.cos(x["alpha4"])
        # In point C
        f[16] = -(init.PRESSURE_TOP - init.PRESSURE)*x["r2"]*np.sin(x["alpha2"]) + (init.PRESSURE_TOP - init.PRESSURE_BOT)*x["r3"]*np.sin(x["alpha3"] + x["phi3"]) \
                + (init.PRESSURE_BOT - init.PRESSURE)*x["r5"]*np.cos(x["alpha5"] + x["phi5"])
        f[17] = (init.PRESSURE_TOP - init.PRESSURE)*x["r2"]*np.cos(x["alpha2"]) - (init.PRESSURE_TOP - init.PRESSURE_BOT)*x["r3"]*np.cos(x["phi3"] + x["alpha3"]) \
                - (init.PRESSURE_BOT - init.PRESSURE)*x["r5"]*np.cos(x["alpha5"] + x["phi5"])
        # In point E
        f[18] = x["pb0"]*x["r4"] - (x["pb0"] - init.PRESSURE)*x["r5"]
        # Preservation of length
        f[19] = x["r1"]*x["phi1"] - self.parameters["Rt"]*self.parameters["phi1nd"]
        f[20] = x["r2"]*x["phi2"] - self.parameters["Rt"]*self.parameters["phi2nd"]
        f[21] = x["r3"]*x["phi3"] - self.parameters["Rt"]*self.parameters["phi3nd"]
        f[22] = x["r4"]*x["phi4"] + x["r5"]*x["phi5"] - self.parameters["Rb"]*self.parameters["phi45nd"]

        # Centers
        # f[24] =


        # Calculating Overpressure
        # Calculating Overpressure

        # Put your code here

        return f

    def findSolution(self, vector: dict, n: int) -> list[float]:
        # vector_0 = {
        # 0: x1, 1: y1, 2: r1, 3: phi1, 4: alpha1,
        # 5: x2, 6: y2, 7: r2, 8: phi2, 9: alpha2,
        # 10: x3, 11: y3, 12: r3, 13: phi3, 14: alpha3,
        # 15: x4, 16: y4, 17: r4, 18: phi4, 19: alpha4,
        # 20: x5, 21: y5, 22: r5, 23: phi5, 24: alpha5 = parameters["alpha5"]



        S = [np.array([vector[0], vector[1], vector[2], vector[3], vector[4], vector[5], vector[6], vector[7], vector[8],
                       vector[9], vector[10], vector[11], vector[12], vector[13], vector[14], vector[15]], vector[16], vector[17],
                      vector[18], vector[19], vector[20], vector[21], vector[22], vector[23], vector[24]) for _ in range(2)]

        key = 0
        while key == 0 or np.linalg.norm(abs(S[0] - S[1]), ord=2) > init.EPS:
            S[0] = S[1].copy()
            system_vector = self.F(vector, n)
            for i in range(25):
                S[1][i] = S[1][i] - system_vector[i] * init.TAU
                vector[i] = S[1][i]
            key = 1

        # # Alphas
        # # MAKE THE EQUATIONS BE EQUAL TO ZERO
        # f[19] = np.pi - np.arccos(abs(x["xt1"] - self.parameters["Ax"]) / x["r1"])
        # f[20] = np.pi - np.arccos(abs(x["xt2"] - self.parameters["Bx"]) / x["r2"])
        # f[21] = np.pi - np.arccos(abs(x["xt3"] - x["x3"]) / x["r3"])
        # f[22] = np.pi - np.arccos(abs(x["xt4"] - x["x4"]) / x["r4"])
        # f[23] = np.pi - np.arccos(abs(x["xt5"] - x["x5"]) / x["r5"])

    # def findSolution(self, vector: dict, n: int):
    #     # vector = {
    #     # 0: Ax, 1: Ay, 2: Bx, 3: By,
    #     # 4: xTop, 5: yTop, 6: xBot,
    #     # 7: yBot, 8: rt, 9: rb,
    #     # 10: pt0, 11: pb0, 12: pac,
    #     # 13: alpha5 = 3*pi/2,
    #     # 14: x5 = x4,
    #     # 15: alpha4 = 3*Pi/2 - phi4
    #     # }
    #     S = [np.array([vector[0], vector[1], vector[2], vector[3], vector[4], vector[5], vector[6], vector[7], vector[8], vector[9],
    #                    vector[10], vector[11], vector[12], vector[13], vector[14], vector[15]]) for _ in range(2)]
    #
    #     key = 0
    #     while key == 0 or np.linalg.norm(abs(S[0] - S[1]), ord=2) > init.EPS:
    #         S[0] = S[1].copy()
    #         system_vector = self.F(vector, n)
    #         for i in range(16):
    #             S[1][i] = S[1][i] - system_vector[i] * init.TAU
    #             vector[i] = S[1][i]
    #         key = 1
    #
    #
    #     # solution = {
    #     #  0: x1, 1: y1, 2: XT1, 3: YT1, 4: r1, 5: phi1,
    #     #  7: x2, 8: y2, 9: XT2, 10: YT2, 11: r2, 12: phi2,
    #     #  14: x3, 15: y3, 16: XT3, 17: YT3, 18: r3, 19: phi3,
    #     #  21: x4, 22: y4, 23: XT4, 24: YT4, 25: r4, 26: phi4,
    #     #  28: x5, 29: y5, 30: XT5, 31: YT5, 32: r5, 33: phi5,
    #     #
    #     # }
    #
    #
    #
    #     # solution = {
    #     #  0: r1, 1: phi1, 2: alpha1,
    #     #  3: r2, 4: phi2, 5: alpha2,
    #     #  6: x3, 7: y3, 8: r3, 9: phi3, 10: alpha3,
    #     #  11: x4, 12: y4, 13: r4, 14: phi4, 15: alpha4,
    #     #  16: x5, 17: y5, 18: r5, 19: phi5, 20: alpha5,
    #     #
    #     # }
    #
    #
    #     solution = np.zeros(29)



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


# TEST FOR getIntersections
# xt, yt = 0, 0.65*2
# xb, yb = 0, 0.22*2
# rt = 0.3*2
# rb = 0.19*2
# # xt, yt = 0, 0
# # rt = 5
# # xb, yb = 2, 2
# # rb = 5
# circle1 = plt.Circle((xt, yt), rt, color='g', fill=False)
# circle2 = plt.Circle((xb, yb), rb, color='b', fill=False)
# fig, ax = plt.subplots()
# ax.set_xlim((-1, 1))
# ax.set_ylim((-0, 2))
# ax.add_artist(circle1)
# ax.add_artist(circle2)
#
# intersections = TwoTierSolver().getIntersections({"x": xt, "y": yt}, {"x": xb, "y": yb}, rt, rb)
# plt.plot([intersections["x3"]], [intersections["y3"]], '.', color='r')
#
# plt.gca().set_aspect('equal', adjustable='box')
# plt.show()