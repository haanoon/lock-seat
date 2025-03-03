from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

def enter_payee_details(driver, wait, mobile, email):
    mobile_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='mobileNo']")))
    mobile_field.send_keys(mobile)
    
    email_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    email_field.send_keys(email)


def proceed_to_payment(driver, wait):
    try:
        # Locate and click the "PROCEED TO PAYEE DETAILS" button
        proceed_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".navswitchbtn")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", proceed_button)
        time.sleep(0.5)  # Small delay to ensure smooth interaction
        proceed_button.click()
        print("Proceeding to payment details...")
    except Exception as e:
        print("Error proceeding to payment details:", str(e))
