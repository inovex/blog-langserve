from pydantic import BaseModel


class Question(BaseModel):
    """Input for the base chat endpoint."""

    question: str
    """Question input"""


class QuestionWithFilter(BaseModel):
    """Input for the rag chat endpoint"""

    question: str
    filter: dict