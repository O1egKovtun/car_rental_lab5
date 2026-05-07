from datetime import date
from typing import List
from models.car import Car, CarStatus
from models.customer import Customer
from models.rental import Rental
from dto.rent_request_dto import RentRequestDTO
from dto.return_request_dto import ReturnRequestDTO
from repositories.car_repository import CarRepository
from repositories.customer_repository import CustomerRepository
from repositories.rental_repository import RentalRepository

MIN_NAME_LEN:    int = 2
MIN_PHONE_LEN:   int = 7
MIN_LICENSE_LEN: int = 5


class RentalService:
    def __init__(self, car_repo, customer_repo, rental_repo):
        self._car_repo      = car_repo
        self._customer_repo = customer_repo
        self._rental_repo   = rental_repo

    # ── Guard clause helpers ───────────────────────────────────────────────
    def _validate_email(self, email: str) -> bool:
        return "@" in email and "." in email

    def _validate_dates(self, start: date, end: date) -> bool:
        return end > start

    def _calculate_cost(self, start: date, end: date,
                        price_per_day: float) -> float:
        return (end - start).days * price_per_day

    # ── Сценарій 1: Реєстрація клієнта ────────────────────────────────────
    def register_customer(self, name, email, phone,
                          driver_license) -> tuple[bool, str]:
        if len(name) < MIN_NAME_LEN:
            return False, "Ім'я надто коротке"
        if not self._validate_email(email):
            return False, "Невалідний email"
        if len(phone) < MIN_PHONE_LEN:
            return False, "Телефон надто короткий"
        if len(driver_license) < MIN_LICENSE_LEN:
            return False, "Невалідне посвідчення водія"
        if self._customer_repo.find_by_email(email):
            return False, "Клієнт з таким email вже існує"
        customer = Customer(0, name, email, phone, driver_license)
        self._customer_repo.add(customer)
        return True, "Клієнта зареєстровано"

    # ── Сценарій 2: Оренда автомобіля ─────────────────────────────────────
    def rent_car(self, dto: RentRequestDTO) -> tuple[bool, str]:
        customer = self._customer_repo.find_by_id(dto.customer_id)
        if customer is None:
            return False, "Клієнта не знайдено"
        car = self._car_repo.find_by_id(dto.car_id)
        if car is None:
            return False, "Автомобіль не знайдено"
        if car.status != CarStatus.AVAILABLE:
            return False, "Автомобіль недоступний для оренди"
        if not self._validate_dates(dto.start_date, dto.end_date):
            return False, "Дата повернення має бути після дати початку"
        cost = self._calculate_cost(
            dto.start_date, dto.end_date, car.price_per_day)
        rental = Rental(0, car.car_id, customer.customer_id,
                        dto.start_date, dto.end_date, cost)
        self._rental_repo.add(rental)
        car.status = CarStatus.RENTED
        self._car_repo.update(car)
        return True, f"Оренду оформлено. Вартість: {cost:.2f} грн"

    # ── Сценарій 3: Повернення автомобіля ─────────────────────────────────
    def return_car(self, dto: ReturnRequestDTO) -> tuple[bool, str]:
        rental = self._rental_repo.find_by_id(dto.rental_id)
        if rental is None:
            return False, "Оренду не знайдено"
        if rental.customer_id != dto.customer_id:
            return False, "Клієнт не є орендарем цього автомобіля"
        if rental.is_returned:
            return False, "Автомобіль вже повернено"
        rental.is_returned = True
        self._rental_repo.update(rental)
        car = self._car_repo.find_by_id(rental.car_id)
        if car:
            car.status = CarStatus.AVAILABLE
            self._car_repo.update(car)
        return True, "Автомобіль успішно повернено"

    # ── Сценарій 4: Пошук доступних автомобілів ───────────────────────────
    def search_available_cars(self, brand: str = "") -> List[Car]:
        available = self._car_repo.find_available()
        if not brand:
            return available
        return [c for c in available if brand.lower() in c.brand.lower()]

    def get_customer_rentals(self, customer_id: int) -> List[Rental]:
        return self._rental_repo.find_by_customer(customer_id)
