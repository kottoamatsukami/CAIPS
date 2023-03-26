import pickle
import libs.error_handler as error_handler


class SettingsManager(object):
    @staticmethod
    def save(data: dict, path: str) -> None:
        with open(path, "wb") as file:
            pickle.dump(data, file)

    @staticmethod
    def load(path: str) -> dict:
        with open(path, "rb") as file:
            data = pickle.load(file)
        return data

    def change_settings(self, required_keys: dict, path: str) -> None:
        # --------------------------------------------------
        # structure
        # required_keys = {
        # key_1 : expected_type ("str", "int" or "float")
        # ...
        # key_n : expected_type ("str", "int" or "float")
        # }
        # --------------------------------------------------
        to_write = dict()
        print("Changing settings:")
        for key in required_keys:
            to_write[key] = self.determine_type(
                s=input(
                    f"key [{key}] ({required_keys[key]}): "
                ),
                expected_type=required_keys[key],
            )
        self.save(
            data=to_write,
            path=path,
        )
        error_handler.raise_info(
            msg="Successfully saved!"
        )

    @staticmethod
    def determine_type(s: str, expected_type: str) -> str or int or float:
        if expected_type == "str":
            return s
        elif expected_type == "int":
            if s.isdigit():
                return int(s)
            else:
                error_handler.raise_error(
                    msg=f"Invalid input <{s}> for type <{expected_type}>"
                )
        elif expected_type == "float":
            try:
                return float(s)
            except:
                error_handler.raise_error(
                    msg=f"Invalid input <{s}> for type <{expected_type}>"
                )

        error_handler.raise_error(
            msg=f"Invalid input <{s}> for type <{expected_type}>"
        )


