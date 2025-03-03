from browser_setup import setup_browser, close_ad, teardown_browser
from journey_details import enter_journey_details, proceed_to_details
from bus_selection import display_available_buses, select_bus_by_time
from seat_selection import select_seat, available_seats
from passenger_details import enter_passenger_details
from payment_processing import enter_payee_details, proceed_to_payment
from points_selection import points
from payment_selection import click_pay_now_button

def main():
    try:
        # Initialize browser
        driver, wait = setup_browser()
        close_ad(driver, wait)

        # Set journey details
        enter_journey_details(driver, wait,
            from_city="kozhikode",
            to_city="Kothamangalam",
            travel_date="01-04-2025"
        )

        # Bus selection
        buses = display_available_buses(driver, wait)
        select_bus_by_time(driver, wait, buses, "22:15")

        # Seat selection
        available_seat = []
        available_seats(driver,available_seat)
        select_seat(driver, wait, "17",available_seat)
        points(wait,driver)
        # Passenger details
        enter_passenger_details(driver, wait,
            name="John Doe",
            age="30",
            gender="Male"
        )
        proceed_to_details(driver,wait)

        # Payment process
        enter_payee_details(driver, wait,
            mobile="9876543210",
            email="johndoe@example.com"
        )
        proceed_to_payment(driver, wait)

        click_pay_now_button(driver,wait)

    finally:
        input("Press Enter to close the browser...")
        teardown_browser(driver)

if __name__ == "__main__":
    main()
