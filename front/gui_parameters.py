import math

# -----------------
# Play (Process) Button
# -----------------
play_button_path = "./front/img/play_button.png"
play_button_width = 90
play_button_height = 90
play_button_x_padding = 45
play_button_y_padding = 90

# --------
# Menu Bar
# --------
current_mode_arrow = "<--"
first_mode = "(1) Determine the shape of a single-cavity air cushion "
second_mode = "(2) Bouncing air cushion "
third_mode = "(3) Double-deck air cushion with side pressure "

# ---------
# Side Menu
# ---------
sm_background = True
sm_scrollbar = False
sm_width = 500
sm_height = 500

slider_Ax = (-10, 10)
slider_Ay = (-10, 10)
slider_Bx = (-10, 10)
slider_By = (-10, 10)
slider_Xtop = (-10, 10)
slider_Ytop = (-10, 10)
slider_Xbot = (-10, 10)
slider_Ybot = (-10, 10)
slider_Rt = (-10, 10)
slider_Rb = (-10, 10)
slider_Pt0 = (0, 100000)
slider_Pb0 = (0, 100000)
slider_Pac = (0, 100000)
slider_alpha5 = (0, math.pi*2)

# -----------
# Canvas Menu
# -----------
cm_background = False
cm_scrollbar = True
cm_width = 500
cm_height = 500


# -----------
# Node System
# -----------
ns_float_node_size = 150
ns_parameter_node_size = 150
ns_x_padding = 500
ns_y_padding = 75

# ----------
# WARNING! ONLY FOR SCRIPT
# ----------
W_count_of_float_nodes = "0"
