import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from dotenv import load_dotenv
from time import sleep


def setDriver(proxy) -> webdriver:
    chrome_options = Options()

    chrome_options.add_argument(f"--proxy-server={proxy}")
    # chrome_options.add_argument('start-maximized')

    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    load_dotenv()
    path = str(os.getenv('CHROME_DRIVER_PATH'))
    service = Service(executable_path=path)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    stealth(driver=driver, languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine")

    return driver


with open("Proxies/filteredProxies.txt") as proxyList:
    for proxy in proxyList:
        try:
            newDriver: webdriver = setDriver(proxy)
            newDriver.get("https://google.com")
            print(f"Proxy Success: {proxy}")
            sleep(20)
        except:
            print(f"Proxy failed: {proxy}")
# newDriver.get("https://amazon.com")
