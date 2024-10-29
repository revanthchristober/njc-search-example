
from app.commons.schema import JudgementSearchRequest
from app.db.solr_config import get_solr_search_client, get_similar_case_solr_client
import traceback
from logger import get_logger
from app.core.response_code import ResponseCode
from app.exception.gen_utilities import Genutilities
import math

logger = get_logger(__name__)

class SearchService():
    def get_search_result(self, judgement_search_request: JudgementSearchRequest):  
        try:
            solr_client = get_solr_search_client()
            #query_fields = ''  
            if judgement_search_request.is_facet_search==1:
                query_fields = "state_high_court_s"
                query = 'state_high_court_s:"'+ judgement_search_request.query +'"'
                query_params = {
                    "fl": "*,score",  # Fields to return in the response
                    "start": judgement_search_request.start,  # Start index for pagination (zero-based)
                    "rows": judgement_search_request.rows  # Number of rows to return per page
                }
                solr_response = solr_client.search(query, **query_params)
            else:
                query_fields = 'charge_number_s^1000 appellants_txt respondents_txt court_name_t state_high_court_s primary_judge_name_t file_id_s'
                query_params = {
                    "q": judgement_search_request.query,
                    "defType": "edismax",  # Use eDisMax query parser
                    "qf" : query_fields,
                    "pf": "citations_txt^10 primary_judge_name_t^5 court_name_t",  # Phrase fields and their boosts
                    "mm": "1<50% 2<75%",  # Minimum should match parameter
                    "fl": "*,score",  # Fields to return in the response
                    "start": judgement_search_request.start,  # Start index for pagination (zero-based)
                    "rows": judgement_search_request.rows  # Number of rows to return per page
                }
                solr_response = solr_client.search(**query_params)
        except Exception as e:
            response_code = ResponseCode.INTERNAL_SERVER_ERROR
            raise Genutilities.getErrorObject(response_code)  

        judgement_search_response = {}
        num_found = solr_response.hits
        judgement_search_response['totalCount'] = num_found
        judgement_search_response['totalPages'] = math.ceil(num_found/judgement_search_request.rows)
        search_response = []
        for item in solr_response:
            search_item = {}
            #search_item["doc_id"] = item['id']
            search_item['file_id'] = item['file_id_s']
            search_item['file_name'] = item['file_name_s']
            #search_item['directory_path'] = item['directory_path_s']
            try:
                if 'court_name_t' in item:
                    search_item['court_name'] = item['court_name_t']
                search_item['court_type'] = item['court_type_t']
                search_item['judge_name'] = item['primary_judge_name_t']
                if 'judgement_date_dt' in item:
                    search_item['date_of_judgement'] = item['judgement_date_dt']
                if 'charge_number_s' in item:    
                    search_item['charge_number'] = item['charge_number_s']
                if 'appellants_txt' in item:
                    search_item['appellant'] = item['appellants_txt']
                if 'respondents_txt' in item:
                    search_item['respondent'] = item['respondents_txt']               
                if 'citations_txt' in item:
                    search_item['citations'] = item['citations_txt']
                    search_item['no_of_citations'] = str(len(item['citations_txt']))  
            except Exception as e:
                logger.error(e)    
            
            search_response.append(search_item)
        judgement_search_response['result'] = search_response
        return judgement_search_response

    def get_autosuggest_result(self, judgement_search_request: JudgementSearchRequest):   
        solr_response = []
        try:
            solr_client = get_solr_search_client()
            query_params = {
            "q": judgement_search_request.query,
            "defType": "edismax",  # Use eDisMax query parser
            "qf": "autoSuggestEdgeNgram",  # Query fields and their boosts
            "fl": "*,score",  # Fields to return in the response
            "start": judgement_search_request.start,  # Start index for pagination (zero-based)
            "rows": judgement_search_request.rows  # Number of rows to return per page
            }    
            solr_response = solr_client.search(**query_params)
        except Exception as e:
            response_code = ResponseCode.INTERNAL_SERVER_ERROR
            raise Genutilities.getErrorObject(response_code)  
        
        search_response = []
        for item in solr_response:
            if 'citations_txt' in item:
                citations = item['citations_txt']
                for citation in citations:
                    if citation.lower().startswith(judgement_search_request.query.lower()):
                        search_response.append(citation)
        
        return search_response 
    
    def get_search_result_for_courtname(self, judgement_search_request: JudgementSearchRequest):  
        try:
            solr_client = get_solr_search_client()
            query_params = {
                "q": judgement_search_request.query,
                "defType": "edismax",  # Use eDisMax query parser
                "qf": "court_type_t^10 court_name_t",  # Query fields and their boosts
                "pf": "court_type_t^10 court_name_t",  # Phrase fields and their boosts
                "mm": "1<50% 2<75%",  # Minimum should match parameter
                "fl": "*,score",  # Fields to return in the response
                "start": judgement_search_request.start,  # Start index for pagination (zero-based)
                "rows": judgement_search_request.rows  # Number of rows to return per page
            }
            solr_response = solr_client.search(**query_params)
        except Exception as e:
            response_code = ResponseCode.INTERNAL_SERVER_ERROR
            raise Genutilities.getErrorObject(response_code)  

        judgement_search_response = {}
        num_found = solr_response.hits
        judgement_search_response['totalCount'] = num_found
        judgement_search_response['totalPages'] = math.ceil(num_found/judgement_search_request.rows)
        search_response = []
        for item in solr_response:
            search_item = {}
            #search_item["doc_id"] = item['id']
            search_item['file_id'] = item['file_id_s']
            search_item['file_name'] = item['file_name_s']
            #search_item['directory_path'] = item['directory_path_s']
            search_item['court_name'] = item['court_name_t']
            search_item['court_type'] = item['court_type_t']
            search_item['judge_name'] = item['primary_judge_name_t']
            if 'judgement_date_dt' in item:
                search_item['date_of_judgement'] = item['judgement_date_dt']
            search_item['charge_number'] = item['charge_number_s']
            if 'appellants_txt' in item:
                search_item['appellant'] = item['appellants_txt']
            if 'respondents_txt' in item:
                search_item['respondent'] = item['respondents_txt']
            
            if 'citations_txt' in item:
                search_item['citations'] = item['citations_txt']
                search_item['no_of_citations'] = str(len(item['citations_txt']))

            search_response.append(search_item)
        judgement_search_response['result'] = search_response
        return judgement_search_response
    
    def get_similar_cases(self, judgement_search_request: JudgementSearchRequest):  
        try:
            solr_client = get_similar_case_solr_client()
            query_params = {
                "q": judgement_search_request.query,
                "defType": "edismax",  # Use eDisMax query parser
                "qf": "charges_arr_txt^1000",  # Query fields and their boosts
                "pf": "charges_arr_txt",  # Phrase fields and their boosts
                "fl": "*,score",  # Fields to return in the response
                "start": judgement_search_request.start,  # Start index for pagination (zero-based)
                "rows": judgement_search_request.rows  # Number of rows to return per page
            }
            excluded_id = judgement_search_request.file_id
            # Add filter query to exclude the specific ID
            if excluded_id is not None:
                query_params["fq"] = f"-file_id_s:{excluded_id}"
                if judgement_search_request.date_of_judgement is not None:
                    query_params["fq"] = f"judgement_date_dt:[* TO {judgement_search_request.date_of_judgement}]"
                
            solr_response = solr_client.search(**query_params)
        except Exception as e:
            print(e)
            response_code = ResponseCode.INTERNAL_SERVER_ERROR
            raise Genutilities.getErrorObject(response_code)  

        judgement_search_response = {}
        num_found = solr_response.hits
        judgement_search_response['totalCount'] = num_found
        search_response = []
        for item in solr_response:
            search_item = {}
            search_item['file_id'] = item['file_id_s']
            search_item['file_name'] = item['file_name_s']
            search_item['charges'] = item['charges_arr_txt']
            search_item['charges_with_details_t'] = item['charges_with_details_t']
            search_item['sentence'] = item['sentence_t']
            search_item['json_data'] = item['json_data']
            if 'judgement_date_dt' in item:
                search_item['judgement_date'] = item['judgement_date_dt']
            search_item['score'] = item['score']
            search_response.append(search_item)
        judgement_search_response['result'] = search_response
        return judgement_search_response
    
    def get_court_cases_count(self):  
        try:
            solr_client = get_solr_search_client()
            query_params = {
                'q': '*:*',  # Main query
                'facet': 'true',  # Enable faceting
                'facet.field': 'state_high_court_s',  # Field to facet on
                'rows': 0  # We don't need actual documents, just the facet counts
            }

            cases_count_response={}  
            # Perform the search
            results = solr_client.search(**query_params)
            facet_counts = results.facets
            logger.debug("facet_counts=%s", facet_counts)
            if 'facet_fields' in facet_counts:
                for field, counts in facet_counts['facet_fields'].items():
                    logger.debug("field: %s", field)
                    for i in range(0, len(counts), 2):
                        value = counts[i]
                        count = counts[i + 1]
                        logger.debug("state=%s : case count=%s", value, count)
                        cases_count_response[value]=count
            return cases_count_response
        except Exception as e:
            print(e)
            response_code = ResponseCode.INTERNAL_SERVER_ERROR
            raise Genutilities.getErrorObject(response_code)

        