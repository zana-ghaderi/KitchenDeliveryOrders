from src.core.KitchenService import KitchenService
from src.core.loggingConfig import logger

if __name__ == "__main__":
    for strategy in ["matched", "fifo"]:
        logger.info(f"\nRunning simulation with {strategy} strategy:")
        simulation = KitchenService(strategy, "config.json")
        simulation.load_orders("dispatch_orders.json")
        simulation.run_simulation()