from pydantic import BaseModel


class URLBase(BaseModel):
    target_url: str


class URL(URLBase):
    is_active: bool
    clicks: int

    class Config:
        orm_mode = True


#  you can use the data in your API without storing it in your database.
class URLInfo(URL):
    url: str
    url_admin: str
