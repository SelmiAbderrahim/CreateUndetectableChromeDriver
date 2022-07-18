import shutil
import requests
import os
import platform
import subprocess
import re
import zipfile
from pathlib import Path
from bs4 import BeautifulSoup
from termcolor import colored
from colorama import init


from .utils import Util

OSNAME = platform.system()
init()
DRIVER = Path(__file__).resolve().absolute().parent / "driver"


class Download(Util):
    """
    It will get the installed Chrome driver and based on the operating system
    it will download the compatible chromedriver.
    """

    if OSNAME == "Windows":
        system = "win"
    elif OSNAME == "Linux":
        system = "linux"
    else:
        system = "mac"

    def update_binary(self, path):
        word = "cdc_".encode()
        new = "tch_".encode()
        while True:
            string = b""
            Flag = 0
            with open(path, 'r+b') as file:
                pos = 0
                data = string = file.read(1)
                while data:
                    data = file.read(1)
                    if data == b" ":
                        if word in string:
                            new_tring = string.decode().replace(word.decode(), new.decode())
                            file.seek(pos)
                            file.write(new_tring.encode())
                            Flag = 1
                            break
                        else:
                            pos = file.tell()
                            data = string = file.read(1)
                    else:
                        string += data
                        continue
            if not Flag:
                break

    def remove_signature_in_javascript(self, path):
        if OSNAME == "Windows":
            os.chmod(path, 755)
        else:
            subprocess.Popen(f"sudo chmod 777 {path}", stdout=subprocess.PIPE, shell=True)
        with open(path, "r", errors="ignore") as chrome:
            content = chrome.read()
        content = content.replace("cdc_", "tch_")   
        self.update_binary(path)


    def check_installed_chrome_version(self):
        try:
            if OSNAME == "Windows":
                cmd_version_output = (
                    subprocess.Popen(
                        'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
                        shell=True,
                        stdout=subprocess.PIPE,
                    )
                    .stdout.read()
                    .decode("utf-8")
                )
            elif OSNAME == "Linux":
                cmd_version_output = (
                    subprocess.Popen(
                        "google-chrome --version", shell=True, stdout=subprocess.PIPE
                    )
                    .stdout.read()
                    .decode("utf-8")
                )
            elif OSNAME == "Darwin":
                cmd_version_output = (
                    subprocess.Popen(
                        "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version",
                        shell=True,
                        stdout=subprocess.PIPE,
                    )
                    .stdout.read()
                    .decode("utf-8")
                )
        except Exception as error:
            print(
                colored("X [Error]", "red")
                + " We couldn't find the version of the installed chrome browser."
            )
            print(f"--> {error}")
            return None
        else:
            installed_chrome_version = re.findall(
                    r"([\d]+\.[\d]+\.[\d]+\.[\d]+)", cmd_version_output
                )[0].split(".")[0]
            print(
                colored("[+]", "green")
                + " You have Chrome version "
                + colored(installed_chrome_version, "blue")
                + " installed."
            )
            self.update_chrome_driver_config(version=installed_chrome_version)
            return installed_chrome_version

    def get_chrome_driver_download_link(self, version):
        base_url = "https://chromedriver.storage.googleapis.com"
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        response = requests.get(base_url, headers=headers)
        content = response.content.decode("utf-8")
        soup = BeautifulSoup(content, features="xml")
        keys = [key.text for key in soup.find_all("Key")]
        try:
            return [key for key in keys if self.system in key and version in key][0]
        except IndexError:
            return None

    def download_chrome_driver(self, chrome_driver_file):
        base_url = "https://chromedriver.storage.googleapis.com"
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        download_link = base_url + "/" + chrome_driver_file
        chrome_file_name = chrome_driver_file.split("/")[1]
        with requests.get(download_link, stream=True, headers=headers) as r:
            print("downloading " + colored(f"{chrome_file_name}", "blue") + " ...")
            with open(os.path.join(DRIVER, chrome_file_name), "wb") as f:
                shutil.copyfileobj(r.raw, f)
        
        return chrome_driver_file

    def extract_chrome_driver_zip(self, chrome_driver_file):
        global filename
        chrome_file_name = chrome_driver_file.split("/")[1]
        path = os.path.join(DRIVER, chrome_file_name)
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(DRIVER)
            filename = zip_ref.namelist()[0]
        os.remove(path)
        print(colored("[+]", "green") + " Chrome driver has been installed.")
        chromedriver_path = os.path.join(DRIVER, filename)
        self.update_chrome_driver_config(chromedriver=chromedriver_path)
        
        self.remove_signature_in_javascript(chromedriver_path)
        return filename