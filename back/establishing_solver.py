import pickle
import back
import numpy as np


class EstablishingSolverV4(object):
    def __init__(self) -> None:
        self.history = []

    @staticmethod
    def load(path: str) -> dict:
        with open(path, "rb") as file:
            data = pickle.load(file)
        return data

    @staticmethod
    def get_system_values(values: list[float]) -> list[float]:
        # ----------------------------------------
        # structure
        # values = {
        # value_1 : x1
        # value_2 : x2
        # value_3 : y
        # value_4 : phi1
        # value_5 : phi2
        # value_6 : Ax
        # value_7 : Ay
        # value_8 : Bx
        # value_9 : By
        # value_10 : C
        # }
        # ----------------------------------------
        F = np.empty([5, 1])
        F[0] = values[0] + values[2] * np.cos(3*np.pi/2 - values[3]) - values[5]
        F[1] = values[1] + values[2] * np.cos(3*np.pi/2 + values[4]) - values[7]
        F[2] = values[2] + values[2] * np.sin(3*np.pi/2 - values[3]) - values[6]
        F[3] = (values[3] + values[4]) * values[2] + (values[1] - values[0]) - values[9]
        F[4] = values[2] + values[2] * np.sin(3*np.pi/2 + values[4]) - values[8]
        return F

    def establish(self, values: list[float], logger) -> list[float]:
        # ----------------------------------------
        # structure
        # values = {
        # value_1 : x1
        # value_2 : x2
        # value_3 : y
        # value_4 : phi1
        # value_5 : phi2
        # value_6 : Ax
        # value_7 : Ay
        # value_8 : Bx
        # value_9 : By
        # value_10 : C
        # }
        # ----------------------------------------
        X = [np.array([values[5], values[7], values[6], values[3], values[4]]) for _ in range(2)]

        key = 0
        epoch = 0
        while key == 0 or np.linalg.norm(abs(X[0]-X[1]), ord=2) > back.EPS:
            epoch += 1
            X[0] = X[1].copy()
            for i in range(5):
                X[1][i] = X[1][i] - self.get_system_values(values)[i] * back.TAU
                values[i] = X[1][i]
            key = 1
            self.history += [np.linalg.norm(abs(X[0]-X[1]), ord=2)]
            if epoch % 250 == 0:
                logger(f"[{epoch}]: {self.history[-1]}")
        logger("Successful!")
        return X[1]



# # Add data from GUI here
# vals = [20.0, 45.0, 30.0, 0.0, 0.0, -0.353, 0.3, 0.353, 0.3, 3*np.pi/8]
# values = EstablishingSolver().establish(vals)

# For test:
# values = np.append(values, -0.353)
# values = np.append(values, 0.3)
# values = np.append(values, 0.353)
# values = np.append(values, 0.3)
# values = np.append(values, 3*np.pi/8)
# print(EstablishingSolver().get_system_values(values))