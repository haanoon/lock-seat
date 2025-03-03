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
# selected_bus_time = input('Enter Time (HH:MM): ').strip()
selected_bus_time = '22:15'
selected = False

for bus in buses:
    try:
        time_element = WebDriverWait(bus, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".float-left.triptimebold.darkText1"))
        )
        time_text = time_element.text.split(',')[0]

        if time_text == selected_bus_time:
            select_bus = bus.find_element(By.CSS_SELECTOR,'.selectbutton')
            select_bus.click()
            print('bus selected on time',time_text)
        
    except:
        print('error time')
try:
    WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.seatlook')))
except Exception as e:
    print('loading seats failed', str(e))

seats = driver.find_elements(By.CSS_SELECTOR,'.seatlook')

print(len(seats),'length')
seat_data = []
for seat in seats:
    try:
        is_available = "cursor: pointer" in seat.get_attribute("style")
        
        # Get seat details using JavaScript to access hidden tooltip
        js_code = """
        return arguments[0].querySelector('.farepopup').innerText;
        """
        tooltip_text = driver.execute_script(js_code, seat)
        
        seat_number = tooltip_text.split("|")[0].split("Seat: ")[1].strip()
        fare = tooltip_text.split("Rs. ")[1].strip()
        
        seat_data.append({
            'element': seat,
            'number': seat_number,
            'fare': fare,
            'available': is_available
        })
    except Exception as e:
        print(f"Error processing seat: {str(e)}")
        continue

# Display available seats
print("\nAvailable Seats:")
print("{:<8} {:<10} {:<10}".format('Seat No.', 'Fare', 'Status'))
print("-"*30)
for seat in seat_data:
    if seat['available']:
        print("{:<8} {:<10} {:<10}".format(
            seat['number'], 
            f"₹{seat['fare']}", 
            'Available'
        ))

# Seat selection process
while True:
    # selected_seat = input("\nEnter seat number to book (or 'q' to quit): ").strip()
    selected_seat = '17'
    if selected_seat.lower() == 'q':
        driver.quit()
        exit()
        
    # Find matching seat
    selected = next((s for s in seat_data if s['number'] == selected_seat and s['available']), None)
    
    if not selected:
        print("Invalid seat number or seat not available!")
        driver.quit()
        exit()
        continue
        
    try:
        # Scroll to and click the seat
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", selected['element'])
        time.sleep(0.5)
        selected['element'].click()
        print(f"Selected seat {selected_seat}!")
        
        # Handle confirmation popup if exists
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.confirm-seat'))
            ).click()
        except:
            pass
            
        break
    except Exception as e:
        print(f"Error selecting seat: {str(e)}")
        continue


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

# Select Dropping Point
# try:
#     dropping_point = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'point-inp') and contains(., 'Drop At')]")))
#     driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", dropping_point)
#     time.sleep(0.5)  # Small delay to ensure smooth interaction
#     dropping_point.click()
#     dropping_point.send_keys(Keys.ARROW_DOWN)
#     dropping_point.send_keys(Keys.ENTER)
#     print("Dropping point selected.")
# except Exception as e:
#     print("Error selecting dropping point:", str(e))

# Proceed to Payment Page
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


# Function to enter passenger details
def enter_passenger_details(driver, wait, name, age, gender):
    try:
        # Locate and fill the Name field
        name_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='paxName[0]']")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", name_field)
        name_field.clear()  # Clear any pre-filled value
        name_field.send_keys(name)
        print(f"Entered Name: {name}")

        # Locate and fill the Age field
        age_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='paxAge[0]']")))
        age_field.clear()  # Clear any pre-filled value
        age_field.send_keys(age)
        print(f"Entered Age: {age}")

        # Locate and click the Gender field to open the popup
        gender_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='paxGenderTemp[0]']")))
        gender_field.click()
        print("Gender dropdown clicked.")

        # Wait for the gender popup to appear and select the desired gender
        gender_option_xpath = f"//div[contains(@class, 'pass--inp--drop')]//div[text()='{gender}']"
        gender_option = wait.until(EC.element_to_be_clickable((By.XPATH, gender_option_xpath)))
        gender_option.click()
        print(f"Selected Gender: {gender}")

    except Exception as e:
        print("Error entering passenger details:", str(e))

# Function to proceed to payment details
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

# Example usage
passenger_name = "John Doe"
passenger_age = "30"
passenger_gender = "Male"

# Enter passenger details
enter_passenger_details(driver, wait, passenger_name, passenger_age, passenger_gender)

# Proceed to payment details
proceed_to_payment(driver, wait)


# Function to enter payee details (mobile number and email)
def enter_payee_details(driver, wait, mobile_number, email):
    try:
       

        # Locate and fill the Mobile Number field
        mobile_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='mobileNo']")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", mobile_field)
        mobile_field.clear()  # Clear any pre-filled value
        mobile_field.send_keys(mobile_number)
        print(f"Entered Mobile Number: {mobile_number}")

        # Locate and fill the Email field
        email_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
        email_field.clear()  # Clear any pre-filled value
        email_field.send_keys(email)
        print(f"Entered Email: {email}")

    except Exception as e:
        print("Error entering payee details:", str(e))

# Function to click the "Proceed" button
# Function to click the "Proceed" button
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
# Example usage
payee_mobile_number = "9876543210"
payee_email = "johndoe@gmial.com"

# Enter payee details
enter_payee_details(driver, wait, payee_mobile_number, payee_email)

# Proceed to the next step
proceed_to_next_step(driver, wait)

# Function to click the "PAY NOW" button
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

# Example usage
# After proceeding to payment options, click the "PAY NOW" button
click_pay_now_button(driver, wait)

driver.quit()