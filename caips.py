import os
import libs
import front
from libs import settings_manager as sm, error_handler


def main(*args):
    # --------------------------------------------------
    # We limit the number of arguments to 2.
    # Use flag -debug to debug this program
    # or
    # Use flag -release to use release version of script
    # --------------------------------------------------
    if not(len(*args) == 2):
        error_handler.raise_error(
            msg=f"You should use one flag: -debug, -release or -change_settings"
        )

    # ----------------------------------
    # Check the correctness of the flags
    # args[0] include a path of the script
    # ----------------------------------
    mode = args[0][1]
    settings_manager = sm.SettingsManager()
    if mode == "-debug":
        debug_mode = True
    elif mode == "-release":
        debug_mode = False
    elif mode == "-change_settings":
        settings_manager.change_settings(
            required_keys={x: str(type(libs.STD_SETTINGS[x]))[8:-2] for x in libs.STD_SETTINGS.keys()},
            path="settings"
        )
        exit(0)
    else:
        error_handler.raise_error(
            msg=f"Error: unexpected flag: {mode}"
        )

    # -----------------
    # Check and load the settings
    # -----------------
    if os.path.exists("settings"):
        settings = settings_manager.load("settings")
    else:
        error_handler.raise_warning(
            msg="Setting file was not found, std_settings were used"
        )
        settings = libs.STD_SETTINGS
        settings_manager.save(settings, "settings")

    if not(all(x in settings.keys() for x in libs.STD_SETTINGS.keys())):
        os.remove("settings")
        error_handler.raise_error(
            msg="setting file was corrupted"
        )

    # -----------------------------------
    # log info about setting and init DPG
    # -----------------------------------
    error_handler.raise_info(
        msg="setting file was successfully used, starting GUI..."
    ) if debug_mode else None

    gui = front.GUI(
        settings=settings,
        debug_mode=debug_mode,
    )
    gui.run()


if __name__ == '__main__':
    import sys
    main(sys.argv)
