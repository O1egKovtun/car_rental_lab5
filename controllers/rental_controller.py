from datetime import date
from services.rental_service import RentalService
from dto.rent_request_dto import RentRequestDTO
from dto.return_request_dto import ReturnRequestDTO


class RentalController:
    """Точка входу — делегує виклики RentalService, не містить логіки."""

    def __init__(self, service: RentalService):
        self._service = service

    def handle_register_customer(self, name, email,
                                  phone, driver_license) -> dict:
        ok, msg = self._service.register_customer(
            name, email, phone, driver_license)
        return {"success": ok, "message": msg}

    def handle_rent_car(self, car_id, customer_id,
                         start_date, end_date) -> dict:
        dto = RentRequestDTO(car_id, customer_id, start_date, end_date)
        ok, msg = self._service.rent_car(dto)
        return {"success": ok, "message": msg}

    def handle_return_car(self, rental_id, customer_id) -> dict:
        dto = ReturnRequestDTO(rental_id, customer_id)
        ok, msg = self._service.return_car(dto)
        return {"success": ok, "message": msg}

    def handle_search_cars(self, brand: str = "") -> dict:
        cars = self._service.search_available_cars(brand)
        return {
            "success": True,
            "cars": [{"car_id": c.car_id, "brand": c.brand,
                       "model": c.model, "year": c.year,
                       "price_per_day": c.price_per_day}
                     for c in cars]
        }
