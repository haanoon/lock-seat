from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def enter_passenger_details(driver, wait, name, age, gender):
    name_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='paxName[0]']")))
    name_field.send_keys(name)
    
    age_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='paxAge[0]']")))
    age_field.send_keys(age)
    
    gender_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='paxGenderTemp[0]']")))
    gender_field.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{gender}']"))).click()
