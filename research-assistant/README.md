# AI Research/Summarizer/Editor Assistant

A multi-agent research system powered by CrewAI that helps with in-depth research on any topic.

## System Architecture

This system uses three specialized AI agents to perform research:

1. **Research Agent**: Gathers and structures information on the research topic
2. **Summarizer Agent**: Condenses research findings into a digestible summary
3. **Editor Agent**: Refines and polishes the content for final delivery

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **AI Framework**: CrewAI with OpenAI's API
- **Deployment**: Docker and Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose
- OpenAI API key

### Setup and Run

1. Clone this repository
2. Set your OpenAI API key in an environment variable:
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```
3. Start the services:
   ```bash
   docker-compose up -d
   ```
4. Open the frontend in your browser:
   ```
   http://localhost:8501
   ```

## Development

### Backend

The backend is located in the `backend/` directory and uses FastAPI. To run it locally:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

The frontend is located in the `frontend/` directory and uses Streamlit. To run it locally:

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
