from typing import Optional, List
from models.rental import Rental

class RentalRepository:
    def __init__(self):
        self._rentals: List[Rental] = []
        self._next_id: int = 1

    def add(self, rental: Rental) -> Rental:
        rental.rental_id = self._next_id
        self._rentals.append(rental)
        self._next_id += 1
        return rental

    def find_by_id(self, rental_id: int) -> Optional[Rental]:
        return next((r for r in self._rentals
                     if r.rental_id == rental_id), None)

    def find_active_by_car(self, car_id: int) -> Optional[Rental]:
        return next((r for r in self._rentals
                     if r.car_id == car_id and not r.is_returned), None)

    def find_by_customer(self, customer_id: int) -> List[Rental]:
        return [r for r in self._rentals if r.customer_id == customer_id]

    def update(self, rental: Rental) -> Rental:
        for i, r in enumerate(self._rentals):
            if r.rental_id == rental.rental_id:
                self._rentals[i] = rental
        return rental

    def get_all(self) -> List[Rental]:
        return list(self._rentals)
