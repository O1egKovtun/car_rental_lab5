from dataclasses import dataclass
from datetime import date

@dataclass
class Rental:
    rental_id:   int
    car_id:      int
    customer_id: int
    start_date:  date
    end_date:    date
    total_cost:  float
    is_returned: bool = False
