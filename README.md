# Legal AI Assistant with Endee Vector Database

An AI-powered legal document search and Q&A system using semantic search and RAG with Endee as the vector database.

## Features
- **Semantic Search**: Find legal documents using natural language queries
- **RAG Q&A**: Ask questions and get answers based on document context
- **Document Management**: Upload and process legal documents (PDF/TXT)
- **Vector Database**: Endee for high-performance similarity search
- **FastAPI Backend**: RESTful API for integration

## Tech Stack
- **Vector Database**: Endee (high-performance, SIMD-optimized)
- **Backend**: FastAPI (Python 3.12)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **LLM**: OpenAI GPT (or open-source alternatives)
- **Containerization**: Docker & Docker Compose

## Quick Start

### Prerequisites
- Python 3.12
- Docker Desktop
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/legal-ai-assistant.git
cd legal-ai-assistant

# Create virtual environment
py -3.12 -m venv venv
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
pip install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cpu

# Start Endee vector database
docker-compose -f docker-compose.endee.yml up -d

# Ingest sample documents
python scripts\ingest_sample.py

# Start API server
uvicorn app.main:app --reload
