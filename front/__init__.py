import os

import dearpygui.dearpygui as dpg
from dearpygui_ext import logger
from back import establishing_solver
import math


class GUI:
    def __init__(self, settings: dict, debug_mode=False):
        self.settings = settings
        self.debug_mode = debug_mode
        self.log = False
        self.logger = None
        self.current_mode = 1
        self.parameters = {
            "Ax": 0,
            "Ay": 0.95 * 2,
            "Bx": 0.30 * 2,
            "By": 0.65 * 2,
            "Rt": 0.30 * 2,
            "Rb": 0.19 * 2,
            "Pt0": 12000 * 2,
            "Pb0": 4000 * 2,
            "Pac": 2000,
            "Xtop": 0,
            "Ytop": 0.65 * 2,
            "Xbot": 0,
            "Ybot": 0.22 * 2,
            "alpha5": 3*math.pi/2,
        }

    def run(self):
        # ------------------------
        # Initialize the dearpygui
        # ------------------------
        dpg.create_context()
        dpg.create_viewport(
            title=self.settings["title"],
            height=self.settings["height"],
            width=self.settings["width"],
            small_icon="front/icons/wing_small.ico",
            large_icon="front/icons/wing_large.ico",
            min_width=self.settings["min_width"],
            min_height=self.settings["min_height"],
        )

        if self.debug_mode:
            dpg.show_debug()
            dpg.show_metrics()
            dpg.show_style_editor()

        # Main window
        with dpg.window(tag="Primary Window"):

            # Process Button
            width, height, channels, data = dpg.load_image("./front/img/play_button.png")
            with dpg.texture_registry():
                dpg.add_static_texture(width=width, height=height, default_value=data, tag="Process Button")
            dpg.add_image_button(
                texture_tag="Process Button",
                width=90,
                height=90,
                pos=(
                    dpg.get_viewport_width()//2 - 45,
                    dpg.get_viewport_height()//2 - 90,
                ),
                tag="Play_button",
                callback=self.callback_play_button,
            )

            # Menu bar
            with dpg.menu_bar():
                with dpg.menu(label="Options"):
                    dpg.add_menu_item(label="Nodes", callback=self.callback_graph_editor)
                    dpg.add_menu_item(label="Save Parameters (Ctrl+S)")
                    dpg.add_menu_item(label="Load Parameters (Ctrl+L)")
                    dpg.add_menu_item(label="Credits")

                with dpg.menu(label="Themes"):
                    dpg.add_menu_item(label="Theme editor", callback=self.callback_show_theme_editor)

                with dpg.menu(label="Tools"):
                    dpg.add_menu_item(label="Show Logger", callback=self.callback_show_logger)
                    dpg.add_menu_item(label="Show About")

                with dpg.menu(label="Mode"):
                    dpg.add_menu_item(
                        label="(1) Determine the shape of a single-cavity air cushion <--",
                        callback=self.callback_set_mode,
                        id="mode 1",
                    )
                    dpg.add_menu_item(
                        label="(2) Bouncing air cushion",
                        callback=self.callback_set_mode,
                        id="mode 2",
                    )
                    dpg.add_menu_item(
                        label="(3) Double-deck air cushion with side pressure",
                        callback=self.callback_set_mode,
                        id="mode 3",
                    )

            with dpg.window(
                    no_resize=True,
                    no_move=True,
                    no_close=True,
                    no_title_bar=True,
                    no_scrollbar=True,
                    width=500,
                    height=500,
                    tag="Side_menu",
                ):
                dpg.add_text(label="side menu", default_value="Parameters")
                dpg.add_slider_double(label="Ax", tag="slider_Ax",
                                      min_value=-10, max_value=10,
                                      default_value=self.parameters["Ax"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Ay", tag="slider_Ay",
                                      min_value=-10, max_value=10,
                                      default_value=self.parameters["Ay"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Bx", tag="slider_Bx",
                                      min_value=-10, max_value=10,
                                      default_value=self.parameters["Bx"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="By", tag="slider_By",
                                      min_value=-10, max_value=10,
                                      default_value=self.parameters["By"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Xtop", tag="slider_Xtop",
                                      min_value=-10, max_value=10,
                                      default_value=self.parameters["Xtop"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Ytop", tag="slider_Ytop",
                                      min_value=-10, max_value=10,
                                      default_value=self.parameters["Ytop"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Xbot", tag="slider_Xbot",
                                      min_value=-10, max_value=10,
                                      default_value=self.parameters["Xbot"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Ybot", tag="slider_Ybot",
                                      min_value=-10, max_value=10,
                                      default_value=self.parameters["Ybot"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Rt", tag="slider_Rt",
                                      min_value=-10, max_value=10,
                                      default_value=self.parameters["Rt"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Rb", tag="slider_Rb",
                                      min_value=-10, max_value=10,
                                      default_value=self.parameters["Rb"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Pt0", tag="slider_Pt0",
                                      min_value=-50000, max_value=50000,
                                      default_value=self.parameters["Pt0"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Pb0", tag="slider_Pb0",
                                      min_value=-10000, max_value=10000,
                                      default_value=self.parameters["Pb0"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Pac", tag="slider_Pac",
                                      min_value=-10000, max_value=10000,
                                      default_value=self.parameters["Pac"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="alpha5", tag="slider_alpha5",
                                      min_value=0, max_value=360,
                                      default_value=self.parameters["alpha5"],
                                      callback=self.universal_slider_callback)

            with dpg.window(
                    no_resize=True,
                    no_move=True,
                    no_close=True,
                    no_title_bar=True,
                    no_scrollbar=True,
                    width=500,
                    height=500,
                    tag="Canvas_window",
            ):
                dpg.add_text(default_value="Canvas")
                with dpg.drawlist(
                    width=500,
                    height=500,
                    tag="canvas",
                ):
                    dpg.draw_line(0, 5)

        dpg.setup_dearpygui()

        dpg.set_viewport_resize_callback(self.callback_resize_viewport_window)
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()

        dpg.destroy_context()

    def _init_std_settings(self):
        None

    @staticmethod
    def callback_resize_viewport_window():
        dpg.set_item_pos(
            item="Side_menu",
            pos=(
                dpg.get_viewport_width() - dpg.get_item_width(item="Side_menu"),
                dpg.get_viewport_height()//2 - dpg.get_item_height(item="Side_menu")//2,
            ),
        )
        dpg.set_item_pos(
            item="Canvas_window",
            pos=(
                0,
                dpg.get_viewport_height()//2 - dpg.get_item_height(item="Canvas_window")//2,
            ),
        )

        dpg.set_item_pos(
            item="Play_button",
            pos=(
                dpg.get_viewport_width() // 2 - dpg.get_item_width(item="Play_button")//2,
                dpg.get_viewport_height() // 2 - dpg.get_item_height(item="Play_button"),
            ),
        )

    def callback_show_logger(self):
        self.log = True
        self.logger = logger.mvLogger()
        self.log_message("Starting log...")

    def log_message(self, msg: str, type_="info"):
        # "type_ can be either 'info', 'warning' or 'critical'"
        if self.log and type_ in ["info", "warning", "critical"]:
            if type_ == "info":
                self.logger.log_info(msg)
            if type_ == "warning":
                self.logger.log_warning(msg)
            if type_ == "critical":
                self.logger.log_critical(msg)

    # -----------------
    # Theme Callbacks
    # -----------------
    def callback_show_theme_editor(self):
        # Load fonts
        with dpg.font_registry():
            for font in os.listdir("./front/fonts"):
                if font.endswith(".ttf") or font.endswith(".otf"):
                    dpg.add_font(
                        file="./front/fonts/" + font,
                        size=20
                    )
                    self.log_message(msg=f"Font {font} was added to theme editor", type_="info")
                else:
                    self.log_message(msg=f"Unknown type of file: {font}", type_="warning")
        dpg.show_style_editor()

    # ------------------
    # Menu Bar Callbacks
    # ------------------
    def callback_set_mode(self, sender):
        # Remove old using
        old = "mode " + str(self.current_mode)
        dpg.set_item_label(
            item=old,
            label=dpg.get_item_label(
                item=old,
            ).replace("<--", "").strip()
        )
        # Add new using
        self.current_mode = int(sender[-1])
        dpg.set_item_label(
            item=sender,
            label=dpg.get_item_label(
                item=sender,
            ).replace("<--", "").strip() + " <--"
        )
        # Logging
        self.log_message(
            msg=f"Change script mode from <{old}> to <{sender}>",
            type_="info",
        )
    # -----------------
    # Play Button callback
    # -----------------
    def callback_play_button(self, sender):
        # Determine target mode

        if self.current_mode == 1:
            # 4 score
            vector = [
                    0,  # x1
                    0,  # x2
                    0,  # y
                    0,  # phi1
                    0,  # phi2
                    self.parameters["Ax"],
                    self.parameters["Ay"],
                    self.parameters["Bx"],
                    self.parameters["By"],
                    0, # C
                ]
            solver = establishing_solver.EstablishingSolverV4()
            self.log_message(f"Used following vector: {vector}")
            self.log_message("Started calculating for first mode...")
            solution = solver.establish(values=vector, logger=self.log_message)

            print(solution)
        else:
            self.log_message(
                msg="BRANCH NOT IMPLEMENTED",
                type_="critical",
            )

    # -----------------
    # Sliders Callbacks
    # -----------------

    def universal_slider_callback(self, sender, app_data):
        user_data = dpg.get_item_label(sender)
        self.log_message(msg=f"Slider {user_data} [{self.parameters[user_data]:.3f}] -> [{app_data:.3f}]", type_="info")
        self.parameters[user_data] = app_data

    # -----------------
    # Node Graph
    # -----------------
    def callback_graph_editor(self):
        with dpg.window(
                label="Options",
                width=dpg.get_viewport_width()//1.5,
                height=dpg.get_viewport_height()//1.5,
                pos=(0, 0),

        ):
            with dpg.node_editor(callback=self.callback_link_node, delink_callback=self.callback_unlink_node):
                with dpg.node(label="Ax"):
                    with dpg.node_attribute(label="Node A1"):
                        dpg.add_input_float(label="F1", width=150)

    def callback_link_node(self, sender, app_data):
        None

    def callback_unlink_node(self, sender, app_data):
        None