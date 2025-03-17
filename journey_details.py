from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def enter_journey_details(driver, wait, from_city, to_city, travel_date):
    # Input from city
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'search-from-city'))).click()
    input_from = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-from-city .chosen-search input')))
    input_from.send_keys(from_city + Keys.ENTER)

    # Input to city
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'search-to-city'))).click()
    input_to = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-to-city .chosen-search input')))
    input_to.send_keys(to_city + Keys.ENTER)

    # Set date
    date_obj = datetime.strptime(travel_date, "%d-%m-%Y")
    formatted_date = date_obj.strftime("%a, %d-%b-%Y")
    driver.execute_script(f"document.getElementById('departDate').value = '{formatted_date}';")

    # Initiate search
    wait.until(EC.element_to_be_clickable((By.ID,'submitSearch'))).click()

    return driver.current_url
def proceed_to_details(driver, wait):
    try:
        # Locate and click the "PROCEED TO PAYEE DETAILS" button
        proceed_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".navswitchbtn")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", proceed_button)
        time.sleep(0.5)  # Small delay to ensure smooth interaction
        proceed_button.click()
        print("Proceeding to payment details...")
    except Exception as e:
        print("Error proceeding to payment details:", str(e))
