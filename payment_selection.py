import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def proceed_to_next_step(driver, wait):
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
        return False
    return True


def click_pay_now_button(driver, wait):
    try:
        # Wait until the "PAY NOW" button is clickable
        pay_now_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".flex-all-c.navswitchbtn[tabindex='10']"))
        )
        
        # Scroll the button into view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", pay_now_button)
        time.sleep(0.5)  # Small delay to ensure smooth interaction
        
        # Use JavaScript to click the button if regular click fails
        driver.execute_script("arguments[0].click();", pay_now_button)
        print("Clicked 'PAY NOW' button.")
    except Exception as e:
        print("Error clicking 'PAY NOW' button:", str(e))
        return False
    return True