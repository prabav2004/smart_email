from typing import Any, Dict
from app.state.state import EmailAgentState
from app.utils.classifier import EmailClassifier
from app.agent.agent import EmailAgent

# Reusable classifier and agent instances
classifier = EmailClassifier()
agent = EmailAgent()


def parse_email_node(state: EmailAgentState) -> Dict[str, Any]:
    """
    Parses the email text and extracts category and confidence score.
    """
    email_text = state.get("email", "")
    
    # Run zero-shot classification
    classification = classifier.classify(email_text)
    
    return {
        "category": classification["category"],
        "confidence": classification["confidence"]
    }


def job_reply_node(state: EmailAgentState) -> Dict[str, Any]:
    """
    Generates a reply draft tailored to job inquiries.
    """
    email_text = state.get("email", "")
    reply_text = agent.generate_reply(email_text, "Job")
    return {
        "reply": reply_text
    }


def complaint_reply_node(state: EmailAgentState) -> Dict[str, Any]:
    """
    Generates a reply draft tailored to complaints.
    """
    email_text = state.get("email", "")
    reply_text = agent.generate_reply(email_text, "Complaint")
    return {
        "reply": reply_text
    }


def sales_reply_node(state: EmailAgentState) -> Dict[str, Any]:
    """
    Generates a reply draft tailored to sales inquiries.
    """
    email_text = state.get("email", "")
    reply_text = agent.generate_reply(email_text, "Sales")
    return {
        "reply": reply_text
    }


def personal_reply_node(state: EmailAgentState) -> Dict[str, Any]:
    """
    Generates a reply draft tailored to personal/other emails.
    """
    email_text = state.get("email", "")
    reply_text = agent.generate_reply(email_text, "Personal")
    return {
        "reply": reply_text
    }
