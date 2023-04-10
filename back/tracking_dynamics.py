import establishing_solver
import Animation
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
        return 1/M * (P * l - M * G)


    def calculate_y(self, values: float or int) -> float or int:
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

        # ADD VALUES TO Y_ARRAY
        data = [[0 for i in range(9)] for _ in range(250)]

        for t_ in range(250):
            for j in range(len(data[0])):
                data[t_][j] = values[j]
            values[6] = values[6] + values[10] * DTIME
            values[8] = values[6]
            X = establishing_solver.EstablishingSolver().establish(values)
            for i in range(3):
                values[i] = X[i]
            l = abs(values[1] - values[0])
            values[10] = values[10] + self.Dvdt(l) * DTIME

            # values[5] = values[0]
            # values[7] = values[1]

            print("t_ =", t_, "l =", l, "values[1] =", values[1], "values[0] =", values[0])
            # if t_ == 41:
            #     print(values)
            #     input()
                # print("\n\n\n\n\n\n\n\n\n")

        return data

vals = [0.0, 0.0, 0.3, 0.0, 0.0, -0.353, 0.3, 0.353, 0.3, 3*np.pi/8, 0]
data = DynamicsSolver().calculate_y(vals)
print(data)
Animation.Animation().create_animation(data)