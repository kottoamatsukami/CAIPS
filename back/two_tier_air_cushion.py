import numpy as np
from matplotlib import pyplot as plt, patches as pth
from PIL import Image
import back


class TwoTierSolver(object):
    def __init__(self, const: list) -> None:
        """
        0 -> Ax  4 -> phiNd1  7 ->  p  10 -> alpha5
        1 -> Ay  5 -> phiNd2  8 -> rt  11 -> pt
        2 -> Bx  6 -> phiNd3  9 -> rb  12 -> pb
        3 -> By
        """
        self.constants = const

    def F(self, x: list, norm=1, return_f=False) -> np.array:
        """
        0 -> x1  5 -> y1  10 -> r1  15 -> phi1  20 -> alpha1  24 -> phiNd4
        1 -> x2  6 -> y2  11 -> r2  16 -> phi2  21 -> alpha2  25 -> phiNd5
        2 -> x3  7 -> y3  12 -> r3  17 -> phi3  22 -> alpha3  EXTRA
        3 -> x4  8 -> y4  13 -> r4  18 -> phi4  23 -> alpha4
        4 -> x5  9 -> y5  14 -> r5  19 -> phi5
        """
        func = np.zeros(24)

        func[0] = x[4] - x[3]
        func[1] = x[23] - 3*np.pi/2 + x[18]

        func[2] = x[10] * x[15] - self.constants[8] * self.constants[4]
        func[3] = x[11] * x[16] - self.constants[8] * self.constants[5]
        func[4] = x[12] * x[17] - self.constants[8] * self.constants[6]
        func[5] = x[13] * x[18] + x[14] * x[19] - self.constants[9] * 5.001905970

        func[6] = x[10] * np.cos(x[20]) + x[0] - self.constants[0]
        func[7] = x[10] * np.sin(x[20]) + x[5] - self.constants[1]

        func[8] = x[11] * np.cos(x[16] + x[21]) + x[1] - self.constants[2]
        func[9] = x[11] * np.sin(x[16] + x[21]) + x[6] - self.constants[3]

        func[10] = x[12] * np.cos(x[22] + x[17]) + x[2] - x[11]*np.cos(x[21]) - x[1]
        func[11] = x[12] * np.sin(x[22] + x[17]) + x[7] - x[11]*np.sin(x[21]) - x[6]
        func[12] = x[12] * np.cos(x[22] + x[17]) + x[2] - x[14]*np.cos(self.constants[10] + x[19]) - x[4]
        func[13] = x[12] * np.sin(x[22] + x[17]) + x[7] - x[14]*np.sin(self.constants[10] + x[19]) - x[9]

        func[14] = x[10] * np.cos(x[20] + x[15]) + x[0] - x[12]*np.cos(x[22]) - x[2]
        func[15] = x[10] * np.sin(x[20] + x[15]) + x[5] - x[12]*np.sin(x[22]) - x[7]
        func[16] = x[10] * np.cos(x[20] + x[15]) + x[0] - x[13]*np.cos(x[23]) - x[3]
        func[17] = x[10] * np.sin(x[20] + x[15]) + x[5] - x[13]*np.sin(x[23]) - x[8]

        func[18] = x[8] - x[13] - x[9] + x[14]

        func[19] = self.constants[11]*x[10]*np.sin(x[20] + x[15]) - (self.constants[11] - self.constants[12])*x[12]*np.sin(x[22]) - self.constants[12]*x[13]*np.sin(x[23])
        func[20] = self.constants[11]*x[10]*np.cos(x[20] + x[15]) - (self.constants[11] - self.constants[12])*x[12]*np.cos(x[22]) - self.constants[12]*x[13]*np.cos(x[23])

        func[21] = (self.constants[11] - self.constants[7])*x[11]*np.sin(x[21]) - (self.constants[11] - self.constants[12])*x[12]*np.sin(x[22] + x[17]) - (self.constants[12] - self.constants[7])*x[14]*np.sin(self.constants[10] + x[19])
        func[22] = (self.constants[11] - self.constants[7])*x[11]*np.cos(x[21]) - (self.constants[11] - self.constants[12])*x[12]*np.cos(x[22] + x[17]) - (self.constants[12] - self.constants[7])*x[14]*np.cos(self.constants[10] + x[19])
        func[23] = self.constants[12]*x[13] - (self.constants[12] - self.constants[7])*x[14]

        func = list(map(lambda v: v**2, func))
        func = np.array(func)
        if return_f:
            return np.linalg.norm(func, norm), func
        return np.linalg.norm(func, norm)

    def findSolution(self, vec, norm=2, weight=None):
        if weight is None:
            weight = np.array([1] * 28)

        for _ in range(1, 5000):
            gradient = np.zeros_like(vec)
            for j in range(len(vec)):
                epsilon = np.zeros_like(vec)
                epsilon[j] = back.EPS
                gradient[j] = (self.F(vec + epsilon) - self.F(vec - epsilon)) / (2 * back.EPS)

            vec -= back.OMI * weight * gradient
            norma = self.F(vec, norm=norm)
            print(norma)
        return vector


constants = np.array([
    0,            # Ax
    1.9,          # Ay
    0.6,          # Bx
    1.3,          # By
    2.753364902,  # phiNd1
    1.182568575,  # phiNd2
    0.776455503,  # phiNd3
    2000,         # p
    0.6,          # rt
    0.38,         # rb
    3*np.pi/2,    # alpha5
    12000*2,      # pt0
    4000*2,       # pb0
])

vector = np.array([
    1,  # --
    1,  #
    1,  # x
    1,  #
    1,  # --
    1,  # --
    1,  #
    1,  # y
    1,  #
    1,  # --
    1,  # --
    1,  #
    1,  # r
    1,  #
    1,  # --
    1,  # --
    1,  #
    1,  # phi
    1,  #
    1,  # --
    1,  # --
    1,  # alpha
    1,  #
    1,  # --
    1,  # phiNd4
    1.,  # phiNd5
])
weights = np.array([
    1,  # --
    1,  #
    1,  # x
    1,  #
    1,  # --
    1,  # --
    1,  #
    1,  # y
    1,  #
    1,  # --
    0.85,  # --
    1,  #
    1,  # r
    1,  #
    1,  # --
    0.07,  # --
    0.01,  #
    0.01,  # phi
    0.01,  #
    0.01,  # --
    0.005,  # --
    0.01,  # alpha
    0.01,  #
    1,  # --
    0.01,  # phiNd4
    0.01,  # phiNd5
])

solver = TwoTierSolver(const=constants)
vector = solver.findSolution(vec=vector, norm=2, weight=weights)

f = solver.F(vector, return_f=True)

for i in range(len(f[1])):
    print(f"Уравнение {i}: {round(f[1][i], 3)}")
print(vector)
