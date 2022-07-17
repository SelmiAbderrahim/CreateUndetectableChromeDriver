import sys
sys.path.append("...")
from lucd.driver import Driver

def test_create_driver():
    driver = Driver()
    chrome = driver.create_driver(headless=True)
    assert chrome.title == "Blog posts"
    chrome.quit()
