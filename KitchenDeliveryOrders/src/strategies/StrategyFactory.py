from src.strategies.DispatchStrategy import DispatchStrategy
from src.strategies.MatchedStrategy import MatchedStrategy
from src.strategies.FifoStrategy import FifoStrategy


class StrategyFactory:
    @staticmethod
    def create_strategy(strategy_type: str, service) -> DispatchStrategy:
        if strategy_type == "matched":
            return MatchedStrategy(service)
        elif strategy_type == "fifo":
            return FifoStrategy(service)
        else:
            raise ValueError("Unknown dispatch strategies")
