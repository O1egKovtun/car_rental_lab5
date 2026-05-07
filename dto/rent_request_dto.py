from dataclasses import dataclass
from datetime import date

@dataclass
class RentRequestDTO:
    car_id:      int
    customer_id: int
    start_date:  date
    end_date:    date
