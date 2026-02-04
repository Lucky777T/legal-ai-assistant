import asyncio
import sys
sys.path.append('.')

from app.core.document_processor import DocumentProcessor
from app.core.embedding_service import EmbeddingService
from app.core.endee_client import EndeeClient

async def test_complete_phase2():
    print("="*60)
    print("PHASE 2 COMPLETE TEST")
    print("="*60)
    
    # 1. Test Document Processor
    print("\n1. Testing Document Processor...")
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=100)
    
    test_text = "This is a test legal document about contract law."
    test_metadata = {"filename": "test.txt", "file_type": "txt"}
    
    chunks = processor.chunk_text(test_text, test_metadata)
    print(f"   ✓ Created {len(chunks)} chunks")
    
    # 2. Test Embedding Service
    print("\n2. Testing Embedding Service...")
    embedding_service = EmbeddingService()
    texts = [chunk['text'] for chunk in chunks]
    embeddings = embedding_service.generate_embeddings(texts)
    print(f"   ✓ Generated {len(embeddings)} embeddings")
    print(f"   ✓ Embedding dimension: {embedding_service.dimension}")
    
    # 3. Test Endee Connection
    print("\n3. Testing Endee Connection...")
    endee_client = EndeeClient()
    is_healthy = await endee_client.health_check()
    
    if is_healthy:
        print("   ✓ Endee is running")
        
        # Create index
        success = await endee_client.create_index("legal_docs", embedding_service.dimension)
        if success:
            print("   ✓ Created 'legal_docs' index")
            
            # Prepare and insert vectors
            metadata_list = []
            for i, chunk in enumerate(chunks):
                meta = chunk['metadata'].copy()
                meta['text'] = chunk['text']
                meta['test_id'] = i
                metadata_list.append(meta)
            
            insert_success = await endee_client.insert_vectors(
                index_name="legal_docs",
                vectors=embeddings,
                metadata=metadata_list
            )
            
            if insert_success:
                print("   ✓ Inserted test vectors")
                
                # Test search
                results = await endee_client.search("legal_docs", embeddings[0], top_k=2)
                print(f"   ✓ Search returned {len(results)} results")
            else:
                print("   ✗ Failed to insert vectors")
        else:
            print("   ✗ Failed to create index")
    else:
        print("   ✗ Endee is not running")
        print("   Start it with: docker-compose -f docker-compose.endee.yml up -d")
    
    print("\n" + "="*60)
    print("PHASE 2 STATUS SUMMARY")
    print("="*60)
    print("✓ Document Processor: Ready")
    print("✓ Embedding Service: Ready")
    print(f"✓ Endee Database: {'Connected' if is_healthy else 'Not Connected'}")
    print("✓ All core components created")
    print("\nNEXT: Move to Phase 3 - Document Ingestion Pipeline")

if __name__ == "__main__":
    asyncio.run(test_complete_phase2())