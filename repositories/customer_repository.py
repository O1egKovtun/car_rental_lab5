from typing import Optional, List
from models.customer import Customer

class CustomerRepository:
    def __init__(self):
        self._customers: List[Customer] = []
        self._next_id: int = 1

    def add(self, customer: Customer) -> Customer:
        customer.customer_id = self._next_id
        self._customers.append(customer)
        self._next_id += 1
        return customer

    def find_by_id(self, customer_id: int) -> Optional[Customer]:
        return next((c for c in self._customers
                     if c.customer_id == customer_id), None)

    def find_by_email(self, email: str) -> Optional[Customer]:
        return next((c for c in self._customers
                     if c.email.lower() == email.lower()), None)

    def get_all(self) -> List[Customer]:
        return list(self._customers)
