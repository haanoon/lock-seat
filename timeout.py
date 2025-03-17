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

def monitor_seat_availability(seat_number,url):
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
                driver.get(url)
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
    result = monitor_seat_availability("22")
    if result:
        print(f"Total monitoring time: {result}")
    else:
        print("Monitoring stopped without finding seat")