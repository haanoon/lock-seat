
from continous_booking import continuous_booking_

details = {
    'INTERVAL':60,
    'COOLDOWN_ERROR': 10,
    'MAX_ATTEMPTS' :100,
    'seat_number' :'35',
    'from': 'Sultan Bathery',
    'to': 'Kumily',
    'date':'31-03-2025',
    'phone':'9876543210',
    'email':'muhammed@gmail.com',
    'name': 'Muhammed',
    'gender':'Male',
    'age':22,
    'bus_time':'20:00',
    'seat_lock':True,
    'full_details':{
        'from': 'Kannur',
        'to': 'Munnar',
        'date':'31-03-2025',
        'bus_time':'21:30',
    }
}

continuous_booking_(details)