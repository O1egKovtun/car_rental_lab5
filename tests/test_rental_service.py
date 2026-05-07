import pytest
from datetime import date
from models.car import Car
from repositories.car_repository import CarRepository
from repositories.customer_repository import CustomerRepository
from repositories.rental_repository import RentalRepository
from services.rental_service import RentalService
from dto.rent_request_dto import RentRequestDTO
from dto.return_request_dto import ReturnRequestDTO


@pytest.fixture
def service():
    return RentalService(CarRepository(), CustomerRepository(),
                         RentalRepository())

@pytest.fixture
def service_with_data(service):
    service._car_repo.add(Car(0, "Toyota", "Camry", 2022, 500.0))
    service.register_customer(
        "Іван Петренко", "ivan@email.com", "0501234567", "AB12345")
    return service


def test_register_customer_success(service):
    ok, msg = service.register_customer(
        "Іван Петренко", "ivan@email.com", "0501234567", "AB12345")
    assert ok is True and "зареєстровано" in msg

def test_register_customer_invalid_email(service):
    ok, msg = service.register_customer(
        "Іван", "bad-email", "0501234567", "AB12345")
    assert ok is False and "email" in msg.lower()

def test_register_customer_duplicate_email(service):
    service.register_customer("Іван", "ivan@email.com", "0501234567", "AB12345")
    ok, msg = service.register_customer(
        "Оля", "ivan@email.com", "0679876543", "CD67890")
    assert ok is False and "вже існує" in msg

def test_rent_car_success(service_with_data):
    dto = RentRequestDTO(1, 1, date(2026, 6, 1), date(2026, 6, 5))
    ok, msg = service_with_data.rent_car(dto)
    assert ok is True and "2000.00" in msg   # 4 дні × 500 грн

def test_rent_already_rented_car(service_with_data):
    dto = RentRequestDTO(1, 1, date(2026, 6, 1), date(2026, 6, 5))
    service_with_data.rent_car(dto)
    ok, msg = service_with_data.rent_car(dto)
    assert ok is False and "недоступний" in msg

def test_rent_car_customer_not_found(service_with_data):
    dto = RentRequestDTO(1, 999, date(2026, 6, 1), date(2026, 6, 5))
    ok, msg = service_with_data.rent_car(dto)
    assert ok is False and "Клієнта не знайдено" in msg

def test_return_car_success(service_with_data):
    service_with_data.rent_car(
        RentRequestDTO(1, 1, date(2026, 6, 1), date(2026, 6, 5)))
    ok, msg = service_with_data.return_car(ReturnRequestDTO(1, 1))
    assert ok is True and "повернено" in msg

def test_return_car_already_returned(service_with_data):
    service_with_data.rent_car(
        RentRequestDTO(1, 1, date(2026, 6, 1), date(2026, 6, 5)))
    service_with_data.return_car(ReturnRequestDTO(1, 1))
    ok, msg = service_with_data.return_car(ReturnRequestDTO(1, 1))
    assert ok is False and "вже повернено" in msg

def test_search_available_cars(service_with_data):
    cars = service_with_data.search_available_cars()
    assert len(cars) == 1 and cars[0].brand == "Toyota"

def test_search_after_rental(service_with_data):
    service_with_data.rent_car(
        RentRequestDTO(1, 1, date(2026, 6, 1), date(2026, 6, 5)))
    assert service_with_data.search_available_cars() == []

def test_search_by_brand(service_with_data):
    service_with_data._car_repo.add(Car(0, "BMW", "X5", 2021, 800.0))
    cars = service_with_data.search_available_cars(brand="Toyota")
    assert len(cars) == 1 and cars[0].brand == "Toyota"

def test_rent_car_invalid_dates(service_with_data):
    dto = RentRequestDTO(1, 1, date(2026, 6, 5), date(2026, 6, 1))
    ok, msg = service_with_data.rent_car(dto)
    assert ok is False and "дата" in msg.lower()
