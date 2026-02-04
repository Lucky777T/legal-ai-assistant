from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime

from app.config import settings
from app.core.endee_client import EndeeClient
from app.core.embedding_service import EmbeddingService

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"Starting {settings.APP_NAME}...")
    
    # Initialize services
    app.state.endee_client = EndeeClient(
        host=settings.ENDEE_HOST,
        port=settings.ENDEE_PORT,
        token=settings.ENDEE_TOKEN
    )
    
    app.state.embedding_service = EmbeddingService(
        model_name=settings.EMBEDDING_MODEL
    )
    
    # Health check
    is_healthy = await app.state.endee_client.health_check()
    if not is_healthy:
        print("Warning: Endee server is not reachable")
    
    yield
    
    # Shutdown
    print(f"Shutting down {settings.APP_NAME}...")

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered legal document search and Q&A system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Legal AI Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health():
    endee_healthy = False
    if hasattr(app.state, 'endee_client'):
        endee_healthy = await app.state.endee_client.health_check()
    
    return {
        "status": "healthy" if endee_healthy else "degraded",
        "endee_connected": endee_healthy,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/search/test")
async def test_search(query: str = "legal document"):
    """Test search endpoint"""
    if not hasattr(app.state, 'endee_client'):
        return {"error": "Endee client not initialized"}
    
    # Generate embedding for query
    embedding = app.state.embedding_service.generate_embeddings([query])[0]
    
    # Search in Endee
    results = await app.state.endee_client.search(
        index_name=settings.INDEX_NAME,
        query_vector=embedding,
        top_k=5
    )
    
    return {
        "query": query,
        "results": results[:2],  # Return only 2 for testing
        "total": len(results)
    }