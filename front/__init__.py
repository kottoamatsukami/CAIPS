import dearpygui.dearpygui as dpg
from dearpygui_ext import logger


class GUI:
    def __init__(self, settings: dict, debug_mode=False):
        self.settings = settings
        self.debug_mode = debug_mode
        self.log = False
        self.logger = None

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

        # Main window
        with dpg.window(tag="Primary Window"):
            dpg.add_text("Hello, world")

            # Menu bar
            with dpg.menu_bar():
                with dpg.menu(label="Options"):
                    dpg.add_menu_item(label="Save Parameters (Ctrl+S)")
                    dpg.add_menu_item(label="Load Parameters (Ctrl+L)")
                    dpg.add_menu_item(label="Credits")

                with dpg.menu(label="Themes"):
                    dpg.add_menu_item(label="Dark")
                    dpg.add_menu_item(label="Light")
                    dpg.add_menu_item(label="Classic")

                with dpg.menu(label="Tools"):
                    dpg.add_menu_item(label="Show Logger", callback=self.callback_show_logger)
                    dpg.add_menu_item(label="Show About")

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
                                      default_value=0)
                dpg.add_slider_double(label="Ay", tag="slider_Ay",
                                      min_value=-10, max_value=10,
                                      default_value=0.95 * 2)
                dpg.add_slider_double(label="Bx", tag="slider_Bx",
                                      min_value=-10, max_value=10,
                                      default_value=0.30 * 2)
                dpg.add_slider_double(label="By", tag="slider_By",
                                      min_value=-10, max_value=10,
                                      default_value=0.65 * 2)
                dpg.add_slider_double(label="Xtop", tag="slider_Xtop",
                                      min_value=-10, max_value=10,
                                      default_value=0)
                dpg.add_slider_double(label="Ytop", tag="slider_Ytop",
                                      min_value=-10, max_value=10,
                                      default_value=0.65 * 2)
                dpg.add_slider_double(label="Xbot", tag="slider_Xbot",
                                      min_value=-10, max_value=10,
                                      default_value=0)
                dpg.add_slider_double(label="Ybot", tag="slider_Ybot",
                                      min_value=-10, max_value=10,
                                      default_value=0.22 * 2)
                dpg.add_slider_double(label="Rt", tag="slider_Rt",
                                      min_value=-10, max_value=10,
                                      default_value=0.3 * 2)
                dpg.add_slider_double(label="Rb", tag="slider_Rb",
                                      min_value=-10, max_value=10,
                                      default_value=0.19 * 2)
                dpg.add_slider_double(label="Pt0", tag="slider_Pt0",
                                      min_value=-10000, max_value=10000,
                                      default_value=12000 * 2)
                dpg.add_slider_double(label="Pb0", tag="slider_Pb0",
                                      min_value=-10000, max_value=10000,
                                      default_value=4000 * 2)
                dpg.add_slider_double(label="Pac", tag="slider_Pac",
                                      min_value=-10000, max_value=10000,
                                      default_value=2000)
                dpg.add_slider_double(label="alpha5", tag="slider_alpha5",
                                      min_value=0, max_value=360,
                                      default_value=270)

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

    @staticmethod
    def callback_resize_viewport_window():
        print(dpg.get_viewport_width(), dpg.get_viewport_height(), dpg.get_item_width(item="Side_menu"), dpg.get_item_pos(item="Side_menu"))
        dpg.set_item_pos(
            item="Side_menu",
            pos=(
                dpg.get_viewport_width() - dpg.get_item_width(item="Side_menu"),
                dpg.get_viewport_height() - dpg.get_item_height(item="Side_menu"),
            ),
        )
        dpg.set_item_pos(
            item="Canvas_window",
            pos=(
                dpg.get_viewport_width()-1200,
                dpg.get_viewport_height()-550,
            ),
        )

    def callback_show_logger(self):
        self.log = True
        self.logger = logger.mvLogger()
        self.logger.log_info("Starting log...")

    # -----------------
    # Sliders Callbacks
    # -----------------




