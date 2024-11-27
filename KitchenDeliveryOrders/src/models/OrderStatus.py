from enum import Enum


class OrderStatus(Enum):
    PREPARING, READY, PICKUP, DELIVERED, CANCELED, NONE = 1, 2, 3, 4, 5, 6
