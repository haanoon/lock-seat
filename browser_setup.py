from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def setup_browser():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/brave-browser"
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)
    driver.get("https://onlineksrtcswift.com/")
    return driver, wait

def close_ad(driver, wait):
    try:
        close_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "g-popup-close")))
        driver.execute_script("arguments[0].click();", close_btn)
        print("Closed ad banner")
    except:
        print("No ad banner found")

def teardown_browser(driver):
    driver.quit()
