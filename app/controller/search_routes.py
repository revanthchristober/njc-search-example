from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from app.core.response_code import ResponseCode
from app.exception.gen_utilities import Genutilities
from app.service.search_service import SearchService
import logging
from app.commons.schema import JudgementSearchRequest

load_dotenv()
search_routes = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Not found"}},
)

@search_routes.get("/ping")
async def ping():
    return {"status" : "OK"}

search_service = SearchService()

@search_routes.post("/judgement_search")
async def judgement_search(judgement_search_request: JudgementSearchRequest):
    
    #validate request
    if judgement_search_request.query == None or len(judgement_search_request.query.strip())==0:
        response_code = ResponseCode.INVALID_REQUEST
        raise Genutilities.getErrorObject(response_code)
    
    result = []
    try:
        logging.info("judgement_search_request.query=%s", judgement_search_request.query)
        result = search_service.get_search_result(judgement_search_request)
        logging.info("result=%s", result)
    except HTTPException as e:
        response_code = ResponseCode.INTERNAL_SERVER_ERROR
        raise Genutilities.getErrorObject(response_code)    
    
    return Genutilities.generate_response("search_response", result)
    # return JSONResponse(
    #         status_code=status.HTTP_200_OK,
    #         content=
    #         {
    #             "status": 2000,
    #             "message": "successful",
    #             "description": "successful",
    #             "timestamp": round(time.time()*1000),
    #             "search_response":result
    #         }
    #     )

@search_routes.post("/autosuggest")
async def judgement_search(judgement_search_request: JudgementSearchRequest):
    #validate request
    if judgement_search_request.query == None or len(judgement_search_request.query.strip())==0:
        response_code = ResponseCode.INVALID_REQUEST
        raise Genutilities.getErrorObject(response_code)
    
    suggestions = []
    try:
        logging.info("judgement_search_request.query=%s", judgement_search_request.query)
        suggestions = search_service.get_autosuggest_result(judgement_search_request)
        logging.info("suggestions=%s", suggestions)
        return Genutilities.generate_response("suggestions", suggestions)
    except HTTPException as e:
        response_code = ResponseCode.INTERNAL_SERVER_ERROR
        raise Genutilities.getErrorObject(response_code) 


@search_routes.post("/courtname_search")
async def courtname_search(judgement_search_request: JudgementSearchRequest):
    
    #validate request
    if judgement_search_request.query == None or len(judgement_search_request.query.strip())==0:
        response_code = ResponseCode.INVALID_REQUEST
        raise Genutilities.getErrorObject(response_code)
    
    result = []
    try:
        logging.info("judgement_search_request.query=%s", judgement_search_request.query)
        result = search_service.get_search_result_for_courtname(judgement_search_request)
        logging.info("result=%s", result)
    except HTTPException as e:
        response_code = ResponseCode.INTERNAL_SERVER_ERROR
        raise Genutilities.getErrorObject(response_code)    
    
    return Genutilities.generate_response("search_response", result)

@search_routes.post("/similar_cases")
async def judgement_search(judgement_search_request: JudgementSearchRequest):
    
    #validate request
    if judgement_search_request.query == None or len(judgement_search_request.query.strip())==0:
        response_code = ResponseCode.INVALID_REQUEST
        raise Genutilities.getErrorObject(response_code)
    
    result = []
    try:
        logging.info("judgement_search_request.query=%s", judgement_search_request.query)
        result = search_service.get_similar_cases(judgement_search_request)
        logging.info("result=%s", result)
    except HTTPException as e:
        print(e)
        response_code = ResponseCode.INTERNAL_SERVER_ERROR
        raise Genutilities.getErrorObject(response_code)
    return Genutilities.generate_response("similar_case", result)

@search_routes.get("/court_cases_count")
async def court_cases_count():
    result = {}
    try:
        result = search_service.get_court_cases_count()
        logging.info("result=%s", result)
    except HTTPException as e:
        print(e)
        response_code = ResponseCode.INTERNAL_SERVER_ERROR
        raise Genutilities.getErrorObject(response_code)
    return Genutilities.generate_response("case_count", result)                
