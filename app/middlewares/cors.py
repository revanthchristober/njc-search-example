from fastapi.middleware.cors import CORSMiddleware
from logger import get_logger
from dotenv import load_dotenv
import os

load_dotenv()
logger = get_logger(__name__)

origins = ["*"]
if os.getenv("allowed_origins") is not None:
    allowed_origins = os.getenv("allowed_origins")
    origins_list = allowed_origins.split(',')
    origins = [s.strip() for s in origins_list]

http_methods = ["*"]
if os.getenv("allowed_http_methods") is not None:
    allowed_http_methods = os.getenv("allowed_http_methods")
    methods_list = allowed_http_methods.split(',')
    http_methods = [s.strip() for s in methods_list]

def add_cors_middleware(app):
    logger.debug("allowed origin for api consumption=%s", origins)
    logger.debug("allowed http-methods for api consumption=%s", http_methods)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=http_methods,
        allow_headers=["*"],
    )

