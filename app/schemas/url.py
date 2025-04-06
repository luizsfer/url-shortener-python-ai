from pydantic import BaseModel, HttpUrl, validator
from typing import List, Optional
from datetime import datetime

class URLInput(BaseModel):
    url: str
    
    @validator("url")
    def validate_url(cls, v):
        if not v.startswith(("http://", "https://")):
            v = "https://" + v
        return v

class URLResponse(BaseModel):
    short_code: str
    original_url: str

class URLStats(BaseModel):
    short_code: str
    original_url: str
    access_count: int
    created_at: datetime
    last_accessed: Optional[datetime] = None

class URLInfo(BaseModel):
    short_code: str
    original_url: str
    access_count: int
    created_at: datetime
    last_accessed: Optional[datetime] = None

class URLList(BaseModel):
    urls: List[URLInfo]
    total: int

class URLUpdate(BaseModel):
    url: str
    
    @validator("url")
    def validate_url(cls, v):
        if not v.startswith(("http://", "https://")):
            v = "https://" + v
        return v 