import numpy as np
from matplotlib import pyplot as plt, patches as pth
from PIL import Image
import back


class TwoTierSolver(object):
    def __init__(self, const: list) -> None:
        """
        0 -> Ax  4 -> phiNd1  7 ->  p  10 -> alpha5
        1 -> Ay  5 -> phiNd2  8 -> rt
        2 -> Bx  6 -> phiNd3  9 -> rb
        3 -> By
        """
        self.constants = const

    def F(self, x: list, norm=1, return_f=False) -> np.array:
        """
        0 -> x1  5 -> y1  10 -> r1  15 -> phi1  20 -> alpha1  24 -> phiNd4
        1 -> x2  6 -> y2  11 -> r2  16 -> phi2  21 -> alpha2  25 -> phiNd5
        2 -> x3  7 -> y3  12 -> r3  17 -> phi3  22 -> alpha3  EXTRA
        3 -> x4  8 -> y4  13 -> r4  18 -> phi4  23 -> alpha4  26 -> pt
        4 -> x5  9 -> y5  14 -> r5  19 -> phi5                27 -> pb
        """
        func = np.zeros(25)

        func[0] = 5.001905970 - x[24] - x[25]
        func[1] = x[4] - x[3]
        func[2] = x[23] - 3*np.pi/2 + x[18]

        func[3] = x[10] * x[15] - self.constants[8] * self.constants[4]
        func[4] = x[11] * x[16] - self.constants[8] * self.constants[5]
        func[5] = x[12] * x[17] - self.constants[8] * self.constants[6]
        func[6] = x[13] * x[18] + x[14] * x[19] - self.constants[9] * (x[24] + x[25])

        func[7] = x[10] * np.cos(x[20]) + x[0] - self.constants[0]
        func[8] = x[10] * np.sin(x[20]) + x[5] - self.constants[1]

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

        func[20] = x[26]*x[10]*np.sin(x[20] + x[15]) - (x[26] - x[27])*x[12]*np.sin(x[22]) - x[27]*x[13]*np.sin(x[23])
        func[21] = x[26]*x[10]*np.cos(x[20] + x[15]) - (x[26] - x[27])*x[12]*np.cos(x[22]) - x[27]*x[13]*np.cos(x[23])

        func[22] = (x[26] - self.constants[7])*x[11]*np.sin(x[21]) - (x[26] - x[27])*x[12]*np.sin(x[22] + x[17]) - (x[27] - self.constants[7])*x[14]*np.sin(self.constants[10] + x[19])
        func[23] = (x[26] - self.constants[7])*x[11]*np.cos(x[21]) - (x[26] - x[27])*x[12]*np.cos(x[22] + x[17]) - (x[27] - self.constants[7])*x[14]*np.cos(self.constants[10] + x[19])
        func[24] = x[27]*x[13] - (x[27] - self.constants[7])*x[14]

        func = list(map(lambda v: v**2, func))
        func = np.array(func)
        if return_f:
            return np.linalg.norm(func, norm), func
        return np.linalg.norm(func, norm)

    def findSolution(self, vec, norm=2):
        for _ in range(1, 500):
            gradient = np.zeros_like(vec)
            for j in range(len(vec)):
                epsilon = np.zeros_like(vec)
                epsilon[j] = back.EPS
                gradient[j] = (self.F(vec + epsilon) - self.F(vec - epsilon)) / (2 * back.EPS)
            vec -= back.OMI * gradient
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
])
vector = np.ones(28)


solver = TwoTierSolver(const=constants)
vector = solver.findSolution(vec=vector, norm=2)

f = solver.F(vector, return_f=True)

for i in range(len(f[1])):
    print(f"Уравнение {i}: {round(f[1][i], 3)}")

