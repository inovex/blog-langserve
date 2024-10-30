from pydantic import BaseModel


class CookieResponse(BaseModel):
    """Model for the body of the set-cookie response."""
    message: str
    value: str