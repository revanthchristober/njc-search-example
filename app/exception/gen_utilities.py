import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.exception.generic_exception import GenericException
import time

class Genutilities():
    
    def getErrorObject(response_code):

        logging.info("status_code=%s", response_code.value[0])
        logging.info("message=%s", response_code.value[1])
        logging.info("description=%s", response_code.value[2])
        exception = GenericException(response_code.value[0], response_code.value[1], response_code.value[2])
        return exception
    
    def custom_exception_handler(request: Request, exc: GenericException) :
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=
            {
                "status": "FAIL",
                "status_code": exc.status_code,
                "message": exc.message,
                "description": exc.desc,
                "timestamp": round(time.time()*1000)
            },
        )
    
    def generate_response(response_name, response_value):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=
            {
                "status": 2000,
                "message": "successful",
                "description": "successful",
                "timestamp": round(time.time()*1000),
                response_name:response_value
            }
        )
