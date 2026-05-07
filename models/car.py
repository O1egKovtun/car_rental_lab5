    from dataclasses import dataclass
from enum import Enum

class CarStatus(Enum):
    AVAILABLE   = "available"
    RENTED      = "rented"
    MAINTENANCE = "maintenance"

@dataclass
class Car:
    car_id:        int
    brand:         str
    model:         str
    year:          int
    price_per_day: float
    status: CarStatus = CarStatus.AVAILABLE
