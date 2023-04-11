import establishing_solver
import numpy as np
import matplotlib.patches as mpatches

M = 100
P = 2000
G = 9.8
DTIME = 0.01

class DynamicsSolver(object):

    global M, P, G, DTIME

    @staticmethod
    def Dvdt(l: float or int) -> float or int:
        # -----------------------------------
        # structure
        # values = {
        # value_1 : x1
        # value_2 : x2
        # }
        # -----------------------------------
        return 1/M * (P * l - M * G)


    def CalculateY(self, values: float or int) -> float or int:
        # -----------------------------------
        # structure
        # values = {
        # value_1 : x1 = Ax
        # value_2 : x2 = Bx
        # value_3 : y = Ay = By
        # value_4 : phi1 = 0
        # value_5 : phi2 = 0
        # value_6 : Ax = from user
        # value_7 : Ay = from user
        # value_8 : Bx = from user
        # value_9 : By = from user
        # value_10 : C = 3pi/8
        # value_11 : vy = 0
        # }
        # -----------------------------------

        Y = []

        for t_ in range(0, 250, 1):
            X = establishing_solver.EstablishingSolver().establish(values)
            for i in range(len(X)):
                values[i] = X[i]
            l = values[1] - values[0]
            values[10] = values[10] + self.Dvdt(l) * DTIME
            values[5] = values[0]
            values[6] = values[6] + values[10] * DTIME
            values[7] = values[1]
            values[8] = values[6]

            print("t_ = ", t_)


        return values

vals = [0.0, 0.0, 0.0, 0.0, 0.0, -0.353, 0.3, 0.353, 0.3, 3*np.pi/8, 0]
values = DynamicsSolver().CalculateY(vals)
print(values)