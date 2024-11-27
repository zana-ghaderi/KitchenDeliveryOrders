from abc import abstractmethod
from src.models.Person import Person


class Employee(Person):
    def __init__(self, employee_id, name, email, phone):
        super().__init__(name, phone)
        self.employee_id = employee_id
        self.email = email
        self.date_joined = None

    @abstractmethod
    def perform_duty(self, order_id: str) -> None:
        pass
