from datetime import datetime
from threading import Thread

from src.models.Courier import Courier
from src.models.Order import Order
from src.models.OrderStatus import OrderStatus
from src.strategies.DispatchStrategy import DispatchStrategy


class MatchedStrategy(DispatchStrategy):

    def handle_courier_arrival(self, courier: Courier):
        # No specific action needed for matched strategies
        pass

    def dispatch_courier(self, order: Order):
        courier = Courier(len(self.service.couriers) + 1, f"Courier {len(self.service.couriers) + 1}",
                          "courier@CloudKitchens.com", "1234567890") # all couriers have the same metadata/ needs change
        courier.dispatched_time = datetime.now()
        courier.assigned_order = order

        self.service.couriers.append(courier)
        courier.perform_duty(order.id)
        Thread(target=self.service.courier_arrival, args=(courier,)).start()

    def try_pickup(self):
        for courier in self.service.couriers:
            if courier.arrival_time and not courier.pickup_time: # courier arrived and didn't pick up its specific order
                assigned_order = courier.assigned_order
                if assigned_order.get_order_status() == OrderStatus.READY:
                    self.pickup_order(courier, assigned_order)
