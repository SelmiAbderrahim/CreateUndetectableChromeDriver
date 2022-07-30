from setuptools import setup, find_packages

VERSION = '0.2.0' 
DESCRIPTION = 'Create Local Undetectable Chrome Driver'
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
        name="lucd", 
        version=VERSION,
        author="Selmi Abderrahim",
        author_email="contact@selmi.tech",
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/SelmiAbderrahim/CreateUndetectableChromeDriver',
        install_requires=[
            "beautifulsoup4==4.11.1",
            "colorama==0.4.4",
            "requests==2.27.1",
            "termcolor==1.1.0",
            "lxml==4.9.1",
            "selenium==4.1.5",
            "fake-useragent==0.1.11",
        ],
        packages=['lucd', 'lucd.*'],
        keywords=['python', 'undetectable', "chrome", "selenium", "webdriver"],
        classifiers= [
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ],
        license='MIT',
)
