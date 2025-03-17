
from continous_booking import continuous_booking_

details = {
    'INTERVAL':60,
    'COOLDOWN_ERROR': 10,
    'MAX_ATTEMPTS' :100,
    'seat_number' :'21',
    'from': 'Kozhikode',
    'to': 'Kothamangalam',
    'date':'01-04-2025',
    'phone':'9876543210',
    'email':'name@gmail.com',
    'name': 'Jhon F',
    'gender':'Male',
    'bus_time':'22:15'
}

continuous_booking_(details)