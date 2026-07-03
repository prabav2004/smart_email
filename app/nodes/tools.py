from langchain_core.tools import tool


@tool
def search_email_archive(query: str) -> str:
    """
    Search the email database archive for context about past conversations.
    """
    # Stub response
    return f"Search result stub for query: '{query}'. Found 0 matches."


@tool
def update_draft_reply(draft_id: str, new_content: str) -> str:
    """
    Updates the email reply draft with edited content.
    """
    # Stub response
    return f"Successfully updated draft {draft_id}."
