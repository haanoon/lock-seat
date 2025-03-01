from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions()
options.binary_location = "/usr/bin/brave-browser"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=options)

driver.get("https://onlineksrtcswift.com/")
wait = WebDriverWait(driver,10)


# try:
#     close_ad = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"g-popup-close")))
#     close_ad.click()
#     print("Banner Closed")
# except:
#     print('No Banner Found')

try:
    close_ad = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "g-popup-close")))
    driver.execute_script("arguments[0].scrollIntoView(true);", close_ad)
    driver.execute_script("arguments[0].click();", close_ad)
    print("Banner Closed")
except:
    print("No Banner Found")


# from_field = driver.find_element(By.ID,"fromCity")
# driver.execute_script("arguments[0].click();", from_field)
# time.sleep(1)
# from_field.send_keys("Kozhikode")

# from_field = wait.until(EC.element_to_be_clickable((By.ID,"fromCity")))
# from_field.click()
# from_field.clear()
# from_field.send_keys("Kozhikode")

from_input_box = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'search-from-city')))
from_input_box.click()
time.sleep(1)

input_from = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'chosen-search')))
search_from = input_from.find_element(By.TAG_NAME,"input")
search_from.send_keys("Kozhikode")
search_from.send_keys(Keys.ENTER)
time.sleep(1)



# from_dropdown = wait.until(EC.element_to_be_clickable((By.ID,'fromCity')))
# select_from = Select(from_dropdown)
# select_from.select_by_visible_text('Kozhikode')

# to_field = driver.find_element(By.ID,"toCity")
# time.sleep(1)
# to_field.send_keys("Kothamangalam")

to_input_box = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'search-to-city')))
to_input_box.click()
time.sleep(1)

input_to = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'chosen-search')))
# input_to = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".chosen-drop .chosen-search")))
search_to = input_to.find_element(By.TAG_NAME,'input')
search_to.send_keys('Kothamangalam')
time.sleep(1)
search_to.send_keys(Keys.ENTER)
# time.sleep(1) 



# date_field = driver.find_element(By.ID,'departDate')
# date_field.clear()
# date_field.send_keys("02/03/2025")
# date_field.send_keys(Keys.ENTER)
# time.sleep(3)

# print(date_field.value_of_css_property)
# Kozhikode

driver.quit()