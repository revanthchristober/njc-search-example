from enum import Enum

class ResponseCode(Enum):
    SUCCESS = (2000, 'SUCCESS', 'successful')
    INVALID_REQUEST = (5001, "INVALID_REQUEST", "The request is invalid.")
    INTERNAL_SERVER_ERROR = (5002, "INTERNAL_SERVER_ERROR", "Oops, Something went wrong.")