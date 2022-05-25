from termcolor import colored
from colorama import init


from .check import get_installed_chrome_path


init()


class Clean:
    chromedriver = get_installed_chrome_path()

    def update_binary(self):
        word = "cdc_".encode()
        new = "tch_".encode()
        path = self.chromedriver
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

    def remove_signature_in_javascript(self):
        with open(self.chromedriver, "r", errors="ignore") as chrome:
            content = chrome.read()
        content = content.replace("cdc_", "tch_")   
        self.update_binary()
