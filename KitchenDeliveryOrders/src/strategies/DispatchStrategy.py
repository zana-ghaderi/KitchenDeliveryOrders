from abc import ABC, abstractmethod
from datetime import datetime
from src.models.Order import Order
from src.models.Courier import Courier
from src.models.OrderStatus import OrderStatus


class DispatchStrategy(ABC):
    def __init__(self, service):
        self.service = service

    @abstractmethod
    def handle_courier_arrival(self, courier: Courier):
        pass

    @abstractmethod
    def dispatch_courier(self, order: Order):
        pass

    @abstractmethod
    def try_pickup(self):
        pass

    def pickup_order(self, courier: Courier, order: Order):
        courier.pickup_time = datetime.now()
        order.pickup_time = courier.pickup_time
        order.set_order_status(OrderStatus.PICKUP)
        food_wait_time = (order.pickup_time - order.ready_time).total_seconds() * 1000
        courier_wait_time = (order.pickup_time - courier.arrival_time).total_seconds() * 1000
        self.service.total_food_wait_time += food_wait_time
        self.service.total_courier_wait_time += courier_wait_time
        self.service.completed_orders += 1
        print(f"Order picked up: {order.id} by courier {courier.id} at {order.pickup_time}")
        print(f"Food wait time: {food_wait_time:.2f} ms")
        print(f"Courier wait time: {courier_wait_time:.2f} ms")
