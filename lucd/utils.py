import json
import os
import platform
from pathlib import Path
import subprocess


DRIVER = Path(__file__).resolve().absolute().parent / "driver"


class Util:
    def create_chrome_driver_config(self):
        if not os.path.isdir(DRIVER):
            os.mkdir(DRIVER)
        config_file = os.path.join(DRIVER, "config.json")
        if not os.path.isfile(config_file):
            with open(config_file, "w") as config:
                data = {"system": platform.system(), "version": "", "chromedriver": ""}
                config.write(json.dumps(data))
        return config_file

    def update_chrome_driver_config(self, version="", chromedriver=""):
        config_file = self.create_chrome_driver_config()
        config_data = json.load(open(config_file, "r"))
        if version:
            config_data["version"] = version
        if chromedriver:
            config_data["chromedriver"] = chromedriver
        with open(config_file, "w") as config:
            config.write(json.dumps(config_data))

    def whereis_google_chrome(self):
        """
        Get the path of the chrome driver
        """
        try:
            chrome_path = (
                subprocess.check_output(["whereis", "google-chrome"])
                .decode("utf-8")
                .strip()
                .split()[1]
            )
        except IndexError:
            return False
        return chrome_path
