import os
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from src.core.KitchenService import KitchenService
from src.models.Order import Order
from src.models.Courier import Courier
from src.models.OrderStatus import OrderStatus


class TestKitchenService(unittest.TestCase):
    def setUp(self):
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config.json"))
        self.simulation = KitchenService("matched", config_path)

    def test_load_orders(self):
        with patch('builtins.open',
                   unittest.mock.mock_open(read_data='[{"id": "1", "name": "Test Order", "prepTime": 10}]')):
            self.simulation.load_orders("test_orders.json")
        self.assertEqual(len(self.simulation.orders), 1)
        self.assertEqual(self.simulation.orders["1"].name, "Test Order")

    def test_receive_order(self):
        order = Order("1", "Test Order", 10)
        with patch.object(self.simulation.strategy, 'dispatch_courier') as mock_dispatch:
            self.simulation.receive_order(order)
        self.assertEqual(order.get_order_status(), OrderStatus.PREPARING)
        mock_dispatch.assert_called_once_with(order)

    @patch('time.sleep')
    def test_prepare_order(self, mock_sleep):
        order = Order("1", "Test Order", 10)
        self.simulation.prepare_order(order)
        self.assertIsNotNone(order.ready_time)
        self.assertEqual(order.get_order_status(), OrderStatus.READY)
        mock_sleep.assert_called_once_with(10)

    def test_dispatch_courier(self):
        order = Order("1", "Test Order", 10)
        with patch('src.strategies.MatchedStrategy.Thread') as mock_thread:
            self.simulation.strategy.dispatch_courier(order)
        self.assertEqual(len(self.simulation.couriers), 1)
        self.assertEqual(self.simulation.couriers[0].assigned_order, order)
        mock_thread.assert_called_once()

    @patch('time.sleep')
    def test_courier_arrival(self, mock_sleep):
        courier = Courier(1, "Test Courier", "test@example.com", "1234567890")
        self.simulation.courier_arrival(courier)
        self.assertIsNotNone(courier.arrival_time)
        mock_sleep.assert_called_once()

    def test_pickup_order(self):
        order = Order("1", "Test Order", 10)
        courier = Courier(1, "Test Courier", "test@example.com", "1234567890")
        order.ready_time = datetime.now() - timedelta(seconds=5)
        courier.arrival_time = datetime.now() - timedelta(seconds=3)
        self.simulation.strategy.pickup_order(courier, order)
        self.assertIsNotNone(order.pickup_time)
        self.assertIsNotNone(courier.pickup_time)
        self.assertEqual(order.get_order_status(), OrderStatus.PICKUP)
        self.assertEqual(self.simulation.completed_orders, 1)

    @patch('main.KitchenService.receive_order')
    @patch('main.KitchenService.prepare_order')
    def test_run_simulation(self, mock_prepare, mock_receive):
        self.simulation.orders = {"1": Order("1", "Test Order", 4)}

        # Mock methods to simulate order processing
        mock_receive.side_effect = lambda order: order.set_order_status(OrderStatus.PREPARING)
        mock_prepare.side_effect = lambda order: [
            order.prepare(),
            order.set_order_status(OrderStatus.READY),
            self.simulation.ready_orders.put(order),
            setattr(self.simulation, 'completed_orders', self.simulation.completed_orders + 1)
        ]

        self.simulation.run_simulation()

        mock_receive.assert_called_once()
        mock_prepare.assert_called_once()


if __name__ == '__main__':
    unittest.main()
