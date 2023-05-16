import pickle
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt, patches as pth
import back


class EstablishingSolver(object):

    def __init__(self, parameters):
        self.parameters = parameters

    @staticmethod
    def load(path: str) -> dict:
        with open(path, "rb") as file:
            data = pickle.load(file)
        return data

    @staticmethod
    def get_system_values(values: list[float]) -> list[float]:
        f = np.zeros(5)
        f[0] = values[0] + values[2] * np.cos(3*np.pi/2 - values[3]) - values[5]
        f[1] = values[1] + values[2] * np.cos(3*np.pi/2 + values[4]) - values[7]
        f[2] = values[2] + values[2] * np.sin(3*np.pi/2 - values[3]) - values[6]
        f[3] = ((values[3] + values[4]) * values[2] + (values[1] - values[0]) - values[9])
        f[4] = (values[2] + values[2] * np.sin(3*np.pi/2 + values[4]) - values[8])
        return f

    def establish(self, values: list[float], logger) -> list[float]:
        # 5 7 6 3 4
        X = [np.array([values[5], values[7], values[6], values[3], values[4]]) for _ in range(2)]

        key = 0
        epoch = 0
        while key == 0 or np.linalg.norm(abs(X[0]-X[1]), ord=2) > back.EPS:
            X[0] = X[1].copy()
            system_vals = self.get_system_values(values)
            for i in range(5):
                X[1][i] = X[1][i] - system_vals[i] * back.TAU
                values[i] = X[1][i]
            key = 1
            if epoch % 250 == 0:
                logger(f"epoch[{epoch}]: norm={np.linalg.norm(abs(X[0]-X[1]), ord=2)}")
            # Critical
            if epoch >= 300_000 or np.linalg.norm(abs(X[0]-X[1]), ord=2) == np.inf:
                logger("It cannot be solved", 'critical')
                break
            epoch += 1
        return X[1]

    @staticmethod
    def euclidean_distance(p1: tuple, p2: tuple) -> float:
        return np.sqrt(
            (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
        )

    def make_animation(self, vector: list[float]) -> None:
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
        fig.savefig("saved_parameters/temp.png")
        im = Image.open("saved_parameters/temp.png")
        im.save("saved_parameters/temp.gif")

