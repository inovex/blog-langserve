from pydantic import BaseModel


class Question(BaseModel):
    """Input for the base chat endpoint."""

    question: str
    """Question input"""
