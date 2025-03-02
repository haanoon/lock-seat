from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from datetime import datetime


options = webdriver.ChromeOptions()
options.binary_location = "/usr/bin/brave-browser"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=options)

driver.get("https://onlineksrtcswift.com/")
wait = WebDriverWait(driver,10)

try:
    close_ad = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "g-popup-close")))
    driver.execute_script("arguments[0].scrollIntoView(true);", close_ad)
    driver.execute_script("arguments[0].click();", close_ad)
    print("Banner Closed")
except:
    print("No Banner Found")

# from_city = input('Enter From City: ').strip()
# to_city = input('Enter To City: ').strip()

from_city = "kozhikode"
to_city = "Kothamangalam"

from_input_box = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'search-from-city')))
from_input_box.click()
input_from = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-from-city .chosen-search input')))
input_from.send_keys(from_city)
input_from.send_keys(Keys.ENTER)
# wait.until(EC.element_to_be_clickable((By.XPATH, f'//li[contains(., "{from_city}")]'))).click()

to_input_box = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'search-to-city')))
to_input_box.click()
input_to = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-to-city .chosen-search input')))
input_to.send_keys(to_city)
input_to.send_keys(Keys.ENTER)
# wait.until(EC.element_to_be_clickable((By.XPATH, f'//li[contains(., "{to_city}")]'))).click()

# travel_date = input("Enter Date (DD-MM-YYYY): ").strip()
travel_date = '01-04-2025'

from datetime import datetime
date_obj = datetime.strptime(travel_date, "%d-%m-%Y")
formatted_date = date_obj.strftime("%a, %d-%b-%Y")

driver.execute_script(
    f"document.getElementById('departDate').value = '{formatted_date}';"
    )

search_button = wait.until(EC.element_to_be_clickable((By.ID,'submitSearch')))
search_button.click()




try:
    WebDriverWait(driver,45).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.srch-card')))
    print('Bus details loaded')
except Exception as e:
    print('Loading bus failed',str(e))
    driver.quit()
    exit()

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

buses = driver.find_elements(By.CSS_SELECTOR, '.srch-card')
print(f"\nFound {len(buses)} buses:")
print("{:<5} {:<12} {:<30} {:<15} {:<10}".format(
    'No.', 'Time', 'Bus Name', 'Seats', 'Fare'))
print("-"*75)

for index, bus in enumerate(buses, 1):
    try:
        # Use CSS selector with proper class concatenation
        time_element = WebDriverWait(bus, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".float-left.triptimebold.darkText1"))
        )
        time_text = time_element.text.split(',')[0]  # Extract just the time
        
        # Updated selectors based on HTML structure
        name = bus.find_element(By.CSS_SELECTOR, '.bus--type').text
        seats = bus.find_element(By.CSS_SELECTOR, '.seatcount').text.split()[0]
        fare = bus.find_element(By.CSS_SELECTOR, '.pricetag').text.replace('₹', '').strip()

        print("{:<5} {:<12} {:<30} {:<15} {:<10}".format(
            index, time_text, name[:25], seats, fare))

    except Exception as e:
        print(f'Error reading bus {index}:', str(e))
        continue



driver.quit()