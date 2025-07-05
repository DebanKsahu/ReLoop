from enum import Enum

class LoggerType(str, Enum):
    USER = "User"
    WORKER = "Worker"

class ResponseType(str, Enum):
    SUCCESS = "Successful"
    FAILURE = "Unsuccessful"

class TransactionType(str, Enum):
    SPEND = "Coin Spent"
    EARN = "Coin Earned"

class ScanMode(str, Enum):
    CHECKOUT = "Checkout"
    RECYCLE = "Recycle"