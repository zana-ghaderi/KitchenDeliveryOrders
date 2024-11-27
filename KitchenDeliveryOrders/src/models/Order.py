from datetime import datetime
import time

from src.models.OrderStatus import OrderStatus


class Order:
    def __init__(self, order_id: str, name: str, prep_time: int):
        self.id = order_id
        self.name = name
        self.prep_time = prep_time
        self.received_time = datetime.now()
        self.ready_time = None
        self.pickup_time = None
        self.order_status = OrderStatus.NONE

    def prepare(self):
        time.sleep(self.prep_time)
        self.ready_time = datetime.now()

    def set_order_status(self, order_status):
        self.order_status = order_status

    def get_order_status(self):
        return self.order_status
