# AI Smart Email Assistant

A production-ready, modular AI Smart Email Assistant built with **FastAPI**, **LangGraph**, **LangChain**, and **Hugging Face Transformers**. Tracing and debugging are integrated with **LangSmith**.

## Features
- **FastAPI Backend**: Serves API endpoints for sending and receiving commands and lists/updates email states.
- **LangGraph Orchestration**: Uses a stateful agent graph workflow to handle complex multi-step reasoning processes (e.g. parsing, drafting replies, fetching tool outputs).
- **Hugging Face Integration**: Powered by open-weights models from Hugging Face via LangChain integration.
- **LangSmith Tracing**: Real-time evaluation, tracing, and prompt-monitoring for agent steps.
- **Sleek Web Interface**: Interactive single-page app displaying real-time agent execution status and communications.

---

## Directory Structure

```text
smart_email/
├── .env.example          # Template for local environment configuration
├── .gitignore            # Git exclusion patterns
├── Dockerfile            # Container definition for web app and backend
├── docker-compose.yml    # Orchestration config for containerized environment
├── requirements.txt      # Python dependencies list
├── README.md             # This document
├── app/                  # FastAPI + LangGraph Backend Package
│   ├── __init__.py
│   ├── main.py           # Application entrypoint
│   ├── config.py         # App settings loader using Pydantic Settings
│   ├── agent/            # Agent initialization and model parameters
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── graph/            # Workflow compilation & routing definition
│   │   ├── __init__.py
│   │   └── graph.py
│   ├── nodes/            # Node functions & executable tools for graph steps
│   │   ├── __init__.py
│   │   ├── email_nodes.py
│   │   └── tools.py
│   ├── state/            # State schemas representing the agent's memory
│   │   ├── __init__.py
│   │   └── state.py
│   └── utils/            # Shared utility functions
│       ├── __init__.py
│       └── helpers.py
└── frontend/             # Single-page web client
    ├── index.html        # Main template
    ├── css/
    │   └── style.css     # Premium UI styling and animations
    └── js/
        └── app.js        # Controller and API fetch interface
```

---

## Getting Started

### Prerequisites
- Python 3.11 or later
- [Docker](https://www.docker.com/) (Optional, for containerized run)

### Local Development Setup

1. **Clone and Navigate**:
   ```bash
   cd smart_email
   ```

2. **Set up Environment**:
   Copy the example environment configuration:
   ```bash
   cp .env.example .env
   ```
   Fill in your tokens in the newly created `.env` file (e.g., `LANGCHAIN_API_KEY`, `HUGGINGFACEHUB_API_TOKEN`).

3. **Install Dependencies**:
   It is highly recommended to run this inside a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/MacOS
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

4. **Run Backend Application**:
   Start the development server with live reload:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   The backend will be running at `http://localhost:8000`. You can test the API interactive docs at `http://localhost:8000/docs`.

---

## Running with Docker

You can run the application containerized using Docker and Docker Compose.

1. Make sure you have created your local `.env` configuration.
2. Build and launch:
   ```bash
   docker-compose up --build
   ```
3. Access the service at `http://localhost:8000`.
