
# Create Local Undetectable Chrome Driver (LUCD)


This program will download and patch a Chrome driver to make it undetectable. So that you can use an undetectable Chrome driver for your Python Selenium code.


## Passed the antibot test [](https://bot.sannysoft.com)


# ![](https://github.com/SelmiAbderrahim/CreateUndetectableChromeDriver/blob/master/lucd/screenshots/antibot-tested.png?raw=true)


# Features

- Download the exact chrome driver based on your OS and installed chrome version.
- Remove browser control flag
- Remove signature in javascript
- Set User-Agent
- Start maximum resolution
- Open Chrome Instance on debugging mode
- Control an existing Chrome instance.
- Unmute the sounds of the browser.
- Save/ load Chrome profiles.
- Run Chrome driver on headless mode.

<br><br>
# Installation

```
pip install lucd 
```

or 

```
pip install git+https://github.com/SelmiAbderrahim/CreateUndetectableChromeDriver
```
<br><br>
# Example

```
from lucd.driver import Driver
driver = Driver()
chrome = driver.create()
```
<br><br>
# Usage

## Create an undetectable Chrome driver

```
from lucd.driver import Driver
driver = Driver()

# headless browser
driver.headless = True

# Mute the browser
driver.mute = True

# Set the profile path
driver.profile = r"C:\\path\\profile"

# Change useragent
driver.useragent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"

chrome = driver.create()

```

## Control/open an existing Chrome driver

```
from lucd.driver import Remote
driver = Remote()

# Open Chrome on debugging mode and control it
chrome = driver.create()

# Control an existing Chrome driver
chrome = driver.create(control_existing_instance, port = 9222)
```

<br><br>

# Tests


**Clone the project**

```
git clone https://github.com/SelmiAbderrahim/CreateUndetectableChromeDriver/blob/master/lucd/screenshots/antibot-tested.png
```

**Create virtual environment**

```
pip install virtualenv
virtualenv env
source env/bin/activate
```

**Install requirements**

```
pip install -r requirements.txt
```

**Run tests**

```
python -m pytest lucd/tests/
```
