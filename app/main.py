import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.config import settings
from app.graph.graph import workflow_graph


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="AI Smart Email Assistant API",
    description="Backend API for LangGraph-powered email assistant",
    version="1.0.0",
)


# =========================================================
# CORS Configuration
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Request Schema
# =========================================================

class AnalyzeRequest(BaseModel):
    email: str


# =========================================================
# Response Schema
# =========================================================

class AnalyzeResponse(BaseModel):
    category: str
    confidence: float
    reply: str


# =========================================================
# Root Route
# Redirect users to the frontend
# =========================================================

@app.get("/", include_in_schema=False)
async def root():
    """
    Redirect the main application URL to the frontend UI.
    """

    return RedirectResponse(
        url="/client/",
        status_code=307,
    )


# =========================================================
# Health Check Route
# =========================================================

@app.get("/health")
async def health():
    """
    Return backend service health information.
    """

    return {
        "status": "healthy",
        "service": "AI Smart Email Assistant",
        "model": "gpt-4o-mini",
        "classifier": "Hugging Face Remote Inference",
        "langsmith_tracing": (
            os.environ.get(
                "LANGCHAIN_TRACING_V2",
                "false",
            ).lower()
            == "true"
        ),
        "langsmith_project": settings.LANGSMITH_PROJECT,
    }


# =========================================================
# Analyze Email Route
# =========================================================

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_email(payload: AnalyzeRequest):
    """
    Execute the compiled LangGraph workflow.

    Workflow:
        Email
          ↓
        Hugging Face Classification
          ↓
        LangGraph Conditional Routing
          ↓
        Single AI Agent
          ↓
        Generated Reply
    """

    email_text = payload.email.strip()

    if not email_text:
        raise HTTPException(
            status_code=400,
            detail="Email content cannot be empty",
        )

    # Initial LangGraph state
    initial_state = {
        "email": email_text,
        "category": "",
        "confidence": 0.0,
        "reply": "",
    }

    try:
        # Execute LangGraph workflow
        result_state = workflow_graph.invoke(initial_state)

    except Exception as e:
        print(
            f"[LangGraph Execution Error] "
            f"{type(e).__name__}: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to analyze the email",
        )

    return AnalyzeResponse(
        category=result_state.get(
            "category",
            "Personal",
        ),
        confidence=float(
            result_state.get(
                "confidence",
                0.0,
            )
        ),
        reply=result_state.get(
            "reply",
            "",
        ),
    )


# =========================================================
# Frontend Static Files
# =========================================================

frontend_dir = os.path.join(
    os.path.dirname(
        os.path.dirname(__file__)
    ),
    "frontend",
)


if os.path.exists(frontend_dir):

    app.mount(
        "/client",
        StaticFiles(
            directory=frontend_dir,
            html=True,
        ),
        name="frontend",
    )

else:

    print(
        f"[Warning] Frontend directory not found: "
        f"{frontend_dir}"
    )