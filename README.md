# Create Local Undetectable Chrome Driver (LUCD)

This program will download a Chrome driver that you can use for your Python Selenium code.

## Features

- Download the exact chrome driver based on your OS and installed chrome version.

- Remove browser control flag

- Remove signature in javascript

- Set User-Agent

- Use maximum resolution

## Installation

```

$ pip install lucd 

```

## Usage

```

from lucd.driver import Driver
driver = Driver()
chrome = driver.create_driver()

chrome.get("https://selmi.tech")

```


---


### Tests

Tested on:

✅ Windows

❌ Linux

❌ Mac
