import json
import os
import platform


class Util:
    def create_chrome_driver_config(self):
        if not os.path.isdir("driver"):
            os.mkdir("driver")
        config_file = os.path.join("driver", "config.json")
        if not os.path.isfile(config_file):
            with open(config_file, "w") as config:
                data = {
                    "system":platform.system(),
                    "version":"",
                    "chromedriver":""
                }
                config.write(json.dumps(data))
        return config_file

    def update_chrome_driver_config(self, version="", chromedriver=""):
        config_file = self.create_chrome_driver_config()
        config_data = json.load(open(config_file, "r"))
        if version:
            config_data["version"]=version
        if chromedriver:
            config_data["chromedriver"] = chromedriver
        with open(config_file, "w") as config:
            config.write(json.dumps(config_data))