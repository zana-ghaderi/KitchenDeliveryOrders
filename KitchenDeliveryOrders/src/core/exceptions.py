from src.core.loggingConfig import logger


class OrderLoadError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        logger.error(message)


class OrderProcessingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        logger.error(message)


class CourierHandlingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        logger.error(message)
