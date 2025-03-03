import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def points(wait,driver):
    try:
        boarding_point = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'point-inp') and contains(., 'Boarding At')]")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boarding_point)
        time.sleep(0.5)  # Small delay to ensure smooth interaction
        boarding_point.click()
        print("Boarding point selected.")
        boarding_point.send_keys(Keys.ARROW_DOWN)
        boarding_point.send_keys(Keys.ENTER)
        time.sleep(5)
        boarding_point.send_keys(Keys.ENTER)
    except Exception as e:
        print("Error selecting boarding point:", str(e))

    
    try:
        # Wait for the "SELECT PICKUP, DROPOFF POINTS" button to become enabled
        proceed_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btnPassDetails"))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", proceed_button)
        time.sleep(0.5)  # Small delay to ensure smooth interaction
        proceed_button.click()
        print("Proceeding to payment page...")
    except Exception as e:
        print("Error proceeding to payment page:", str(e))
