from pydantic import BaseModel
from typing import Optional

class Prompt(BaseModel):
    text:  Optional[str]
    numOfImages: int 

class SuperRes(BaseModel):
    image_url: str

class TextPrompt(BaseModel):
    text:  str

class JudgementSearchRequest(BaseModel):
    query:  str
    file_id:  Optional[str] = None
    start: int
    rows: int
    is_facet_search: Optional[int] = 0  # Default value is 0
    date_of_judgement: Optional[str] = None