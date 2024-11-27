from src.models.Employee import Employee


class Courier(Employee):
    def __init__(self, courier_id: int, name: str, email: str, phone_number: str):
        super().__init__(courier_id, name, email, phone_number)
        self.id = courier_id
        self.dispatched_time = None
        self.arrival_time = None
        self.pickup_time = None
        self.assigned_order = None

    def perform_duty(self, order_id: str) -> None:
        print(f"Courier dispatched: {self.id} for order {order_id} at {self.dispatched_time}")

    def get_details(self):
        return f"Courier: {self.name}, ID: {self.id}, Phone: {self.phone_number}"
