from enum import Enum

class LoggerType(str, Enum):
    USER = "User"
    WORKER = "Worker"

class ResponseType(str, Enum):
    SUCCESS = "Successful"
    FAILURE = "Unsuccessful"