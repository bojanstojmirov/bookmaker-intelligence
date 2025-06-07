import os, time, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def init_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    chrome_driver_path = os.path.join(current_dir, "chromedriver")

    return webdriver.Chrome(
        service=Service(chrome_driver_path),
        options=options
    )

def get_and_sleep(driver, url, delay=5):
    driver.get(url)
    time.sleep(delay)

def regex_match(text, pattern, suffix=''):
    match = re.search(pattern, text)
    if match:
        return match.group(1) + suffix
    return None

def append_if_found(text, keyword, label, container):
    if keyword.lower() in text.lower():
        container.append(label)
