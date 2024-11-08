from pydantic import BaseModel


class QuestionWithFilter(BaseModel):
    """Input for the rag chat endpoint"""

    question: str
    filter: dict
