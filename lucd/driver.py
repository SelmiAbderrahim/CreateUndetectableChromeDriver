from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import random
from fake_useragent import UserAgent
import sys
from termcolor import colored
from colorama import init
init()


from .check import get_installed_chrome_path
from .clean import Clean


ua = UserAgent()
clean = Clean()


class Driver:

    def generate_user_agent(self):
        try:
            user_agent = ua['google chrome']
        except:
            user_agent = random.choice([          
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            ])
        return user_agent

    def create_driver(self, headless=False, profile_path="", mute=False):
        clean.remove_signature_in_javascript()
        path = get_installed_chrome_path()
        if path is not None:
            options = webdriver.ChromeOptions()
            options.headless = headless
            if profile_path:
                options.add_argument(r"--user-data-dir=%s" % profile_path)
            options.add_argument("--start-maximized")
            options.add_argument("--log-level=3")
            options.add_experimental_option(
                "excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option(
                'prefs', {'intl.accept_languages': 'en_US,en'})
            options.add_argument(f"user-agent={self.generate_user_agent()}")
            if mute:
                options.add_argument("--mute-audio")
                options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-features=UserAgentClientHint')
            prefs = {"profile.default_content_setting_values.notifications" : 2}
            options.add_experimental_option("prefs",prefs)
            webdriver.DesiredCapabilities.CHROME['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
            try:
                driver = webdriver.Chrome(executable_path=path, options=options)
            except TypeError:
                driver = webdriver.Chrome(service=Service(path), options=options)
            except Exception as error:
                sys.exit(colored("[-] ", "red")+f" {error}")
            else:
                driver.get("https://selmi.tech")
                return driver
        else:
            sys.exit(colored(f"Make sure you have chrome installed on your machine!", "red"))
