# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import Select

# from datetime import datetime
# from browser_setup import setup_browser, close_ad, teardown_browser
# from journey_details import enter_journey_details, proceed_to_details
# from bus_selection import display_available_buses, select_bus_by_time
# from seat_selection import select_seat, available_seats
# from passenger_details import enter_passenger_details
# from payment_processing import enter_payee_details, proceed_to_payment
# from points_selection import points
# from payment_selection import click_pay_now_button

# def time_taken(seat):
#     start_time = datetime.now()
#     options = webdriver.ChromeOptions()
#     options.binary_location = "/usr/bin/brave-browser"

#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service,options=options)

#     driver.get("https://onlineksrtcswift.com/search?fromCity=10072%7CKozhikode&toCity=455%7CKothamangalam&departDate=01-04-2025&mode=oneway&src=h&stationInFromCity=&stationInToCity=")
#     wait = WebDriverWait(driver,10)

#     buses = display_available_buses(driver, wait)
#     select_bus_by_time(driver,wait,buses,'22:15')

#     seat_avai = False

#     while seat_avai == False:
#         seats_available = []
#         available_seats(driver,available_seats)



# time_taken()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bus_selection import display_available_buses, select_bus_by_time
from seat_selection import select_seat, available_seats

def monitor_seat_availability(seat_number):
    # Setup browser
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/brave-browser"
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver,10)
    try:
        start_time = datetime.now()
        refresh_count = 0
        seat_found = False
        
        while not seat_found:
            refresh_count += 1
            try:
                # Load page
                driver.get("https://onlineksrtcswift.com/search?fromCity=10072%7CKozhikode&toCity=455%7CKothamangalam&departDate=01-04-2025&mode=oneway&src=h&stationInFromCity=&stationInToCity=")
                buses = display_available_buses(driver, wait)
                select_bus_by_time(driver,wait,buses,'22:15')
                # Wait for seats to load
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".seatlook"))
                )                
                # Check seat availability
                seats = driver.find_elements(By.CSS_SELECTOR, '.seatlook')
                for seat in seats:
                    try:
                        # Check if seat is available and matches target number
                        if "cursor: pointer" in seat.get_attribute("style"):
                            seat_details = driver.execute_script(
                                "return arguments[0].querySelector('.farepopup').innerText;", seat)
                            if f"Seat: {seat_number}" in seat_details:
                                seat_found = True
                                elapsed = datetime.now() - start_time
                                print(f"\nSeat {seat_number} became available after {elapsed}")
                                break
                    except Exception as e:
                        continue
                
                if seat_found:
                    break
                
                # Print status
                print(f"Refresh #{refresh_count} - Seat {seat_number} not available - {datetime.now().strftime('%H:%M:%S')}")
                
                # Wait before next refresh
                time.sleep(5)
                
            except Exception as e:
                print(f"Error during refresh #{refresh_count}: {str(e)}")
                time.sleep(5)  # Wait longer if error occurs
        
        return True if seat_found else None
        
    finally:
        driver.quit()

# Run monitoring for seat 17
if __name__ == "__main__":
    print("Starting seat availability monitor...")
    result = monitor_seat_availability("17")
    if result:
        print(f"Total monitoring time: {result}")
    else:
        print("Monitoring stopped without finding seat")