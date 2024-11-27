from datetime import datetime
from threading import Thread

from src.models.Courier import Courier
from src.models.Order import Order
from src.strategies.DispatchStrategy import DispatchStrategy


class FifoStrategy(DispatchStrategy):

    def handle_courier_arrival(self, courier: Courier):
        self.service.waiting_couriers.put(courier)

    def dispatch_courier(self, order: Order):
        courier = Courier(len(self.service.couriers) + 1, f"Courier {len(self.service.couriers) + 1}",
                          "courier@CloudKitchens.com", "1234567890")
        courier.dispatched_time = datetime.now()
        self.service.couriers.append(courier)
        courier.perform_duty(order.id)
        Thread(target=self.service.courier_arrival, args=(courier,)).start()

    def try_pickup(self):
        while not self.service.ready_orders.empty() and not self.service.waiting_couriers.empty():
            order = self.service.ready_orders.get()
            courier = self.service.waiting_couriers.get()
            self.pickup_order(courier, order)
