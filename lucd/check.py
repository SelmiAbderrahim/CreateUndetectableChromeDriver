import os
import sys
import json


from .download import Download


download = Download()


def get_installed_chrome_path():
    config_file = os.path.join("driver", "config.json")
    if os.path.isfile(config_file):
        chromedriver = json.load(open(config_file, "r"))["chromedriver"]
        if chromedriver:
            return chromedriver
    chrome_version = download.check_installed_chrome_version()
    if chrome_version:
        chrome_driver_name = download.get_chrome_driver_download_link(chrome_version)
        download.download_chrome_driver(chrome_driver_name)
        filename = download.extract_chrome_driver_zip(chrome_driver_name)
        chromedriver = os.path.join("driver", filename)
        return chromedriver
    else:
        return None