from optlib import vector_function
from numpy import *

Ax, Ay, Bx, By = 0, 1.9, 0.6, 1.3
rt, rb = 0.6, 0.38
fNd1, fNd2, fNd3 = 2.753364902, 1.182568575, 0.7764555030
P, Pb, Pt = 2000, 8000, 24000


def fill_system(x):
    # a1 -> 0   <>   f1 -> 5
    # a2 -> 1   <>   f2 -> 6
    # a3 -> 2   <>   f3 -> 7
    # a4 -> 3   <>   f4 -> 8
    # a5 -> 4   <>   f5 -> 9
    a1, f1 = x[0], x[5]
    a2, f2 = x[1], x[6]
    a3, f3 = x[2], x[7]
    a4, f4 = x[3], x[8]
    a5, f5 = x[4], x[9]

    rt1, rt2, rt3 = rt * fNd1 / f1, rt * fNd2 / f2, rt * fNd3 / f3
    alef = (5.001905970) / (Pb * f5 + Pb * f4 - P * f4)

    result = zeros(10)

    result[0] = rt1 * sin(a1 + f1 / 2) * sin(f1 / 2) \
                + rt2 * sin(a2 + f2 / 2) * sin(f2 / 2) \
                + rt3 * sin(a3 + f3 / 2) * sin(f3 / 2) \
                + (Bx - Ax) / 2

    result[1] = rt1 * cos(a1 + f1 / 2) * sin(f1 / 2) \
                + rt2 * cos(a2 + f2 / 2) * sin(f2 / 2) \
                + rt3 * cos(a3 + f3 / 2) * sin(f3 / 2) \
                + (Ay - By) / 2

    result[2] = (alef / 2) * rb * ((Pb - P) * cos(a4) - Pb * sin(f5)) \
                + rt1 * sin(a1 + f1 / 2) * sin(f1 / 2) \
                + rt2 * sin(a2 + f2 / 2) * sin(f2 / 2) \
                + (Bx - Ax) / 2

    result[3] = (alef / 2) * rb * (P - (Pb - P) * sin(a4) - Pb * cos(f5)) \
                + rt1 * cos(a1 + f1 / 2) * sin(f1 / 2) \
                + rt2 * cos(a2 + f2 / 2) * sin(f2 / 2) \
                + (Ay - By) / 2

    result[4] = Pt * rt1 * sin(a1 + f1) \
                - (Pt - Pb) * rt3 * sin(a3) \
                - Pb * rb * (Pb - P) * alef * sin(a4)

    result[5] = Pt * rt1 * cos(a1 + f1) \
                - (Pt - Pb) * rt3 * cos(a3) \
                - Pb * rb * (Pb - P) * alef * cos(a4)

    result[6] = (Pt - P) * rt2 * sin(a2) \
                - (Pt - Pb) * rt3 * sin(a3 + f3) \
                + Pb * rb * (Pb - P) * alef * cos(f5)

    result[7] = (Pt - P) * rt2 * cos(a2) \
                - (Pt - Pb) * rt3 * cos(a3 + f3) \
                - Pb * rb * (Pb - P) * alef * sin(f5)

    result[8] = a4 + f4 - 3 * pi / 2

    result[9] = a5 - 3 * pi / 2

    return result


solver = vector_function.GDUniformGrid()
solver.optimize(
    function=fill_system,
    vector_length=10,
    min_value=0.00000001,
    max_value=2*pi,
    step=1,
    iters=100,
    criterion=vector_function.MSELoss,
    target=0.5,
)