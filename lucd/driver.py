from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import sys
from termcolor import colored
from colorama import init
import platform
import os
from .check import get_installed_chrome_path
from .base import Base
from .clear import PreLaunch


init()


class Driver(Base, PreLaunch):
    """
    Create undetectable Chrome driver

    Args:
        headless (bool): Hide the browser's window, defualt = False
        mute (bool): Mute the sound of the browser, defualt = False
        profile (Path): The absolute path of the Chrome profile

    Returns
        None
    """
    def __init__(self):
        super().__init__()
        self._useragent = self.generate_user_agent()

    @property
    def useragent(self):
        return self._useragent

    @useragent.setter
    def useragent(self, value: str):
        self._useragent = value

    def create(self):
        path = get_installed_chrome_path()
        if path is not None:
            options = webdriver.ChromeOptions()
            options.headless = self.headless
            if self.profile:
                options.add_argument(r"--user-data-dir=%s" % self.profile)

            options.add_argument("start-maximized")
            options.add_experimental_option(
                "excludeSwitches", ["enable-automation", 'enable-logging']
            )
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument(f"user-agent={self.useragent}")
            options.add_argument("--no-sandbox")
            if self.mute:
                options.add_argument("--mute-audio")
            try:
                driver = webdriver.Chrome(service=Service(path), options=options)
            except TypeError:
                driver = webdriver.Chrome(executable_path=path, options=options)
            except Exception as error:
                sys.exit(colored("[-] ", "red") + f" {error}")
            else:
                driver = self.driver_navigator(driver)
                driver = self.replace_user_agent(driver)
                driver.get("https://selmi.tech")
                return driver
        else:
            sys.exit(
                colored("Make sure you have chrome installed on your machine!", "red")
            )


class Remote(Base):
    def open_new_cmd_and_run_command(self, port):
        """
        This function opens a new cmd window and runs the command
         that runs the Chrome driver in the debugging mode
        """
        system = platform.system()
        if not self.profile:
            cmd = f"chrome.exe -remote-debugging-port={port}"
        else:
            cmd = f'chrome.exe --remote-debugging-port={port} --user-data-dir="{self.profile}"'
        if system == 'Windows':
            os.system('start cmd /k ' + cmd)
        else:
            google = self.whereis_google_chrome()
            if not google:
                raise Exception("whereis: Google Chrome is not installed")
            if not self.profile:
                cmd = f'{google} --remote-debugging-port={port}'
            else:
                cmd = f'{google} --remote-debugging-port={port} --user-data-dir="{self.profile}"'
            os.system(f'gnome-terminal -- bash -c "{cmd}"')

    def create(self, control_existing_instance: bool = False, port: int = 9222):
        path = get_installed_chrome_path()
        if path is not None:
            options = webdriver.ChromeOptions()
            if not control_existing_instance:
                self.open_new_cmd_and_run_command(
                    port=port
                )
            options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
            try:
                driver = webdriver.Chrome(service=Service(path), options=options)
            except TypeError:
                driver = webdriver.Chrome(executable_path=path, options=options)
            except Exception as error:
                sys.exit(colored("[-] ", "red") + f" {error}")
            else:
                driver.get("https://selmi.tech")
                return driver
        else:
            sys.exit(colored("Make sure you have chrome installed on your machine!", "red"))
