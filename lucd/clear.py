from fake_useragent import UserAgent
from random import choice
from selenium.webdriver.chrome import webdriver


class PreLaunch:
    def generate_user_agent(self) -> str:
        try:
            ua = UserAgent()
            user_agent = ua["google chrome"]
        except IndexError:
            user_agent = choice(
                [
                    (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
                    ),
                    (
                        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
                    ),
                    (
                        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, "
                        "like Gecko) Chrome/96.0.4664.45 Safari/537.36"
                    ),
                    (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        " (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
                    )
                ]
            )
        return user_agent

    def replace_user_agent(self, driver: webdriver) -> webdriver:
        ua = driver.execute_script("return navigator.userAgent")
        driver.execute_cdp_cmd(
            "Network.setUserAgentOverride",
            {
                "userAgent": ua.replace("Headless", ""),
            },
        )
        return driver

    def driver_navigator(self, driver: webdriver) -> webdriver:
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
        return driver
