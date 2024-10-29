from dotenv import load_dotenv
import os
import logging
import pysolr
from app.core.response_code import ResponseCode
from app.exception.gen_utilities import Genutilities
from fastapi import HTTPException
from logger import get_logger
from dotenv import dotenv_values

logger = get_logger(__name__)

# Set connection timeout and read timeout values (in seconds)
connection_timeout = 5
read_timeout = 10
solr_search_client = None

# def get_solr_search_client():
#     global solr_search_client
#     try:
#         if solr_search_client is None:
#             load_dotenv()
#             # Azure Cognitive Search configuration
#             solr_service_endpoint = os.getenv("SOLR_SEARCH_SERVICE_ENDPOINT")  
#             solr_search_client = pysolr.Solr(solr_service_endpoint, timeout=(connection_timeout, read_timeout))
#             logging.info("solr_service_endpoint=%s", solr_service_endpoint)
#         return solr_search_client
    
#     except HTTPException as e:
#         response_code = ResponseCode.INTERNAL_SERVER_ERROR
#         raise Genutilities.getErrorObject(response_code) 

def get_solr_search_client():
    solr_search_client=None
    try:
        # Load .env file contents
        env_values = dotenv_values(".env")
        #Debugging Code
        # print("***************************************************")
        # print(env_values)
        # solr_service_endpoint = env_values.get("SOLR_SEARCH_SERVICE_ENDPOINT")
        # print(solr_service_endpoint)
        # print("***************************************************")
        #load_dotenv()
        
        solr_service_endpoint = env_values.get("SOLR_SEARCH_SERVICE_ENDPOINT")  
        solr_search_client = pysolr.Solr(solr_service_endpoint, timeout=(connection_timeout, read_timeout))
        logging.info("solr_service_endpoint=%s", solr_service_endpoint)
    except Exception as e:
        logger.error("Error occured while creating Solr connection!")
    
    return solr_search_client

def get_similar_case_solr_client():
    solr_search_client=None
    try:
        load_dotenv()
        solr_service_endpoint = os.getenv("SOLR_SIMILAR_CASES_SERVICE_ENDPOINT")  
        solr_search_client = pysolr.Solr(solr_service_endpoint, timeout=(connection_timeout, read_timeout))
        logging.info("solr_service_endpoint=%s", solr_service_endpoint)
    except Exception as e:
        logger.error("Error occured while creating Solr connection!")
    
    return solr_search_client