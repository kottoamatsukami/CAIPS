# import tracking_dynamics
from matplotlib import pyplot as plt
from celluloid import Camera
import numpy as np


class Animation:

    def draw_arc(self, values: float or int, ax) -> None:
        # -----------------------------------
        # structure
        # values = {
        # values_1 : x1_0 = 0
        # values_2 : x2_0 = 0
        # values_3 : y_0 = Ay = By
        # values_4 : phi1_0 = 0
        # values_5 : phi2_0 = 0
        # values_6 : Ax = from user
        # values_7 : Ay = from user
        # values_8 : Bx = from user
        # values_9 : By = from user
        # }
        # -----------------------------------
        arc_x = values[5]
        arc_y = values[2] / 2
        arc_width = None
        arc_height = values[2]
        arc_theta1 = None
        arc_theta2 = None

    def create_animation(self, data: float or int) -> float or int:
        # -----------------------------------
        # structure
        # data = {
        # data_1 : x1_0 = 0
        # data_2 : x2_0 = 0
        # data_3 : y_0 = Ay = By
        # data_4 : phi1_0 = 0
        # data_5 : phi2_0 = 0
        # data_6 : Ax = from user
        # data_7 : Ay = from user
        # data_8 : Bx = from user
        # data_9 : By = from user
        # }
        # -----------------------------------
        x = np.linspace(-5, 5, 100)
        fig = plt.figure()
        ax = plt.subplot()
        plt.grid(linestyle='--')
        # fig, ax = plt.subplots()
        camera = Camera(fig)

        ax.set(xlim=[-0.4, 0.4],
               ylim=[0, 0.4],
               title='Pneumatic Structure Animation',
               xlabel='x',
               ylabel='y')
        ax.set_aspect("equal")

        for i in range(0, 250):
            plt.hlines(0, data[i][0], data[i][1])
            plt.hlines(data[i][2], data[i][5], data[i][7])

            camera.snap()
        animation = camera.animate()
        plt.show()


