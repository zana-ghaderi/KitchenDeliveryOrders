# Kitchen Delivery Service

This project simulates a real-time system for fulfilling delivery orders in a kitchen. It implements two different courier dispatch strategies: Matched and First-in-first-out (FIFO).
I used PyCharm 2024.1.4 (Community Edition) for development

## Requirements

- Python 3.12+
- No additional libraries required

## Project Structure

The project is organized into several directories and Python files, each containing a specific class or set of related classes:

### root Directory

- **main.py**: Contains the main simulation logic.
- **config.json**: Configuration file for adjusting simulation parameters.
- **dispatch_orders.json**: JSON file containing order data.
- **README**: this readme file

### src Directory

- src/core/: **Core functionality**

  - **KitchenService.py**: Contains the KitchenService class.
  - **LoggingConfig.py**: Configures the logging setup.
  - **Exceptions.py**: Defines custom exceptions for order and courier handling errors.
  
- src/models/: **Data models**
  - **Person.py**: Defines the abstract Person class.
  - **Employee.py**: Defines the abstract Employee class, which inherits from Person.
  - **Courier.py**: Defines the Courier class, which inherits from Employee.
  - **Order.py**: Defines the Order class.
  - **OrderStatus.py**: Defines the OrderStatus enum.
  
- src/strategies/: **Dispatch strategies**

  - **DispatchStrategy.py**: Defines the abstract DispatchStrategy class.
  - **MatchedStrategy.py**: Implements the MatchedStrategy for dispatching couriers.
  - **FifoStrategy.py**: Implements the FifoStrategy for dispatching couriers.
  - **StrategyFactory.py**: Provides a factory method to create dispatch strategies.
  
### tests Directory

  - **TestKitchenService.py**: Contains unit tests for the KitchenService class.

## How to Run

1. Ensure you have Python 3.12 or higher installed on your system.
2. Place all the Python files in your working directory.
3. Create a file named `dispatch_orders.json` in the same directory with your order data.
4. Run the simulation using the following command:

```bash
   python main.py
```

The simulation will run **_twice_**, once for each dispatch strategy (Matched and FIFO).

## Running Tests

To run the unit tests:

1. Ensure TestKitchenService.py is in the same directory as the other Python files.

2. Run the tests using the following command:

```bash
python -m unittest tests/TestKitchenService.py
```

## Design Decisions

- **Service-Oriented Architecture**: The main logic is encapsulated in the `KitchenService` class, which manages the entire simulation process.
- **Object-Oriented Design**: The simulation uses a class hierarchy (`Person` -> `Employee` -> `Courier`) to represent different entities in the system.
- **Enum for Order Status**: An `OrderStatus` enum is used to represent the different states an order can be in, improving code readability and maintainability.
- **Multithreading**: The service uses Python's threading module to simulate concurrent order preparation and courier arrivals.
- **Queue Data Structure**: Queues are used to manage ready orders and waiting couriers in the FIFO strategy, ensuring efficient order assignment and pickup.
- **Lock Mechanism**: A `threading.Lock` is used to ensure thread-safe operations when accessing shared resources, preventing race conditions.
- **Strategy Pattern**: The `DispatchStrategy` abstract base class and its concrete implementations (`MatchedStrategy` and `FifoStrategy`) define and encapsulate different dispatch algorithms, allowing the `KitchenService` to use different strategies interchangeably.
- **Factory Pattern**: The `StrategyFactory` class is used to create instances of the appropriate `DispatchStrategy` based on the configuration or input, promoting loose coupling and flexibility in strategy selection.

## Configuration File

A configuration file (config.json) is used to adjust simulation parameters without modifying the code directly. 
This allows for greater flexibility and easier customization of simulation settings.

Configuration File Structure
The configuration file should be in JSON format and can include the following parameters:

- order_frequency: Interval between order arrivals in seconds (default: 0.5).
- courier_arrival_time_range: A list specifying the range (min, max) for courier arrival delay in seconds (default: [3, 15]).
- number_of_orders: Total number of orders to process (default: 10).


```json
{
    "order_frequency": 0.5,
    "courier_arrival_time_range": [3, 15],
    "number_of_orders": 10
}
```

## Loging
- Logging Configuration: Logs are configured in logging_config.py to provide detailed information about events such as order receipt, preparation, courier dispatch, arrival, and pickup.
- Exception Logging: Custom exceptions (OrderLoadError, OrderProcessingError, CourierHandlingError) log errors using the configured logger.


# Output
The service prints events as they occur, including:

- Order received
- Order prepared
- Courier dispatched
- Courier arrived
- Order picked up 

After each order pickup, it prints:

- Food wait time
- Courier wait time

At the end of the simulation, it prints:

- Average food wait time
- Average courier wait time for each strategy

## Limitations

- **Performance**: The simulation currently runs in real-time, which may be slow for large datasets. A discrete-event simulation approach could be implemented for faster processing of large order volumes, or we can have micro-batches using Spark.