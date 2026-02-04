import asyncio
import sys
sys.path.append('.')

from app.core.endee_client import EndeeClient

async def test_endee():
    print("Testing Endee connection...")
    
    # Create client
    client = EndeeClient(host="localhost", port=8080)
    
    # Test health
    is_healthy = await client.health_check()
    
    if is_healthy:
        print("✓ Endee is running and healthy!")
        
        # Create test index
        success = await client.create_index("test_index", dimension=384)
        if success:
            print("✓ Created test index")
            
            # Test empty search
            results = await client.search("test_index", [0.1]*384, top_k=3)
            print(f"✓ Search test: {len(results)} results")
        else:
            print("✗ Failed to create index")
    else:
        print("✗ Endee is not responding")
        print("Make sure Endee is running with:")
        print("  docker-compose -f docker-compose.endee.yml up -d")

if __name__ == "__main__":
    asyncio.run(test_endee())