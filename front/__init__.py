import os
import libs
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pickle
import time
import numpy
import dearpygui.dearpygui as dpg
import front.gui_parameters as gp
from dearpygui_ext import logger
from back import establishing_solver, tracking_dynamics, two_tier_air_cushion
from PIL import Image, ImageSequence
import numpy as np


class GUI(object):
    def __init__(self, settings: dict, debug_mode=False) -> None:
        self.do_log = False
        self.logger = None
        self.settings = settings
        self.debug_mode = debug_mode
        self.current_mode = 1
        self.root = os.getcwd()
        self.parameters = libs.STD_PARAMETERS

    def run(self):
        # ------------------------
        # Initialize the dearpygui
        # ------------------------
        dpg.create_context()
        dpg.create_viewport(
            title=self.settings["title"],
            height=self.settings["height"],
            width=self.settings["width"],
            small_icon=self.settings["small_icon_path"],
            large_icon=self.settings["large_icon_path"],
            min_width=self.settings["min_width"],
            min_height=self.settings["min_height"],
        )
        # Enable debug info
        if self.debug_mode:
            dpg.show_debug()
            dpg.show_metrics()
            dpg.show_style_editor()

        # Generate Main window
        with dpg.window(tag="Primary Window"):
            # Process Button
            width, height, channels, data = dpg.load_image(gp.play_button_path)
            with dpg.texture_registry():
                dpg.add_static_texture(width=width, height=height, default_value=data, tag="Process Button")

            dpg.add_image_button(
                texture_tag="Process Button",
                width=gp.play_button_width,
                height=gp.play_button_height,
                pos=(
                    dpg.get_viewport_width() // 2 - gp.play_button_x_padding,
                    dpg.get_viewport_height() // 2 - gp.play_button_y_padding,
                ),
                tag="Play_Button",
                callback=self.callback_play_button,
            )

            # Menu bar
            with dpg.menu_bar():
                with dpg.menu(label="Options"):
                    dpg.add_menu_item(
                        label="Nodes",
                        callback=self.callback_graph_editor
                    )
                    dpg.add_menu_item(
                        label="Save Parameters",
                        callback=self.callback_save_parameters
                    )
                    dpg.add_menu_item(
                        label="Load Parameters",
                        callback=self.callback_load_parameters
                    )
                    dpg.add_menu_item(
                        label="Open Last GIF",
                        callback=self.callback_open_last_gif,
                    )
                    dpg.add_menu_item(
                        label="Credits",
                        callback=self.callback_show_credits,
                    )

                with dpg.menu(label="Themes"):
                    dpg.add_menu_item(label="Theme editor", callback=self.callback_show_theme_editor)

                with dpg.menu(label="Tools"):
                    dpg.add_menu_item(label="Show Logger", callback=self.callback_show_logger)
                    dpg.add_menu_item(label="Show About")

                with dpg.menu(label="Mode"):
                    dpg.add_menu_item(
                        label=gp.first_mode + (gp.current_mode_arrow
                                               if self.current_mode == 1
                                               else ""),
                        callback=self.callback_set_mode,
                        id="mode 1",
                    )
                    dpg.add_menu_item(
                        label=gp.second_mode + (gp.current_mode_arrow
                                                if self.current_mode == 2
                                                else ""),
                        callback=self.callback_set_mode,
                        id="mode 2",
                    )
                    dpg.add_menu_item(
                        label=gp.third_mode + (gp.current_mode_arrow
                                               if self.current_mode == 3
                                               else ""),
                        callback=self.callback_set_mode,
                        id="mode 3",
                    )

            with dpg.window(
                    no_resize=True,
                    no_move=True,
                    no_close=True,
                    no_title_bar=True,
                    no_scrollbar=gp.sm_scrollbar,
                    no_background=gp.sm_background,
                    width=gp.sm_width,
                    height=gp.sm_height,
                    tag="Side_menu",
            ):
                dpg.add_text(label="side menu", default_value="Parameters")
                dpg.add_slider_double(label="Ax", tag="slider_Ax",
                                      min_value=gp.slider_Ax[0], max_value=gp.slider_Ax[1],
                                      default_value=self.parameters["Ax"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Ay", tag="slider_Ay",
                                      min_value=gp.slider_Ay[0], max_value=gp.slider_Ay[1],
                                      default_value=self.parameters["Ay"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Bx", tag="slider_Bx",
                                      min_value=gp.slider_Bx[0], max_value=gp.slider_Bx[1],
                                      default_value=self.parameters["Bx"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="By", tag="slider_By",
                                      min_value=gp.slider_By[0], max_value=gp.slider_By[1],
                                      default_value=self.parameters["By"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Xtop", tag="slider_Xtop",
                                      min_value=gp.slider_Xtop[0], max_value=gp.slider_Xtop[1],
                                      default_value=self.parameters["Xtop"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Ytop", tag="slider_Ytop",
                                      min_value=gp.slider_Ytop[0], max_value=gp.slider_Ytop[1],
                                      default_value=self.parameters["Ytop"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Xbot", tag="slider_Xbot",
                                      min_value=gp.slider_Xbot[0], max_value=gp.slider_Xbot[1],
                                      default_value=self.parameters["Xbot"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Ybot", tag="slider_Ybot",
                                      min_value=gp.slider_Ybot[0], max_value=gp.slider_Ybot[1],
                                      default_value=self.parameters["Ybot"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Rt", tag="slider_Rt",
                                      min_value=gp.slider_Rt[0], max_value=gp.slider_Rt[1],
                                      default_value=self.parameters["Rt"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Rb", tag="slider_Rb",
                                      min_value=gp.slider_Rb[0], max_value=gp.slider_Rb[1],
                                      default_value=self.parameters["Rb"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Pt0", tag="slider_Pt0",
                                      min_value=gp.slider_Pt0[0], max_value=gp.slider_Pt0[1],
                                      default_value=self.parameters["Pt0"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="Pb0", tag="slider_Pb0",
                                      min_value=gp.slider_Pb0[0], max_value=gp.slider_Pb0[1],
                                      default_value=self.parameters["Pb0"],
                                      callback=self.universal_slider_callback)
                dpg.add_slider_double(label="alpha5", tag="slider_alpha5",
                                      min_value=gp.slider_alpha5[0], max_value=gp.slider_alpha5[1],
                                      default_value=self.parameters["alpha5"],
                                      callback=self.universal_slider_callback)

                dpg.add_tab_bar()
                dpg.add_text("Set the exact values: <name> <value> <$>")
                dpg.add_input_text(callback=self.callback_set_parameter)
                self.callback_set_mode("mode 1")

            with dpg.window(
                    no_resize=True,
                    no_move=True,
                    no_close=True,
                    no_title_bar=True,
                    no_background=gp.cm_background,
                    no_scrollbar=gp.cm_scrollbar,
                    width=gp.cm_width,
                    height=gp.cm_height,
                    tag="Canvas_window",
                    pos=(
                        0,
                        dpg.get_viewport_height() // 2 - gp.cm_height // 2,
                    )
            ):
                dpg.add_text(default_value="Canvas")
                self.init_canvas()
                dpg.add_image("current image")

        dpg.setup_dearpygui()

        dpg.set_viewport_resize_callback(self.callback_resize_viewport_window)
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()

        dpg.destroy_context()

    @staticmethod
    def callback_resize_viewport_window():
        dpg.set_item_pos(
            item="Side_menu",
            pos=(
                dpg.get_viewport_width() - dpg.get_item_width(item="Side_menu"),
                dpg.get_viewport_height() // 2 - dpg.get_item_height(item="Side_menu") // 2,
            ),
        )
        dpg.set_item_pos(
            item="Canvas_window",
            pos=(
                0,
                dpg.get_viewport_height() // 2 - dpg.get_item_height(item="Canvas_window") // 2,
            ),
        )

        dpg.set_item_pos(
            item="Play_Button",
            pos=(
                dpg.get_viewport_width() // 2 - dpg.get_item_width(item="Play_Button") // 2,
                dpg.get_viewport_height() // 2 - dpg.get_item_height(item="Play_Button"),
            ),
        )

    def callback_show_logger(self):
        self.do_log = True
        self.logger = logger.mvLogger()
        self.log_message("Starting log...")

    def log_message(self, msg: str, type_="info"):
        # "type_ can be either 'info', 'warning' or 'critical'"
        if self.do_log and type_ in ["info", "warning", "critical"]:
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
            for font in os.listdir(os.path.join(self.root, "front/fonts")):
                if font.endswith(".ttf") or font.endswith(".otf"):
                    dpg.add_font(
                        file=os.path.join(self.root, "front/fonts", font),
                        size=20
                    )
                    self.log_message(msg=f"Font {font} was added to theme editor", type_="info")
                else:
                    self.log_message(msg=f"Unknown type of file: {font}", type_="warning")
        dpg.show_style_editor()

    # -----------------
    # Post Slider Input
    # -----------------
    def callback_set_parameter(self, sender, value):
        if len(value.split()) == 3:
            variable, value, end = value.split()
            if end != "$":
                return
            if variable not in self.parameters.keys():
                self.log_message(msg=f"Unknown parameter: {variable}", type_="warning")
            else:
                self.universal_slider_callback(
                    sender="slider_" + variable,
                    app_data=float(value),
                )

    # ------------------
    # Menu Bar Callbacks
    # ------------------

    def slider_intersection(self, req: list):
        for slider_type in self.parameters.keys():
            if slider_type in req:
                dpg.show_item(
                    item=f"slider_{slider_type}"
                )
            else:
                dpg.hide_item(
                    item=f"slider_{slider_type}"
                )

    def callback_set_mode(self, sender):
        # Remove old using
        old = "mode " + str(self.current_mode)
        dpg.set_item_label(
            item=old,
            label=dpg.get_item_label(
                item=old,
            ).replace(gp.current_mode_arrow, "").strip()
        )
        # Add new using
        self.current_mode = int(sender[-1])
        dpg.set_item_label(
            item=sender,
            label=dpg.get_item_label(
                item=sender,
            ).replace(gp.current_mode_arrow, "").strip() + " " + gp.current_mode_arrow
        )
        if self.current_mode == 1 or self.current_mode == 2:
            self.slider_intersection(
                req=["Ax", "Ay", "Bx", "By"]
            )
        else:
            self.slider_intersection(
                req=["Ax", "Ay", "Bx", "By", "Xtop", "Ytop", "Xbot", "Ybot", "Rt", "Rb"]
            )

        # Logging
        self.log_message(
            msg=f"Change script mode from <{old}> to <{sender}>",
            type_="info",
        )

    def callback_save_parameters(self):
        Tk().withdraw()
        path = asksaveasfilename(
            initialdir=self.root,
        )
        if len(path) == 0:
            return
        path = path.replace(".caips", "")
        with open(path + ".caips", "wb") as f:
            pickle.dump(self.parameters, f)
            self.log_message("Successfully saved parameters")

    def callback_load_parameters(self):
        Tk().withdraw()
        path = askopenfilename(
            initialdir=self.root,
        )
        if len(path) == 0:
            return
        if os.path.exists(path) and len(path) > 0:
            if path.endswith(".caips"):
                with open(path, "rb") as f:
                    self.parameters = pickle.load(f)
                    for key in self.parameters.keys():
                        self.update_slider(
                            sender="slider_" + key,
                            value=self.parameters[key],
                        )
                    self.log_message("Successfully loaded new parameters")

            else:
                self.log_message(
                    msg=f"Unknown file extension: {path}",
                    type_="critical",
                )
        else:
            self.log_message(
                msg=f"Unknown file path: {path}",
                type_="critical",
            )

    def callback_open_last_gif(self):
        if os.path.exists("saved_parameters/temp.gif"):
            self.update_canvas(
                gif_path="saved_parameters/temp.gif")

    @staticmethod
    def callback_show_credits():
        import webbrowser
        webbrowser.open(
            url="https://github.com/kottoamatsukami/CAIPS/graphs/contributors"
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
                0,  # C
            ]
            solver = establishing_solver.EstablishingSolver(parameters=self.parameters)
            self.log_message(f"Used following vector: {vector}")
            self.log_message("Started calculating for first mode...")
            solution = solver.establish(values=vector, logger=self.log_message)
            solver.make_animation(solution)

        elif self.current_mode == 2:
            # 6 score
            vector = [
                0,                      # x1
                0,                      # x2
                self.parameters["Ay"],  # y
                0,                      # phi1
                0,                      # phi2
                self.parameters["Ax"],  # Ax
                self.parameters["Ay"],  # Ay
                self.parameters["Bx"],  # Bx
                self.parameters["By"],  # By
                3*numpy.pi/8,           # C
                0                       # Vy
            ]
            solver = tracking_dynamics.DynamicsSolver(self.parameters)
            self.log_message(f"Used following vector: {vector}")
            self.log_message("Started calculating for second mode...")
            solution = solver.find_solution(values=vector, logger=self.log_message)
            solver.make_animation(solution)

        else:
            # 9 score
            constants = np.zeros(17)
            constants[0] = 2.0  # p
            constants[1] = self.parameters['Ax']  # Ax
            constants[2] = self.parameters['Ay']  # Ay
            constants[3] = self.parameters['Bx']  # Bx
            constants[4] = self.parameters['By']  # By
            constants[5] = self.parameters['Xtop']  # xTop
            constants[6] = self.parameters['Ytop']  # yTop
            constants[7] = self.parameters['Xbot']  # xBot
            constants[8] = self.parameters['Ybot']  # yBot
            constants[9] = self.parameters['Rt']  # rt
            constants[10] = self.parameters['Rb']  # rb
            constants[11] = 24.0  # pt
            constants[12] = 8.0  # pb
            constants[13] = 2.753364902  # phiNd1
            constants[14] = 1.182568575  # phiNd2
            constants[15] = 0.776455503  # phiNd3
            constants[16] = 5.001905970  # phiSum

            vector = np.array([-0.09873235, -0.08371553, -0.01807103, -0.25989637, -0.25989644,  1.34486033,
                              1.45343776,  1.77163468,  0.4914802,   0.60352888,  0.56418933,  0.70054672,
                              0.99360681,  0.33614595,  0.4481946,   2.9280291,   1.01325743,  0.468752,
                              2.98332936,  2.00351769,  1.39454183,  5.04875036,  4.41082301,  1.7290595,
                              4.71238898])

            solver = two_tier_air_cushion.TwoTierSolver(self.parameters)
            self.log_message(f"Used following vector: {constants}")
            self.log_message("Started calculating for third mode...")
            solution = solver.gradient_descent(vector, constants, self.log_message, learn_rate=0.0007)
            solver.makePlot(vector=solution, constants=constants)

        # Draw in Canvas
        self.update_canvas(
            "saved_parameters/temp.gif",
        )
    # -----------------
    # Sliders Callbacks
    # -----------------
    @staticmethod
    def update_slider(sender, value):
        dpg.set_value(sender, value)

    def universal_slider_callback(self, sender, app_data):
        user_data = dpg.get_item_label(sender)
        self.update_slider(sender, app_data)
        self.log_message(msg=f"Slider {user_data} [{self.parameters[user_data]:.3f}] -> [{app_data:.3f}]", type_="info")
        self.parameters[user_data] = app_data

    # -----------------
    # Node Graph
    # -----------------
    def callback_graph_editor(self):
        if dpg.does_item_exist("Node Editor Window"):
            dpg.show_item("Node Editor Window")
        else:
            with dpg.window(
                    label="Node Editor",
                    width=dpg.get_viewport_width() // 1.5,
                    height=dpg.get_viewport_height() // 1.5,
                    pos=(0, 0),
                    tag="Node Editor Window"

            ):
                with dpg.menu_bar():
                    dpg.add_menu_item(
                        label="Add float value",
                        callback=self.callback_add_float_node
                    )
                    dpg.add_menu_item(
                        label="Delete",
                        callback=self.callback_unlink_node
                    )
                with dpg.node_editor(
                        callback=self.callback_link_node,
                        delink_callback=self.callback_unlink_node,
                        label="Node_Editor",
                        tag="NE",
                ):
                    for i, key in enumerate(self.parameters):
                        with dpg.node(
                                label=key,
                                pos=(gp.ns_x_padding, gp.ns_y_padding * i)):
                            with dpg.node_attribute(label=key, tag="Parameter_"+key,):
                                dpg.add_input_float(
                                    width=gp.ns_parameter_node_size,
                                    default_value=self.parameters[key],
                                    tag="Parameter_"+key+"_value"
                                )

                        self.callback_add_float_node()
                with dpg.handler_registry():
                    dpg.add_key_press_handler(dpg.mvKey_Delete, callback=self.callback_unlink_node)
                    dpg.add_key_press_handler(dpg.mvKey_Back, callback=self.callback_unlink_node)

    def callback_add_float_node(self):
        with dpg.node(
                label="Float Value",
                tag="fn_"+gp.W_count_of_float_nodes,
                parent="NE",
                pos=(0, int(gp.W_count_of_float_nodes)*gp.ns_y_padding)):
            dpg.add_node_attribute(
                tag="fn_"+gp.W_count_of_float_nodes+"_attr",
                attribute_type=dpg.mvNode_Attr_Output,
                parent="fn_"+gp.W_count_of_float_nodes
            )
            dpg.add_input_float(
                parent="fn_"+gp.W_count_of_float_nodes+"_attr",
                width=gp.ns_float_node_size,
                tag="fn_"+gp.W_count_of_float_nodes+"_attr"+"_value",
            )
            dpg.add_input_text(
                parent="fn_"+gp.W_count_of_float_nodes+"_attr",
                default_value="Rename Block: ",
                width=gp.ns_float_node_size,
            )

        gp.W_count_of_float_nodes = str(int(gp.W_count_of_float_nodes)+1)

    def callback_link_node(self, sender, app_data):
        dpg.add_node_link(app_data[0], app_data[1], parent=sender)
        if "attr" in app_data[0] and "Parameter" in app_data[1]:
            dpg.set_value(
                item=app_data[1]+"_value",
                value=dpg.get_value(app_data[0]+"_value"),
            )
            self.universal_slider_callback(
                sender="slider_"+app_data[1].replace("Parameter_", ""),
                app_data=dpg.get_value(app_data[0]+"_value"),
            )

    def callback_unlink_node(self, sender, app_data):
        for link in dpg.get_selected_links("NE") + dpg.get_selected_nodes("NE"):
            if dpg.get_item_label(link) not in self.parameters.keys():
                dpg.delete_item(link)


    @staticmethod
    def init_canvas():
        texture_data = []
        for i in range(dpg.get_item_height("Canvas_window")*dpg.get_item_width("Canvas_window")):
            texture_data.append(255/255)
            texture_data.append(0)
            texture_data.append(255/255)
            texture_data.append(255/255)
        with dpg.texture_registry():
            dpg.add_dynamic_texture(
                width=dpg.get_item_width("Canvas_window"),
                height=dpg.get_item_height("Canvas_window"),
                default_value=texture_data,
                tag="current image"
            )

    def update_canvas(self, gif_path: str, sleep=0.05):
        # Open GIF
        img = Image.open(gif_path)

        for part in ImageSequence.Iterator(img):
            part = part.convert("RGBA")
            part = numpy.frombuffer(part.tobytes(), dtype=numpy.uint8) / 255.0
            dpg.set_value("current image", part)
            time.sleep(sleep)


