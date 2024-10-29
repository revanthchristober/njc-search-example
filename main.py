import uvicorn
from fastapi import FastAPI
from app.controller import search_routes as search_router
import logging
from uvicorn.config import LOGGING_CONFIG
from app.exception.generic_exception import GenericException
from app.exception.gen_utilities import Genutilities
from app.middlewares.cors import add_cors_middleware
import os

app = FastAPI()
# add origins and methods that are to be allowed
add_cors_middleware(app)

#adding custom exceptional handler
app.add_exception_handler(GenericException, Genutilities.custom_exception_handler)

#Adding routers
app.include_router(search_router.search_routes)

@app.get("/ping")
async def index():
   logging.info("ping function is working fine!")
   return {"message": "sucess"}

if __name__ == "__main__":

   server_log_format = "%(asctime)s [%(process)d] %(levelname)s %(filename)s : %(lineno)d - %(message)s"
   
   #log format for logger
   logging.basicConfig(
        level=logging.DEBUG,
        format=server_log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
   
   LOGGING_CONFIG["formatters"]["default"]["fmt"] = server_log_format
   
   # Starting uvicorn server
   uvicorn_host = os.getenv("UVICORN_HOST")
   uvicorn_port = os.getenv("UVICORN_PORT")
   uvicorn_workers = os.getenv("UVICORN_WORKERS")
   uvicorn.run(
               "main:app", 
               host=uvicorn_host, 
               port=int(uvicorn_port), 
               reload=False, 
               workers=int(uvicorn_workers)
            )