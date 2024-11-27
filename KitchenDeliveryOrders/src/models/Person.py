from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.address = None
        self.email = None

    @abstractmethod
    def get_details(self):
        pass
