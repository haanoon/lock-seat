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
        # Wait until the "Proceed" button is clickable
        proceed_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".navswitchbtn.flex-all-c[tabindex='9']"))
        )
        
        # Scroll the button into view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", proceed_button)
        time.sleep(0.5)  # Small delay to ensure smooth interaction
        
        # Use JavaScript to click the button if regular click fails
        driver.execute_script("arguments[0].click();", proceed_button)
        print("Clicked 'Proceed' button.")
    except Exception as e:
        print("Error clicking 'Proceed' button:", str(e))
