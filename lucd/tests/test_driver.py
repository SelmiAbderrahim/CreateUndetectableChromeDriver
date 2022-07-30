import sys

sys.path.append("...")
from lucd.driver import Driver


def test_create_driver():
    driver = Driver()
    driver.headless = True
    chrome = driver.create()
    assert chrome.title == "Blog posts"
    chrome.quit()
