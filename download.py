import requests, shutil, os
from bs4 import BeautifulSoup


def get_chrome_driver_download_link(system, version):
    base_url = "https://chromedriver.storage.googleapis.com"
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    response = requests.get(base_url, headers=headers)
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, "xml")
    keys = [key.text for key in soup.find_all("Key")]
    try:
        return [key for key in keys if system in key and version in key][0]
    except IndexError:
        return None

def download_chrome_driver(chrome_driver_file):
    base_url = "https://chromedriver.storage.googleapis.com"
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    download_link = base_url+"/"+chrome_driver_file
    chrome_file_name = chrome_driver_file.split("/")[1]
    if not os.path.isdir("driver"):
        os.mkdir("driver")
    with requests.get(download_link, stream=True, headers=headers) as r:
        print(f"downloading {chrome_file_name} ...")
        with open(os.path.join("driver", chrome_file_name), 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return chrome_driver_file
