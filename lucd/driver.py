from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import random
import os
import platform
from fake_useragent import UserAgent
import sys
from termcolor import colored
from colorama import init
init()
# import Keys
from selenium.webdriver.common.keys import Keys


from .clean import Clean
from .utils import Util

clean = Clean()
util = Util()

class Driver:

    def generate_user_agent(self):
        try:
            ua = UserAgent()
            user_agent = ua['google chrome']
        except IndexError:
            user_agent = random.choice([          
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            ])
        return user_agent

    def driver_navigator(self, driver):
        if driver.execute_script("return navigator.webdriver"):
            driver.execute_cdp_cmd(
                    "Page.addScriptToEvaluateOnNewDocument",
                    {
                        "source": """

                                Object.defineProperty(window, 'navigator', {
                                    value: new Proxy(navigator, {
                                    has: (target, key) => (key === 'webdriver' ? false : key in target),
                                    get: (target, key) =>
                                        key === 'webdriver'
                                        ? undefined
                                        : typeof target[key] === 'function'
                                        ? target[key].bind(target)
                                        : target[key]
                                    })
                                });
                                    
                                                            
                        """
                    },
                )

    def open_new_cmd_and_run_command(self, profile_path="", port=9222, default_profile=False):
        """
        This function opens a new cmd window and runs the command
        a command that runs the Chrome driver in the debugging mode
        """
        system = platform.system()
        pwd = os.getcwd()
        if not profile_path and not default_profile:
            profile_path = pwd + f"/profile{random.randint(1,100)}"
        if profile_path and system == 'Windows':
            profile_path = profile_path.replace('/', '\\') if "/" in profile_path else profile_path
        if default_profile:
            command = f"chrome.exe -remote-debugging-port={port}"
        else:
            command = f'chrome.exe --remote-debugging-port={port} --user-data-dir="{profile_path}"'
        if system == 'Windows':
            os.system('start cmd /k ' + command)
        else:
            google = util.whereis_google_chrome()
            if not google:
                raise Exception("whereis: Google Chrome is not installed")
            if default_profile:
                command = f'{google} --remote-debugging-port={port}'
            else:
                command = f'{google} --remote-debugging-port={port} --user-data-dir="{profile_path}"'
            os.system(f'gnome-terminal -- bash -c "{command}"')

    def create_driver(self, headless=False, profile_path="", mute=False, debugging=False, default_profile=False, debug_port=9222, control_existing_instance=False):
        from .check import get_installed_chrome_path
        path = get_installed_chrome_path()
        os.chmod(path, 755)
        if not path:
            clean.remove_signature_in_javascript()
        if path is not None:
            options = webdriver.ChromeOptions()
            options.headless = headless
            options.add_argument("--start-maximized")
            options.add_argument("--lang=en-US")
            if profile_path:
                options.add_argument(r"--user-data-dir=%s" % profile_path)
            if debugging:
                if not control_existing_instance:
                    self.open_new_cmd_and_run_command(profile_path=profile_path, port=debug_port, default_profile=default_profile)
                options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debug_port}")
            else:
                options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
                options.add_argument("--log-level=3")
                options.add_experimental_option('useAutomationExtension', False)
                options.add_argument(f"user-agent={self.generate_user_agent()}")
                if mute:
                    options.add_argument("--mute-audio")
                    options.add_argument('--no-sandbox')
                options.add_argument("start-maximized")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_argument("--disable-blink-features=AutomationControlled")
            try:
                driver = webdriver.Chrome(executable_path=path, options=options)
            except TypeError:
                driver = webdriver.Chrome(service=Service(path), options=options)
            except Exception as error:
                sys.exit(colored("[-] ", "red")+f" {error}")
            else:
                self.driver_navigator(driver)
                driver.get("https://selmi.tech")
                return driver
        else:
            sys.exit(colored(f"Make sure you have chrome installed on your machine!", "red"))
