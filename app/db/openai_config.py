from dotenv import load_dotenv
import os
from openai import AzureOpenAI

azure_openai_rag_client = None
def get_azure_openai_rag_client():
    global azure_openai_rag_client
    if azure_openai_rag_client is None:
        load_dotenv()
        azure_openai_rag_client = AzureOpenAI(
            api_key = os.getenv("AZURE_OPENAI_RAG_API_KEY"),  
            api_version = os.getenv("AZURE_OPENAI_RAG_API_VERSION"),
            azure_endpoint = os.getenv("AZURE_OPENAI_RAG_ENDPOINT"),
            azure_deployment = os.getenv("AZURE_OPENAI_RAG_DEPLOYMENT_NAME")
    )
    return azure_openai_rag_client