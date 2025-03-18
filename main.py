
from continous_booking import continuous_booking_

details = {
    'INTERVAL':60,
    'COOLDOWN_ERROR': 10,
    'MAX_ATTEMPTS' :100,
    'seat_number' :'18',
    'from': 'Kozhikode',
    'to': 'Kothamangalam',
    'date':'19-03-2025',
    'phone':'9876543210',
    'email':'muhammed@gmail.com',
    'name': 'Muhammed',
    'gender':'Male',
    'bus_time':'22:35',
    'seat_lock':True,
    'full_details':{
        'from': 'Kannur',
        'to': 'Munnar',
        'date':'19-03-2025',
        'bus_time':'21:30',
    }
}

continuous_booking_(details)