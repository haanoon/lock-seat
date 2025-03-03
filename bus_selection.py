from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


def display_available_buses(driver, wait):
    buses = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.srch-card')))
    
    print(f"\nFound {len(buses)} buses:")
    print("{:<5} {:<12} {:<30} {:<15} {:<10}".format(
        'No.', 'Time', 'Bus Name', 'Seats', 'Fare'))
    
    for idx, bus in enumerate(buses, 1):
        time_text = bus.find_element(By.CSS_SELECTOR, ".float-left.triptimebold.darkText1").text.split(',')[0]
        name = bus.find_element(By.CSS_SELECTOR, '.bus--type').text
        seats = bus.find_element(By.CSS_SELECTOR, '.seatcount').text.split()[0]
        fare = bus.find_element(By.CSS_SELECTOR, '.pricetag').text.replace('₹', '')
        print("{:<5} {:<12} {:<30} {:<15} {:<10}".format(idx, time_text, name[:25], seats, fare))
    
    return buses

def select_bus_by_time(driver, wait, buses, selected_time):
    for bus in buses:
        time_text = bus.find_element(By.CSS_SELECTOR, ".float-left.triptimebold.darkText1").text.split(',')[0]
        if time_text == selected_time:
            bus.find_element(By.CSS_SELECTOR, '.selectbutton').click()
            print(f"Selected bus at {selected_time}")
            return True
    return False
