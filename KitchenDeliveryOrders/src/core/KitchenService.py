import json
import random
import time
from queue import Queue
from threading import Thread, Lock
from typing import List, Dict
from datetime import datetime

from src.core.exceptions import CourierHandlingError, OrderLoadError, OrderProcessingError
from src.core.loggingConfig import logger
from src.strategies.DispatchStrategy import DispatchStrategy
from src.strategies.StrategyFactory import StrategyFactory
from src.models.Order import Order
from src.models.Courier import Courier
from src.models.OrderStatus import OrderStatus


class KitchenService:
    DEFAULT_CONFIG = {
        "order_frequency": 0.5,
        "courier_arrival_time_range": [3, 15],
        "number_of_orders": 10
    }

    def __init__(self, dispatch_strategy: str, config_file: str = "../config.json"):
        self.config = self.DEFAULT_CONFIG
        self.load_config(config_file)
        self.orders: Dict[str, Order] = {}
        self.couriers: List[Courier] = []
        self.ready_orders: Queue[Order] = Queue() # used for FIFO
        self.waiting_couriers: Queue[Courier] = Queue() # used for FIFO
        self.lock = Lock()
        self.total_food_wait_time = 0
        self.total_courier_wait_time = 0
        self.completed_orders = 0

        try:
            self.strategy: DispatchStrategy = StrategyFactory.create_strategy(dispatch_strategy, self)
        except ValueError as e:
            raise ValueError(f"Invalid dispatch strategy '{dispatch_strategy}': {e}")

    def load_config(self, config_file: str):
        try:
            with open(config_file, "r") as file:
                config = json.load(file)
                self.config.update(config)
        except FileNotFoundError:
            logger.error("Configuration file 'config.json' not found. Using default values.")
        except json.JSONDecodeError:
            logger.error("Error decoding JSON from configuration file. Using default values.")
        except Exception as e:
            logger.error(f"Unexpected error while loading configuration: {e}. Using default values.")

    def courier_arrival(self, courier: Courier):
        try:
            # Use the configured arrival time range
            min_delay, max_delay = self.config.get("courier_arrival_time_range", [3, 15])
            arrival_delay = random.uniform(min_delay, max_delay)
            time.sleep(arrival_delay)
            with self.lock:
                courier.arrival_time = datetime.now()
                logger.info(f"Courier arrived: {courier.id} at {courier.arrival_time}")
                self.strategy.handle_courier_arrival(courier)
                self.strategy.try_pickup() # check if any orders are available
        except Exception as e:
            raise CourierHandlingError(f"Error handling arrival for courier {courier.id}: {e}")

    def load_orders(self, file_path: str):
        try:
            with open(file_path, 'r') as f:
                orders_data = json.load(f)
        except FileNotFoundError:
            raise OrderLoadError(f"The file '{file_path}' was not found.")
        except json.JSONDecodeError:
            raise OrderLoadError("Error decoding JSON from the file.")
        except Exception as e:
            raise OrderLoadError(f"Failed to load orders: {e}")

        for order_data in orders_data:
            try:
                order = Order(order_data['id'], order_data['name'], order_data['prepTime'])
                self.orders[order.id] = order
            except KeyError as e:
                raise OrderLoadError(f"Missing expected key in order data: {e}")
            except Exception as e:
                raise OrderLoadError(f"Error creating order from data: {e}")

    def receive_order(self, order: Order):
        with self.lock:
            try:
                order.set_order_status(OrderStatus.PREPARING)
                logger.info(f"Order received: {order.id} at {order.received_time}")
                self.strategy.dispatch_courier(order)
            except Exception as e:
                raise OrderProcessingError(f"Error processing order {order.id}: {e}")

    def prepare_order(self, order: Order):
        try:
            order.prepare()
            with self.lock:
                order.ready_time = datetime.now()
                order.set_order_status(OrderStatus.READY)
                logger.info(f"Order ready: {order.id} at {order.ready_time}")
                self.ready_orders.put(order)
                self.strategy.try_pickup() # check if any couriers are available
        except Exception as e:
            raise OrderProcessingError(f"Error preparing order {order.id}: {e}")

    def run_simulation(self):
        start_time = datetime.now()
        self.threads = []
        try:
            for order in self.orders.values():
                # if order_count >= self.config.get("number_of_orders", 10):
                #     break
                current_time = datetime.now()
                # every two seconds
                if (current_time - start_time).total_seconds() < len(self.orders) * self.config.get("order_frequency",
                                                                                                    0.5):
                    # slow down the pace
                    time.sleep(self.config.get("order_frequency", 0.5) - (
                                current_time - start_time).total_seconds() % self.config.get("order_frequency", 0.5))
                self.receive_order(order) # 1
                thread = Thread(target=self.prepare_order, args=(order,)) # 2
                thread.start()
                self.threads.append(thread)

            # make sure all orders are completed
            # for thread in self.threads: # increased complexity
            #     thread.join() # join can be more resource intensive
            while self.completed_orders < len(self.orders):
                time.sleep(0.1) # 100 millisecond

            avg_food_wait_time = self.total_food_wait_time / self.completed_orders if self.completed_orders else 0
            avg_courier_wait_time = self.total_courier_wait_time / self.completed_orders if self.completed_orders else 0
            logger.info(f"\nSimulation completed.")
            logger.info(f"Average food wait time: {avg_food_wait_time:.2f} ms")
            logger.info(f"Average courier wait time: {avg_courier_wait_time:.2f} ms")
        except Exception as e:
            raise RuntimeError(f"Error during simulation: {e}")
