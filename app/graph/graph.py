from langgraph.graph import StateGraph, END

from app.state.state import EmailAgentState
from app.nodes.email_nodes import (
    parse_email_node,
    job_reply_node,
    complaint_reply_node,
    sales_reply_node,
    personal_reply_node,
)


def route_by_category(state: EmailAgentState) -> str:
    """
    Conditional routing logic that inspects the classified category in state
    and returns the next node target name.
    """
    category = state.get("category", "Personal")
    
    # Standardize category matching
    if category == "Job":
        return "job_reply"
    elif category == "Complaint":
        return "complaint_reply"
    elif category == "Sales":
        return "sales_reply"
    else:
        return "personal_reply"


# 1. Define the workflow builder using the minimal state
workflow = StateGraph(EmailAgentState)

# 2. Add nodes
workflow.add_node("classify_email", parse_email_node)
workflow.add_node("job_reply", job_reply_node)
workflow.add_node("complaint_reply", complaint_reply_node)
workflow.add_node("sales_reply", sales_reply_node)
workflow.add_node("personal_reply", personal_reply_node)

# 3. Set entrypoint
workflow.set_entry_point("classify_email")

# 4. Set conditional edges for category routing
workflow.add_conditional_edges(
    "classify_email",
    route_by_category,
    {
        "job_reply": "job_reply",
        "complaint_reply": "complaint_reply",
        "sales_reply": "sales_reply",
        "personal_reply": "personal_reply",
    }
)

# 5. Set terminal edges from replies to END
workflow.add_edge("job_reply", END)
workflow.add_edge("complaint_reply", END)
workflow.add_edge("sales_reply", END)
workflow.add_edge("personal_reply", END)

# 6. Compile the graph
workflow_graph = workflow.compile()
