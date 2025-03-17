from datetime import datetime
import time
from selenium.common.exceptions import WebDriverException
from browser_setup import setup_browser, teardown_browser, close_ad
from journey_details import enter_journey_details
from bus_selection import display_available_buses, select_bus_by_time
from seat_selection import select_seat, available_seats
from passenger_details import enter_passenger_details
from payment_processing import enter_payee_details, proceed_to_payment
from points_selection import points
from payment_selection import click_pay_now_button, proceed_to_next_step
from timeout import monitor_seat_availability

def booking_attempt(driver, wait, details):
    """Perform a complete booking cycle"""
    SEAT_NUMBER = details['seat_number']
    try:
        # Initialize fresh session
        driver.delete_all_cookies()
        driver.get("https://onlineksrtcswift.com/")
        close_ad(driver, wait)

        # Set journey details
        url = enter_journey_details(driver, wait,
            from_city=details['from'],
            to_city=details['to'],
            travel_date=details['date']
        )

        # Bus selection
        buses = display_available_buses(driver, wait)
        if not select_bus_by_time(driver, wait, buses, details['bus_time']):
            return False

        # Seat selection
        seats = available_seats(driver, wait)
        if not select_seat(driver, wait, SEAT_NUMBER, seats):
            print('false')
            return False

        # Complete booking steps
        points(wait, driver)
        enter_passenger_details(driver, wait,
            name="John Doe",
            age="30",
            gender="Male"
        )
        proceed_to_payment(driver, wait)
        enter_payee_details(driver, wait,
            mobile="9876543210",
            email="johndoe@example.com"
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
def load_page(driver,wait,details):
    SEAT_NUMBER = details['seat_number']
    try:
        # Initialize fresh session
        driver.delete_all_cookies()
        driver.get("https://onlineksrtcswift.com/")
        close_ad(driver, wait)

        # Set journey details
        url = enter_journey_details(driver, wait,
            from_city=details['from'],
            to_city=details['to'],
            travel_date=details['date']
        )
    except Exception as e:
        print(e)
    return url
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
                booking_attempt(driver, wait, details)
            
            # if booking_attempt(driver, wait, details):
            #     print('true',driver.current_url)
            #     success_count += 1
            #     print(f"Successfully locked seat! (Total locks: {success_count})")
                
            #     # Monitor current booking while waiting
            #     start_lock = datetime.now()
            #     while (datetime.now() - start_lock).total_seconds() < 560:  # 9 minutes
            #         try:
            #             # Quick availability check
            #             driver.execute_script("window.open('');")
            #             driver.switch_to.window(driver.window_handles[1])
            #             driver.get("https://onlineksrtcswift.com/")
                        
            #             if check_seat_availability(driver, wait, details):
            #                 print("Seat became available again! Restarting cycle...")
            #                 driver.close()
            #                 driver.switch_to.window(driver.window_handles[0])
            #                 break
                            
            #             driver.close()
            #             driver.switch_to.window(driver.window_handles[0])
            #             time.sleep(60)  # Check every minute
                        
            #         except Exception as e:
            #             print(f"Monitoring error: {str(e)}")
            #             break
                
            else:
                print("Seat not available, retrying...")
                print('false',driver.current_url)
                
                time.sleep(COOLDOWN_NORMAL)
                
        finally:
            teardown_browser(driver)
            time.sleep(COOLDOWN_ERROR)

def check_seat_availability(driver, wait, details):
    """Quick check if target seat is available"""
    SEAT_NUMBER = details['seat_number']
    try:
        print()

        close_ad(driver,wait)
        enter_journey_details(driver, wait,
            from_city=details['from'],
            to_city=details['to'],
            travel_date=details['date']
        )

        
        buses = display_available_buses(driver, wait)
        if not select_bus_by_time(driver, wait, buses, details['bus_time']):
            return False
            
        seats = available_seats(driver, wait)
        return any(seat['number'] == SEAT_NUMBER and seat['available'] for seat in seats)
        
    except Exception as e:
        print(f"Availability check failed: {str(e)}")
        return False
