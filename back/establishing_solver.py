import pickle
import numpy as np

class EstablishingSolver(object):

    @staticmethod
    def load(path: str) -> dict:
        with open(path, "rb") as file:
            data = pickle.load(file)
        return data

    # C = (3*np.pi)/8

    def get_system_values(self, values: float or int) -> float or int:
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
        eps = 0.001
        F = np.empty([5, 1])
        F[0] = values[0] + values[2] * np.cos(3*np.pi/2 - values[3]) - values[5]
        F[1] = values[1] + values[2] * np.cos(3*np.pi/2 + values[4]) - values[7]
        F[2] = values[2] + values[2] * np.sin(3*np.pi/2 - values[3]) - values[6]
        F[3] = (values[3] + values[4]) * values[2] + (values[1] - values[0]) - values[9]
        F[4] = values[2] + values[2] * np.sin(3*np.pi/2 + values[4]) - values[8]
        return F

    def establish(self, values: float or int) -> float or int:
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
        X = [np.empty([5, 1]) for _ in range(2)]
        eps = 0.01
        tau = 0.005

        key = 0
        while (key == 0 or np.linalg.norm(abs(X[0]-X[1]), ord=2) > eps):
            X[0] = X[1]
            for i in range(5):
                X[1][i] = X[1][i] - self.get_system_values(values)[i] * tau
            key = 1
        return X[1]


vals = [4.0, 5.0, 3.0, 0.0, 0.0, -0.353, 0.3, 0.353, 0.3, 3*np.pi/8]
res0 = EstablishingSolver().establish(vals)
print(res0)
res = res0
res = np.append(res, -0.353)
res = np.append(res, 0.3)
res = np.append(res, 0.353)
res = np.append(res, 0.3)
res = np.append(res, 3*np.pi/8)
print(EstablishingSolver().get_system_values(res))