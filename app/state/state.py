from typing import TypedDict


class EmailAgentState(TypedDict):
    """
    Minimal LangGraph state representing the email, classification category,
    classification confidence score, and drafted reply.
    """
    email: str
    category: str
    confidence: float
    reply: str
