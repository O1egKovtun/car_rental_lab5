from typing import Optional, List
from models.car import Car, CarStatus

class CarRepository:
    def __init__(self):
        self._cars: List[Car] = []
        self._next_id: int = 1

    def add(self, car: Car) -> Car:
        car.car_id = self._next_id
        self._cars.append(car)
        self._next_id += 1
        return car

    def find_by_id(self, car_id: int) -> Optional[Car]:
        return next((c for c in self._cars if c.car_id == car_id), None)

    def find_available(self) -> List[Car]:
        return [c for c in self._cars if c.status == CarStatus.AVAILABLE]

    def find_by_brand(self, brand: str) -> List[Car]:
        return [c for c in self._cars if brand.lower() in c.brand.lower()]

    def update(self, car: Car) -> Car:
        for i, c in enumerate(self._cars):
            if c.car_id == car.car_id:
                self._cars[i] = car
        return car

    def get_all(self) -> List[Car]:
        return list(self._cars)
