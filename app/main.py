import os

from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.config import settings
from app.graph.graph import workflow_graph

app = FastAPI(
    title="AI Smart Email Assistant API",
    description="Backend API for stateful LangGraph-powered email assistant",
    version="1.0.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Input Request Schema
class AnalyzeRequest(BaseModel):
    email: str


# Output Response Schema
class AnalyzeResponse(BaseModel):
    category: str
    confidence: float
    reply: str


@app.get("/")
async def root():
    """
    GET / endpoint returning service health status.
    """
    return {
        "status": "healthy",
        "service": "AI Smart Email Assistant",
        "model": "gpt-4o-mini",
        "langsmith_tracing": os.environ.get("LANGCHAIN_TRACING_V2", "false") == "true",
        "langsmith_project": settings.LANGSMITH_PROJECT
    }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_email(payload: AnalyzeRequest):
    """
    POST /analyze endpoint executing the compiled LangGraph workflow.
    """
    if not payload.email or not payload.email.strip():
        raise HTTPException(status_code=400, detail="Email content cannot be empty")

    # Define initial LangGraph state structure
    initial_state = {
        "email": payload.email,
        "category": "",
        "confidence": 0.0,
        "reply": ""
    }

    try:
        # Execute compiled LangGraph workflow pipeline
        result_state = workflow_graph.invoke(initial_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LangGraph execution error: {str(e)}")

    # Return exactly the requested fields
    return AnalyzeResponse(
        category=result_state.get("category", "Personal"),
        confidence=float(result_state.get("confidence", 0.0)),
        reply=result_state.get("reply", "")
    )


# Mount the frontend static files if directory exists under "/static" or fallback mount
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/client", StaticFiles(directory=frontend_dir, html=True), name="frontend")
else:
    print(f"Warning: Frontend static directory not found at: {frontend_dir}")
