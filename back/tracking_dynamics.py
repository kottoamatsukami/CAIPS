from back import establishing_solver
import numpy as np
import math
from matplotlib import pyplot as plt, patches as pth
from celluloid import Camera

M = 100
P = 2000
G = 9.8
DTIME = 0.01

alpha5 = 3*math.pi/2


class DynamicsSolver(object):

    global M, P, G, DTIME
    global alpha5

    def __init__(self, parameters):
        self.parameters = parameters

    @staticmethod
    def Dvdt(l: float) -> float:
        return 1/M * (P * l - M * G)

    def find_solution(self, values: list[float], logger) -> float:
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
        data = [[0 for i in range(9)] for _ in range(250)]
        for t in range(250):
            for j in range(len(data[0])):
                data[t][j] = values[j]
            values[6] = values[6] + values[10] * DTIME
            values[8] = values[6]
            X = establishing_solver.EstablishingSolver(parameters=self.parameters).establish(values, logger)
            for i in range(3):
                values[i] = X[i]
            l = abs(values[1] - values[0])
            values[10] = values[10] + self.Dvdt(l) * DTIME

        return data

    @staticmethod
    def euclidean_distance(p1: tuple, p2: tuple) -> float:
        return math.sqrt(
            (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
        )

    def make_animation(self, matrix: list[list[float]]):
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
                theta1=(alpha5 - matrix[i][3]) * 180 / math.pi,
                theta2=(alpha5 * 180 / math.pi),

            )
            axs.add_patch(arc1)

            arc2 = pth.Arc(
                xy=(matrix[i][1], matrix[i][2]),
                width=r2 * 2,
                height=r2 * 2,
                angle=270,
                theta1=0,
                theta2=matrix[i][4] * 180 / math.pi,

            )
            axs.add_patch(arc2)

            camera.snap()

        animation = camera.animate()
        plt.show()
        animation.save('saved_parameters/temp.gif')