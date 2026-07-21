

```markdown
#🤖 Multi-Agent Workflow Orchestrator

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green.svg)](https://fastapi.tiangolo.com/)
[![Celery](https://img.shields.io/badge/Celery-5.4.0-purple.svg)](https://docs.celeryq.dev/)
[![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)](https://www.docker.com/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Free-orange.svg)](https://openrouter.ai/)

An autonomous research pipeline powered by LangGraph, FastAPI, Celery, Redis, PostgreSQL, and Docker Compose.

## 🎯 Problem

Complex research tasks require multiple specialized steps:
- 📚 **Research** – Gather information on a topic
- 🔍 **Extract** – Pull out key facts from the research
- ✍️ **Summarize** – Condense findings into a clear summary

This project solves the problem by orchestrating **3 specialized AI agents** that work together seamlessly, with a **human-in-the-loop** ready architecture and **persistent state management**.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Request                            │
│                  (POST /workflow)                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI (API Gateway)                      │
│          Creates task ID, stores in PostgreSQL              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│               Celery + Redis (Task Queue)                   │
│               Async background processing                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   LangGraph Workflow                        │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐       │
│  │  Researcher │───▶│  Extractor │───▶│ Summarizer │       │
│  └────────────┘    └────────────┘    └────────────┘       │
│         │                 │                 │               │
│         └─────────────────┴─────────────────┘               │
│                    OpenRouter (Free AI)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                 PostgreSQL (Database)                       │
│               Stores task status and results                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Features

- ✅ **3 Specialized AI Agents** – Researcher, Extractor, Summarizer
- ✅ **Asynchronous Task Processing** – Celery + Redis for long-running jobs
- ✅ **Persistent State** – PostgreSQL stores task history across sessions
- ✅ **Containerized** – Full Docker Compose setup for easy deployment
- ✅ **Free AI Integration** – OpenRouter provides free LLM access
- ✅ **Interactive API Docs** – Swagger UI at `/docs`
- ✅ **Production-Ready** – Proper error handling, logging, and environment configuration

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **LangGraph** | Agent workflow orchestration |
| **FastAPI** | REST API gateway |
| **Celery** | Async task queue |
| **Redis** | Message broker for Celery |
| **PostgreSQL** | Persistent task storage |
| **Docker Compose** | Container orchestration |
| **OpenRouter** | Free LLM API access |

---

## 📦 Quick Start

### Prerequisites

- [Python 3.11+](https://www.python.org/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [OpenRouter Account](https://openrouter.ai/) (free)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Edubio228/multi-agent-orchestrator.git
cd multi-agent-orchestrator
```

2. **Create a `.env` file** with your OpenRouter API key:
```env
OPENROUTER_API_KEY=sk-or-v1-...
DATABASE_URL=postgresql://user:password@db:5432/mydb
REDIS_URL=redis://redis:6379/0
```

3. **Build and run with Docker:**
```bash
docker-compose up --build
```

4. **Access the API docs:**
```
http://localhost:8000/docs
```

---

## 🔧 API Usage

### Start a Research Task

```http
POST /workflow
Content-Type: application/json

{
  "topic": "What are the benefits of eating bananas?"
}
```

**Response:**
```json
{
  "task_id": "abc123-def456-ghi789",
  "status": "PENDING"
}
```

### Check Task Status

```http
GET /workflow/{task_id}
```

**Response (In Progress):**
```json
{
  "task_id": "abc123-def456-ghi789",
  "status": "RUNNING",
  "result": null
}
```

**Response (Complete):**
```json
{
  "task_id": "abc123-def456-ghi789",
  "status": "SUCCESS",
  "result": {
    "topic": "What are the benefits of eating bananas?",
    "research": "Bananas are a nutrient-dense fruit...",
    "extracted_facts": [
      "Bananas contain potassium which helps heart health.",
      "They are rich in vitamin B6.",
      "Bananas provide quick energy from natural sugars."
    ],
    "summary": "Eating bananas supports heart health, provides essential vitamins, and gives a quick energy boost."
  }
}
```

---

## 📁 Project Structure

```
multi-agent-orchestrator/
├── app/
│   ├── agents.py          # LangGraph agent definitions
│   ├── celery_worker.py   # Celery configuration
│   ├── database.py        # PostgreSQL connection
│   ├── main.py            # FastAPI application
│   ├── models.py          # SQLAlchemy models
│   └── tasks.py           # Celery task definitions
├── .env                   # Environment variables (not committed)
├── .gitignore             # Git ignore rules
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker build recipe
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## 🧪 Testing Locally (Without Docker)

If you prefer to run without Docker:

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start PostgreSQL and Redis locally** (or use Docker for just these services).

3. **Update `.env` to use localhost:**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
REDIS_URL=redis://localhost:6379/0
```

4. **Run the FastAPI app:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. **Run the Celery worker:**
```bash
celery -A app.tasks worker --loglevel=info
```

---

## 💡 Next Steps

Here are features you can add to make this even more impressive:

- 🔄 **Human-in-the-Loop** – Pause workflow for manual review before summarization
- 📊 **Dashboard** – Web UI showing all tasks and results
- 🧪 **Unit Tests** – pytest coverage for agents and API
- 🌐 **Cloud Deployment** – Deploy to AWS, GCP, or Azure
- 📈 **Monitoring** – Add Prometheus metrics and Grafana dashboards

---

## 🤝 Contributing

This is a portfolio project – feel free to fork it and make it your own!

---

## 📝 License

MIT License – feel free to use this project for learning and portfolio purposes.

---

## 🙏 Acknowledgments

- [LangGraph](https://www.langchain.com/langgraph) – For agent orchestration
- [OpenRouter](https://openrouter.ai/) – For free LLM API access
- [FastAPI](https://fastapi.tiangolo.com/) – For the beautiful API framework
- [Docker](https://www.docker.com/) – For containerization

---

## 📬 Contact

**Emmanuel Edubio** – [edubioemmanuel4@gmail.com](mailto:edubioemmanuel4@gmail.com)  
GitHub: [@your-username](https://github.com/edubio228)

---

⭐ **If you found this project helpful, please give it a star!**
```
