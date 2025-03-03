from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

def  available_seats(driver,wait):
    seat_data = []
    try:
        WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.seatlook')))
    except Exception as e:
        print('loading seats failed', str(e))

    seats = driver.find_elements(By.CSS_SELECTOR,'.seatlook')

    print(len(seats),'length')
    try:
        for index, seat in enumerate(seats,1):
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
                    'index':index,
                    'element': seat,
                    'number': seat_number,
                    'fare': fare,
                    'available': is_available
                })
            except Exception as e:
                print(f"Error processing seat: {str(e)}")
                continue
    except Exception as e:
        print('error loading seats',str(e))

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
    return seat_data

def select_seat(driver, wait, selected_seat,seat_data):
    while True:
        # selected_seat = input("\nEnter seat number to book (or 'q' to quit): ").strip()
        
        if selected_seat.lower() == 'q':
            driver.quit()
            exit()
            
        # Find matching seat
        selected = next((s for s in seat_data if s['number'] == selected_seat and s['available']), None)
        print(selected)
        if not selected:
            print("Invalid seat number or seat not available!")
            driver.quit()
            return False
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
    return True

