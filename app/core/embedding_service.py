from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any
import asyncio

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()
    
    async def generate_embeddings_async(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """Generate embeddings asynchronously"""
        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(
            None, lambda: self.model.encode(texts, batch_size=batch_size)
        )
        return embeddings.tolist()