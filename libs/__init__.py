import math  # Working with the math library

STD_SETTINGS = {
    "width": 1200,
    "height": 800,
    "min_width": 1200,
    "min_height": 800,
    "title": "CAIPS - Simulation",
    "small_icon_path": "front/icons/wing_small.ico",
    "large_icon_path": "front/icons/wing_large.ico",
}

STD_PARAMETERS = {
            "Ax": 0,
            "Ay": 0.95*2,
            "Bx": 0.3*2,
            "By": 0.65*2,
            "Rt": 0.30 * 2,
            "Rb": 0.19 * 2,
            "Pt0": 12000 * 2,
            "Pb0": 4000 * 2,
            "Xtop": 0,
            "Ytop": 0.65 * 2,
            "Xbot": 0,
            "Ybot": 0.22 * 2,
            "alpha5": 3*math.pi/2,
}