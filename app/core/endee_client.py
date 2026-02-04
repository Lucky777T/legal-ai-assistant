import httpx
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class EndeeClient:
    def __init__(self, host: str = "localhost", port: int = 8080, token: Optional[str] = None):
        self.base_url = f"http://{host}:{port}"
        self.headers = {}
        if token:
            self.headers["Authorization"] = token
        
    async def health_check(self) -> bool:
        """Check if Endee server is healthy"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/api/v1/health", headers=self.headers)
                return response.status_code == 200
            except:
                return False
    
    async def create_index(self, index_name: str, dimension: int) -> bool:
        """Create a new vector index"""
        async with httpx.AsyncClient() as client:
            payload = {
                "name": index_name,
                "dimension": dimension,
                "metric": "cosine"
            }
            response = await client.post(
                f"{self.base_url}/api/v1/index/create",
                json=payload,
                headers=self.headers
            )
            return response.status_code == 200
    
    async def insert_vectors(self, index_name: str, vectors: List[List[float]], 
                            metadata: List[Dict[str, Any]], ids: Optional[List[str]] = None) -> bool:
        """Insert vectors with metadata"""
        async with httpx.AsyncClient() as client:
            if ids is None:
                ids = [str(i) for i in range(len(vectors))]
            
            payload = {
                "index": index_name,
                "vectors": vectors,
                "ids": ids,
                "metadata": metadata
            }
            
            response = await client.post(
                f"{self.base_url}/api/v1/vector/insert",
                json=payload,
                headers=self.headers
            )
            return response.status_code == 200
    
    async def search(self, index_name: str, query_vector: List[float], 
                    top_k: int = 10, filter_dict: Optional[Dict] = None) -> List[Dict]:
        """Search for similar vectors"""
        async with httpx.AsyncClient() as client:
            payload = {
                "index": index_name,
                "vector": query_vector,
                "top_k": top_k
            }
            
            if filter_dict:
                payload["filter"] = filter_dict
            
            response = await client.post(
                f"{self.base_url}/api/v1/vector/search",
                json=payload,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json().get("results", [])
            return []
    
    async def get_index_info(self, index_name: str) -> Dict:
        """Get information about an index"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/index/{index_name}/info",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            return {}