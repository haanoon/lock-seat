from datetime import datetime
import time
from selenium.common.exceptions import WebDriverException
from browser_setup import setup_browser, teardown_browser, close_ad, load_page
from bus_selection import display_available_buses, select_bus_by_time
from seat_selection import select_seat, available_seats
from passenger_details import enter_passenger_details
from payment_processing import enter_payee_details, proceed_to_payment
from points_selection import points
from payment_selection import click_pay_now_button, proceed_to_next_step
from timeout import monitor_seat_availability

def booking_attempt(driver, wait, details,url):
    """Perform a complete booking cycle"""
    SEAT_NUMBER = details['seat_number']
    try:
        # Initialize fresh session
        # driver.delete_all_cookies()
        # driver.get("https://onlineksrtcswift.com/")
        # close_ad(driver, wait)

        # # Set journey details
        # url = enter_journey_details(driver, wait,
        #     from_city=details['from'],
        #     to_city=details['to'],
        #     travel_date=details['date']
        # )
        driver.get(url)

        # Bus selection
        buses = display_available_buses(driver, wait)
        if not select_bus_by_time(driver, wait, buses, details['bus_time']):
            return False

        # Seat selection
        seats = available_seats(driver, wait)
        if not select_seat(driver, wait, SEAT_NUMBER, seats):
            return False

        # Complete booking steps
        points(wait, driver)

        enter_passenger_details(driver, wait,
            name=details['name'],
            age=details['age'],
            gender=details['gender']
        )

        proceed_to_payment(driver, wait)

        enter_payee_details(driver, wait,
            mobile=details['phone'],
            email=details['email']
        )

        proceed_to_next_step(driver,wait)

        payment_page = click_pay_now_button(driver, wait)
        if  payment_page:
            return True
       
    except WebDriverException as e:
        print(f"Browser error: {str(e)}")
        return False
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False
    



def continuous_booking_(details):
    """Main control loop for continuous booking"""

    MAX_ATTEMPTS = details['MAX_ATTEMPTS']
    COOLDOWN_NORMAL = details['INTERVAL']
    SEAT_NUMBER = details['seat_number']
    COOLDOWN_ERROR = details['COOLDOWN_ERROR']
    
    attempt_count = 0
    success_count = 0
    
    while attempt_count < MAX_ATTEMPTS:
        attempt_count += 1
        driver, wait = setup_browser()
        
        try:
            print(f"\nAttempt #{attempt_count} [{datetime.now().strftime('%H:%M:%S')}]")

            url = load_page(driver, wait,details)

            if monitor_seat_availability(SEAT_NUMBER,url):
                booking_attempt(driver, wait, details,url)
                time.sleep(COOLDOWN_NORMAL)
            else:
                print("Seat not available, retrying...")
                print('false',driver.current_url)
                time.sleep(COOLDOWN_ERROR)
                
        finally:
            teardown_browser(driver)
            time.sleep(COOLDOWN_ERROR)