#!/usr/bin/env python3
import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.document_processor import DocumentProcessor
from app.core.embedding_service import EmbeddingService
from app.core.endee_client import EndeeClient

async def ingest_documents():
    """Ingest sample legal documents into Endee"""
    print("="*60)
    print("LEGAL AI ASSISTANT - DOCUMENT INGESTION")
    print("="*60)
    
    # Initialize services
    endee_client = EndeeClient(host="localhost", port=8080)
    embedding_service = EmbeddingService()
    processor = DocumentProcessor(chunk_size=800, chunk_overlap=150)
    
    # Check Endee health
    print("\n1. Checking Endee connection...")
    is_healthy = await endee_client.health_check()
    if not is_healthy:
        print("   ✗ Endee server is not reachable")
        print("   Please start Endee with: docker-compose -f docker-compose.endee.yml up -d")
        return
    
    print("   ✓ Endee is connected")
    
    # Create index if not exists
    dimension = embedding_service.dimension
    await endee_client.create_index("legal_documents", dimension)
    print(f"   ✓ Created/verified index 'legal_documents' (dimension: {dimension})")
    
    # Process sample documents
    print("\n2. Processing sample documents...")
    sample_dir = "./sample_docs"
    if not os.path.exists(sample_dir):
        print(f"   ✗ Sample directory not found: {sample_dir}")
        print("   Create sample_docs/ folder with legal documents")
        return
    
    chunks = processor.process_directory(sample_dir)
    print(f"   ✓ Processed {len(chunks)} chunks from sample documents")
    
    if len(chunks) == 0:
        print("   ⚠ No documents found in sample_docs/")
        print("   Add PDF or TXT files to sample_docs/ folder")
        return
    
    # Generate embeddings
    print("\n3. Generating embeddings...")
    texts = [chunk['text'] for chunk in chunks]
    embeddings = embedding_service.generate_embeddings(texts)
    print(f"   ✓ Generated {len(embeddings)} embeddings")
    
    # Prepare metadata
    print("\n4. Preparing metadata...")
    metadata_list = []
    for i, chunk in enumerate(chunks):
        meta = chunk['metadata'].copy()
        meta['text'] = chunk['text']  # Store text for retrieval
        meta['chunk_index'] = i
        meta['document_type'] = 'contract' if 'contract' in meta['filename'].lower() else 'case_law'
        metadata_list.append(meta)
    
    # Insert into Endee
    print("\n5. Inserting into Endee vector database...")
    success = await endee_client.insert_vectors(
        index_name="legal_documents",
        vectors=embeddings,
        metadata=metadata_list
    )
    
    if success:
        print("   ✓ Successfully ingested documents into Endee")
        print(f"   ✓ Total chunks: {len(chunks)}")
        print(f"   ✓ Total vectors: {len(embeddings)}")
        
        # Get index info
        index_info = await endee_client.get_index_info("legal_documents")
        if index_info:
            print(f"   ✓ Index size: {index_info.get('size', 'N/A')} vectors")
    else:
        print("   ✗ Failed to ingest documents")
    
    print("\n" + "="*60)
    print("INGESTION COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Start the API server: uvicorn app.main:app --reload")
    print("2. Test search at: http://localhost:8000/docs")
    print("3. Open web interface: client/index.html")

if __name__ == "__main__":
    asyncio.run(ingest_documents())