import numpy as np
from numpy import sin, cos, pi
from PIL import Image
from matplotlib import pyplot as plt, patches as pth


class TwoTierSolver(object):

    def __init__(self, parameters: dict) -> None:
        self.parameters = parameters

    def F(self, vector, constants):
        x1, x2, x3, x4, x5 = vector[0:5]
        y1, y2, y3, y4, y5 = vector[5:10]
        r1, r2, r3, r4, r5 = vector[10:15]
        phi1, phi2, phi3, phi4, phi5 = vector[15:20]
        alpha1, alpha2, alpha3, alpha4, alpha5 = vector[20:25]
        p, Ax, Ay, Bx, By = constants[0:5]
        rt, rb, pt, pb = constants[9:13]
        phi1_nd, phi2_nd, phi3_nd, phiSum = constants[13:17]

        f = np.zeros(25)
        f[0] = r1 * phi1 - rt * phi1_nd
        f[1] = r2 * phi2 - rt * phi2_nd
        f[2] = r3 * phi3 - rt * phi3_nd
        f[3] = r4 * phi4 + r5 * phi5 - rb * phiSum

        f[4] = r1 * cos(alpha1) + x1 - Ax
        f[5] = r1 * sin(alpha1) + y1 - Ay

        f[6] = r2 * cos(phi2 + alpha2) + x2 - Bx
        f[7] = r2 * sin(phi2 + alpha2) + y2 - By

        f[8] = r3 * cos(alpha3 + phi3) + x3 - r2 * cos(alpha2) - x2
        f[9] = r3 * sin(alpha3 + phi3) + y3 - r2 * sin(alpha2) - y2
        f[10] = r3 * cos(alpha3 + phi3) + x3 - r5 * cos(alpha5 + phi5) - x5
        f[11] = r3 * sin(alpha3 + phi3) + y3 - r5 * sin(alpha5 + phi5) - y5

        f[12] = r1 * cos(alpha1 + phi1) + x1 - r3 * cos(alpha3) - x3
        f[13] = r1 * sin(alpha1 + phi1) + y1 - r3 * sin(alpha3) - y3
        f[14] = r1 * cos(alpha1 + phi1) + x1 - r4 * cos(alpha4) - x4
        f[15] = r1 * sin(alpha1 + phi1) + y1 - r4 * sin(alpha4) - y4

        f[16] = x4 - x5
        f[17] = -r4 + y4 + r5 - y5

        f[18] = pt * r1 * sin(alpha1 + phi1) - (pt - pb) * r3 * sin(alpha3) - pb * r4 * sin(alpha4)
        f[19] = -pt * r1 * cos(alpha1 + phi1) + (pt - pb) * r3 * cos(alpha3) + pb * r4 * cos(alpha4)

        f[20] = -(pt - p) * r2 * sin(alpha2) + (pt - pb) * r3 * sin(alpha3 + phi3) + (pb - p) * r5 * sin(alpha5 + phi5)
        f[21] = (pt - p) * r2 * cos(alpha2) - (pt - pb) * r3 * cos(phi3 + alpha3) - (pb - p) * r5 * cos(alpha5 + phi5)

        f[22] = pb * r4 - (pb - p) * r5
        f[23] = alpha4 - 3 * pi / 2 + phi4
        f[24] = alpha5 - 3 * pi / 2

        return f

    def calc_gradient(self, vector, constants):
        x1, x2, x3, x4, x5 = vector[0:5]
        y1, y2, y3, y4, y5 = vector[5:10]
        r1, r2, r3, r4, r5 = vector[10:15]
        phi1, phi2, phi3, phi4, phi5 = vector[15:20]
        alpha1, alpha2, alpha3, alpha4, alpha5 = vector[20:25]
        p, Ax, Ay, Bx, By = constants[0:5]
        rt, rb, pt, pb = constants[9:13]
        phi1_nd, phi2_nd, phi3_nd, phiSum = constants[13:17]

        gradient = np.zeros(25)

        # x1
        gradient[0] = 2 * (r1 * cos(alpha1) + x1 - Ax) \
                      + 2 * (r1 * cos(alpha1 + phi1) + x1 - r3 * cos(alpha3) - x3) \
                      + 2 * (r1 * cos(alpha1 + phi1) + x1 - r4 * cos(alpha4) - x4)
        # x2
        gradient[1] = 2 * (r2 * cos(phi2 + alpha2) + x2 - Bx) \
                      + 2 * (r3 * cos(alpha3 + phi3) + x3 - r2 * cos(alpha2) - x2) * (-1)

        # x3
        gradient[2] = 2 * (r3 * cos(alpha3 + phi3) + x3 - r2 * cos(alpha2) - x2) \
                      + 2 * (r3 * cos(alpha3 + phi3) + x3 - r5 * cos(alpha5 + phi5) - x5) \
                      + 2 * (r1 * cos(alpha1 + phi1) + x1 - r3 * cos(alpha3) - x3) * (-1)
        # x4
        gradient[3] = 2 * ( (x4 - x5)
                            - 2 * (r1 * cos(alpha1 + phi1) + x1 - r4 * cos(alpha4) - x4)
                            - 2 * (r3 * cos(alpha3 + phi3) + x3 - r5 * cos(alpha5 + phi5) - x5) )

        # x5
        gradient[4] = 0

        # --------------------------< Y >--------------------------------
        # y1
        gradient[5] = 2 * (r1 * sin(alpha1) + y1 - Ay) \
                      + 2 * (r1 * sin(alpha1 + phi1) + y1 - r3 * sin(alpha3) - y3) \
                      + 2 * (r1 * sin(alpha1 + phi1) + y1 - r4 * sin(alpha4) - y4)
        # y2
        gradient[6] = 2 * (r2 * sin(phi2 + alpha2) + y2 - By) \
                      + 2 * (r3 * sin(alpha3 + phi3) + y3 - r2 * sin(alpha2) - y2) * (-1)

        # y3
        gradient[7] = 2 * (r3 * sin(alpha3 + phi3) + y3 - r2 * sin(alpha2) - y2) \
                      + 2 * (r3 * sin(alpha3 + phi3) + y3 - r5 * sin(alpha5 + phi5) - y5) \
                      + 2 * (r1 * sin(alpha1 + phi1) + y1 - r3 * sin(alpha3) - y3) * (-1)

        # y4
        gradient[8] = 2 * ( (-r4 + y4 + r5 - y5)
                            - (r1 * sin(alpha1 + phi1) + y1 - r4 * sin(alpha4) - y4)
                            - (r3 * sin(alpha3 + phi3) + y3 - r5 * sin(alpha5 + phi5) - y5) )

        # y5
        gradient[9] = 0

        # --------------------------< R >--------------------------------
        # r1
        gradient[10] = 2 * (r1 * phi1 - rt * phi1_nd) * phi1 \
                      + 2 * (r1 * cos(alpha1) + x1 - Ax) * cos(alpha1) \
                      + 2 * (r1 * sin(alpha1) + y1 - Ay) * sin(alpha1) \
                      + 2 * (r1 * cos(alpha1 + phi1) + x1 - r3 * cos(alpha3) - x3) * cos(alpha1 + phi1) \
                      + 2 * (r1 * sin(alpha1 + phi1) + y1 - r3 * sin(alpha3) - y3) * sin(alpha1 + phi1) \
                      + 2 * (r1 * cos(alpha1 + phi1) + x1 - r4 * cos(alpha4) - x4) * cos(alpha1 + phi1) \
                      + 2 * (r1 * sin(alpha1 + phi1) + y1 - r4 * sin(alpha4) - y4) * sin(alpha1 + phi1) \
                      + 2 * (pt * r1 * sin(alpha1 + phi1) - (pt - pb) * r3 * sin(alpha3) - pb * r4 * sin(
                        alpha4)) * pt * sin(alpha1 + phi1) \
                      + 2 * (-pt * r1 * cos(alpha1 + phi1) + (pt - pb) * r3 * cos(alpha3) + pb * r4 * cos(alpha4)) * (
                        -pt) * cos(alpha1 + phi1)

        # r2
        gradient[11] = 2 * (r2 * phi2 - rt * phi2_nd) * phi2 \
                      + 2 * (r2 * cos(phi2 + alpha2) + x2 - Bx) * cos(phi2 + alpha2) \
                      + 2 * (r2 * sin(phi2 + alpha2) + y2 - By) * sin(phi2 + alpha2) \
                      + 2 * (r3 * cos(alpha3 + phi3) + x3 - r2 * cos(alpha2) - x2) * (-cos(alpha2)) \
                      + 2 * (r3 * sin(alpha3 + phi3) + y3 - r2 * sin(alpha2) - y2) * (-sin(alpha2)) \
                      + 2 * (-(pt - p) * r2 * sin(alpha2) + (pt - pb) * r3 * sin(alpha3 + phi3) + (pb - p) * r5 * sin(
                        alpha5 + phi5)) * (-sin(alpha2) * (pt - p)) \
                      + 2 * ((pt - p) * r2 * cos(alpha2) - (pt - pb) * r3 * cos(phi3 + alpha3) - (pb - p) * r5 * cos(
                        alpha5 + phi5)) * cos(alpha2) * (pt - p)

        # r3
        gradient[12] = 2 * (r3 * phi3 - rt * phi3_nd) * phi3 \
                       + 2 * (r3 * cos(alpha3 + phi3) + x3 - r2 * cos(alpha2) - x2) * cos(alpha3 + phi3) \
                       + 2 * (r3 * sin(alpha3 + phi3) + y3 - r2 * sin(alpha2) - y2) * sin(alpha3 + phi3) \
                       + 2 * (r3 * cos(alpha3 + phi3) + x3 - r5 * cos(alpha5 + phi5) - x5) * cos(alpha3 + phi3) \
                       + 2 * (r3 * sin(alpha3 + phi3) + y3 - r5 * sin(alpha5 + phi5) - y5) * sin(alpha3 + phi3) \
                       + 2 * (r1 * cos(alpha1 + phi1) + x1 - r3 * cos(alpha3) - x3) * (-cos(alpha3)) \
                       + 2 * (r1 * sin(alpha1 + phi1) + y1 - r3 * sin(alpha3) - y3) * sin(alpha3) \
                       + 2 * (pt * r1 * sin(alpha1 + phi1) - (pt - pb) * r3 * sin(alpha3) - pb * r4 * sin(alpha4)) * (
                        -sin(alpha3) * (pt - pb)) \
                       + 2 * (-pt * r1 * cos(alpha1 + phi1) + (pt - pb) * r3 * cos(alpha3) + pb * r4 * cos(alpha4)) * (
                         pt - pb) * cos(alpha3) \
                       + 2 * (-(pt - p) * r2 * sin(alpha2) + (pt - pb) * r3 * sin(alpha3 + phi3) + (pb - p) * r5 * sin(
                        alpha5 + phi5)) * (pt - pb) * sin(alpha3 + phi3) \
                       + 2 * ((pt - p) * r2 * cos(alpha2) - (pt - pb) * r3 * cos(phi3 + alpha3) - (pb - p) * r5 * cos(
                        alpha5 + phi5)) * (-cos(phi3 + alpha3) * (pt - pb))

        # r4
        gradient[13] = 2 * (r4 * phi4 + (pb * r4) / (pb - p) * phi5 - rb * phiSum) * (phi4 + pb / (pb - p) * phi5) \
                        + 2 * (r3 * cos(alpha3 + phi3) + x3 - (pb * r4) / (pb - p) * cos(alpha5 + phi5) - x5) * (-pb / (pb - p) * cos(alpha5 + phi5)) \
                       + 2 * (r3 * sin(alpha3 + phi3) + y3 - (pb * r4) / (pb - p) * sin(alpha5 + phi5) - (pb * r4) / (pb - p) + r4 - y4) * (-pb / (pb - p) * sin(alpha5 + phi5) - pb / (pb - p) + 1) \
                       + 2 * (r1 * cos(alpha1 + phi1) + x1 - r4 * cos(alpha4) - x4) * (-cos(alpha4)) \
                       + 2 * (r1 * sin(alpha1 + phi1) + y1 - r4 * sin(alpha4) - y4) * (-sin(alpha4)) \
                       + 2 * (pt * r1 * sin(alpha1 + phi1) - (pt - pb) * r3 * sin(alpha3) - pb * r4 * sin(alpha4)) * (-sin(alpha4) * pb) \
                       + 2 * (-pt * r1 * cos(alpha1 + phi1) + (pt - pb) * r3 * cos(alpha3) + pb * r4 * cos(alpha4)) * pb * cos(alpha4) \
                       + 2 * (-(pt - p) * r2 * sin(alpha2) + (pt - pb) * r3 * sin(alpha3 + phi3) + pb * r4 * sin(alpha5 + phi5)) * pb * sin(alpha5 + phi5) \
                       + 2 * ((pt - p) * r2 * cos(alpha2) - (pt - pb) * r3 * cos(phi3 + alpha3) - pb * r4 * cos(alpha5 + phi5)) * (-pb * cos(alpha5 + phi5))


        # r5
        gradient[14] = 0

        # --------------------------< Phi >--------------------------------
        # phi1
        gradient[15] = 2 * (r1 * phi1 - rt * phi1_nd) * r1 \
                       + 2 * (r1 * cos(alpha1 + phi1) + x1 - r3 * cos(alpha3) - x3) * (-r1 * sin(alpha1 + phi1)) \
                       + 2 * (r1 * sin(alpha1 + phi1) + y1 - r3 * sin(alpha3) - y3) * (r1 * cos(alpha1 + phi1)) \
                       + 2 * (r1 * cos(alpha1 + phi1) + x1 - r4 * cos(alpha4) - x4) * (-r1 * sin(alpha1 + phi1)) \
                       + 2 * (r1 * sin(alpha1 + phi1) + y1 - r4 * sin(alpha4) - y4) * (r1 * cos(alpha1 + phi1)) \
                       + 2 * (pt * r1 * sin(alpha1 + phi1) - (pt - pb) * r3 * sin(alpha3) - pb * r4 * sin(alpha4)) * (
                        pt * r1 * cos(alpha1 + phi1)) \
                       + 2 * (-pt * r1 * cos(alpha1 + phi1) + (pt - pb) * r3 * cos(alpha3) + pb * r4 * cos(alpha4)) * (
                        pt * r1 * sin(alpha1 + phi1))

        # phi2
        gradient[16] = 2 * (r2 * phi2 - rt * phi2_nd) * r2 \
                       + 2 * (r2 * cos(phi2 + alpha2) + x2 - Bx) * (-sin(phi2 + alpha2) * r2) \
                       + 2 * (r2 * sin(phi2 + alpha2) + y2 - By) * (cos(phi2 + alpha2) * r2)

        # phi3
        gradient[17] = 2 * (r3 * phi3 - rt * phi3_nd) * r3 \
                       + 2 * (r3 * cos(alpha3 + phi3) + x3 - r2 * cos(alpha2) - x2) * (-sin(alpha3 + phi3)) * r3 \
                       + 2 * (r3 * sin(alpha3 + phi3) + y3 - r2 * sin(alpha2) - y2) * (cos(alpha3 + phi3) * r3) \
                       + 2 * (r3 * cos(alpha3 + phi3) + x3 - r5 * cos(alpha5 + phi5) - x5) * (-sin(alpha3 + phi3) * r3) \
                       + 2 * (r3 * sin(alpha3 + phi3) + y3 - r5 * sin(alpha5 + phi5) - y5) * (cos(alpha3 + phi3) * r3) \
                       + 2 * (-(pt - p) * r2 * sin(alpha2) + (pt - pb) * r3 * sin(alpha3 + phi3) + (pb - p) * r5 * sin(
                        alpha5 + phi5)) * cos(alpha3 + phi3) * r3 * (pt - pb) \
                       + 2 * ((pt - p) * r2 * cos(alpha2) - (pt - pb) * r3 * cos(phi3 + alpha3) - (pb - p) * r5 * cos(
                        alpha5 + phi5)) * sin(phi3 + alpha3) * r3 * (pt - pb)

        # phi4
        gradient[18] = 2 * (alpha4 - 3 * pi / 2 + phi4) \
                       + 2 * (r4 * phi4 + r5 * phi5 - rb * phiSum) * r4 \
                       + 2 * (r1 * cos(alpha1 + phi1) + x1 - r4 * cos(3 * pi / 2 - phi4) - x4) * (-r4 * sin(3 * pi / 2 - phi4)) \
                       + 2 * (r1 * sin(alpha1 + phi1) + y1 - r4 * sin(3 * pi / 2 - phi4) - y4) * r4 * cos(3 * pi / 2 - phi4) \
                       + 2 * (pt * r1 * sin(alpha1 + phi1) - (pt - pb) * r3 * sin(alpha3) - pb * r4 * sin(3 * pi / 2 - phi4)) * pb * r4 * cos(3 * pi / 2 - phi4) \
                       + 2 * (-pt * r1 * cos(alpha1 + phi1) + (pt - pb) * r3 * cos(alpha3) + pb * r4 * cos(3 * pi / 2 - phi4)) * pb * r4 * sin(3 * pi / 2 - phi4)

        # phi5
        gradient[19] = 2 * (r4 * phi4 + r5 * phi5 - rb * phiSum) * r5 \
                       + 2 * (r3 * cos(alpha3 + phi3) + x3 - r5 * cos(alpha5 + phi5) - x5) * sin(alpha5 + phi5) * r5 \
                       + 2 * (r3 * sin(alpha3 + phi3) + y3 - r5 * sin(alpha5 + phi5) - y5) * (-cos(alpha5 + phi5)) * r5 \
                       + 2 * (-(pt - p) * r2 * sin(alpha2) + (pt - pb) * r3 * sin(alpha3 + phi3) + (pb - p) * r5 * sin(
                        alpha5 + phi5)) * cos(alpha5 + phi5) * (pb - p) * r5 \
                       + 2 * ((pt - p) * r2 * cos(alpha2) - (pt - pb) * r3 * cos(phi3 + alpha3) - (pb - p) * r5 * cos(
                        alpha5 + phi5)) * sin(alpha5 + phi5) * (pb - p) * r5

        # --------------------------< Alpha >--------------------------------
        # alpha1
        gradient[20] = 2 * (r1 * cos(alpha1) + x1 - Ax) * (-sin(alpha1)) * r1 \
                       + 2 * (r1 * sin(alpha1) + y1 - Ay) * cos(alpha1) * r1 \
                       + 2 * (r1 * cos(alpha1 + phi1) + x1 - r3 * cos(alpha3) - x3) * (-sin(alpha1 + phi1)) * r1 \
                       + 2 * (r1 * sin(alpha1 + phi1) + y1 - r3 * sin(alpha3) - y3) * cos(alpha1 + phi1) * r1 \
                       + 2 * (r1 * cos(alpha1 + phi1) + x1 - r4 * cos(alpha4) - x4) * (-sin(alpha1 + phi1) * r1) \
                       + 2 * (r1 * sin(alpha1 + phi1) + y1 - r4 * sin(alpha4) - y4) * cos(alpha1 + phi1) * r1 \
                       + 2 * (pt * r1 * sin(alpha1 + phi1) - (pt - pb) * r3 * sin(alpha3) - pb * r4 * sin(
                        alpha4)) * cos(alpha1 + phi1) * pt * r1 \
                       + 2 * (-pt * r1 * cos(alpha1 + phi1) + (pt - pb) * r3 * cos(alpha3) + pb * r4 * cos(
                        alpha4)) * sin(alpha1 + phi1) * pt * r1

        # alpha2
        gradient[21] = 2 * (r2 * cos(phi2 + alpha2) + x2 - Bx) * sin(phi2 + alpha2) * r2 * (-1) \
                       + 2 * (r2 * sin(phi2 + alpha2) + y2 - By) * (-cos(phi2 + alpha2)) * r2 * (-1) \
                       + 2 * (r3 * cos(alpha3 + phi3) + x3 - r2 * cos(alpha2) - x2) * sin(alpha2) * r2 \
                       + 2 * (r3 * sin(alpha3 + phi3) + y3 - r2 * sin(alpha2) - y2) * (-cos(alpha2)) * r2 \
                       + 2 * (-(pt - p) * r2 * sin(alpha2) + (pt - pb) * r3 * sin(alpha3 + phi3) + (pb - p) * r5 * sin(
                        alpha5 + phi5)) * (-cos(alpha2)) * r2 * (pt - p) \
                       + 2 * ((pt - p) * r2 * cos(alpha2) - (pt - pb) * r3 * cos(phi3 + alpha3) - (pb - p) * r5 * cos(
                        alpha5 + phi5)) * (-sin(alpha2)) * r2 * (pt - p)

        # alpha3
        gradient[22] = 2 * (r3 * cos(alpha3 + phi3) + x3 - r2 * cos(alpha2) - x2) * (-sin(alpha3 + phi3)) * r3 \
                       + 2 * (r3 * sin(alpha3 + phi3) + y3 - r2 * sin(alpha2) - y2) * cos(alpha3 + phi3) * r3 \
                       + 2 * (r3 * cos(alpha3 + phi3) + x3 - r5 * cos(alpha5 + phi5) - x5) * (-sin(alpha3 + phi3)) * r3 \
                       + 2 * (r3 * sin(alpha3 + phi3) + y3 - r5 * sin(alpha5 + phi5) - y5) * cos(alpha3 + phi3) * r3 \
                       + 2 * (r1 * cos(alpha1 + phi1) + x1 - r3 * cos(alpha3) - x3) * sin(alpha3) * r3 \
                       + 2 * (r1 * sin(alpha1 + phi1) + y1 - r3 * sin(alpha3) - y3) * (-cos(alpha3)) * r3 \
                       + 2 * (pt * r1 * sin(alpha1 + phi1) - (pt - pb) * r3 * sin(alpha3) - pb * r4 * sin(alpha4)) * (
                        -cos(alpha3)) * (pt - pb) * r3 \
                       + 2 * (-pt * r1 * cos(alpha1 + phi1) + (pt - pb) * r3 * cos(alpha3) + pb * r4 * cos(alpha4)) * (
                        -sin(alpha3)) * (pt - pb) * r3 \
                       + 2 * (-(pt - p) * r2 * sin(alpha2) + (pt - pb) * r3 * sin(alpha3 + phi3) + (pb - p) * r5 * sin(
                        alpha5 + phi5)) * cos(alpha3 + phi3) * r3 * (pt - pb) \
                       + 2 * ((pt - p) * r2 * cos(alpha2) - (pt - pb) * r3 * cos(phi3 + alpha3) - (pb - p) * r5 * cos(
                        alpha5 + phi5)) * sin(phi3 + alpha3) * r3 * (pt - pb)

        # alpha4
        gradient[23] = 0

        # alpha5
        gradient[24] = 0

        return gradient

    def gradient_descent(self, vector, constants, logger, learn_rate=0.0005, tolerance=1e-3):
        stop = 300000
        for heatstop in range(stop):
            gradient = self.calc_gradient(vector, constants)

            x4 = vector[3]
            y4 = vector[8]
            r4 = vector[13]
            p, pb = constants[0], constants[12]
            phi4 = vector[18]

            vector[23] = 3*pi/2 - phi4 # alpha4
            vector[24] = 3*pi/2 # alpha5
            vector[14] = (pb*r4) / (pb - p) # r5
            r5 = vector[14]
            vector[9] = r5 - r4 + y4 # y5
            vector[4] = x4 # x5

            for i in range(len(vector)):
                vector[i] -= learn_rate*gradient[i]

            if np.linalg.norm(self.F(vector, constants), 2) < tolerance:
                return vector
            if heatstop % 1000 == 0:
                logger(f"[{heatstop}] Error = {np.linalg.norm(self.F(vector, constants), 2)}")
        logger("Heatstop", "warning")
        return vector

    def makePlot(self, vector, constants):

        x1, x2, x3, x4, x5 = vector[0:5]
        y1, y2, y3, y4, y5 = vector[5:10]
        r1, r2, r3, r4, r5 = vector[10:15]
        phi1, phi2, phi3, phi4, phi5 = vector[15:20]
        alpha1, alpha2, alpha3, alpha4, alpha5 = vector[20:25]
        Ax, Ay, Bx, By = constants[1:5]

        # init PLT
        fig, axs = plt.subplots(figsize=(5, 5))
        axs.grid(linestyle='--')
        axs.set_aspect('equal')

        # Line AB
        axs.plot(
            (Ax, Bx),
            (Ay, By),
            color="black"
        )

        arcad = pth.Arc(
            xy=(x1, y1),
            width=r1*2,
            height=r1*2,
            angle=0,
            theta1=np.rad2deg(alpha1),
            theta2=np.rad2deg(alpha1) + np.rad2deg(phi1),

        )
        axs.add_patch(arcad)
        arccb = pth.Arc(
            xy=(x2, y2),
            width=r2 * 2,
            height=r2 * 2,
            angle=0,
            theta1=np.rad2deg(alpha2),
            theta2=np.rad2deg(alpha2) + np.rad2deg(phi2),

        )
        axs.add_patch(arccb)
        arcdc = pth.Arc(
            xy=(x3, y3),
            width=r3 * 2,
            height=r3 * 2,
            angle=0,
            theta1=np.rad2deg(alpha3),
            theta2=np.rad2deg(alpha3) + np.rad2deg(phi3),

        )
        axs.add_patch(arcdc)
        arcde = pth.Arc(
            xy=(x4, y4),
            width=r4 * 2,
            height=r4 * 2,
            angle=0,
            theta1=np.rad2deg(alpha4),
            theta2=np.rad2deg(alpha4) + np.rad2deg(phi4),

        )
        axs.add_patch(arcde)
        arcec = pth.Arc(
            xy=(x5, y5),
            width=r5 * 2,
            height=r5 * 2,
            angle=0,
            theta1=np.rad2deg(alpha5),
            theta2=np.rad2deg(alpha5) + np.rad2deg(phi5),

        )
        axs.add_patch(arcec)

        # plt.show()

        # Convert to GIF format
        fig.savefig("saved_parameters/temp.png")
        im = Image.open("saved_parameters/temp.png")
        im.save("saved_parameters/temp.gif")