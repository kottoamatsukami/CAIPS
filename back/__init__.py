import os
import pickle
import asyncio
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt, patches as pth
from celluloid import Camera
#import settings as stg

# HYPER PARAMETERS
EPS = 1e-7
TAU = 0.9
TIME_STAMP = 0.01
ACCELERATION = 0
MASS = 100
GRAVITY_CONSTANT = 9.81
PRESSURE = 2000
alpha5 = 3*np.pi/2


class FirstModeSolver(object):

    global EPS, TAU

    def __init__(self, parameters):
        self.parameters = parameters

    @staticmethod
    def load(path: str) -> dict:
        with open(path, "rb") as file:
            data = pickle.load(file)
        return data

    @staticmethod
    def F(values: list[float]) -> list[float]:
        f = np.zeros(5)
        f[0] = values[0] + values[2] * np.cos(3*np.pi/2 - values[3]) - values[5]
        f[1] = values[1] + values[2] * np.cos(3*np.pi/2 + values[4]) - values[7]
        f[2] = values[2] + values[2] * np.sin(3*np.pi/2 - values[3]) - values[6]
        f[3] = ((values[3] + values[4]) * values[2] + (values[1] - values[0]) - values[9])
        f[4] = (values[2] + values[2] * np.sin(3*np.pi/2 + values[4]) - values[8])
        return f

    async def findSolution(self, values: list[float], logger) -> list[float]:
        # 5 7 6 3 4
        x = [np.array([values[5], values[7], values[6], values[3], values[4]]) for _ in range(2)]

        key = 0
        epoch = 0
        while key == 0 or np.linalg.norm(abs(x[0]-x[1]), ord=2) > EPS:
            x[0] = x[1].copy()
            system_vals = self.F(values)
            for i in range(5):
                x[1][i] = x[1][i] - system_vals[i] * TAU
                values[i] = x[1][i]
            key = 1
            if epoch % 250 == 0:
                logger(f"epoch[{epoch}]: norm={np.linalg.norm(abs(x[0]-x[1]), ord=2)}")
            # Critical
            if epoch >= 300_000 or np.linalg.norm(abs(x[0]-x[1]), ord=2) == np.inf:
                logger("It cannot be solved", 'critical')
                break
            epoch += 1
        return x[1]

    @staticmethod
    def euclidean_distance(p1: tuple, p2: tuple) -> float:
        return np.sqrt(
            (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
        )

    def makeAnimation(self, vector: list[float]) -> None:
        fig, axs = plt.subplots(1, 1, figsize=(5, 5))
        axs.set_aspect("equal")
        r1 = self.euclidean_distance(
            p1=(self.parameters["Ax"], self.parameters["Ay"]),
            p2=(vector[0], vector[2]),
        )
        r2 = self.euclidean_distance(
            p1=(self.parameters["Bx"], self.parameters["By"]),
            p2=(vector[1], vector[2]),
        )
        # Line AB
        axs.plot((self.parameters["Ax"], self.parameters["Bx"]), (self.parameters["Ay"], self.parameters["By"]),
                 color='black')
        # Line X1X2
        axs.plot((vector[0], vector[1]), (0, 0),
                 color='black')

        arc1 = pth.Arc(
            xy=(vector[0], vector[2]),
            width=r1 * 2,
            height=r1 * 2,
            angle=0,
            theta1=(self.parameters["alpha5"] - vector[3]) * 180 / np.pi,
            theta2=(self.parameters["alpha5"] * 180 / np.pi),

        )
        axs.add_patch(arc1)

        arc2 = pth.Arc(
            xy=(vector[1], vector[2]),
            width=r2 * 2,
            height=r2 * 2,
            angle=270,
            theta1=0,
            theta2=vector[4] * 180 / np.pi,

        )
        axs.add_patch(arc2)

        # Convert to GIF format
        #fig.savefig(os.path.join(stg.ROOT_PATH, "temp/temp.png"))
        #im = Image.open(os.path.join(stg.ROOT_PATH, "temp/temp.png"))
        #im.save(os.path.join(stg.ROOT_PATH, "temp/result.gif"))
        #os.remove(os.path.join(stg.ROOT_PATH, "temp/temp.png"))


class SecondModeSolver(object):

    global MASS, PRESSURE, GRAVITY_CONSTANT, TIME_STAMP, alpha5

    def __init__(self, parameters):
        self.parameters = parameters

    @staticmethod
    def Dvdt(length: float) -> float:
        return 1/MASS * (PRESSURE * length - MASS * GRAVITY_CONSTANT)

    async def findSolution(self, values: list[float], logger) -> float:
        # -----------------------------------
        # structure
        # values = {
        # value_1 : x1_0 = 0
        # value_2 : x2_0 = 0
        # value_3 : y_0 = Ay = By
        # value_4 : phi1_0 = 0
        # value_5 : phi2_0 = 0
        # value_6 : Ax = from user
        # value_7 : Ay = from user
        # value_8 : Bx = from user
        # value_9 : By = from user
        # value_10 : C = 3pi/8
        # value_11 : vy = 0
        # }
        # -----------------------------------
        data = [[0 for _ in range(9)] for _ in range(250)]
        for t in range(250):
            for j in range(len(data[0])):
                data[t][j] = values[j]
            values[6] = values[6] + values[10] * TIME_STAMP
            values[8] = values[6]
            x = FirstModeSolver(parameters=self.parameters).findSolution(values, logger)
            for i in range(3):
                values[i] = x[i]
            length = abs(values[1] - values[0])
            values[10] = values[10] + self.Dvdt(length) * TIME_STAMP

        return data

    @staticmethod
    def euclidean_distance(p1: tuple, p2: tuple) -> float:
        return np.sqrt(
            (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
        )

    def makeAnimation(self, matrix: list[list[float]]):
        # -----------------------------------
        # structure
        # matrix[i] = {
        # matrix[i]_1 : x1_0 = 0
        # matrix[i]_2 : x2_0 = 0
        # matrix[i]_3 : y_0 = Ay = By
        # matrix[i]_4 : phi1_0 = 0
        # matrix[i]_5 : phi2_0 = 0
        # matrix[i]_6 : Ax = from user
        # matrix[i]_7 : Ay = from user
        # matrix[i]_8 : Bx = from user
        # matrix[i]_9 : By = from user
        # }
        # -----------------------------------
        fig = plt.figure(figsize=(5, 5))
        axs = plt.subplot()

        plt.grid(linestyle='--')
        axs.set_aspect('equal')

        camera = Camera(fig)
        for i in range(0, 250):
            r1 = self.euclidean_distance(
                p1=(matrix[i][5], matrix[i][6]),
                p2=(matrix[i][0], matrix[i][2]),
            )
            r2 = self.euclidean_distance(
                p1=(matrix[i][7], matrix[i][8]),
                p2=(matrix[i][1], matrix[i][2]),
            )

            # Line AB
            axs.plot((matrix[i][5], matrix[i][7]), (matrix[i][6], matrix[i][8]),
                     color='black')
            # Line X1X2
            axs.plot((matrix[i][0], matrix[i][1]), (0, 0),
                     color='black')

            arc1 = pth.Arc(
                xy=(matrix[i][0], matrix[i][2]),
                width=r1 * 2,
                height=r1 * 2,
                angle=0,
                theta1=(alpha5 - matrix[i][3]) * 180 / np.pi,
                theta2=(alpha5 * 180 / np.pi),

            )
            axs.add_patch(arc1)

            arc2 = pth.Arc(
                xy=(matrix[i][1], matrix[i][2]),
                width=r2 * 2,
                height=r2 * 2,
                angle=270,
                theta1=0,
                theta2=matrix[i][4] * 180 / np.pi,

            )
            axs.add_patch(arc2)

            camera.snap()

        animation = camera.animate()
        plt.show()
        animation.save('settings/temp.gif')


class ThirdModeSolver(object):
    def __init__(self, parameters) -> None:
        self.history = []
        self.p_history = {}
        self.parameters = parameters

    def F(self, x: dict, n: int) -> np.array:
        f = np.zeros(14)
        # In point A
        f[0] = x["r1"] * np.cos(x["alpha1"]) + x["x1"] - self.parameters["Ax"]
        f[1] = x["r1"] * np.sin(x["alpha1"]) + x["y1"] - self.parameters["Ay"]
        # In point B
        f[2] = x["r2"] * np.cos(x["phi2"] + x["alpha2"]) + x["x2"] - self.parameters["Bx"]
        f[3] = x["r2"] * np.sin(x["phi2"] + x["alpha2"]) + x["y2"] - self.parameters["By"]
        # In point C
        f[4] = x["r3"] * np.cos(x["alpha3"] + x["phi3"]) + x["x3"] - x["r2"] * np.cos(x["alpha2"]) - x["x2"]
        f[5] = x["r3"] * np.sin(x["alpha3"] + x["phi3"]) + x["y3"] - x["r2"] * np.sin(x["alpha2"]) - x["y2"]
        f[6] = x["r3"] * np.cos(x["alpha3"] + x["phi3"]) + x["x3"] - x["r5"] * np.cos(x["alpha5"] + x["phi5"]) - x[
                "x5"]
        f[7] = x["r3"] * np.sin(x["alpha3"] + x["phi3"]) + x["y3"] - x["r5"] * np.sin(x["alpha5"] + x["phi5"]) - x[
                "y5"]
        # In point D
        f[8] = x["r1"] * np.cos(x["alpha1"] + x["phi1"]) + x["x1"] - x["r3"] * np.cos(x["alpha3"]) - x["x3"]
        f[9] = x["r1"] * np.sin(x["alpha1"] + x["phi1"]) + x["y1"] - x["r3"] * np.sin(x["alpha3"]) - x["y3"]
        f[10] = x["r1"] * np.cos(x["alpha1"] + x["phi1"]) + x["x1"] - x["r4"] * np.cos(x["alpha4"]) - x["x4"]
        f[11] = x["r1"] * np.sin(x["alpha1"] + x["phi1"]) + x["y1"] - x["r4"] * np.sin(x["alpha4"]) - x["y4"]
        # In point E
        f[12] = x["x4"] - x["x5"]
        f[13] = x["y4"] - x["r4"] + x["r5"] - x["y5"]

        # Calculating Overpressure

        # Put your code here

        return f

    async def findSolution(self, vector):
        ...

    async def makeAnimation(self, vector):
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
        fig.savefig("settings/temp.png")
        im = Image.open("settings/temp.png")
        if rotate:
            im = im.rotate(180)
        im.save("settings/temp.gif")

    def calculate_overpressure(self, n):
        ...
