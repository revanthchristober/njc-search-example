from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import logging

cogn_search_client = None
def get_cogn_search_client():
    global cogn_search_client
    if cogn_search_client is None:
        load_dotenv()
        # Azure Cognitive Search configuration
        cogn_search_service_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT") 
        cogn_search_index_name = os.getenv("AZURE_SEARCH_RAG_INDEX_NAME") 
        cogn_search_admin_key = os.getenv("AZURE_SEARCH_ADMIN_KEY")
        logging.info("cogn_search_service_endpoint=%s", cogn_search_service_endpoint)
        logging.info("cogn_search_index_name=%s", cogn_search_index_name)
        logging.info("cogn_search_admin_key=%s", cogn_search_admin_key)
        credential = AzureKeyCredential(cogn_search_admin_key)
        cogn_search_client = SearchClient(endpoint=cogn_search_service_endpoint, 
                                          index_name=cogn_search_index_name, 
                                          credential=credential) 
       
    return cogn_search_client  