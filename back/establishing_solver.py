import pickle
import numpy as np

EPS = 0.0001
TAU = 0.005
class EstablishingSolver(object):

    global EPS, TAU

    @staticmethod
    def load(path: str) -> dict:
        with open(path, "rb") as file:
            data = pickle.load(file)
        return data

    def get_system_values(self, values: float or int) -> float or int:
        # ----------------------------------------
        # structure
        # values = {
        # value_1 : x1_0 = 0
        # value_2 : x2_0 = 0
        # value_3 : y_0 = Ay = By
        # value_4 : phi1_0 = 0
        # value_5 : phi2_0 = 0
        # value_6 : Ax
        # value_7 : Ay
        # value_8 : Bx
        # value_9 : By
        # value_10 : C
        # }
        # ----------------------------------------
        F = np.zeros(5)
        # values[3] = values[3] % (2*np.pi)
        # values[4] = values[4] % (2*np.pi)
        F[0] = values[0] + values[2] * np.cos(3*np.pi/2 - values[3]) - values[5]
        F[1] = values[1] + values[2] * np.cos(3*np.pi/2 + values[4]) - values[7]
        F[2] = values[2] + values[2] * np.sin(3*np.pi/2 - values[3]) - values[6]
        # print(values[3], values[4], values[2], values[1], values[0], values[9])
        F[3] = ((values[3] + values[4]) * values[2] + (values[1] - values[0]) - values[9])
        # print(F[3])
        F[4] = (values[2] + values[2] * np.sin(3*np.pi/2 + values[4]) - values[8])
        return F

    def establish(self, values: float or int) -> float or int:
        # ----------------------------------------
        # structure
        # values = {
        # value_1 : x1_0 = 0
        # value_2 : x2_0 = 0
        # value_3 : y_0 = Ay = By
        # value_4 : phi1_0 = 0
        # value_5 : phi2_0 = 0
        # value_6 : Ax
        # value_7 : Ay
        # value_8 : Bx
        # value_9 : By
        # value_10 : C
        # }
        # ----------------------------------------
        X = [np.array([values[0], values[1], values[2], values[3], values[4]]) for _ in range(2)]

        key = 0
        while (key == 0 or np.linalg.norm(abs(X[0]-X[1]), ord=2) > EPS):
            X[0] = X[1].copy()
            system_vals = self.get_system_values(values)
            for i in range(5):
                X[1][i] = X[1][i] - system_vals[i] * TAU
                values[i] = X[1][i]
            key = 1
            # print("norm=", np.linalg.norm(abs(X[0]-X[1]), ord=2))
        return X[1]



# Add data from GUI here.
vals = [0.0, 0.0, 0.3, 0.0, 0.0, -0.353, 0.3, 0.353, 0.3, 3*np.pi/8]
values = EstablishingSolver().establish(vals)

# For test:
values = np.append(values, -0.353)
values = np.append(values, 0.3)
values = np.append(values, 0.353)
values = np.append(values, 0.3)
values = np.append(values, 3*np.pi/8)
print(EstablishingSolver().get_system_values(values))