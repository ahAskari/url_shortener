"""
Your schema states what your API expects as a request body
and what the client can expect in the response body.
You’ll implement type hinting to verify that the request and
the response match the data types that you define.
"""
from pydantic import BaseModel


class UrlBase(BaseModel):
    target_url: str


class URL(UrlBase):
    is_active: bool
    clicks: int

    class Config:
        from_attributes = True


class URLInfo(URL):
    url: str
    admin_url: str
